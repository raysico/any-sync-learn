# any-sync 学习计划：本机部署含命名系统的完整网络

> 适用环境：macOS 14+ / Apple Silicon（arm64）单机
> 编制日期：2026-10-17
> 版本基线：any-sync-learn v0.0.0
> 事实来源：本机实测 + 官方仓库原文 + 官方兼容版本 API（详见文末「证据与来源」）
> 状态标记：`[ ]` 未开始 / `[~]` 进行中 / `[x]` 已完成 / `[!]` 阻塞

---

## 0. 先读这一节：计划的事实基础与一处必须先知道的结论

### 0.1 一个必须先说清楚的问题

你的目标是「本机部署整套**含有命名系统**的 any-sync 网络」。核实后的结论是：

| 部分 | 可行性 | 依据 |
| --- | --- | --- |
| any-sync 同步网络本体（协调 + 共识 + 同步 ×3 + 文件 + 对象存储 + MongoDB + Redis） | ✅ **完全可自建，官方提供一键 compose** | 官方 `any-sync-dockercompose` v8.0.1 |
| AnyNS 命名系统**服务端 + 合约**（自建 `any-ns` 合约 + `any-ns-node`） | ✅ **可自建**，但**官方零部署文档、零示例 compose**，需自行拼装 | `any-ns` v1.0.0、`any-ns-node` v0.7.2 均开源 |
| AnyNS 的**支付处理节点**（`paymentProcessingNode`） | ❌ **不开源，无法自建** | 本机实测 `anyproto/any-sync-ppnode` 等 5 个候选仓库名**全部不存在**（`git ls-remote` 返回需凭据，即私有或不存在） |
| 客户端侧「用户自助注册 `.any` 域名」完整产品链路 | ❌ **本计划范围内无法打通** | 依赖上面的闭源支付节点 |

**这对计划的影响**：命名系统仍然可以自建并跑通**管理员代注册**（`admin-name-register`），也就是「你作为网络所有者，为指定 AnyID / 以太坊地址注册并解析域名」。但「终端用户在客户端里自己付费注册一个 `.any` 域名」这条链路补不齐。这是**产品链路缺口，不是技术研究缺口**——协议层、合约层、服务节点层你都能摸到。

因此本计划把「完整命名系统」拆成**两个递进目标**：

- **目标 A（必达）**：自建 any-sync 网络 + 自建 AnyNS 命名系统，跑通「注册 → 解析 → 客户端按名字寻址」。
- **目标 B（研究性，可失败）**：尝试补齐用户自助注册链路，或明确论证其不可补齐的原因。

### 0.2 本机当前状态（已实测）

| 项 | 实测结果 | 对计划的影响 |
| --- | --- | --- |
| 架构 | arm64 (Apple Silicon) | 官方全部镜像**均有原生 linux/arm64**，无需 `--platform` 或 QEMU ✅ |
| Docker | Docker 29.2.1 已装（`/Applications/Docker.app`），**守护进程未运行** | 第一步就要启动 Docker Desktop |
| bash | GNU bash 3.2.57 | 工作区脚本已兼容 bash 3.2 ✅ |
| 磁盘 | 可用 162 GiB | 足够（镜像 + Garage 数据 + 链数据） |
| 端口 27001 / 6379 / 3900 / 3901 / 1001–1006 | **全部空闲** | 无冲突，可直接用官方默认端口 ✅ |
| 端口 27017 | 空闲 | 宿主机无本地 MongoDB 服务 |
| Go / Node | Node v24.4.1 有；**Go 未安装** | 阶段 4 若要源码编译需先装 Go |

### 0.3 本计划的三条方法论（重要）

1. **先容器跑通，再源码复刻。** 官方 compose 已经把「正确的配置长什么样」固化下来。先用它把「能同步」跑通并拿到一份可工作的配置基线，再逐组件换成自己 `make build` 的二进制。反过来做，你会在版本兼容和端口配置上浪费数天。
2. **每一步都要有「能失败」的验证。** 每个阶段都给出验证命令与**预期输出**；没有验证输出就不算完成，不许靠「看起来启动了」推进。
3. **命名系统单独作为一条支线。** 它的阻塞点是闭源的，不要让它卡住网络本体的进度。先拿到能同步的网络（阶段 1），命名系统放在后面独立推进。

---

## 1. 学习目标与验收标准

学完并跑完本计划后，你应当能够：

1. 用自己的话解释 any-sync 网络里 `coordinator` / `consensus` / `tree`（同步）/ `file` / `namingNode` / `paymentProcessingNode` 六种节点类型的职责与相互依赖。
2. 从零生成一份可工作的网络配置（`network.yml` + 各节点 `config.yml` + 客户端 `client.yml`），并说清密钥体系：`networkId`、`peerId` / `peerKey`、`signingKey` 各自的用途与存放位置。
3. 用自己编译的二进制替换官方镜像中的组件，且网络仍然通过 `netcheck`。
4. 部署一套自建 AnyNS 合约 + `any-ns-node`，并让它作为 `namingNode` 挂进网络配置。
5. 让 Anytype 客户端连上你的网络，并解析一个你自建的 `.any` 域名。
6. 说清哪些环节依赖闭源组件、哪些环节有中心化依赖（Alchemy）、以及自建命名系统与官方 `.any` 命名空间**不互通**这一事实的产品含义。

**总验收（目标 A）**：客户端连上自建网络 → 上传一个文件（走 filenode + Garage）→ 管理员为某地址注册 `test.any` → 客户端能解析 `test.any` 到对应地址。

---

## 2. 阶段总览

| 阶段 | 内容 | 预估 | 关键依赖 | 阻塞风险 |
| --- | --- | --- | --- | --- |
| 0 | 环境准备与概念预习 | 0.5 天 | Docker Desktop 启动 | 低 |
| 1 | 官方 compose 跑通完整同步网络 | 1 天 | Docker + 磁盘 | 低 |
| 2 | 读懂配置：网络配置生成与密钥体系 | 1–2 天 | 阶段 1 产物 | 低 |
| 3 | 源码编译与替换（自建二进制接管） | 2–3 天 | Go 工具链 + CGO | 中（版本锁定） |
| 4 | AnyNS 合约部署（本地私链） | 2–3 天 | Node 版本、Hardhat | 中（私链适配） |
| 5 | any-ns-node 部署并挂入网络 | 2–4 天 | 阶段 4 合约地址、Alchemy 账号 | **高** |
| 6 | 客户端接入与端到端验证 | 1 天 | 阶段 1/5 | 中 |
| 7 | 目标 B 研究：自助注册链路 | 研究性 | 闭源组件 | **阻塞（已知）** |

**建议节奏**：阶段 0–1 一定要一次做完，拿到「能同步」的正反馈；阶段 4–5 是全程最难的部分，建议单独留出整块时间，不要和其他阶段并行。

---

## 3. 阶段 0：环境准备与概念预习（0.5 天）

### 3.1 动作

- [ ] 启动 Docker Desktop，确认守护进程可用：
  ```bash
  docker info --format '{{.ServerVersion}} / {{.OSType}}/{{.Architecture}}'
  ```
  **预期**：打印出 ServerVersion 与 `linux/arm64`。若报 socket 不存在，说明 Docker Desktop 没起来。

- [ ] 确认 Docker 资源充足（Docker Desktop → Settings → Resources）：内存建议 ≥ 8 GB，磁盘 ≥ 40 GB。

- [ ] 建工作目录骨架（放在项目的 `playground/` 下，该目录已被 `.gitignore` 忽略，是放第三方副本的正确位置）：
  ```bash
  cd dev/any-sync-learn
  mkdir -p playground/01-official-compose      # 阶段 1：官方 compose 副本
  mkdir -p playground/02-source-build          # 阶段 3：各组件源码克隆
  mkdir -p playground/03-anyns                 # 阶段 4-5：合约与命名节点
  ```

- [ ] 预习节点类型（先建概念，阶段 2 再落到配置）：读 `any-sync/nodeconf/config.go` 里的类型枚举，确认存在 `tree` / `consensus` / `file` / `fileV2` / `coordinator` / `namingNode` / `paymentProcessingNode`。

### 3.2 本阶段验证

能回答这三个问题即算过关：

1. 我的机器架构是什么，官方镜像是否需要特殊处理？（答：arm64；不需要，官方镜像全有原生 arm64）
2. 网络里哪两类节点**不是**数据同步必需，而是可选/命名相关？（答：`namingNode`、`paymentProcessingNode`）
3. 为什么 Docker 守护进程必须先起来？（答：所有节点与依赖服务都跑在容器里）

---

## 4. 阶段 1：用官方 compose 跑通完整同步网络（1 天）

> **为什么先做这个**：官方 compose 把「正确答案」固化了。先跑通它，你就有了一个**可工作的配置基线**，后面所有自建动作都可以和它对照。这一步还会一次性暴露端口、版本兼容、架构等环境问题。

### 4.1 动作

- [ ] 克隆官方 compose 仓库（**签出 v8.0.1，不要用 v8.0.0**，后者迁移 profile 会拉取已停更的官方 MinIO 镜像）：
  ```bash
  cd dev/any-sync-learn/playground/01-official-compose
  git clone https://github.com/anyproto/any-sync-dockercompose.git
  cd any-sync-dockercompose
  git checkout v8.0.1
  ```

- [ ] 初始化环境文件：
  ```bash
  cp .env.example .env
  ```
  本机是单机本地测试，`EXTERNAL_LISTEN_HOSTS` 可留默认（仅本机/局域网访问）。

- [ ] 拉取「当前客户端兼容」的版本组合（**必做**，`.env.example` 里钉的版本已落后于官方兼容集合）：
  ```bash
  ./update-versions.sh
  ```
  **预期**：脚本会从官方兼容 API 取值并写入 `.env`。该脚本已专门处理 macOS 的 `sed -i` 差异，可放心跑。

- [ ] 启动整套 stack：
  ```bash
  docker compose up -d
  docker compose ps
  ```
  **预期**：`mongo-1`、`redis`、`garage`、`any-sync-coordinator`、`any-sync-consensusnode`、`any-sync-filenode`、`any-sync-node-1/2/3`、`netcheck` 全部为 running/healthy。

- [ ] **关键验证：netcheck**（这是官方给出的「网络真的通了」的唯一权威判据）：
  ```bash
  docker compose logs netcheck
  ```
  **预期**：日志中出现 `netcheck success`。若不断失败，先 `docker compose logs any-sync-coordinator any-sync-node-1` 看配置错误。

### 4.2 你要在这阶段搞清楚的清单（不写代码，只读）

- [ ] 打开生成的 `etc/client.yml`，认出 `networkId`、`nodes[]` 各条目、`types` 字段。
- [ ] 打开 `docker-generateconfig/init.sh`，看清 `anyconf create-network` → `anyconf generate-nodes` 的完整流程，以及**协调节点与共识节点共用同一个 network signingKey** 这一点。
- [ ] 打开 `docker-compose.yml`，记下 Redis 的启动参数原文：`--appendonly yes`、`--maxmemory-policy noeviction`，以及**最关键的那句** `--loadmodule /opt/redis-stack/lib/redisbloom.so`（filenode 的索引依赖 Bloom，缺了它 filenode 起不来）。
- [ ] 打开 `garage/garage.toml`，确认 S3 API 端口 3900、`s3_region = us-east-1`、`replication_factor = 1`。
- [ ] 确认桶是**自动创建**的（`--default-bucket`），桶名 `any-sync-files`，**不需要手动建桶**。

### 4.3 本阶段验收

- [ ] `docker compose logs netcheck` 出现 `netcheck success`
- [ ] `docker compose ps` 无 unhealthy / restarting
- [ ] 能指出 `etc/client.yml` 的位置，并说清它和 `etc/any-sync-coordinator/network.yml` 的区别

### 4.4 常见坑（本机已知）

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| filenode 起不来，日志报 Bloom 相关命令不存在 | 用了普通 `redis-server` 镜像 | 必须用 `redis/redis-stack-server`（带 `redisbloom.so`） |
| coordinator 报副本集错误 | MongoDB 没以 replica set 模式启动 | 官方 compose 已带 `--replSet rs0`，别改成 standalone |
| 端口被占用 | 本机已有 Redis(6379) 等服务 | 本机实测这些端口当前空闲；若后续冲突改 `.env` 的 `REDIS_PORT` 等 |
| `volumes ... :Z` 相关告警 | `:Z` 是 SELinux 语义，macOS 无 SELinux | 属预期，可忽略（若报错再移除 `Z`） |

---

## 5. 阶段 2：读懂配置——网络配置生成与密钥体系（1–2 天）

> 目标：能**从零手写**一份网络配置，而不是只会跑 compose。

### 5.1 密钥体系（先建立正确心智模型）

| 名称 | 是什么 | 谁持有 | 用在哪 |
| --- | --- | --- | --- |
| `networkId` | 全网唯一标识（配置哈希） | 所有节点 + 客户端 | 节点间握手校验、客户端选网络 |
| `peerId` / `peerKey` | 每个节点的 Ed25519 身份 | **各自节点** | 节点间 P2P 认证 |
| `signingKey` | 网络签名密钥，**协调节点与共识节点共用同一把** | coordinator + consensus | 网络配置签名，防止配置被篡改 |
| 客户端身份 | BIP39 助记词经 SLIP-0010 派生的 Ed25519 | 客户端 | 接入自建网络 |

⚠️ **接入自建网络必须使用全新身份**，不要沿用官方网络的身份。

### 5.2 动作

- [ ] 装 Go（阶段 3 也要用），确认 `CGO_ENABLED=1` 可用（需 Xcode Command Line Tools：`xcode-select --install`）。
- [ ] 编译 `any-sync-tools`，得到 `any-sync-network`：
  ```bash
  cd dev/any-sync-learn/playground/02-source-build
  git clone https://github.com/anyproto/any-sync-tools.git
  cd any-sync-tools
  make deps && make build    # 产物在 ./bin
  ```
- [ ] 读懂 `any-sync-network` 的模板与输出。**注意**：官方 `tech-docs/self-hosting.md` 里写的输出文件名（`coordinator.yml` / `sync_N.yml` / `heart.yml`）是**过期行为**，以源码 `any-sync-network/cmd/create.go` 为准，实际输出是：
  ```
  etc/any-sync-coordinator/config.yml
  etc/any-sync-coordinator/network.yml      # 给 any-sync-confapply 用
  etc/any-sync-consensusnode/config.yml
  etc/any-sync-node-1..N/config.yml
  etc/any-sync-filenode/config.yml
  etc/client.yml                            # 导入客户端
  ```
- [ ] **手工生成一份配置**（单机多节点必须错开所有端口）。参考端口规划：

  | 节点 | Yamux (TCP) | QUIC (UDP) |
  | --- | --- | --- |
  | coordinator | 14430 | 15430 |
  | consensus | 14431 | 15431 |
  | filenode | 14432 | 15432 |
  | sync node 1 | 14433 | 15433 |
  | **namingNode（阶段 5 用）** | 14434 | 15434 |

  ⚠️ 工具默认端口是 coordinator 4830/5830、consensus 4530/5530、filenode 4730/5730、sync 4430+/5430+；换端口时**最容易漏改 `network.nodes[].addresses`**，改完务必全文搜索核对。
- [ ] 用自己生成的配置启动（先用官方镜像跑，阶段 3 再换成自建二进制），并用 `netcheck` 复验：
  ```bash
  # any-sync-tools 里带 netcheck
  ./bin/any-sync-netcheck -c <你的节点配置>
  ```
- [ ] 动手改一次配置并用 `any-sync-confapply` 下发，观察节点是否热加载新配置：
  ```bash
  ./bin/any-sync-confapply -c <coordinator配置> -n network.yml -e
  ```

### 5.3 本阶段验收

- [ ] 能徒手（对照源码）生成一份配置并让 `netcheck` 通过
- [ ] 能解释「为什么改端口后要同步改 `network.nodes[].addresses`」
- [ ] 能用 `any-sync-confapply` 成功下发一次网络配置变更

---

## 6. 阶段 3：源码编译与替换（2–3 天）

> 目标：把官方镜像换成你自己 `make build` 出来的二进制，网络仍然通过 `netcheck`。

### 6.1 版本锁定（这一阶段最大的坑）

**规则不是「四个组件版本号必须相同」**，而是**必须落在官方同一组兼容集合内**。官方兼容版本 API：

- 生产：`https://puppetdoc.anytype.io/api/v1/prod-any-sync-compatible-versions/`
- 测试台：`https://puppetdoc.anytype.io/api/v1/stage1-any-sync-compatible-versions/`

实测该 API 返回的是**历史所有兼容版本组的字典**（键为时间戳），取**最后一个键**即为「当前推荐组合」。本次实测最后一组为：

```json
{"pkg::any-sync-consensusnode":"0.13.3","pkg::any-sync-coordinator":"0.13.2",
 "pkg::any-sync-filenode":"0.13.2","pkg::any-sync-filenode2":"0.0.7",
 "pkg::any-sync-node":"0.13.4"}
```

取最新一组的命令：

```bash
curl -s https://puppetdoc.anytype.io/api/v1/prod-any-sync-compatible-versions/ \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d[max(d,key=int)],indent=2))"
```

注意版本号本来就各不相同（0.13.4 / 0.13.2 / 0.13.2 / 0.13.3），所以「四个仓库必须同版本号」是错的；且其中 `any-sync-filenode2`（0.0.7）**没有公开仓库**——这是官方 v2 文件协议的闭源/未公开组件，选 v1 文件协议可绕开。

### 6.2 动作

- [ ] 按兼容集合逐个签出对应 tag 并编译。需要 clone 的**只有节点类仓库**；`any-sync`、`any-block`、`any-store` 是 Go module 依赖库，`make deps` 会自动拉取，**不需要单独 clone 和 build**（也没有节点二进制）。
  ```bash
  cd playground/02-source-build
  for r in any-sync-node any-sync-coordinator any-sync-consensusnode any-sync-filenode; do
    git clone https://github.com/anyproto/$r.git
  done
  # 分别 cd 进去，git checkout <兼容集合里的对应 tag>，然后 make deps && make build
  ```
- [ ] 注意各仓库 README 的 Go 版本要求**互相矛盾**（`any-sync-node` 写 Go 1.26，coordinator/consensusnode/filenode 写 Go 1.22）——以**各仓库自身 README** 为准，必要时用容器内编译规避。
- [ ] 注意 CGO：`any-sync-node` / `coordinator` / `filenode` / `any-sync-tools` / `any-ns-node` 的 Makefile 都有 `export CGO_ENABLED:=1`，macOS 本地编译需要 Xcode Command Line Tools。
- [ ] 用自建二进制替换容器：改写 `Dockerfile` 的 `FROM ghcr.io/anyproto/...` 为 `FROM alpine` 并 `COPY` 你的二进制；或直接用 `docker-compose.override.yml` 挂载二进制进容器覆盖 `/bin/...`。
- [ ] 重新 `docker compose up -d` 并复验 `netcheck success`。
- [ ] 同步节点记得在其工作目录下建 `db` 文件夹（官方 self-hosting 文档明确警告，否则生成的配置无法工作）。

### 6.3 本阶段验收

- [ ] `docker compose ps` 中至少 coordinator + consensus + filenode + node-1 用的是你自己构建的镜像
- [ ] `netcheck success` 复现
- [ ] 记录下每个组件的「仓库 + tag + commit」，写入 `TECH.md`

### 6.4 工程建议（来自既有调研）

- 把 `any-sync` 依赖版本 fork 并 vendor 住（`go.mod` 用 `replace` 指向自己的 fork），避免上游漂移导致「昨天能编译今天不行」。
- 保留 `any-sync-netcheck` 作为连通性回归测试，保留 `any-sync-acl-cli` 排查 space 权限。

---

## 7. 阶段 4：AnyNS 合约部署（2–3 天）

> 从这一阶段起进入命名系统支线。**先决条件：阶段 1 的网络已能同步**。

### 7.1 先做一个决策：Sepolia 测试网 vs 本地私链

| 方案 | 优点 | 缺点 | 建议 |
| --- | --- | --- | --- |
| **Sepolia 测试网** | 官方 `any-ns` 的 hardhat 配置与 `any-ns-node` 的 `config-sepolia.yml` 都现成；官方已部署地址可做对照 | 需要测试网 ETH；依赖 Infura/Alchemy 外网；官方已部署地址有**三套互相矛盾**的记录 | 想快速跑通用它 |
| **本地私链（Hardhat node / Geth）** | 完全离线、可控、免费 | `hardhat.config.ts` 网络列表**硬编码**，接自建链必须自己加 network 条目（含 `chainId`、`accounts`、`tags: ['test','legacy','use_root']`）；且 `00_deploy_registrar.ts` 在 `network.tags.use_root` 为假时会**直接 `return true` 跳过**，私链部署不是「启动就行」 | 想彻底掌握机理用它 |

**推荐**：先用 Sepolia 跑通一次（拿到正确的合约地址集合），再回到本地私链重做一次（彻底理解部署脚本）。

### 7.2 动作

- [ ] 准备部署钱包：**需要有测试网 ETH 用于部署 Gas**。⚠️ 这只是给**部署合约**用的；域名注册费**不支持原生 ETH**，只支持 ERC20 稳定币（USDT/USDC/DAI）。
- [ ] 克隆合约仓库并注意 Node 版本陷阱：
  ```bash
  cd playground/03-anyns
  git clone https://github.com/anyproto/any-ns.git
  cd any-ns && git checkout v1.0.0
  cat .nvmrc    # 注意：仓库锁的是 v14.15.0，且有 husky prepare 钩子，不是「Node 18+」
  ```
  既有调研记录该仓库 `.nvmrc` 为 `v14.15.0`、只带 `yarn.lock`。建议**用容器化或 nvm 切到仓库锁定版本**，不要用系统 Node 24 硬上。
- [ ] 配置 `.env` 并部署：
  ```bash
  # .env 需要：DEPLOYER_KEY / INFURA_API_KEY / ADMIN_SCW / MINTER_SCW
  npx hardhat --network sepolia deploy --tags "anytype"
  ```
  **预期**：hardhat-deploy 会自动带上 `registry` / `root` 等依赖 tag。
- [ ] **记录全部合约地址**。⚠️ 清单类文档常只列 5 个，实际 `deployments/sepolia/` 有 **14 个条目**。至少要拿到：
  `ENSRegistry`、`AnytypeResolver`、`AnytypeRegistrarImplementation`、`AnytypeRegistrarController`、`AnytypeRegistrarControllerPrivate`、`AnytypePriceOracle`、`ERC20NameToken`、`Root`、`ReverseRegistrar`、`AnytypeNameWrapper`、`LegacyENSRegistry`、`StaticMetadataService`。
- [ ] **极易配错的一处**：`contracts.registrarController` 在官方 sepolia 配置里指向的是 **Implementation**，不是 Controller。`AnytypeRegistrarController`（公开控制器，需 ERC20 支付）与 `AnytypeRegistrarImplementation` 是两个不同合约。
- [ ] 若走公开注册路径：确认 ERC20 支付选项已通过 `addERC20UsdPaymentOption` 注册（`AnytypeRegistrarControllerPrivate` 私有控制器路径不需要稳定币）。

### 7.3 本阶段验收

- [ ] `deployments/<network>/` 目录存在，条目数与预期一致
- [ ] 把地址表完整记录到 `TECH.md`（含每个合约的用途）
- [ ] 能在链上浏览器（Sepolia）查到你的 `AnytypeNameWrapper` 等合约

### 7.4 注册费与代币参数（配置时要填）

| 参数 | 值 | 说明 |
| --- | --- | --- |
| `tokenDecimals` | 6 | ERC20 名称代币精度 |
| `nameTokensPerName` | 10 | 每个域名消耗的代币数 |
| 域名过期宽限期 | 默认 90 天 | 链上过期后缓存仍保留 |

---

## 8. 阶段 5：any-ns-node 部署并挂入网络（2–4 天，全程最难）

> ⚠️ **本阶段是全计划的最高风险点**。官方**没有** AnyNS 的部署文档、**没有**示例 compose；`any-sync-dockercompose` 与 `tech-docs` 全仓库 grep `any-?ns|nsnode|naming|payment.?process` **零命中**。

### 8.1 配置必须写对（清单类文档在这份配置上错得最多）

以官方 `any-ns-node/etc/config-sepolia.yml` 为模板，**不要**用网上清单里的样例。以下字段极易写错：

| 常见错误写法 | 正确写法 | 后果 |
| --- | --- | --- |
| `account.signKey` | `account.signingKey` | 启动即失败 / 无签名 |
| `cache.mongo: mongodb://...` | Mongo 是**顶层** `mongo.connect` + `mongo.database`；`cache` 段只有 `allowUnsafeStandalone` / `repairIntervalSec` | cache 段被解析为空配置 |
| 缺 `contracts.nameToken` / `registrarImplementation` / `tokenDecimals` | 均为必需字段 | 代币支付与注记逻辑不可用 |
| 缺整段 `accountAbstraction` | 必需：`alchemyRpcUrl` / `accountFactory` / `entryPoint` / `gasPolicyID` / `alchemyApiKey` / `chainID` / `nameTokensPerName` | 代付 Gas 功能全废；且 `-rpc-url` 校验要与此段 `chainID` 比对 |
| 缺 `network` / `networkStorePath` / `limiter` / `sentry` / `drpc` | 均为必需或强约束项 | 起不来或连不上 |

### 8.2 动作

- [ ] 部署 MongoDB 副本集（本地开发若确实要绕过，可设 `cache.allowUnsafeStandalone: true`，**仅限本地**）：
  ```bash
  mongod --port 27017 --dbpath ./mongo-data --replSet rs0 --bind_ip 127.0.0.1
  mongosh --eval 'rs.initiate({_id:"rs0", members:[{_id:0, host:"127.0.0.1:27017"}]})'
  ```
- [ ] 编译 `any-ns-node`：
  ```bash
  git clone https://github.com/anyproto/any-ns-node.git   # v0.7.2
  cd any-ns-node && make deps && make build
  ```
  注意：该仓库需要 `export GOPRIVATE=github.com/anyproto`，依赖公开仓库 `github.com/anyproto/alchemy-aa-sdk`；Makefile 有 `prereqs-for-mac` 目标可装齐 protoc 等工具。
- [ ] 准备 **Alchemy 账号与 Gas Policy**。⚠️ 这一步是**硬性的中心化依赖**：`any-ns-node` 的账户抽象实现无条件走 Alchemy AA SDK（`GetSmartWalletAddress` → `CreateRequestGasAndPaymasterData` → `SendRequest(alchemyApiKey, ...)`），**连 admin 私有控制器路径也不例外**。官方示例里的 `accountFactory: 0x123` / `entryPoint: 0x234` / `gasPolicyID: 123` / `alchemyApiKey: xYZ_aBC` **全是占位符**，必须替换为真实值。
- [ ] 写 `ns-node.yml`（参照阶段骨架，含 `account` / `network` / `mongo` / `cache` / `contracts` / `accountAbstraction` / `limiter`）。
- [ ] 启动节点：
  ```bash
  ./bin/any-ns-node -c ./ns-node.yml
  ```
- [ ] **关键一步：把命名节点挂进网络配置。** 集成点是**网络配置本身**，不是协调节点配置：
  - 协调节点配置里**没有**任何 AnyNS / NS 节点地址 / 命名解析开关字段（只有 `mongo` 与 `spaceStatus` 两段）。网上流传的「在协调节点配置里添加 AnyNS 节点地址」是**错误结论**。
  - 正确做法：
    1. 手工编辑 `network.yml`（以及各节点配置里的 `network` 段），加入本节点条目，`types: [namingNode]`。
    2. `any-sync-network` 工具**不支持**生成 `namingNode`（合法类型选项被硬编码为 `tree` / `file` / `consensus` / `coordinator`），所以只能手工改。
    3. 用 `any-sync-confapply` 下发：
       ```bash
       ./bin/any-sync-confapply -c <coordinator配置> -n network.yml -e
       ```
    4. 客户端的 `client.yml` / `heart.yml` 同样要含 `namingNode` 条目（客户端 nameservice 从 nodeconf 取 `NamingNodePeers()` 去连）。
- [ ] 用 CLI 验证命名功能（**合法命令只有这些**）：
  ```bash
  # 注意：不存在 name-register 这个命令
  # 合法命令：admin-name-register, admin-name-renew, admin-fund-user, is-name-available,
  #          name-by-address, get-operation, batch-is-name-available,
  #          batch-name-by-anyid, name-by-anyid
  ./bin/any-ns-node -cl --cmd=is-name-available --params='{"FullName":"test.any"}'
  ./bin/any-ns-node -cl --cmd=admin-name-register \
      --params='{"FullName":"test.any","OwnerAnyAddress":"A...","OwnerEthAddress":"0x...","SpaceId":"bafy..."}'
  ```
  `admin-*` 系列要求执行身份具备 admin 权限（签名匹配 admin，或调用方是 `paymentProcessingNode` 类型节点）。CLI 用独立的 `etc/config-client.yml`，**不是**节点配置。

### 8.3 本阶段验收（目标 A 的核心）

- [ ] `any-ns-node` 启动无报错，日志显示已连上 MongoDB 与 EVM RPC
- [ ] `is-name-available` 对 `test.any` 返回可用
- [ ] `admin-name-register` 注册成功，`name-by-address` / `name-by-anyid` 能查回
- [ ] `any-sync-confapply` 下发后，其他节点配置里的 `network.nodes` 确实含 `namingNode` 条目

### 8.4 缓存运维纪律（**必读，做错会丢数据**）

- `ns.cache`（MongoDB 里的域名缓存）是「谁拥有哪个域名」的**唯一权威记录**——链上域名过期或过宽限期后，缓存仍永久保留。
- **每次执行 `-refresh-apply` 前必须备份**：
  ```bash
  mongodump   # 或 mongoexport
  ```
- 相关命令：`-refresh-cache`（先 dry run，不带 `-refresh-apply`）、`-dedupe-cache -refresh-apply`、`-release-name test.any -refresh-apply`。
- 缓存有 **+5/+30 分钟重读与退避机制**，所以「域名变更实时同步」的「实时」不成立。
- 从 0.7.1 升级到 0.7.2 涉及 tombstone 恢复流程，自建前应读 `any-ns-node` README 的 Rollout 章节。

---

## 9. 阶段 6：客户端接入与端到端验证（1 天）

### 9.1 动作

- [ ] **用全新身份**（不要沿用官方网络的身份）。
- [ ] macOS 直连自建网络（官方 Usage 文档给出的原文命令）：
  ```bash
  ANYTYPE_LOG_LEVEL="*=DEBUG" ANYPROF=:6060 \
  ANY_SYNC_NETWORK=$(pwd)/etc/client.yml \
  /Applications/Anytype.app/Contents/MacOS/Anytype
  ```
  或者走 GUI：设置 → 网络 → 自建 → 上传 `etc/client.yml` → 用全新身份登录。
- [ ] **注意外联**：Push / Publish 默认会外联官方服务（`anytype-push-server.anytype.io:443`、`anytype-publish-server.anytype.io:443`）。自建网络里应显式留空或自建这两个服务，否则你的「自建网络」仍在向官方发数据。
- [ ] 确认 `external-addresses` 是**客户端可达**的地址（对应 compose 的 `EXTERNAL_LISTEN_HOSTS`），否则局域网外连不上。

### 9.2 端到端验收清单（目标 A 完成判据）

- [ ] 客户端能连上自建网络并创建 space
- [ ] 建立两个 space / 两台设备，验证跨设备同步
- [ ] **上传一个文件**，确认走 filenode + Garage（在 Garage 数据目录里能看到对象增长）
- [ ] `admin-name-register` 注册一个域名，客户端能解析它（**注意**：是「用我自己的命名系统解析」，不是「全球 Anytype 客户端都能解析」）
- [ ] 重启整个 stack（`docker compose restart` + 重启 ns-node），数据与域名缓存仍在

### 9.3 必须理解的一条产品事实

自建的 `ENSRegistry` / `AnytypeResolver` / `AnytypeNameWrapper` 是**你自己的合约**，构成**独立命名空间**，与官方 `.any` **不互通**。
所以「用 `.any` 用户名搜索并添加好友」这个需求，在自建语境下必须重述为「**用我自己的命名系统**解析并添加好友」。如果目标是「全球任何 Anytype 客户端都能解析」，那只能连官方合约 + 官方 ns-node——那就不叫自建了。

---

## 10. 阶段 7：目标 B 研究——用户自助注册链路（研究性，已知阻塞）

### 10.1 阻塞点与依据

「终端用户在客户端自助付费注册 `.any` 域名」依赖 `paymentProcessingNode`（支付处理节点）：

| 事实 | 依据 |
| --- | --- |
| `any-sync-ppnode` 及 4 个候选仓库名全部**不存在/私有** | 本机 `git ls-remote` 实测，5/5 失败（返回需凭据） |
| `any-sync-dockercompose` 与 `tech-docs` 全仓库 grep 命名系统相关关键词**零命中** | 克隆后 grep 实测 |
| `any-ns-node` 的 `isAdmin()` = 调用方是 `paymentProcessingNode` 类型节点，**或**签名匹配 admin 身份 | 源码 `anynsrpc/anynsrpc.go` |
| 客户端 `anytype-heart/core/payments` 依赖 `ppclient.AnyPpClientService`，而实现未开源 | 源码 + 仓库探测 |

**因此**：你自己作为 `admin` 可以注册域名（`admin-name-register` 已验证可用路径），但**无法补齐「客户端内自助付费注册」的产品闭环**。

### 10.2 值得尝试的研究方向（可选）

- [ ] **协议层：自任 paymentProcessingNode。** 把你自己中间件的 peerId 以 `types: [paymentProcessingNode]` 写进网络配置，在协议层即合法获得调用 `AdminNameRegisterSigned` 的权限（已有源码依据）。这能验证「协议是否真的把门」，但**不等于**补齐产品链路（客户端仍要对接 ppclient 的接口形状）。
- [ ] **替代实现**：替换 `alchemysdk` 包，或 fork `any-ns-node` 把账户抽象改成 EOA 直接发交易，从而摆脱 Alchemy 依赖（这是去掉中心化依赖最实际的一条路）。
- [ ] **先不做命名系统**：在自己的中间件/HTTP API 里做一张「名字 → AnyID / spaceId」映射表，API 形状对齐 `nameserviceclient` 的方法名（`IsNameAvailable` / `NameByAddress` / `NameByAnyId` / `BatchGetNameByAnyId`）。产品验证成立后，再决定是否换成 AnyNS dRPC 客户端。
  > 参考判断：如果命名只是产品功能而非抗审查诉求，直接上 AnyNS 的 ROI 是负的——代价是 EVM 链 + 合约 + 账户抽象 + Alchemy + NS 缓存运维。

### 10.3 本阶段产出

- [ ] 一份书面结论：自助注册链路是否可补齐，依据是什么，缺的具体是什么
- [ ] （可选）验证「自任 paymentProcessingNode」是否真能获得 admin 权限，记录实测结果

---

## 11. 全程风险登记表

| # | 风险 | 影响 | 概率 | 缓解 |
| --- | --- | --- | --- | --- |
| 1 | **支付处理节点闭源** → 用户自助注册不可达 | 目标 B 无法完成 | 已确认为事实 | 明确降级为「管理员代注册」；把目标 B 记为研究项 |
| 2 | **Alchemy 硬依赖** → 账户抽象无条件走 Alchemy | 中心化依赖；无账号则节点不可用 | 高 | 申请 Alchemy 账号 + Gas Policy；长期考虑 fork 改 EOA |
| 3 | **版本漂移** → 从各仓库 HEAD 编译，配置互通但版本不兼容 | 浪费数天排查 | 高 | 严格按官方兼容 API 锁 tag；vendor 住 `any-sync` 依赖 |
| 4 | **Sepolia 地址三套矛盾** | 配错合约地址，功能异常 | 高 | 自己部署一套并完整记录；不盲信任何文档地址 |
| 5 | `any-sync-network` 不生成 `namingNode` | 配置漏项，客户端连不上命名节点 | 中 | 手工编辑 `network.yml` + `any-sync-confapply` 下发 |
| 6 | `ns.cache` 被误清 | 域名归属记录丢失 | 中 | 每次 `-refresh-apply` 前 `mongodump` |
| 7 | 本地私链下 `00_deploy_registrar.ts` 跳过 | 私链缺关键合约 | 中 | 正确设置 `network.tags.use_root` |
| 8 | macOS 本地编译 CGO / Go 版本不一 | 编译失败 | 中 | 装 Xcode CLT；版本以各仓库 README 为准；必要时容器内编译 |
| 9 | 端口映射漏改 `network.nodes[].addresses` | 节点互相连不上 | 中 | 改完全文搜索核对；用 `netcheck` 复验 |
| 10 | Push/Publish 默认外联官方 | 数据外泄到官方服务 | 低 | 显式留空或自建 |

---

## 12. 学习产出物清单（每阶段都要留痕）

| 阶段 | 产出 | 存放位置 |
| --- | --- | --- |
| 1 | 官方 compose 的可工作基线、`client.yml` 副本、netcheck 成功日志 | `playground/01-official-compose/` |
| 2 | 自己生成的一份完整配置 + 密钥体系笔记 | `playground/02-source-build/`、笔记入 `TECH.md` |
| 3 | 各组件的「仓库 + tag + commit」锁定表、自建镜像 Dockerfile | `TECH.md`、`playground/02-source-build/` |
| 4 | 完整合约地址表（含用途）、部署脚本与 `.env` 模板（**脱敏**） | `TECH.md`、`playground/03-anyns/` |
| 5 | `ns-node.yml`（**脱敏**）、缓存备份脚本、CLI 验证记录 | `playground/03-anyns/`、`TECH.md` |
| 6 | 端到端验证清单的实测结果 | `README.md` 的「使用方法」章节 |
| 7 | 自助注册链路的可行性结论 | `TECH.md` |

⚠️ **脱敏提醒**：私钥（`DEPLOYER_KEY`、`adminPk`、任何 `signingKey` / `peerKey`）、Alchemy API Key **绝不能**提交进 git。`.env` 已在 `.gitignore` 中，但 `playground/` 整个目录也被忽略——**这意味着你的笔记放在 `playground/` 里不会进仓库**，需要长期保留的内容要另外整理进 `TECH.md`。

---

## 13. 最小可行路径（如果只有两天）

只想先尝到「能同步」的甜头，按这个顺序做，**跳过命名系统**：

1. **半天**：启动 Docker → clone `any-sync-dockercompose`（v8.0.1）→ `cp .env.example .env` → `./update-versions.sh` → `docker compose up -d` → `docker compose logs netcheck` 看到 `netcheck success`。
2. **半天**：读完 `etc/client.yml` 和 `docker-generateconfig/init.sh`，说清节点类型与密钥体系。
3. **一天**：macOS 上用全新身份启动 Anytype 客户端并指定 `ANY_SYNC_NETWORK=$(pwd)/etc/client.yml`，建立 space、上传文件、验证跨设备同步。

命名系统作为独立支线，等网络本体稳定后再启动阶段 4–5。

---

## 14. 证据与来源

### 14.1 本机实测（2026-10-17）

| 实测项 | 方法 | 结果 |
| --- | --- | --- |
| arm64 架构 | `uname -m` | `arm64` |
| Docker 已装但守护进程未运行 | `docker info` | 报 socket 不存在 |
| 端口空闲 | `lsof -nP -iTCP:<port> -sTCP:LISTEN` | 27001/6379/3900/3901/1001–1006/27017 全部空闲 |
| 磁盘可用 | `df -h /` | 162 GiB |
| bash 版本 | `bash --version` | 3.2.57 |
| 支付节点仓库不存在 | `git ls-remote https://github.com/anyproto/<name>` | `any-sync-ppnode` / `any-sync-paymentnode` / `any-sync-payment-processing-node` / `ppnode` / `any-payments` 全部 5/5 失败 |
| 官方镜像 arm64 支持 | `docker buildx imagetools inspect` | mongo/redis-stack/garage/各节点/any-ns-node 均有原生 linux/arm64 |

### 14.2 官方来源

- 官方一键自托管：[anyproto/any-sync-dockercompose](https://github.com/anyproto/any-sync-dockercompose)（v8.0.1，含 wiki：Installation / Configuration / Compatible-versions / Upgrade-Guide / Troubleshooting-&-FAQ）
- 官方兼容版本 API：[prod](https://puppetdoc.anytype.io/api/v1/prod-any-sync-compatible-versions/) ｜ [stage1](https://puppetdoc.anytype.io/api/v1/stage1-any-sync-compatible-versions/)
- 官方自托管文档：[anyproto/tech-docs · how-to/self-hosting.md](https://github.com/anyproto/tech-docs/blob/main/how-to/self-hosting.md)（⚠️ 最后更新 2024-09-05，**输出文件名与 MinIO 相关内容已过期**）
- 工具集：[anyproto/any-sync-tools](https://github.com/anyproto/any-sync-tools)（v0.7.0，内含 any-sync-network / netcheck / acl-cli / signing）
- 命名系统合约：[anyproto/any-ns](https://github.com/anyproto/any-ns)（v1.0.0）
- 命名服务节点：[anyproto/any-ns-node](https://github.com/anyproto/any-ns-node)（v0.7.2）
- 部署自动化（**不支持 macOS**）：[ansible-anysync](https://github.com/anyproto/ansible-anysync)（platform: Debian / RHEL）、[puppet-anysync](https://github.com/anyproto/puppet-anysync)
- 对象存储：[Garage](https://garagehq.deuxfleurs.fr/)
- 账户抽象 SDK：[anyproto/alchemy-aa-sdk](https://github.com/anyproto/alchemy-aa-sdk)（公开）

### 14.3 本项目内既有调研（`resources/any-sync/`）

- `Any-Sync 去中心化同步网络自建工作清单（含 AnyNS 命名系统）.md` —— 七阶段清单（**含多处已被勘误的结论**）
- `Any-Sync 部署方案评估报告.md` —— 对上者的勘误与官方路径推荐
- `Any-Sync 自研路线补充评估.md` —— 后续修正（文件节点必需、撤销 P0-3、闭源缺口）
- `决策科普：空间语义与 Redis Stack 成本.md` —— 空间语义与 Redis 选型成本

⚠️ 阅读这些文档时请注意已被推翻的结论：**文件节点「可选」已作废（必需）**；**「单机最小集群可省略 Redis 与对象存储」已作废**；**「在协调节点配置里对接命名系统」是错的**（集成点是 `network.nodes` 里的 `types: [namingNode]`）；**「暂无 `name-register` 命令」**。

### 14.4 尚未核实、需本地实验确认的项

1. Apple Silicon 上 MongoDB 镜像是否会触发 AVX 相关检查（官方 FAQ 的 AVX 说明只针对 x86）。
2. macOS Docker Desktop 对 compose 卷 `:Z` 标签的实际处理（SELinux 语义，预期忽略或告警）。
3. `any-ns-node` 配合自建合约在本地私链上的最小可运行配置（官方无示例）。
4. Sepolia 上官方已部署地址**三套记录互相矛盾**，哪一套当前有效未知——建议自行部署，不要依赖官方地址。
5. 任何 macOS/Apple Silicon 专属的已知 issue（GitHub Issues API 限流，未能检索）。
