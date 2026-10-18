# TECH.md

> 本文件只记录**已在本地网络实测跑通**的做法，以及可直接复用的外部资料索引。
> 历史环境搭建与迁移细节见归档 [TECH-ARCHI.md](TECH-ARCHI.md)。

---

## 1. 项目边界

| 项 | 结论 |
| --- | --- |
| 目标 | 自研 userDomain Web 客户端：用 any-sync 网络承载「用户域 → 库 / 记录」 |
| 禁止 | **不使用 anytype-heart**（非 MIT 协议，且数据模型与本项目不一致），只可读其源码作参考 |
| 网络职责 | 只负责 SpacePush 与 HeadSync（对象同步）；对象语义全部由应用定义 |
| 身份 | BIP-39 12 词 → `m/44'/2046'/i'` 派生账户密钥 |
| 协议 | DRPC（**不是 gRPC**），编码在握手阶段协商（None / Snappy） |

---

## 2. 术语与对象模型

```
用户域（Space，一个空间 ID）
 ├─ 库对象     根变更 changeType=library
 ├─ 记录对象   根变更 changeType=entry，载荷内 lib=<库对象 ID>
 └─ 记录对象   …
```

| 概念 | 落地方式 |
| --- | --- |
| 对象 | 空间内一棵独立的树：`根（RootChange）+ 变更链`，对象 ID = 根变更的 CID |
| 库与记录的关系 | **平级**。归属只由记录载荷里的 `lib` 字段表达 |
| 对象清单 | **空间里没有对象清单**。`SpaceSettingsContent` 只有 `ObjectDelete` / `SpaceDelete`，不登记新增对象 |
| 加密 | 根变更的 `ChangePayload` 用空间 ReadKey（AES）加密后写入，节点只见密文 |
| ACL | 每个变更都引用创建时刻的 ACL 头；权限由 ACL 记录链定义 |

---

## 3. 已跑通的四条链路

### 3.1 取网络配置（不要自算节点）

客户端向**协调节点**要配置，而不是读本地 `nodes.yml` 自己算：

```
Coordinator.NetworkConfiguration(空请求)
  → configurationId、networkId、nodes[]（peerId + addresses + types）
```

实测返回：networkId `N97tZ7HUEZdxoC2JUzFHmuQphYetQbJnjTY3VcAcy6dRmzc5`，6 个节点（3 tree / 1 coordinator / 1 file / 1 consensus）。

### 3.2 建用户域（仅首次）

```
spacepayloads.StoragePayloadForSpaceCreate(...)         // 生成头部 + ACL 根
objecttree.BuildRoot(settings 根, changeType=any-sync.space)
Coordinator.SpaceSign(spaceId, rawHeader)               // 取回执
Spacesync.SpacePush(                                    // 推给每个负责节点
  SpacePayload{SpaceHeader, AclPayload+AclPayloadId,
               SpaceSettingsPayload+Id},
  Credential=serialized(receipt))
```

判据：`SpaceStatusCheck` 返回 `SpaceStatusCreated` + `SpacePermissionsOwner`；`SpacePull` 能取回 settings 与 ACL 记录。

### 3.3 写对象（关键：节点会反向开流）

```
ObjectSyncStream(双向流)
  ① 先发 SpaceSubscription{SpaceIds, Subscribe}
  ② 再发 headUpdate{Heads:[对象ID], Changes:[根变更], RootChange:根}
  ③ 节点发现本地没有该对象 → 在【同一条 yamux 连接上反向开流】
  ④ 客户端必须在已拨出的连接上 MultiConn.Accept()
     → handshake.IncomingProtoHandshake
     → drpcserver.ServeOne(conn)
     → 以 SpaceSync 服务端响应 ObjectSyncRequestStream
  ⑤ 回传 TreeFullSyncResponse{Heads:[对象ID], Changes:[根]}
```

**必须接受反向流**，否则节点侧只会反复出现 `tree does not exist`，对象永不落盘。

### 3.4 读对象（按 ID 拉根）

```
ObjectSyncRequestStream(TreeSyncMessage{
    FullSyncRequest{Probe:true}}, spaceId, objectId)
  → 取回 RootChange
  → sk.Decrypt(rootChange.ChangePayload)
```

**不要用 `HeadSync` 判定写入成败**：它是差异同步语义，新建对象即使已落盘也不会出现在其结果里。

---

## 4. 实测数据与判据

| 项 | 结果 |
| --- | --- |
| 用户域创建 | 3/3 负责节点 `SpacePush` 成功 |
| 库对象写入 | 3/3 节点接受；按 ID 回读 `changeType=library`，载荷为密文 |
| 2 库 + 4 记录 | 主实例 `:8787` 与副本 `:8788` 均从网络读回，`lib` 归属正确 |
| 节点持久化 | `anyStorage/<spaceId>/store.db` 的 `_heads_docs` / `_changes_docs` 含新对象；重启后可回读 |

**判定方式**（唯一可信）：

1. 按对象 ID 调 `ObjectSyncRequestStream(Probe:true)` 能取回根；
2. 解密后的 `changeType` 与载荷内容与写入时一致；
3. 直接查节点 SQLite：`sqlite3 store.db "select * from _heads_docs;"` 能看到该对象 ID。

---

## 5. 本地网络基线

| 组件 | 地址 | 说明 |
| --- | --- | --- |
| coordinator | 127.0.0.1:2004 | 配置下发、SpaceSign、空间状态 |
| consensus | 127.0.0.1:2006 | ACL 校验 |
| filenode | 127.0.0.1:2005 | 文件 |
| node-1/2/3 | 2001 / 2002 / 2003 | 同步节点（tree API），quic 3001–3006 |
| mongo / redis / minio | 27001 / 6379 / 9000 | Docker |

- 配置：`playground/local-net/nodes.yml`、`etc/any-sync-node-{1,2,3}.yml`
- 数据：`playground/local-net/data/node-{1,2,3}/anyStorage/<spaceId>/store.db`
- 节点空间缓存 TTL：`space.gcTTL: 60`（60 秒不活跃即卸载，属正常行为）

---

## 6. 错误码与协议约定

wire 码 = 区间基准 + 本地码；两组撞码会导致进程启动 panic。

| 区间 | 服务 |
| --- | --- |
| 1 / 2 | `Unexpected` / `Closed`（全局保留） |
| 100–199 | spacesync |
| 200–299 | filesync v1 |
| 300–399 | coordinator |
| 400–499 | treechange（`tree not found` 属此段） |
| 500–599 | consensus |
| 600–699 | payment |
| 700–799 | limiter |
| 800–899 | filesync v2 |
| 900–999 | filesync p2p |
| 1000–1099 | nodesync |
| 1100–1199 | pubsub |

其他约定：

- **pubsub 是独立服务与独立 DRPC 长连接**，四种帧 `Subscribe/Unsubscribe/Publish/Status`；禁止复用 `ObjectSyncStream`；payload 用 ReadKey 加密 + 账户密钥签名，节点只转发密文。
- `changeType` 是**任意字符串**，网络不解释。
- 空间头部当前为 **v0**：ACL 与 settings 不内联在头部，而是在 `SpacePayload` 里单独传递。

---

## 7. 资料索引

### 7.1 官方文档（外部）

| 资料 | 用途 |
| --- | --- |
| https://sync.any.org/ | 协议总览：概念、网络与基础设施、访问控制 |
| https://sync.any.org/concepts/ | Space / Object / Change / ACL / 冲突解决 / 快照 |
| https://sync.any.org/networking/ | 四类节点职责；**Channel Routing：客户端向协调节点查询该 Channel 存在哪** |
| https://sync.any.org/access-control/ | ACL 记录类型、密钥分发 |
| https://github.com/anyproto/any-sync-sdk/tree/main/docs | SDK 文档：`object.md`、`space.md`、`crdt.md`、`data-structure.md` 等 24 篇 |

### 7.2 仓库内文档

| 路径 | 内容 |
| --- | --- |
| `src/any-sync/docs/rpc-error-offsets.md` | 错误码全局分配表 |
| `src/any-sync/docs/stateless-pubsub.md` | 空间内无状态 Pub/Sub 设计 |
| `docs/protoinchinese/` | 38 个 `.proto` 中文注释版（10 个核心协议人工精翻）+ `README.md` 索引 |
| `TECH-ARCHI.md` | 历史环境搭建、迁移记录 |

### 7.3 关键源码位置

| 主题 | 位置 |
| --- | --- |
| 对象同步入口 | `any-sync/commonspace/sync/objectsync/synchandler.go` |
| 请求/响应收集 | `any-sync/commonspace/sync/requestmanager.go`、`object/tree/synctree/responsecollector.go` |
| 树根构造 | `object/tree/objecttree/objecttreefactory.go`（`CreateObjectTreeRoot`） |
| 空间创建载荷 | `commonspace/spacepayloads` |
| 节点侧流处理 | `any-sync-node/nodespace/streamopener.go`、`rpchandler.go` |
| 节点空间加载 | `any-sync-node/nodespace/service.go`（`loadSpace`） |

---

## 8. 当前实现状态

| 能力 | 状态 | 位置 |
| --- | --- | --- |
| 协调节点取配置 | ✅ | 探针 `playground/probe-coord` |
| 建用户域 + SpacePush | ✅ | `test/tools/userdomain-web/objectmodel.go` |
| 库/记录对象写入（含反向流服务端） | ✅ | `objectsync.go`、`objectmodel.go` |
| 按 ID 读对象并解密 | ✅ | `objects.go`（`fetchTreeRoot` / `decryptRootPayload`） |
| 可视化库列表 / 新建库 / 写记录 / 从网络刷新 | ✅ | `web/index.html` |
| 跨设备对象枚举（全新安装） | ❌ 未实现 | 目前靠本地 `data/libraries.jsonl` 记录对象 ID |
| PubSub 订阅推送 | ❌ 未实现 | 见第 6 节约定 |

> `test/` 与 `playground/` 按约定不入库，仅本地保留。

---

## 9. 空间内对象写入与自举（20261017 22:45-01 已实施）

本节记录**用户域 → 库 → 信息对象**的落地模型，以及写入链路上三个必须避开的坑。全部结论来自本地网络实测（2 库 4 信息对象，主/副本双实例回归）。

### 9.1 数据模型

```
SpaceHeaderPayload = {v, spaceType:"userdomain",
                      registry:{changeType, changePayload, parentId}}
        │ 确定性推导（派生根：ID 只由 spaceId + 参数决定）
        ▼
库注册表树（派生根）── 变更 ──▶ 每次新建库追加一条 {op:add, libId, name}
        │
        ▼
库树（派生根，ID = f(spaceId, 库名)）── 变更 ──▶ {op:addInfo, infoId}
        │
        ▼
信息对象（独立根，载荷含 lib=<库树 ID>，内容用 ReadKey 加密）
```

| 层 | 可变性 | 说明 |
| --- | --- | --- |
| SpaceHeaderPayload | **不可变**（签名 + spaceId 由它算出） | 只放“注册表推导描述”，不放字面 ID，避免循环依赖 |
| 注册表树 / 库树 | 可追加变更 | 用**派生根**才能被节点接受追加（实测：签名根追加会被拒） |
| 信息对象 | 各自独立根 | 内容密文；`lib` 属性表达归属 |

### 9.2 新设备自举流程

```
助记词 → 账户密钥
      → 协调节点 NetworkConfiguration
      → SpacePull(spaceId) 得到 spaceHeaderPayload
      → 推导 registryId
      → 拉注册表树全部变更 → 库 ID 列表
      → 逐库拉库树变更 → 字段定义 + 信息对象 ID
      → 逐对象拉根 → ReadKey 解密 → 本地重建
```

接口：`GET /api/domain/libraries?mnemonic=…`，返回库、字段与信息对象。

### 9.3 三个必须避开的坑（本轮实测）

| # | 坑 | 正确做法 |
| --- | --- | --- |
| 1 | 推送变更时把 **变更 ID** 当作 `ObjectSyncMessage.objectId` | 必须是**树 ID**，否则节点当成未知新对象，变更永远不落盘 |
| 2 | 把整条 `RawTreeChange` 当密文解密 | 先解 `RawTreeChange → TreeChange`，再解 `TreeChange.changesData` |
| 3 | 用**签名根**的树追加变更 | 实测被节点拒绝；改用**派生根**（`BuildDerivedRoot`）后追加成功 |

追加变更时 `BuilderContent` 的必备字段（对齐 anytype-heart 的 `prepareBuilderContent`）：

```go
BuilderContent{
    TreeHeadIds:    heads,              // 从网络拉到的当前 heads
    AclHeadId:      aclHead,            // SpacePull 的 ACL 头
    SnapshotBaseId: root.GetId(),       // 树根 ID（漏了会重建失败）
    ReadKeyId:      firstAclRecordId,   // 读密钥引入记录（漏了节点无法校验）
    PrivKey:        signKey,
    ReadKey:        spaceReadKey,
    Content:        plaintext,          // 明文，由 builder 加密（不要自己先加密）
    Timestamp:      now,
}
```

### 9.4 验收判据

| 项 | 预期 |
| --- | --- |
| 注册表树变更数 | 根 + 每个库一条 |
| 每条库登记变更 | `snapshotBaseId = 根`、`prevIds` 指向上一 head |
| 自举结果 | 库数、字段数、信息对象数与写入一致 |
| 副本实例 | 仅凭助记词得到相同结果（不依赖本地索引） |

### 9.5 账户与用户域必须一致（本轮踩坑）

现象：点击「从网络重建」后看到的是别人的库 / 与本地列表不一致。

根因：UI 自动填充助记词时取了**历史记录第一条**，它属于另一个账户；用这把钥匙建库会被节点拒绝（ACL 不允许），
而注册表读取时又按**用户域所有者**解析，于是两边对不上。

落地规则：

| 规则 | 实现 |
| --- | --- |
| 用户域有唯一所有者 | `domain.json.ownerAccount` |
| 助记词必须与所有者一致 | 建库、写记录、自举三处均校验，不一致直接返回 400 并提示正确账户 |
| UI 默认助记词按所有者匹配 | 先读 `GET /api/domain/info` 拿 ownerAccount，再从历史里找对应助记词 |
| 页面显式展示域与所有者 | 库面板顶部显示 `用户域：<spaceId>　所有者：<accountId>` |
| 重建结果合并本地 | 同 space、同 owner、且链上能拉到详情的本地库会并入自举结果，避免登记缺失造成缺项 |

### 9.6 客户端交互契约（本轮调整）

| 操作 | 语义 | 实现 |
| --- | --- | --- |
| 右侧用户域列表点击 | **只把助记词填入登录面板，不触发登录** | 前端仅赋值输入框，提示“点「使用助记词登录」” |
| 使用助记词登录 | 清空本地库与对象残留 → 用该助记词派生密钥与网络握手 → 拉取远程用户域内容写入本地 | `POST /api/login`：`clearLocalData` → 握手 → `pullAndSave`；返回 notes 说明拉取数量 |
| 新建库 | 用当前密钥建库树并推送到负责节点，同时在注册表登记 | `POST /api/libraries`（账户必须与用户域所有者一致） |
| 删除本地数据 | 清空本地库与对象索引，**保留用户域身份**，便于再次拉取 | `POST /api/domain/clear` |
| 刷新本地 | 只重读本地存档，不访问网络 | `GET /api/libraries` |
| 从网络拉取 | 视作本地为空，全量拉取并覆盖本地记录 | `GET /api/domain/libraries?save=1` |

按钮顺序（库面板）：**新建库 → 删除本地数据 → 刷新本地 → 从网络拉取**。

登录语义补充：用户域身份（`spaceId` + `readKey`）保存在 `data/domain.json`，`删除本地数据` **不清除**它，否则无法再次定位空间；清掉它等同于放弃该用户域的本地入口。

### 9.7 删除与用户域隔离（本轮修正）

**删除即更新**：客户端删除库不是删本地记录，而是往**库注册表树**追加一条 `{op:"del", libId}` 变更，
由网络同步给所有设备；本地随后才移除记录。

| 行为 | 实现 | 判据 |
| --- | --- | --- |
| 删除库 | 注册表追加 `del` 变更 → 删除本地记录 | 再次拉取不再出现；副本同样消失 |
| 删除本地数据 | 只清本地记录，**不写网络** | 重新拉取可恢复 |
| 注册表状态解析 | 顺序回放变更：`add` 加入、`del` 移除 | 以最后一次操作为准 |

**新建用户域 = 新建空间**：点「生成用户域」会：

1. 生成新助记词并派生密钥；
2. 调用 `SpaceSign` + `SpacePush` 创建**新的空间**；
3. 把 `data/domain.json` 指向新空间（`spaceId` + `readKey` + `ownerAccount`）；
4. 清空本地库记录。

因此“新用户域 → 登录 → 从网络拉取”必然得到**空结果**；此前的错误数据来自 `domain.json` 仍指向旧空间。

**空注册表**：新用户域还没有任何库时，注册表树尚未创建，拉取应返回空列表而不是报错
（`tree not found` 视为“无库”）。

### 9.8 记录级删除与交互细节（本轮调整）

**记录删除同样是“更新”**：往**库树**追加一条 `{op:"delInfo", infoId}` 变更，读取时按顺序回放
（`addInfo` 加入、`delInfo` 移除，以最后一次为准）。接口：`DELETE /api/libraries/entries?id=<libId>&changeId=<infoId>`。

| 层级 | 操作 | 变更写在哪 | 读取时如何生效 |
| --- | --- | --- | --- |
| 库 | 删除库 | 注册表树 `{op:"del", libId}` | 回放时移除该库 |
| 记录 | 删除记录 | 库树 `{op:"delInfo", infoId}` | 回放时移除该记录 |
| 本地 | 删除本地数据 | 不写网络 | 重新拉取可恢复 |

**UI 不锁**：新建库、写记录、删除记录都不禁用按钮，也不阻塞其他操作；结果统一走库面板的绿字提示
（成功即提示，不弹窗）。

**登录按账户切换用户域**：`data/domains.json` 保存 `accountId → 用户域`；
登录时先按账户查这份登记，命中则把 `domain.json` 切到该域再拉取，避免“用新域助记词却拉到旧域数据”。
服务启动时会把已有的 `domain.json` 补登记进 `domains.json`。

### 9.9 版本页脚

页面最下方固定一条 **40px 高、内容居中** 的页脚：

```
power by hoxiudimdim anythinks V{version} @ dev：{commit}
```

| 字段 | 来源 |
| --- | --- |
| version | 仓库根 `package.json` 的 `version`（运行期读取，向上最多找 6 层目录） |
| commit | 构建时注入：`-X main.buildCommit=<短哈希>`，未注入时为 `unknown` |
| 分支 | 固定 `dev` |

接口：`GET /api/version` → `{version, commit, branch}`。

推荐构建命令（在工具目录执行）：

```bash
go build -ldflags "-X main.buildCommit=$(git -C ../../.. rev-parse --short HEAD)"   -o bin/userdomain-web .
```

页脚通过接口异步填充，加载失败时降级为 `power by hoxiudimdim anythinks`。

### 9.10 副本同步与缓存（本轮修正）

**问题**：OTHER 副本（:8788）页面显示旧内容 / 未及时更新。

**两个根因**：

| 根因 | 修复 |
| --- | --- |
| 浏览器缓存了旧 `index.html` | 静态与接口统一加 `Cache-Control: no-store, no-cache, must-revalidate`（`noCache` 包装） |
| 副本没有主动同步 | 副本实例启动后台任务，每 **20 秒** 从网络 `pullAndSave` 一次 |

**前端**：页面加载后每 **5 秒** 重读一次 `/api/libraries`，内容变化即重绘（不打扰正在输入的表单）。

**注意**：本机主/副本共用同一个 `data/libraries.jsonl`，所以本地记录天然一致；
副本后台拉取的意义在于把**网络上其他设备的更新**带进本地，界面轮询再把变化呈现出来。

### 9.11 实时同步（head update 订阅）

对象变更的实时通知**不需要 PubSub**：节点把 head update 广播给所有带该 spaceId 标签的流，
客户端只要把 `ObjectSyncStream` 常驻并先发 `SpaceSubscription` 即可收到。

```
ObjectSyncStream（常驻）
  ① SpaceSubscription{SpaceIds:[space], Subscribe}   → 节点给这条流打上 space 标签
  ② 其他实例写入 → 节点 nodePeerManager.BroadcastMessage → streamPool.Broadcast(spaceId)
  ③ 客户端收到 HeadUpdate{objectId, heads, changes}
  ④ 去抖 500ms → pullAndSave（按对象或整域拉取）
```

| 项 | 实现要点 |
| --- | --- |
| 订阅生命周期 | 跟随当前用户域；`domain.json` 变化即取消旧订阅、订阅新空间 |
| 断线重连 | 读流出错后 5 秒重试；重连成功做一次全量对账 |
| 去抖 | 500ms 合并同一批事件，避免重复拉取 |
| 兜底 | 保留定时轮询（副本 20 秒），广播 at-most-once 不保证送达 |
| 观测 | `GET /api/sync/status`：connected / events / pulls / lastEventAt / lastError |

**必须记住的坑（实测）**

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 订阅几秒后 `context canceled`，节点日志 `peer close` + `stream removed` | 同一个**设备密钥（peerId）**存在多条连接：新连接到达时节点关闭旧连接 | 每个进程、每种用途各用独立 device key：业务用 `device-<实例>.key`，订阅用 `device-<实例>-sub.key` |
| 多进程共享助记词时互相踢线 | 助记词派生出相同 device key | 账户密钥仍来自助记词，**device key 单独生成并持久化** |

结论：**同一账户下，设备身份的粒度是“每个客户端实例、每种连接用途”**；绝不能让两个进程或两类连接共用同一 device key。

## 10. 排障时最容易踩的坑

| 现象 | 真实原因 |
| --- | --- |
| 节点日志反复 `tree does not exist` | 客户端没有接受节点在已拨出连接上反向打开的流 |
| `HeadSync` 看不到新对象 | HeadSync 是差异同步，不是全量枚举 |
| `ObjectSyncRequestStream` 直接推 headUpdate 返回 `tree not found` | 该接口是**拉取**语义，只接受 `FullSyncRequest` |
| 两个客户端 networkId 不一致 | 用了本地配置 ID 而非协调节点返回的 `networkId` |
| 空间 60 秒后被关闭 | `space.gcTTL` 正常回收，不是错误 |
| 只推一个节点时另外两个返回 `tree not found` | 写入需遍历全部负责节点 |
| 订阅几秒后断流、节点日志 `peer close` / `stream removed` | 同一设备密钥（peerId）存在多条连接，被节点挤掉；每进程/每用途用独立 device key（见 9.11） |
| 自举结果与本地列表对不上 | 助记词账户与用户域所有者不一致（见 9.5） |
| 往已有树追加变更后 heads 不变 | 推送时 `objectId` 用了变更 ID，必须用树 ID（见 9.3） |

## 11. 密钥体系（S1–S9）

> 本节的**定义**按项目既定口径（用户确认版本）记录；"实现状态"列标注本客户端的落地情况。

| 编号 | 名称 | 定义 | 实现状态 |
| --- | --- | --- | --- |
| **S1** | 助记词 | 12 词 BIP39。当前落盘保存，最终由用户自行保管，用于登录 | ✅ 已实现（落盘 `userdomains.jsonl`，0600；属过渡手段） |
| **S2** | SLIP-10 主节点 MasterKey | 助记词 → `m/44'/2046'/i'`。用于派生全部账号密钥；作为 `MasterKey` 参与空间创建（写入 ACL 根并由其签名）；`accountKey` 即它的 base64 | ✅ 已修正：空间创建改传 SLIP-10 MasterKey（此前误传设备密钥） |
| **S3** | 账号签名 key（Identity, Ed25519） | 主节点派生 `m/44'/2046'/i'/0'`。public → **Account() = 账号 ID**；作为 any-sync `SignKey` 签名空间 / ACL / 树操作；派生出账号元数据对称 key（见 S6） | ✅ 已实现 |
| **S4** | 设备 / 对端 key（Ed25519） | 每个客户端随机、每库随机。`device.key` 用账号 key 加密落盘。public → **PeerId() = 设备网络身份**；作为 any-sync `PeerKey` 完成网络握手 / 对端身份 | ⚠️ 部分：已随机 + 按实例/用途持久化；**仍为明文 base64（0600），未用账号 key 加密** |
| **S5** | Ethereum key（ECDSA/secp256k1） | 主节点派生 `m/44'/60'/0'/0/i`。签 Ethereum 交易 + **Any Naming Service**（.any 域名） | ✅ 已派生并展示地址 |
| **S6** | 账号元数据对称 key（ProfileSymKey） | 由账号签名 key 经 SLIP-0021 路径 `m/SLIP-0021/anythinks/account/metadata` 派生。用于账号元数据的 E2EE（含 profile 对称 key），供换设备登录时解密 | ❌ 未实现（路径口径待确认，见下） |
| **S7** | 用户域密钥 | 派生类空间（个人/默认库、技术空间、一对一）的空间标识与读密钥均由账号密钥确定性派生，可跨设备恢复；新建/共享空间（Create）的 ReadKey 为随机 AES、MetadataKey 为随机 Ed25519，不从账号密钥派生。读密钥用于空间内容加密，账号 SignKey 用于变更签名，防止传输中被篡改 | ✅ 已核对源码（派生路径与差异见 11.4） |
| **S8** | 会话 / app-link 密钥 | `WalletCreateSession` 随机生成，用于本地 API 授权 grant（app link） | ❌ 未实现（当前无本地 API 授权层） |
| **S9** | localApiSecret（传输级） | 每次启动随机 32B，stdin 注入；用于授权 gRPC 引导调用，非派生密钥 | ❌ 未实现 |

### 11.1 与源码的对照备注

| 项 | 事实 | 影响 |
| --- | --- | --- |
| S2 与空间 ID | `spaceId = CID(RawSpaceHeader)`，头部含**随机 seed**、identity、spaceType 等；MasterKey 不进头部，只进 **ACL 根**（公钥 + 签名） | “MasterKey 参与空间 ID 派生”仅对 **Derive 空间**成立；普通 Create 空间不成立 |
| S4 落盘 | heart：`accountKey.GetPublic().Encrypt(proto)` 后写文件 | 我们当前为明文 base64，需按此改进 |
| S6 路径 | heart 现有常量为 `m/SLIP-0021/anytype/account/metadata`（`core/domain/account.go`）与 `m/SLIP-0021/anytype/space/key`（pushnotificationkeys） | 若需与 Anytype 共用账号元数据，路径须用 `anytype`；若为本项目自有命名，则按 `anythinks` 独立体系 |
| S7 说明 | 派生类空间读密钥由账号 SignKey 经 SLIP-0021 派生（`m/SLIP-0021/anysync/space`），不是"无读密钥"；共享空间 ReadKey 为随机 AES | 详见 11.4 |

### 11.2 设备密钥的使用规则（已实现）

- 账户密钥来自助记词（S3），设备密钥**独立生成**并持久化；
- 同一账户下按「实例 + 用途」分离：`device-<实例>.key`（业务连接）、`device-<实例>-sub.key`（实时订阅）；
- 原因：同一 peerId 多连接会被节点关闭旧连接（详见 9.11）。

### 11.4 空间分类与密钥来源（按用户表格重构）

> 术语对应：any-sync / anytype 的 **Space ↔ 我们的「库」**。用户域是我们系统独有的账号级概念，any-sync 侧没有单一等价物（由默认库 + 账号元数据 + 协作库等共同构成）。

| | 空间标识 Space ID | 空间密钥（加密 / 签名） |
| --- | --- | --- |
| 派生类空间（个人 / 技术 / 一对一） | ✅ 确定性派生（SignKey + MasterKey + SpaceType） | ✅ 由账号密钥确定性派生 |
| 新建 / 共享空间（Create） | ❌ 新生成 | ❌ ReadKey 随机 AES、MetadataKey 随机 Ed25519 |

- **派生类空间**：空间 ID 与空间密钥确定性派生，可跨设备恢复。个人空间即我们的「默认库」。
- **新建 / 共享空间**：ReadKey / MetadataKey 随机、空间 ID 新生成——因为共享空间要由 ACL 管理多参与者，不能从单一账号密钥派生。

**与源码的校准（已确认）**：

| 项 | 校准结论 | 依据 |
| --- | --- | --- |
| 派生空间 ID 的输入 | v0 派生器不含 MasterKey；只有 v1 内嵌 ACL 根才间接包含 | `spacepayloads.go` 两套派生函数对比 |
| 派生空间读密钥来源 | 由 **SignKey** 经 SLIP-0021 派生，不是 MasterKey | `AclState.deriveKey()`（`aclstate.go:1107`）、`aclstatebuilder.go:13` |
| 共享空间 ID 的产生方 | 客户端本地生成随机 seed 的头部算出 ID；协调节点只做签名授权与配额校验 | `StoragePayloadForSpaceCreate` + `coordinator.SpaceSign` |

**派生空间 ID 公式（v0）**：`spaceId = CID(header{identity, spaceType, spaceHeaderPayload, replicationKey = fnv(identityPub)})`
**派生空间读密钥**：`readKey = DeriveSymmetricKey(SignKey.Raw(), "m/SLIP-0021/anysync/space")`

### 11.3 待办

| # | 待办 | 关联 |
| --- | --- | --- |
| 1 | 设备密钥改用账号公钥加密后落盘 | S4 |
| 2 | 界面展示的 devicePeerId 与真实连接设备统一 | S4 |
| 3 | 账号元数据对称 key 与 profile 加密 | S6 |
| 4 | 按 11.4 的新模型重构：库=空间、用户域=账号级视图 | S7 / 空间分类 |
| 5 | 本地 API 授权（app link / localApiSecret） | S8 / S9 |
