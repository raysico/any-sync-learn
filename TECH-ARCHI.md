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
| ~~any-sync-admin~~ | ~~v0.0.7~~ | ~~`2344b3f`~~ |
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

唯一权威判据是 netcheck。注意两点：日志里 `netcheck` 与 `success` 之间是**制表符**而非空格；容器健康检查读的是容器内 `/tmp/netcheck-last.log`。

```bash
# 方式一：直接看健康状态（最省事，官方 compose 的 healthcheck 就是判它）
docker inspect any-sync-dockercompose-netcheck-1 --format '{{.State.Health.Status}} {{.State.Health.FailingStreak}}'
# 预期输出：healthy 0

# 方式二：统计日志中的成功次数（用 [[:space:]] 兼容制表符）
docker logs any-sync-dockercompose-netcheck-1 2>&1 | grep -cE "netcheck[[:space:]]+success"
```

所有服务 `Up` 且 netcheck 为 `healthy`（`FailingStreak: 0`）即健康。compose 内置的健康检查命令为：

```
grep -qE 'netcheck\s+success' /tmp/netcheck-last.log
```

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

---

## 7. userDomain Web 客户端（用户域登录与历史）

> 实现位置：`test/tools/userdomain-web/`（本地调试工具，按约定留在 `test/`，不入库）
> 启动：`./bin/userdomain-web -addr 0.0.0.0:8787 -network <nodes.yml> [-store data/userdomains.jsonl]`

### 7.1 术语与边界

| 术语 | 定义 | 对标 Anytype |
| --- | --- | --- |
| **用户域（userDomain）** | 由助记词在本机离线派生出的一组密钥身份；是「登录」与权限的主体 | 账户 / Vault |
| **库（library）** | 用户在用户域下自己管理、可列出的资源单元（本轮不实现） | Channel / Space |
| **登录** | 与网络完成握手，证明密钥被该网络受理 | 客户端连接 any-sync 网络 |
| **网络配置** | `nodes.yml`/`client.yml`，决定连哪个网络；**不参与密钥派生** | Subnet Configuration |

### 7.2 密钥边界

- 助记词（12 词）用 `crypto/rand` 在本机生成，**不参与任何上传**；网络只收到签名。
- 派生：`m/44'/2046'/<index>'`（master）、`m/44'/2046'/<index>'/0'`（signing/身份）、`m/44'/60'/0'/0/<index>`（Ethereum）。
- 助记词是唯一真源：同一助记词 + 同一 index → 同一账户 ID；导入记录时一律按助记词重新派生账户 ID，忽略文件中的 `accountId`。
- 历史记录保存于本机 JSON Lines 文件（默认 `data/userdomains.jsonl`，权限 0600），内含助记词，属于敏感文件。

### 7.3 接口清单

统一前缀：`http://<host>:8787`；请求与响应均为 `application/json; charset=utf-8`；错误统一为 `{"error": "<中文说明>"}`。

#### GET /api/network —— 读取当前网络配置

请求参数：无。响应字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| path | string | 网络配置文件绝对路径 |
| networkId | string | 网络 ID；`nodes.yml` 中为空时回退为配置 id |
| configurationId | string | 配置 ID（anyconf 的 `id`） |
| loadedAt | string(RFC3339) | 本次读取时间 |
| coordinator | string | coordinator 的 TCP 地址（首个非 `quic://` 地址） |
| nodes[].peerId | string | 节点 peerId |
| nodes[].types | string[] | `tree` / `coordinator` / `file` / `consensus` |
| nodes[].addresses | string[] | 地址列表 |

错误：500（配置文件不可读 / YAML 非法 / 无任何节点）。

#### POST /api/userdomain —— 生成用户域并登录

| 项 | 内容 |
| --- | --- |
| 请求体 | `{"index": 0}`（可选，省略按 0 处理） |
| 行为 | 本机生成 12 词助记词 → 派生密钥 → 与 coordinator 握手 → 写入历史记录 |
| 响应 | userDomain 对象（见 7.4） |
| 错误 | 500（生成助记词失败 / 网络配置不可读） |

#### POST /api/login —— 用已有助记词登录

| 项 | 内容 |
| --- | --- |
| 请求体 | `{"mnemonic": "<12 词>", "index": 0}` |
| 行为 | 校验助记词 → 派生同一用户域 → 与 coordinator 握手 → 以账户 ID 合并写入历史 |
| 响应 | userDomain 对象（见 7.4） |
| 错误 | 400（请求体非合法 JSON / 助记词词数、拼写或校验和不对）；500（网络配置不可读） |

> 握手失败**不是** HTTP 错误：返回 200，结果体现在 `login.ok=false` 与 `login.error`，便于前端展示「已生成、但连不上」。

#### GET /api/userdomains —— 历史列表

请求参数：无。响应：userDomain 对象数组，按 `createdAt` 倒序。错误：500（历史文件不可读）。

#### GET /api/userdomains/export —— 导出全部历史

| 项 | 内容 |
| --- | --- |
| 请求参数 | 无 |
| 响应头 | `Content-Type: application/json`；`Content-Disposition: attachment; filename="userdomain-export-YYYYMMDD-HHMMSS.json"` |
| 响应体 | userDomain 对象数组 |
| 错误 | 500 |

> 前端用 `fetch + Blob + <a download>` 触发下载，不依赖顶层导航。

#### POST /api/userdomains/import —— 导入历史

| 项 | 内容 |
| --- | --- |
| 请求体 | userDomain 对象**或**对象数组；上限 4 MB |
| 行为 | 有助记词的记录按助记词重新派生 `accountId`，`id` 一律等于 `accountId`；同 id 覆盖、否则新增；助记词非法或缺字段的记录跳过 |
| 响应 | `{"imported": <新增或覆盖条数>, "skipped": <跳过条数>}` |
| 错误 | 400（请求体既不是合法数组也不是合法对象） |

#### POST /api/userdomains/delete?id=<accountId> —— 删除历史记录

| 项 | 内容 |
| --- | --- |
| 请求参数 | `id`（query，必填，账户 ID） |
| 响应 | `{"deleted": "<accountId>"}` |
| 错误 | 400（缺 id）；500（写入失败） |

> 删除只影响本机历史文件，不影响该账户在网络上已有的任何数据。

### 7.4 userDomain 对象

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | string | 用户域标识，等于 `accountId` |
| mnemonic | string | 12 词助记词 |
| accountId | string | 身份公钥账户 ID（`m/44'/2046'/i'/0'`） |
| devicePeerId | string | 设备 peerId |
| ethereumAddress | string | Ethereum 地址（ANS 用） |
| derivation | string | 派生路径说明 |
| networkId | string | 登录时所用网络的 ID |
| networkPath | string | 网络配置文件路径 |
| createdAt | string(RFC3339) | 生成时间 |
| serverHost | string | 生成时的请求 Host |
| keys.masterKeyBase64 | string | master key（protobuf 编码后 base64） |
| keys.deviceKeyBase64 | string | device key |
| keys.signingKeyBase64 | string | signing key |
| keys.ethereumPrivateKeyHex | string | Ethereum 私钥 hex（**极高敏感**） |
| login.ok | bool | 是否握手成功 |
| login.addr | string | 握手目标地址 |
| login.durationMs | int | 握手耗时 |
| login.error | string | 失败原因（成功时省略） |
| login.notes | string | 说明（含局域网补全地址信息） |

### 7.5 登录判据

- 握手链路：TCP → libp2p TLS 安全握手（`secureservice`）→ DRPC 协议握手（`handshakeproto.ProtoType_DRPC`）。
- 目标：网络配置中的 coordinator；`login.ok=true` 表示该密钥被网络受理。
- 局域网访问：服务监听 `0.0.0.0` 时，在**内存中**给每个节点追加本机私有网段地址（`10/8`、`172.16/12`、`192.168/16`），不改配置文件。

### 7.6 后续待定

| # | 待定 | 说明 |
| --- | --- | --- |
| 1 | 用户域 ⇄ 个人空间 ID 的确定性推导 | 官方用 v0 头部构造器 + 密钥推导；本客户端暂不创建空间，只认证身份 |
| 2 | 库（library）与 `listLibrary` | 对标 Anytype Channel，下一轮实现 |
| 3 | 历史记录是否服务端加密 | 当前为明文 JSONL，仅靠文件权限保护 |

## 8. 用户域对象模型与对象同步通道（20261017 20:05-01 已实施）

本节记录**实测确认**的写入/读取链路，供后续实现与排障复核。所有结论均来自本地 6 进程网络（coordinator 2004 / consensus 2006 / filenode 2005 / node-1~3 2001–2003）的日志与数据库取证。

### 8.1 对象模型（用户域 = Space）

| 概念 | 落地方式 |
| --- | --- |
| 用户域 | any-sync 的 Space，一个空间 ID |
| 库（library） | 空间内一棵独立对象树，根变更 `changeType=library` |
| 记录（entry） | 空间内另一棵独立对象树，根变更 `changeType=entry`，载荷内 `lib=<库对象 ID>` |
| 归属关系 | 由记录对象载荷里的 `lib` 属性表达，**网络不解释**，空间里没有“对象清单”字段 |
| 加密 | 根变更的 `ChangePayload` 用空间 ReadKey（AES）加密后再写入 |

对象 ID = 根变更的 CID。库与记录在空间内**平级**，不存在“记录挂在库下面”的树结构。

### 8.2 写入通道（关键：节点会反向开流）

新对象入网需要四步，缺一不可：

1. **协调节点取配置**：`NetworkConfiguration` 拿到 networkId 与节点清单（不要用本地 nodes.yml 自算）；
2. **建空间**（仅首次）：`SpaceSign` 取回执 → `SpacePush` 到全部负责节点；
3. **推对象**：在 `ObjectSyncStream`（双向长连接）上发送 `headUpdate`，携带对象根；
4. **接受节点回拉**：节点发现本地没有该对象，会**在同一条 yamux 连接上反向开流**，调用 `ObjectSyncRequestStream` 索要数据；客户端必须在该连接上 `MultiConn.Accept()` 接受流、完成 DRPC 协议握手、以 SpaceSync 服务端应答 `FullSyncResponse`（含 `RootChange` 与 `Heads`）。

**易错点**：只做“出站推送”而不接受反向流，节点会反复记录 `tree does not exist`，对象永远不落盘。

### 8.3 读取通道

- **不要用 `HeadSync` 判成败**：它是差异同步语义，新建对象不会出现在其结果里，即使对象已经落盘。
- 正确做法：**按对象 ID 拉根**——`ObjectSyncRequestStream` 发 `FullSyncRequest{Probe:true}`，取回 `RootChange`，用 ReadKey 解密 `ChangePayload`。
- 各节点独立持有：未推送到的节点会返回 `tree not found`，因此写入要遍历全部负责节点。

### 8.4 已完成的验证

| 项 | 结果 |
| --- | --- |
| 用户域创建（含 SpaceSign/SpacePush） | 3/3 负责节点成功 |
| 库对象写入 | 3/3 节点接受，按 ID 可原样回读（`changeType=library`，载荷为密文） |
| 2 库 + 4 记录 | 主实例（:8787）与副本实例（:8788）均可从网络读回，`lib` 属性正确归属 |
| 节点持久化 | 空间 `store.db` 的 `_heads_docs` 含新对象条目；重启后仍可回读 |
