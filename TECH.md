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

## 9. 排障时最容易踩的坑

| 现象 | 真实原因 |
| --- | --- |
| 节点日志反复 `tree does not exist` | 客户端没有接受节点在已拨出连接上反向打开的流 |
| `HeadSync` 看不到新对象 | HeadSync 是差异同步，不是全量枚举 |
| `ObjectSyncRequestStream` 直接推 headUpdate 返回 `tree not found` | 该接口是**拉取**语义，只接受 `FullSyncRequest` |
| 两个客户端 networkId 不一致 | 用了本地配置 ID 而非协调节点返回的 `networkId` |
| 空间 60 秒后被关闭 | `space.gcTTL` 正常回收，不是错误 |
| 只推一个节点时另外两个返回 `tree not found` | 写入需遍历全部负责节点 |
