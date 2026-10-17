# TECH.md

> 本项目技术文档：架构、模块设计、数据流、约束、选型决策、数据模型、接口设计。
> 版本号真源：`package.json`（当前 0.0.0）

---

## 1. 环境基线（2026-10-17 建立）

### 1.1 本机环境

| 项 | 值 |
| --- | --- |
| 架构 | arm64 (Apple Silicon) |
| Go | 1.27.1 darwin/arm64，安装于 `~/.local/go` |
| Node | v24.4.1 |
| Docker | Docker Desktop 4.61.0，compose v5.0.2 |
| Xcode / clang | `/Applications/Xcode.app`，Apple clang 17.0.0（CGO 依赖） |
| brew | 7.0.9 |

**Go 环境变量**（已写入 `~/.zshrc` 与 `~/.zprofile`，登录/交互式 shell 均生效）：

```
PATH        += $HOME/.local/go/bin
GOPATH      =  $HOME/go
GOPROXY     =  https://goproxy.cn,direct
GOPRIVATE   =  github.com/anyproto
```

> ⚠️ 非登录非交互 shell（如部分脚本 `zsh -c`）不读 `.zshrc`/`.zprofile`。写构建脚本时请显式加 `export PATH="$HOME/.local/go/bin:$PATH"`。

### 1.2 目录布局

| 路径 | 用途 | 是否入库 |
| --- | --- | --- |
| `src/` | 14 个官方仓库的 **git 克隆**（各自独立仓库） | 否（`.gitignore`） |
| `compose/any-sync-dockercompose/` | **运行中的** any-sync 网络（含 `etc/` 私有配置与 `storage/` 数据） | 否（`.gitignore`） |
| `docs/` | 学习计划与产出文档 | 是 |
| `docs/imported/` | 从旧 `any-sync-ecosystem` 抢救的自制调研资产 | 是 |
| `scripts/` | 工具脚本 | 是 |
| `playground/` | 临时实验 | 否（`.gitignore`） |

---

## 2. 源码版本基线

**决策：锁定 0.13.x 系列**，与本地运行中的镜像严格对齐。理由：这是「改一行代码 → 观察行为变化」因果链最短的配置；升级会引入无关变量，干扰能力边界判断。

### 2.1 网络组件（构建目标）

| 仓库 | Tag | Commit |
| --- | --- | --- |
| any-sync | v0.13.1 | `f71a247` |
| any-sync-node | v0.13.1 | `7426c31` |
| any-sync-coordinator | v0.13.0 | `d65eec4` |
| any-sync-consensusnode | v0.13.0 | `0333ed5` |
| any-sync-filenode | v0.13.0 | `e196aeb` |
| any-sync-tools | v0.7.0 | `e5d018a` |

**关键约束：节点版本 ≠ 它依赖的 any-sync 库版本。**

实测四个节点的 `go.mod` **全部依赖 `any-sync v0.13.1`**：

| 节点 | 运行版本 | 依赖的 any-sync 库 |
| --- | --- | --- |
| any-sync-node | v0.13.1 | v0.13.1 |
| any-sync-coordinator | v0.13.0 | v0.13.1 |
| any-sync-consensusnode | v0.13.0 | v0.13.1 |
| any-sync-filenode | v0.13.0 | v0.13.1 |

> 因此 `src/any-sync` 必须 checkout **v0.13.1**，不能取最新 tag v0.13.8，否则库层与镜像不匹配。

### 2.2 其余克隆仓库

| 仓库 | Tag/分支 | Commit |
| --- | --- | --- |
| any-sync-dockercompose | v8.0.1 | `8035d68` |
| any-sync-admin | v0.0.7 | `2344b3f` |
| any-ns | v1.0.0 | `77cc311` |
| any-ns-node | v0.7.2 | `3d1c531` |
| any-block | main（v2.0.0-rc6+1） | `cd807bb` |
| anytype-heart | main（v0.51.6） | `d98420b` |
| ansible-anysync | v1.1 | `cf65932` |
| puppet-anysync | v3.4.5 | `5bf1108` |

### 2.3 Go 版本要求（各仓库 `go.mod` 实测）

| 仓库 | 要求 |
| --- | --- |
| any-sync v0.13.1 | go 1.25.7 |
| any-sync-node / coordinator / consensusnode / tools | go 1.25.7 |
| any-sync-filenode | go 1.26.4 |
| any-sync-node（README 口径） | go 1.26（与 go.mod 不一致，以 go.mod 为准） |

本机 Go 1.27.1 满足全部要求。

---

## 3. 运行中的网络

### 3.1 拓扑

| 服务 | 镜像 | 宿主端口 |
| --- | --- | --- |
| coordinator | `ghcr.io/anyproto/any-sync-coordinator:v0.13.0` | 1004/tcp, 1014/udp |
| consensusnode | `ghcr.io/anyproto/any-sync-consensusnode:v0.13.0` | 1006/tcp, 1016/udp |
| any-sync-node-1/2/3 | `ghcr.io/anyproto/any-sync-node:v0.13.1` | 1001-1003/tcp, 1011-1013/udp |
| filenode | `ghcr.io/anyproto/any-sync-filenode:v0.13.0` | 1005/tcp, 1015/udp |
| netcheck | `ghcr.io/anyproto/any-sync-tools:latest` | —— |
| mongo-1 | `mongo:7.0.28`（replica set `rs0`） | 127.0.0.1:27001 |
| redis | `redis/redis-stack-server:7.2.0-v6`（Bloom 模块） | 127.0.0.1:6379 |
| minio | `quay.io/minio/minio:RELEASE.2025-09-07T16-13-09Z` | 9000/9001（容器内） |

各节点另暴露 8000/8080 等内部端口（绑定 127.0.0.1:8001-8006、8081-8083）。

### 3.2 重要约束与已知状态

- **对象存储是 MinIO，不是 Garage**。官方 v8.0.0 起已迁至 Garage；本项目沿用旧栈（MinIO 官方镜像已停更）。迁移与否待决策。
- 桶名 `minio-bucket`（当前 compose 栈），不是 v8 的 `any-sync-files`。
- Redis **必须**带 Bloom 模块：启动参数 `--loadmodule /opt/redis-stack/lib/redisbloom.so`，否则 filenode 起不来。
- 网络配置：`compose/any-sync-dockercompose/etc/`，客户端接入用 `etc/client.yml`（本机）/ `etc/client-lan.yml`（局域网 `192.168.3.191`）。
- 数据目录 `storage/` 约 551MB（mongo 423MB / minio 60MB / redis 49MB / anyStorage 26MB）。

### 3.3 健康判据

唯一权威判据是 netcheck：

```bash
docker logs --tail 5 any-sync-dockercompose-netcheck-1 | grep -c "netcheck success"
```

所有服务 `Up` 且 netcheck 输出 `netcheck success` 即健康。

---

## 4. 迁移记录（2026-10-17）

原 `whynownote/any-sync-ecosystem`（621MB，tarball 解压副本，无 git 历史）已拆除，内容去向：

| 原内容 | 去向 |
| --- | --- |
| 14 个仓库源码 | `src/`，改为 **git clone**（可切 tag、可 diff、可打补丁） |
| `docs/`（42 个自制文件，含 387KB protobuf 接口参考、4 个 HTML 可视化、2 个生成工具） | `docs/imported/`，已 md5 逐项校验 |
| `any-sync-dockercompose/`（含 `etc/` 私有配置 + `storage/` 数据） | `compose/any-sync-dockercompose/`，数据文件数逐目录校验一致 |
| `fetch_all.sh`、`restart-local-cluster.sh` | `scripts/` |

**客户端适配**：`whynownote-heart/go.mod` 的 `replace github.com/anyproto/any-sync` 已从旧路径改指向 `src/any-sync`；迁移后 `go build` 验证通过（9 秒，30MB 产物）。

---

## 5. 待决策项

| # | 待定 | 影响 |
| --- | --- | --- |
| 1 | 继续用 MinIO 旧栈，还是迁移到 v8 + Garage | 旧栈稳定但停止演进；迁移需改配置与数据 |
| 2 | `docs/imported/` 是否纳入版本控制 | 目前设计为入库（已从 `.gitignore` 排除），需确认无敏感路径 |
| 3 | `src/` 是否需要 vendor 化以长期锁定 | 当前靠 tag + commit 锁定，上游删除 tag 即失效 |

---

## 6. 架构与接口资料索引

| 资料 | 位置 |
| --- | --- |
| 协议 Protobuf 全量参考（28 proto / 17 service / **112 RPC** / 727 message / 133 enum） | `docs/imported/any-sync-protobuf-接口参考.md` |
| 密钥派生可视化 | `docs/imported/any-sync-vault-key-derivation.html` |
| 两层哈希可视化 | `docs/imported/any-sync-two-layer-hashing.html` |
| ReadKey 轮换可视化 | `docs/imported/any-sync-read-key-rotation.html` |
| 节点拓扑可视化 | `docs/imported/any-sync-node-topology.html` |
| proto 解析/文档生成工具 | `docs/imported/tools/` |
| 技术文档中文导入（Feishu） | `docs/imported/.feishu_import/` |
