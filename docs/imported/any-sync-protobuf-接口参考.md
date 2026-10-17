# any-sync 协议 Protobuf 接口参考

> **固定版本学习底稿**
>
>  —— 由本地 
>
> `any-sync-ecosystem`
>
>  快照中的 
>
> `.proto`
>
>  源码自动解析生成（2026-09-16 快照）。
> 协议核心 any-sync v0.13.2；本文档锁定的就是当前这份快照，后续学习、测试、自研客户端均以此为准。

## 范围与统计



| 项           | 值                                                                                |
| ----------- | -------------------------------------------------------------------------------- |
| 覆盖仓库        | `any-sync`（协议核心）、`any-sync-node`、`any-sync-filenode`、`any-block`（format/v1 数据格式） |
| 文件数         | 28 个 `.proto`                                                                    |
| 服务（service） | 17 个                                                                             |
| RPC 方法      | 112 个                                                                            |
| 消息（message） | 727 个（含嵌套消息）                                                                     |
| 枚举（enum）    | 133 个                                                                            |
| 明确排除        | `anytype-heart`（官方客户端 API，本学习路径不使用）；`any-block` 根目录旧副本（以 `format/v1/proto` 为准）   |

> 注：
>
> `nameservice`
>
> 、
>
> `paymentservice`
>
>  系列文件无 
>
> `package`
>
>  声明，本文档按 
>
> `go_package`
>
>  目录归组。

## 目录



1. [协议总览](#一协议总览)

2. [RPC 方法详表](#二rpc-方法详表)

3. [消息结构](#三消息结构)

4. [枚举](#四枚举)

5. [附录](#五附录)

## 一、协议总览

### 1.1 服务全景



| 包                | 服务                        | RPC 数 | 职责                                                | 调用关系                       |
| ---------------- | ------------------------- | ----- | ------------------------------------------------- | -------------------------- |
| `anyNodeSync`    | `NodeSync`                | 3     | sync node 之间的空间数据同步（节点间复制、对账）                     | sync node ↔ sync node      |
| `clientspace`    | `ClientSpace`             | 2     | 客户端空间辅助：space 级轻量远程调用（会话 / 存储信息获取）                | 客户端 ↔ sync node            |
| `consensusProto` | `Consensus`               | 4     | ACL 共识校验：成员 / 权限变更记录的校验与批准（sync node 间由 RAFT 承载）  | sync node ↔ consensus node |
| `coordinator`    | `Coordinator`             | 22    | 协调器：空间注册 / 路由、网络配置下发、空间列表与配置查询                    | 客户端 ↔ coordinator          |
| `filesync`       | `File`                    | 14    | 文件同步 v1：CID 寻址的文件块上传 / 下载 / 校验（客户端↔filenode）      | 客户端 ↔ filenode             |
| `filesyncp2p`    | `FileP2P`                 | 2     | P2P 文件传输：客户端之间直接传输文件块（不经 filenode）                | 客户端 ↔ 客户端                  |
| `filesyncv2`     | `FileV2`                  | 5     | 文件同步 v2：文件组 / 文件快照粒度的同步接口（客户端↔filenode）           | 客户端 ↔ filenode             |
| `identityRepo`   | `IdentityRepo`            | 3     | 身份仓库：identity 元数据的注册、查询、删除                        | 客户端 ↔ identity node        |
| `nodeapi`        | `NodeApi`                 | 6     | 节点调试 / 管理 API：仅用于调试运维，非业务协议                       | 运维工具 ↔ sync node           |
| `pubsub`         | `PubSub`                  | 1     | 空间事件发布订阅：推送空间内对象变更事件                              | 客户端 ↔ sync node            |
| `spacesync`      | `SpaceSync`               | 10    | 空间同步核心：对象变更同步、空间存储操作、对象拉取 / 订阅（客户端↔sync node 主协议） | 客户端 ↔ sync node            |
| `testService`    | `Test`                    | 4     | 协议测试服务：仅用于框架自测（endtoendtest /streampool）          | 测试                         |
| `testService`    | `Test`                    | 2     | 协议测试服务：仅用于框架自测（endtoendtest /streampool）          | 测试                         |
| `（无 package）`    | `AnyPaymentProcessing`    | 11    | 支付处理 v1：套餐 / 订阅 / 支付意图、余额查询                       | 客户端 ↔ payment service      |
| `（无 package）`    | `AnyPaymentProcessingV2`  | 8     | 支付处理 v2：会话支付、订阅管理、发票、权益                           | 客户端 ↔ payment service      |
| `（无 package）`    | `Anyns`                   | 8     | 名字服务：.any 名称的可用性查询、注册、解析、续期、转移                    | 客户端 ↔ name service         |
| `（无 package）`    | `AnynsAccountAbstraction` | 7     | 名字服务账户抽象：链上交易 / 账户相关的名称操作                         | 客户端 ↔ name service         |

### 1.2 文件清单



| 相对路径                                                                            | package          | 服务                      | RPC | 消息  | 枚举 |
| ------------------------------------------------------------------------------- | ---------------- | ----------------------- | --- | --- | -- |
| `any-block/format/v1/proto/changes.proto`                                       | `anytype`        | —                       | 0   | 34  | 1  |
| `any-block/format/v1/proto/events.proto`                                        | `anytype`        | —                       | 0   | 226 | 8  |
| `any-block/format/v1/proto/models.proto`                                        | `anytype.model`  | —                       | 0   | 125 | 74 |
| `any-block/format/v1/proto/snapshot.proto`                                      | `anytype`        | —                       | 0   | 3   | 0  |
| `any-sync-filenode/index/indexproto/protos/index.proto`                         | `fileIndexProto` | —                       | 0   | 6   | 0  |
| `any-sync-node/debug/nodedebugrpc/nodedebugrpcproto/protos/nodedebugrpc.proto`  | `nodeapi`        | NodeApi                 | 6   | 13  | 0  |
| `any-sync-node/nodesync/nodesyncproto/protos/nodesync.proto`                    | `anyNodeSync`    | NodeSync                | 3   | 9   | 3  |
| `any-sync/commonfile/fileproto/filep2p/protos/filep2p.proto`                    | `filesyncp2p`    | FileP2P                 | 2   | 5   | 2  |
| `any-sync/commonfile/fileproto/fileprotov2/protos/filev2.proto`                 | `filesyncv2`     | FileV2                  | 5   | 20  | 2  |
| `any-sync/commonfile/fileproto/protos/file.proto`                               | `filesync`       | File                    | 14  | 27  | 2  |
| `any-sync/commonspace/clientspaceproto/protos/clientspace.proto`                | `clientspace`    | ClientSpace             | 2   | 5   | 0  |
| `any-sync/commonspace/object/acl/aclrecordproto/protos/aclrecord.proto`         | `aclrecord`      | —                       | 0   | 23  | 2  |
| `any-sync/commonspace/object/tree/treechangeproto/protos/treechange.proto`      | `treechange`     | —                       | 0   | 13  | 1  |
| `any-sync/commonspace/pubsub/pubsubproto/protos/pubsub.proto`                   | `pubsub`         | PubSub                  | 1   | 5   | 1  |
| `any-sync/commonspace/spacesyncproto/protos/spacesync.proto`                    | `spacesync`      | SpaceSync               | 10  | 33  | 6  |
| `any-sync/consensus/consensusproto/protos/consensus.proto`                      | `consensusProto` | Consensus               | 4   | 16  | 1  |
| `any-sync/coordinator/coordinatorproto/protos/coordinator.proto`                | `coordinator`    | Coordinator             | 22  | 59  | 11 |
| `any-sync/identityrepo/identityrepoproto/protos/identityrepo.proto`             | `identityRepo`   | IdentityRepo            | 3   | 7   | 0  |
| `any-sync/nameservice/nameserviceproto/protos/nameservice.proto`                | `—`              | Anyns                   | 8   | 10  | 0  |
| `any-sync/nameservice/nameserviceproto/protos/nameservice_aa.proto`             | `—`              | AnynsAccountAbstraction | 7   | 16  | 1  |
| `any-sync/net/endtoendtest/testpeer/testproto/protos/testservice.proto`         | `testService`    | Test                    | 4   | 1   | 0  |
| `any-sync/net/rpc/limiter/limiterproto/protos/limiter.proto`                    | `limiter`        | —                       | 0   | 0   | 1  |
| `any-sync/net/secureservice/handshake/handshakeproto/protos/handshake.proto`    | `anyHandshake`   | —                       | 0   | 4   | 4  |
| `any-sync/net/streampool/testservice/protos/testservice.proto`                  | `testService`    | Test                    | 2   | 1   | 0  |
| `any-sync/paymentservice/paymentserviceproto/protos/paymentservice.proto`       | `—`              | AnyPaymentProcessing    | 11  | 29  | 5  |
| `any-sync/paymentservice/paymentserviceproto/protos/paymentservice2.proto`      | `—`              | AnyPaymentProcessingV2  | 8   | 31  | 6  |
| `any-sync/paymentservice/paymentserviceproto/protos/paymentservice_tiers.proto` | `—`              | —                       | 0   | 5   | 1  |
| `any-sync/util/crypto/cryptoproto/protos/crypto.proto`                          | `crypto`         | —                       | 0   | 1   | 1  |

## 二、RPC 方法详表

> 流式列：
>
> `R`
>
> \= 请求流式，
>
> `S`
>
> \= 响应流式，
>
> `RS`
>
> \= 双向流式，空 = 普通一元调用。

### NodeApi · `nodeapi`

**文件**：`any-sync-node/debug/nodedebugrpc/nodedebugrpcproto/protos/nodedebugrpc.proto`　　**职责**：节点调试 / 管理 API：仅用于调试运维，非业务协议



| 方法                      | 流式 | 请求                             | 响应                              | 说明 |
| ----------------------- | -- | ------------------------------ | ------------------------------- | -- |
| `DumpTree`              | —  | `DumpTreeRequest`              | `DumpTreeResponse`              |    |
| `TreeParams`            | —  | `TreeParamsRequest`            | `TreeParamsResponse`            |    |
| `AllTrees`              | —  | `AllTreesRequest`              | `AllTreesResponse`              |    |
| `AllSpaces`             | —  | `AllSpacesRequest`             | `AllSpacesResponse`             |    |
| `ForceNodeSync`         | —  | `ForceNodeSyncRequest`         | `ForceNodeSyncResponse`         |    |
| `NodesAddressesBySpace` | —  | `NodesAddressesBySpaceRequest` | `NodesAddressesBySpaceResponse` |    |

### NodeSync · `anyNodeSync`

**文件**：`any-sync-node/nodesync/nodesyncproto/protos/nodesync.proto`　　**职责**：sync node 之间的空间数据同步（节点间复制、对账）



| 方法              | 流式 | 请求                     | 响应                      | 说明                                                                                                                                                                                                              |
| --------------- | -- | ---------------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PartitionSync` | —  | `PartitionSyncRequest` | `PartitionSyncResponse` | PartitionSync compares all spaces by given c-hash partition                                                                                                                                                     |
| `ColdSync`      | S  | `ColdSyncRequest`      | `ColdSyncResponse`      | ColdSync requests cold sync stream for fast space download                                                                                                                                                      |
| `AdoptArchive`  | —  | `AdoptArchiveRequest`  | `AdoptArchiveResponse`  | AdoptArchive offers the receiver an archived space snapshot parked in the shared archive store; the receiver copies the object into its own prefix and registers the space as archived without materializing it |

### FileP2P · `filesyncp2p`

**文件**：`any-sync/commonfile/fileproto/filep2p/protos/filep2p.proto`　　**职责**：P2P 文件传输：客户端之间直接传输文件块（不经 filenode）

> FileP2P is the peer-to-peer file transfer service. It is served READ-ONLY by a client to other LAN peers so a device can fetch a file's encrypted CAR object directly from a nearby peer that already holds it, instead of the file-node / object-storage path — enabling local-network file sync, offline (no reachable node) reads, and durability takeover (a peer re-uploading a file whose creator never made it durable).  drpc route prefix is "/filesyncp2p.FileP2P/..." — DISTINCT from v1 "/filesync.File/..." and v2 "/filesyncv2.FileV2/...", so all three can be mounted on one drpc mux. Names are load-bearing: method paths derive from 
>
> `package filesyncp2p`
>
>  \+ 
>
> `service FileP2P`
>
> .  Model: a client stores one immutable, content-addressed CARv2 object per file, byte-identical to the object the S3/public-read path serves. So a peer is simply an ALTERNATE SOURCE of that same object: ObjectRead returns object byte RANGES exactly like an HTTP Range GET, and the fetcher's existing seed/verify path (parse header+index, then verify every block against its cid) is reused unchanged. Because a partial local copy has holes, ObjectRead is served only by peers that hold the file in FULL; FileCheck reports which.  Conventions: * requests are ROOT-SCOPED (rootCid) — the store is one CAR per root, keyed by rootCid, with no global block-CID index; * identity is NEVER a request field — it is the authenticated connection; authorization (may this peer read this space) is the server's job; * object bytes are CIPHERTEXT (the file layer is encrypted before the DAG is built), so serving them discloses no plaintext; the FETCHER verifies every block against its cid (nothing on this wire does).



| 方法           | 流式 | 请求                  | 响应                   | 说明                                                                                                                                                                                                               |
| ------------ | -- | ------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `FileCheck`  | —  | `FileCheckRequest`  | `FileCheckResponse`  | FileCheck reports, per requested rootCid, whether the server holds the file fully, partially, or not at all — so a client can pick a FULL peer to ObjectRead from without first knowing the object geometry.     |
| `ObjectRead` | —  | `ObjectReadRequest` | `ObjectReadResponse` | ObjectRead returns a byte range of the file's CARv2 object. Mirrors an HTTP Range GET: totalSize echoes the whole-object size (for the head probe / index-tail read). Served only when the file is held in full. |

### FileV2 · `filesyncv2`

**文件**：`any-sync/commonfile/fileproto/fileprotov2/protos/filev2.proto`　　**职责**：文件同步 v2：文件组 / 文件快照粒度的同步接口（客户端↔filenode）

> FileV2 is the v2 filenode broker (S3-direct uploads/downloads).  drpc route prefix is "/filesyncv2.FileV2/..." — DISTINCT from v1 "/filesync.File/..." so both services can be mounted on the same drpc mux without a Register() panic. The package/service names are load-bearing: method paths are derived from 
>
> `package filesyncv2`
>
>  \+ 
>
> `service FileV2`
>
> .  Conventions (all four SPACE-SCOPED RPCs are BATCH; Info is node-level): * request carries a single shared spaceId (or repeated spaceIds for SpaceInfo) + a repeated list of items; * identity is NEVER a request field — it is taken from the authenticated connection, and all per-space/per-cid authorization derives from it; * rootCid is bytes (raw self-describing CID, as in v1's 
>
> `bytes cid`
>
> ); * every result echoes its own key (rootCid bytes, or spaceId string) so clients build map[string(key)]->result in one pass — results are matched by key, NEVER by positional index; the server may reorder/dedupe; * per-item result = flat status enum (ErrCode, Ok=0) + exactly one typed payload message that is valid ONLY when code == Ok; * one bad/forbidden item never fails the whole batch.  Two error layers: 1. whole-RPC drpc error (err != nil), carrying an ErrCodes value from the offset-800 rpcerr registry, returned ONLY for cross-cutting failures: failed/absent auth (Forbidden), malformed input (InvalidRequest), an over-sized batch (QuerySizeExceeded), or a misrouted single-space request (NotResponsible — retry against the space's responsible pair); 2. per-item business outcome lives in the in-body ErrCode 
>
> `code`
>
>  field (err == nil for the RPC as a whole).



| 方法                | 流式 | 请求                       | 响应                        | 说明                                                                                                                             |
| ----------------- | -- | ------------------------ | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `Upload`          | —  | `UploadRequest`          | `UploadResponse`          | Upload issues a presigned upload target per requested file root.                                                               |
| `RequestSign`     | —  | `RequestSignRequest`     | `RequestSignResponse`     | RequestSign returns a network-signed durable-custody receipt per rootCid.                                                      |
| `RequestDownload` | —  | `RequestDownloadRequest` | `RequestDownloadResponse` | RequestDownload returns a signed GET target per rootCid.                                                                       |
| `SpaceInfo`       | —  | `SpaceInfoRequest`       | `SpaceInfoResponse`       | SpaceInfo returns quota/usage per requested space (batch quota-info).                                                          |
| `Info`            | —  | `InfoRequest`            | `InfoResponse`            | Info returns static node-level metadata (no spaceId, no responsibility gate, no auth beyond the connection); clients cache it. |

### File · `filesync`

**文件**：`any-sync/commonfile/fileproto/protos/file.proto`　　**职责**：文件同步 v1：CID 寻址的文件块上传 / 下载 / 校验（客户端↔filenode）



| 方法                   | 流式 | 请求                          | 响应                    | 说明                                                                                                                                                                 |
| -------------------- | -- | --------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `BlockGet`           | —  | `BlockGetRequest`           | `BlockGetResponse`    | BlockGet gets one block from a server                                                                                                                              |
| `BlockPush`          | —  | `BlockPushRequest`          | `Ok`                  | BlockPush pushes one block to a server                                                                                                                             |
| `BlockPushMany`      | —  | `BlockPushManyRequest`      | `Ok`                  | BlockPushMany pushes many blocks to a server                                                                                                                       |
| `BlocksCheck`        | —  | `BlocksCheckRequest`        | `BlocksCheckResponse` | BlocksCheck checks is CIDs exists                                                                                                                                  |
| `BlocksBind`         | —  | `BlocksBindRequest`         | `Ok`                  | BlocksBind binds CIDs to space                                                                                                                                     |
| `FilesDelete`        | —  | `FilesDeleteRequest`        | `FilesDeleteResponse` | FilesDelete deletes files by id                                                                                                                                    |
| `FilesInfo`          | —  | `FilesInfoRequest`          | `FilesInfoResponse`   | FilesInfo return info by given files id                                                                                                                            |
| `FilesGet`           | S  | `FilesGetRequest`           | `FilesGetResponse`    | FilesGet returns a stream that streams all file ids in the space                                                                                                   |
| `Check`              | —  | `CheckRequest`              | `CheckResponse`       | Check checks the connection and credentials                                                                                                                        |
| `SpaceInfo`          | —  | `SpaceInfoRequest`          | `SpaceInfoResponse`   | SpaceInfo returns usage, limit, etc about space                                                                                                                    |
| `AccountInfo`        | —  | `AccountInfoRequest`        | `AccountInfoResponse` | AccountInfo returns usage, limit, etc by all spaces                                                                                                                |
| `AccountLimitSet`    | —  | `AccountLimitSetRequest`    | `Ok`                  | AccountLimitSet sets the account file storage limit (available only for nodeconf members)                                                                          |
| `SpaceLimitSet`      | —  | `SpaceLimitSetRequest`      | `Ok`                  | SpaceLimitSet sets the space limit. Limit 0 means space will use account limits.                                                                                   |
| `BlockDeleteUnbound` | —  | `BlockDeleteUnboundRequest` | `Ok`                  | BlockDeleteUnbound permanently deletes a block that is not bound to any space (refs == 0). Available only for coordinator nodes; intended for invite-file cleanup. |

### ClientSpace · `clientspace`

**文件**：`any-sync/commonspace/clientspaceproto/protos/clientspace.proto`　　**职责**：客户端空间辅助：space 级轻量远程调用（会话 / 存储信息获取）



| 方法                | 流式 | 请求                       | 响应                        | 说明                                                                                                                                                                                                                                                                                                                                                                                                |
| ----------------- | -- | ------------------------ | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SpaceExchange`   | —  | `SpaceExchangeRequest`   | `SpaceExchangeResponse`   | SpaceExchange sends plaintext space id lists to any LAN peer. Deprecated: leaks the full space set to unauthenticated strangers; use SpaceExchangeV2.                                                                                                                                                                                                                                             |
| `SpaceExchangeV2` | —  | `SpaceExchangeV2Request` | `SpaceExchangeV2Response` | SpaceExchangeV2 lets two LAN peers learn only the intersection of their space sets. Instead of space ids, peers exchange per-space HMAC tokens keyed by a discovery key derived from the space's first ACL read key — a secret only members hold. A valid token both hides the space from non-members and proves the sender's membership. See clientspaceproto/exchange2.go for token derivation. |

### PubSub · `pubsub`

**文件**：`any-sync/commonspace/pubsub/pubsubproto/protos/pubsub.proto`　　**职责**：空间事件发布订阅：推送空间内对象变更事件



| 方法             | 流式 | 请求              | 响应              | 说明                                                                                                     |
| -------------- | -- | --------------- | --------------- | ------------------------------------------------------------------------------------------------------ |
| `PubSubStream` | RS | `PubSubMessage` | `PubSubMessage` | PubSubStream is a long-lived bidirectional stream multiplexing all spaces and topics between two peers |

### SpaceSync · `spacesync`

**文件**：`any-sync/commonspace/spacesyncproto/protos/spacesync.proto`　　**职责**：空间同步核心：对象变更同步、空间存储操作、对象拉取 / 订阅（客户端↔sync node 主协议）



| 方法                        | 流式 | 请求                     | 响应                      | 说明                                                                                                       |
| ------------------------- | -- | ---------------------- | ----------------------- | -------------------------------------------------------------------------------------------------------- |
| `HeadSync`                | —  | `HeadSyncRequest`      | `HeadSyncResponse`      | HeadSync compares all objects and their hashes in a space                                                |
| `StoreDiff`               | —  | `StoreDiffRequest`     | `StoreDiffResponse`     | StoreDiff compares all objects and their hashes in a space                                               |
| `StoreElements`           | RS | `StoreKeyValue`        | `StoreKeyValue`         | StoreElements exchanges elements between peers                                                           |
| `SpacePush`               | —  | `SpacePushRequest`     | `SpacePushResponse`     | SpacePush sends new space to the node                                                                    |
| `SpacePull`               | —  | `SpacePullRequest`     | `SpacePullResponse`     | SpacePull gets space from the remote peer                                                                |
| `ObjectSyncStream`        | RS | `ObjectSyncMessage`    | `ObjectSyncMessage`     | ObjectSyncStream opens object sync stream with node or client                                            |
| `ObjectSync`              | —  | `ObjectSyncMessage`    | `ObjectSyncMessage`     | ObjectSync sends object sync message and synchronously gets response message                             |
| `ObjectSyncRequestStream` | S  | `ObjectSyncMessage`    | `ObjectSyncMessage`     | ObjectSyncRequestStream opens sends a request and gets streamed response                                 |
| `AclAddRecord`            | —  | `AclAddRecordRequest`  | `AclAddRecordResponse`  | AclAddRecord adds a new record to acl log. Works only with any-sync-node deprecated: use coordinator api |
| `AclGetRecords`           | —  | `AclGetRecordsRequest` | `AclGetRecordsResponse` | AclGetRecords gets acl records deprecated: use coordinator api                                           |

### Consensus · `consensusProto`

**文件**：`any-sync/consensus/consensusproto/protos/consensus.proto`　　**职责**：ACL 共识校验：成员 / 权限变更记录的校验与批准（sync node 间由 RAFT 承载）



| 方法          | 流式 | 请求                 | 响应                | 说明                                                |
| ----------- | -- | ------------------ | ----------------- | ------------------------------------------------- |
| `LogAdd`    | —  | `LogAddRequest`    | `Ok`              | LogAdd adds new log to consensus                  |
| `RecordAdd` | —  | `RecordAddRequest` | `RawRecordWithId` | RecordAdd adds new record to log                  |
| `LogWatch`  | RS | `LogWatchRequest`  | `LogWatchEvent`   | LogWatch fetches log and subscribes for a changes |
| `LogDelete` | —  | `LogDeleteRequest` | `Ok`              | LogDelete deletes the log from the consensus      |

### Coordinator · `coordinator`

**文件**：`any-sync/coordinator/coordinatorproto/protos/coordinator.proto`　　**职责**：协调器：空间注册 / 路由、网络配置下发、空间列表与配置查询



| 方法                      | 流式 | 请求                             | 响应                              | 说明                                                                                                                                                                                                           |
| ----------------------- | -- | ------------------------------ | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `SpaceSign`             | —  | `SpaceSignRequest`             | `SpaceSignResponse`             | SpaceSign signs a space creation operation                                                                                                                                                                   |
| `SpaceStatusCheck`      | —  | `SpaceStatusCheckRequest`      | `SpaceStatusCheckResponse`      | SpaceStatusCheck checks the status of space and tells if it is deleted or not                                                                                                                                |
| `SpaceStatusCheckMany`  | —  | `SpaceStatusCheckManyRequest`  | `SpaceStatusCheckManyResponse`  | SpaceStatusCheckMany checks the statuses of spaces and tells if they are deleted or not                                                                                                                      |
| `SpaceStatusChange`     | —  | `SpaceStatusChangeRequest`     | `SpaceStatusChangeResponse`     | SpaceStatusChange changes the status of space - Deprecated                                                                                                                                                   |
| `SpaceMakeShareable`    | —  | `SpaceMakeShareableRequest`    | `SpaceMakeShareableResponse`    | SpaceMakeShareable makes space shareable                                                                                                                                                                     |
| `SpaceMakeUnshareable`  | —  | `SpaceMakeUnshareableRequest`  | `SpaceMakeUnshareableResponse`  | SpaceMakeUnshareable marks space unshareable                                                                                                                                                                 |
| `NetworkConfiguration`  | —  | `NetworkConfigurationRequest`  | `NetworkConfigurationResponse`  | NetworkConfiguration retrieves the latest network configuration                                                                                                                                              |
| `DeletionLog`           | —  | `DeletionLogRequest`           | `DeletionLogResponse`           | DeletionLog gets the latest deletion log records                                                                                                                                                             |
| `SpaceDelete`           | —  | `SpaceDeleteRequest`           | `SpaceDeleteResponse`           | SpaceDelete deletes a space                                                                                                                                                                                  |
| `AccountDelete`         | —  | `AccountDeleteRequest`         | `AccountDeleteResponse`         | AccountDelete deletes an account                                                                                                                                                                             |
| `AccountRevertDeletion` | —  | `AccountRevertDeletionRequest` | `AccountRevertDeletionResponse` | AccountRevertDeletion reverts an account deletion                                                                                                                                                            |
| `AclAddRecord`          | —  | `AclAddRecordRequest`          | `AclAddRecordResponse`          | AclAddRecord adds a new record to acl log. Works only with any-sync-node                                                                                                                                     |
| `AclGetRecords`         | —  | `AclGetRecordsRequest`         | `AclGetRecordsResponse`         | AclGetRecords gets acl records                                                                                                                                                                               |
| `AccountLimitsSet`      | —  | `AccountLimitsSetRequest`      | `AccountLimitsSetResponse`      | AccountLimitsSet sets limits to the account. Can be used only by a network config member                                                                                                                     |
| `AclEventLog`           | —  | `AclEventLogRequest`           | `AclEventLogResponse`           | EventLog gets the latest event log records                                                                                                                                                                   |
| `InboxFetch`            | —  | `InboxFetchRequest`            | `InboxFetchResponse`            | InboxFetch returns a set of (new) messages starting from a given offset                                                                                                                                      |
| `InboxAddMessage`       | —  | `InboxAddMessageRequest`       | `InboxAddMessageResponse`       | InboxFetch returns a set of (new) messages starting from a given offset                                                                                                                                      |
| `NotifySubscribe`       | S  | `NotifySubscribeRequest`       | `NotifySubscribeEvent`          | NotifySubscribe returns a subscription to new inbox msg                                                                                                                                                      |
| `AclUploadInvite`       | —  | `AclUploadInviteRequest`       | `AclUploadInviteResponse`       | AclUploadInvite uploads invite binary data to the filenodes                                                                                                                                                  |
| `AclDeleteInvite`       | —  | `AclDeleteInviteRequest`       | `AclDeleteInviteResponse`       | AclDeleteInvite permanently removes an invite file from the filenodes. The caller must be the space owner and the invite must be revoked in the acl.                                                         |
| `FileLimitsGet`         | —  | `FileLimitsGetRequest`         | `FileLimitsGetResponse`         | FileLimitsGet returns the file-storage pool bounds for an uploader identity in a space (files v2; fileV2 nodes only). The response carries absolute bounds — the caller computes effective headroom locally. |
| `FileUsageReport`       | —  | `FileUsageReportRequest`       | `FileUsageReportResponse`       | FileUsageReport accepts per-(space, identity) durable file usage reports from fileV2 nodes. The reporting node is taken from the authenticated peer context. Values are absolute (idempotent re-reports).    |

### IdentityRepo · `identityRepo`

**文件**：`any-sync/identityrepo/identityrepoproto/protos/identityrepo.proto`　　**职责**：身份仓库：identity 元数据的注册、查询、删除



| 方法           | 流式 | 请求                  | 响应                 | 说明                                               |
| ------------ | -- | ------------------- | ------------------ | ------------------------------------------------ |
| `DataPut`    | —  | `DataPutRequest`    | `Ok`               | DataPut puts client data to a repository         |
| `DataDelete` | —  | `DataDeleteRequest` | `Ok`               | DataDelete deletes client data from a repository |
| `DataPull`   | —  | `DataPullRequest`   | `DataPullResponse` | DataPull pulls client data from a repository     |

### Anyns · `（无 package）`

**文件**：`any-sync/nameservice/nameserviceproto/protos/nameservice.proto`　　**职责**：名字服务：.any 名称的可用性查询、注册、解析、续期、转移



| 方法                        | 流式 | 请求                          | 响应                           | 说明                                                                                                                      |
| ------------------------- | -- | --------------------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `IsNameAvailable`         | —  | `NameAvailableRequest`      | `NameAvailableResponse`      | Lookup: name -> address                                                                                                 |
| `BatchIsNameAvailable`    | —  | `BatchNameAvailableRequest` | `BatchNameAvailableResponse` |                                                                                                                         |
| `GetNameByAddress`        | —  | `NameByAddressRequest`      | `NameByAddressResponse`      | Reverse lookup: address -> name                                                                                         |
| `BatchGetNameByAddress`   | —  | `BatchNameByAddressRequest` | `BatchNameByAddressResponse` |                                                                                                                         |
| `GetNameByAnyId`          | —  | `NameByAnyIdRequest`        | `NameByAddressResponse`      | Reverse lookup: ANY ID -> name                                                                                          |
| `BatchGetNameByAnyId`     | —  | `BatchNameByAnyIdRequest`   | `BatchNameByAddressResponse` |                                                                                                                         |
| `AdminNameRegisterSigned` | —  | `NameRegisterRequestSigned` | `OperationResponse`          | Register new name for the user (on behalf of the user) Anytype CAN only register names for users, but can not transfer! |
| `AdminNameRenewSigned`    | —  | `NameRenewRequestSigned`    | `OperationResponse`          |                                                                                                                         |

### AnynsAccountAbstraction · `（无 package）`

**文件**：`any-sync/nameservice/nameserviceproto/protos/nameservice_aa.proto`　　**职责**：名字服务账户抽象：链上交易 / 账户相关的名称操作



| 方法                            | 流式 | 请求                                    | 响应                            | 说明                                                                                                                                                                                                                                                                                               |
| ----------------------------- | -- | ------------------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `GetOperation`                | —  | `GetOperationStatusRequest`           | `OperationResponse`           | COMMON METHODS:                                                                                                                                                                                                                                                                                  |
| `AdminFundUserAccount`        | —  | `AdminFundUserAccountRequestSigned`   | `OperationResponse`           | ADMIN METHODS: Will send "access tokens" to the user's account (to his SmartContractWallet). User will be able to use these "access tokens" to register his name later directly.  Blocking, will send TX to EVM chain If finished without error -> please use GetUserAccount to get updated info |
| `AdminFundGasOperations`      | —  | `AdminFundGasOperationsRequestSigned` | `OperationResponse`           | Each operation is a single blockchain TX like "name update". User will be able to send operations without having any gas in his wallet later                                                                                                                                                     |
| `GetUserAccount`              | —  | `GetUserAccountRequest`               | `UserAccount`                 | USER METHODS: Use it to: 1 - get your SmartContractWallet address 2 - get how many operations you still have                                                                                                                                                                                     |
| `GetDataNameRegister`         | —  | `NameRegisterRequest`                 | `GetDataNameRegisterResponse` | Example usage: 1. get data + context 2. sign it with your Ethereum private key 3. send it using CreateUserOperation 4. check operation status using GetOperation  Register new name for my Any identity                                                                                          |
| `GetDataNameRegisterForSpace` | —  | `NameRegisterForSpaceRequest`         | `GetDataNameRegisterResponse` | Register new name and attach Space ID to it                                                                                                                                                                                                                                                      |
| `CreateUserOperation`         | —  | `CreateUserOperationRequestSigned`    | `OperationResponse`           | TODO rpc GetDataNameUpdate(NameUpdateRequest) returns (GetDataNameRegisterResponse) {}                                                                                                                                                                                                           |

### Test · `testService`

**文件**：`any-sync/net/endtoendtest/testpeer/testproto/protos/testservice.proto`　　**职责**：协议测试服务：仅用于框架自测（endtoendtest /streampool）



| 方法                    | 流式 | 请求              | 响应              | 说明 |
| --------------------- | -- | --------------- | --------------- | -- |
| `BiDirectionalStream` | RS | `StreamMessage` | `StreamMessage` |    |
| `ServerStream`        | S  | `StreamMessage` | `StreamMessage` |    |
| `ClientStream`        | R  | `StreamMessage` | `StreamMessage` |    |
| `Unary`               | —  | `StreamMessage` | `StreamMessage` |    |

### Test · `testService`

**文件**：`any-sync/net/streampool/testservice/protos/testservice.proto`　　**职责**：协议测试服务：仅用于框架自测（endtoendtest /streampool）



| 方法            | 流式 | 请求              | 响应              | 说明 |
| ------------- | -- | --------------- | --------------- | -- |
| `TestStream`  | RS | `StreamMessage` | `StreamMessage` |    |
| `TestStream2` | S  | `StreamMessage` | `StreamMessage` |    |

### AnyPaymentProcessing · `（无 package）`

**文件**：`any-sync/paymentservice/paymentserviceproto/protos/paymentservice.proto`　　**职责**：支付处理 v1：套餐 / 订阅 / 支付意图、余额查询

> NOTICE: 1 - User can not ask for a payment/other links on behalf of another user (a signature is required) 2 - Admin can do that on behalf of any user



| 方法                          | 流式 | 请求                                       | 响应                                  | 说明                                                                                                                                                                                                                                                                               |
| --------------------------- | -- | ---------------------------------------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GetSubscriptionStatus`     | —  | `GetSubscriptionRequestSigned`           | `GetSubscriptionResponse`           |                                                                                                                                                                                                                                                                                  |
| `IsNameValid`               | —  | `IsNameValidRequest`                     | `IsNameValidResponse`               | Check if the requested name is valid for the requested tier before requesting a payment link and paying                                                                                                                                                                          |
| `BuySubscription`           | —  | `BuySubscriptionRequestSigned`           | `BuySubscriptionResponse`           | Save a new BillingID to DB, and return a payment link. You can call BuySubscription multiple times even if current payment is not processed yet (to get new payment link). If user has already an active subscription, then this will return an error.                           |
| `FinalizeSubscription`      | —  | `FinalizeSubscriptionRequestSigned`      | `FinalizeSubscriptionResponse`      | If your subscription is in StatusPendingRequiresFinalization, then you need to call this method                                                                                                                                                                                  |
| `GetSubscriptionPortalLink` | —  | `GetSubscriptionPortalLinkRequestSigned` | `GetSubscriptionPortalLinkResponse` | Generate a link to the portal where user can: a) change her billing details b) see payment info, invoices, etc c) cancel/renew the subscription                                                                                                                                  |
| `GetVerificationEmail`      | —  | `GetVerificationEmailRequestSigned`      | `GetVerificationEmailResponse`      | Verify user's email: 1st step - get a verification link to the email Will fail if already verified, i.e. you can not change your email                                                                                                                                           |
| `VerifyEmail`               | —  | `VerifyEmailRequestSigned`               | `VerifyEmailResponse`               | Enter the code from the email Will fail if: link was not requested, link is expired, if email is already verified                                                                                                                                                                |
| `GetAllTiers`               | —  | `GetTiersRequestSigned`                  | `GetTiersResponse`                  | Returns all available application tiers, including inactive 1 - this list does not depend on the current platform (iOS, Android, Desktop) 2 - this list can be different for different users, based on their account ID 3 - user can not buy stripe 4 - some tiers are custom () |
| `VerifyAppStoreReceipt`     | —  | `VerifyAppStoreReceiptRequestSigned`     | `VerifyAppStoreReceiptResponse`     | Verify purchase in case subscription was bought via AppStore Incoming receipt contains all information to register purchase on Payment Node                                                                                                                                      |
| `CodeGetInfo`               | —  | `CodeGetInfoRequestSigned`               | `CodeGetInfoResponse`               |                                                                                                                                                                                                                                                                                  |
| `CodeRedeem`                | —  | `CodeRedeemRequestSigned`                | `CodeRedeemResponse`                |                                                                                                                                                                                                                                                                                  |

### AnyPaymentProcessingV2 · `（无 package）`

**文件**：`any-sync/paymentservice/paymentserviceproto/protos/paymentservice2.proto`　　**职责**：支付处理 v2：会话支付、订阅管理、发票、权益



| 方法                   | 流式 | 请求                                       | 响应                                        | 说明 |
| -------------------- | -- | ---------------------------------------- | ----------------------------------------- | -- |
| `SubscribeToUpdates` | —  | `MembershipV2.SubscribeToUpdatesRequest` | `MembershipV2.SubscribeToUpdatesResponse` |    |
| `GetProducts`        | —  | `MembershipV2.GetProductsRequest`        | `MembershipV2.GetProductsResponse`        |    |
| `GetStatus`          | —  | `MembershipV2.GetStatusRequest`          | `MembershipV2.GetStatusResponse`          |    |
| `WebAuth`            | —  | `MembershipV2.WebAuthRequest`            | `MembershipV2.WebAuthResponse`            |    |
| `AnyNameIsValid`     | —  | `MembershipV2.AnyNameIsValidRequest`     | `MembershipV2.AnyNameIsValidResponse`     |    |
| `AnyNameAllocate`    | —  | `MembershipV2.AnyNameAllocateRequest`    | `MembershipV2.AnyNameAllocateResponse`    |    |
| `StoreCartGet`       | —  | `MembershipV2.StoreCartGetRequest`       | `MembershipV2.StoreCartGetResponse`       |    |
| `StoreCartUpdate`    | —  | `MembershipV2.StoreCartUpdateRequest`    | `MembershipV2.StoreCartUpdateResponse`    |    |

## 三、消息结构

> 按文件分组；嵌套消息用 
>
> `Parent.Child`
>
>  点路径表示。
>
> `oneof`
>
>  行无字段编号。

### any-block/format/v1/proto/changes.proto

#### `Change`

> the element of change tree used to store and internal apply smartBlock history



| # | 类型                  | 字段           | 说明                                                    |
| - | ------------------- | ------------ | ----------------------------------------------------- |
| 3 | `repeated Content`  | `content`    | set of actions to apply                               |
| 4 | `repeated Snapshot` | `snapshot`   | snapshot - when not null, the Content will be ignored |
| 6 | `repeated FileKeys` | `fileKeys`   | file keys related to changes content                  |
| 7 | `repeated int64`    | `timestamp`  | creation timestamp                                    |
| 8 | `repeated uint32`   | `version`    | version of business logic                             |
| 9 | `repeated uint32`   | `changeType` | business-level type of change applied to object       |

#### `Change.BlockCreate`



| # | 类型                                      | 字段         | 说明 |
| - | --------------------------------------- | ---------- | -- |
| 1 | `repeated string`                       | `targetId` |    |
| 2 | `repeated anytype.model.Block.Position` | `position` |    |
| 3 | `repeated anytype.model.Block`          | `blocks`   |    |

#### `Change.BlockDuplicate`



| # | 类型                                      | 字段         | 说明 |
| - | --------------------------------------- | ---------- | -- |
| 1 | `repeated string`                       | `targetId` |    |
| 2 | `repeated anytype.model.Block.Position` | `position` |    |
| 3 | `repeated string`                       | `ids`      |    |

#### `Change.BlockMove`



| # | 类型                                      | 字段         | 说明 |
| - | --------------------------------------- | ---------- | -- |
| 1 | `repeated string`                       | `targetId` |    |
| 2 | `repeated anytype.model.Block.Position` | `position` |    |
| 3 | `repeated string`                       | `ids`      |    |

#### `Change.BlockRemove`



| # | 类型                | 字段    | 说明 |
| - | ----------------- | ----- | -- |
| 1 | `repeated string` | `ids` |    |

#### `Change.BlockUpdate`



| # | 类型                       | 字段       | 说明 |
| - | ------------------------ | -------- | -- |
| 2 | `repeated Event.Message` | `events` |    |

#### `Change.Content`



| # | 类型            | 字段 | 说明 |
| - | ------------- | -- | -- |
| — | (oneof) value |    |    |

#### `Change.DetailsSet`



| # | 类型                               | 字段      | 说明 |
| - | -------------------------------- | ------- | -- |
| 1 | `repeated string`                | `key`   |    |
| 2 | `repeated google.protobuf.Value` | `value` |    |

#### `Change.DetailsUnset`



| # | 类型                | 字段    | 说明 |
| - | ----------------- | ----- | -- |
| 1 | `repeated string` | `key` |    |

#### `Change.DeviceAdd`



| # | 类型                                  | 字段       | 说明 |
| - | ----------------------------------- | -------- | -- |
| 1 | `repeated anytype.model.DeviceInfo` | `device` |    |

#### `Change.DeviceUpdate`



| # | 类型                | 字段     | 说明 |
| - | ----------------- | ------ | -- |
| 1 | `repeated string` | `id`   |    |
| 2 | `repeated string` | `name` |    |

#### `Change.FileKeys`



| # | 类型                             | 字段     | 说明 |
| - | ------------------------------ | ------ | -- |
| 1 | `repeated string`              | `hash` |    |
| 2 | `repeated map<string, string>` | `keys` |    |

#### `Change.NotificationCreate`



| # | 类型                                    | 字段             | 说明 |
| - | ------------------------------------- | -------------- | -- |
| 1 | `repeated anytype.model.Notification` | `notification` |    |

#### `Change.NotificationUpdate`



| # | 类型                                           | 字段       | 说明 |
| - | -------------------------------------------- | -------- | -- |
| 1 | `repeated string`                            | `id`     |    |
| 2 | `repeated anytype.model.Notification.Status` | `status` |    |

#### `Change.ObjectTypeAdd`



| # | 类型                | 字段    | 说明 |
| - | ----------------- | ----- | -- |
| 1 | `repeated string` | `url` |    |
| 2 | `repeated string` | `key` |    |

#### `Change.ObjectTypeRemove`



| # | 类型                | 字段    | 说明 |
| - | ----------------- | ----- | -- |
| 1 | `repeated string` | `url` |    |
| 2 | `repeated string` | `key` |    |

#### `Change.OriginalCreatedTimestampSet`



| # | 类型               | 字段   | 说明 |
| - | ---------------- | ---- | -- |
| 1 | `repeated int64` | `ts` |    |

#### `Change.RelationAdd`



| # | 类型                                    | 字段              | 说明 |
| - | ------------------------------------- | --------------- | -- |
| 1 | `repeated anytype.model.RelationLink` | `relationLinks` |    |

#### `Change.RelationRemove`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `relationKey` |    |

#### `Change.SetFileInfo`



| # | 类型                        | 字段         | 说明 |
| - | ------------------------- | ---------- | -- |
| 1 | `repeated model.FileInfo` | `fileInfo` |    |

#### `Change.Snapshot`



| # | 类型                                              | 字段         | 说明                           |
| - | ----------------------------------------------- | ---------- | ---------------------------- |
| 1 | `repeated map<string, string>`                  | `logHeads` | logId -> lastChangeId        |
| 2 | `repeated anytype.model.SmartBlockSnapshotBase` | `data`     | snapshot data                |
| 3 | `repeated FileKeys`                             | `fileKeys` | all file keys related to doc |

#### `Change.StoreKeySet`



| # | 类型                               | 字段      | 说明 |
| - | -------------------------------- | ------- | -- |
| 1 | `repeated string`                | `path`  |    |
| 2 | `repeated google.protobuf.Value` | `value` |    |

#### `Change.StoreKeyUnset`



| # | 类型                | 字段     | 说明 |
| - | ----------------- | ------ | -- |
| 1 | `repeated string` | `path` |    |

#### `Change.StoreSliceUpdate`



| # | 类型                | 字段    | 说明 |
| - | ----------------- | ----- | -- |
| 1 | `repeated string` | `key` |    |
| — | (oneof) operation |       |    |

#### `Change.StoreSliceUpdate.Add`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `afterId` |    |
| 2 | `repeated string` | `ids`     |    |

#### `Change.StoreSliceUpdate.Move`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `afterId` |    |
| 2 | `repeated string` | `ids`     |    |

#### `Change.StoreSliceUpdate.Remove`



| # | 类型                | 字段    | 说明 |
| - | ----------------- | ----- | -- |
| 1 | `repeated string` | `ids` |    |

#### `ChangeNoSnapshot`



| # | 类型                         | 字段           | 说明                                              |
| - | -------------------------- | ------------ | ----------------------------------------------- |
| 3 | `repeated Change.Content`  | `content`    | set of actions to apply                         |
| 6 | `repeated Change.FileKeys` | `fileKeys`   | file keys related to changes content            |
| 7 | `repeated int64`           | `timestamp`  | creation timestamp                              |
| 8 | `repeated uint32`          | `version`    | version of business logic                       |
| 9 | `repeated uint32`          | `changeType` | business-level type of change applied to object |

#### `DocumentCreate`



| # | 类型                | 字段           | 说明   |
| - | ----------------- | ------------ | ---- |
| 1 | `repeated string` | `collection` |      |
| 2 | `repeated string` | `documentId` |      |
| 3 | `repeated string` | `value`      | json |

#### `DocumentDelete`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated string` | `collection` |    |
| 2 | `repeated string` | `documentId` |    |

#### `DocumentModify`



| # | 类型                   | 字段           | 说明 |
| - | -------------------- | ------------ | -- |
| 1 | `repeated string`    | `collection` |    |
| 2 | `repeated string`    | `documentId` |    |
| 4 | `repeated KeyModify` | `keys`       |    |

#### `KeyModify`



| # | 类型                  | 字段            | 说明                                       |
| - | ------------------- | ------------- | ---------------------------------------- |
| 1 | `repeated string`   | `keyPath`     | key path; example: \[user, email]        |
| 3 | `repeated ModifyOp` | `modifyOp`    | modify op: set, unset, inc, etc.         |
| 4 | `repeated string`   | `modifyValue` | json value; example: '"new@example.com"' |

#### `StoreChange`



| # | 类型                            | 字段          | 说明 |
| - | ----------------------------- | ----------- | -- |
| 1 | `repeated StoreChangeContent` | `changeSet` |    |

#### `StoreChangeContent`



| # | 类型             | 字段 | 说明 |
| - | -------------- | -- | -- |
| — | (oneof) change |    |    |

### any-block/format/v1/proto/events.proto

#### `Event`



| # | 类型                               | 字段          | 说明 |
| - | -------------------------------- | ----------- | -- |
| 1 | `repeated Message`               | `messages`  |    |
| 2 | `repeated string`                | `contextId` |    |
| 3 | `repeated anytype.model.Account` | `initiator` |    |
| 4 | `repeated string`                | `traceId`   |    |

#### `Event.Account`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Account.Config`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Account.Config.Update`



| # | 类型                                      | 字段       | 说明 |
| - | --------------------------------------- | -------- | -- |
| 1 | `repeated anytype.model.Account.Config` | `config` |    |
| 2 | `repeated anytype.model.Account.Status` | `status` |    |

#### `Event.Account.Details`



| # | 类型                                | 字段          | 说明 |
| - | --------------------------------- | ----------- | -- |
| 1 | `repeated string`                 | `profileId` |    |
| 2 | `repeated google.protobuf.Struct` | `details`   |    |

#### `Event.Account.LinkChallenge`



| # | 类型                                          | 字段           | 说明 |
| - | ------------------------------------------- | ------------ | -- |
| 1 | `repeated string`                           | `challenge`  |    |
| 2 | `repeated ClientInfo`                       | `clientInfo` |    |
| 3 | `repeated model.Account.Auth.LocalApiScope` | `scope`      |    |

#### `Event.Account.LinkChallenge.ClientInfo`



| # | 类型                | 字段                  | 说明 |
| - | ----------------- | ------------------- | -- |
| 1 | `repeated string` | `processName`       |    |
| 2 | `repeated string` | `processPath`       |    |
| 4 | `repeated string` | `name`              |    |
| 3 | `repeated bool`   | `signatureVerified` |    |

#### `Event.Account.LinkChallengeHide`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Account.Show`



| # | 类型               | 字段      | 说明 |
| - | ---------------- | ------- | -- |
| 1 | `repeated int32` | `index` |    |

#### `Event.Account.Update`



| # | 类型                                      | 字段       | 说明 |
| - | --------------------------------------- | -------- | -- |
| 1 | `repeated anytype.model.Account.Config` | `config` |    |
| 2 | `repeated anytype.model.Account.Status` | `status` |    |

#### `Event.Block`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Add`



| # | 类型                             | 字段       | 说明 |
| - | ------------------------------ | -------- | -- |
| 1 | `repeated anytype.model.Block` | `blocks` |    |

#### `Event.Block.Dataview`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Dataview.GroupOrderUpdate`



| # | 类型                                                         | 字段           | 说明 |
| - | ---------------------------------------------------------- | ------------ | -- |
| 1 | `repeated string`                                          | `id`         |    |
| 2 | `repeated anytype.model.Block.Content.Dataview.GroupOrder` | `groupOrder` |    |

#### `Event.Block.Dataview.IsCollectionSet`



| # | 类型                | 字段      | 说明 |
| - | ----------------- | ------- | -- |
| 1 | `repeated string` | `id`    |    |
| 2 | `repeated bool`   | `value` |    |

#### `Event.Block.Dataview.ObjectOrderUpdate`



| # | 类型                     | 字段             | 说明 |
| - | ---------------------- | -------------- | -- |
| 1 | `repeated string`      | `id`           |    |
| 2 | `repeated string`      | `viewId`       |    |
| 3 | `repeated string`      | `groupId`      |    |
| 4 | `repeated SliceChange` | `sliceChanges` |    |

#### `Event.Block.Dataview.OldRelationDelete`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `id`          |    |
| 2 | `repeated string` | `relationKey` |    |

#### `Event.Block.Dataview.OldRelationSet`

> sent when the dataview relation has been changed or added



| # | 类型                                | 字段            | 说明 |
| - | --------------------------------- | ------------- | -- |
| 1 | `repeated string`                 | `id`          |    |
| 2 | `repeated string`                 | `relationKey` |    |
| 3 | `repeated anytype.model.Relation` | `relation`    |    |

#### `Event.Block.Dataview.RelationDelete`



| # | 类型                | 字段             | 说明 |
| - | ----------------- | -------------- | -- |
| 1 | `repeated string` | `id`           |    |
| 2 | `repeated string` | `relationKeys` |    |

#### `Event.Block.Dataview.RelationSet`

> sent when the dataview relation has been changed or added



| # | 类型                | 字段   | 说明 |
| - | ----------------- | ---- | -- |
| 1 | `repeated string` | `id` |    |

#### `Event.Block.Dataview.SliceChange`



| # | 类型                        | 字段        | 说明 |
| - | ------------------------- | --------- | -- |
| 1 | `repeated SliceOperation` | `op`      |    |
| 2 | `repeated string`         | `ids`     |    |
| 3 | `repeated string`         | `afterId` |    |

#### `Event.Block.Dataview.SourceSet`



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `id`     |    |
| 2 | `repeated string` | `source` |    |

#### `Event.Block.Dataview.TargetObjectIdSet`



| # | 类型                | 字段               | 说明 |
| - | ----------------- | ---------------- | -- |
| 1 | `repeated string` | `id`             |    |
| 2 | `repeated string` | `targetObjectId` |    |

#### `Event.Block.Dataview.ViewDelete`



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `id`     |    |
| 2 | `repeated string` | `viewId` |    |

#### `Event.Block.Dataview.ViewOrder`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `id`      |    |
| 2 | `repeated string` | `viewIds` |    |

#### `Event.Block.Dataview.ViewSet`

> sent when the view have been changed or added



| # | 类型                                                   | 字段     | 说明                                           |
| - | ---------------------------------------------------- | ------ | -------------------------------------------- |
| 1 | `repeated string`                                    | `id`   |                                              |
| 3 | `repeated anytype.model.Block.Content.Dataview.View` | `view` | doesn't switch the active view in the middle |

#### `Event.Block.Dataview.ViewUpdate`



| # | 类型                  | 字段         | 说明 |
| - | ------------------- | ---------- | -- |
| 1 | `repeated string`   | `id`       |    |
| 2 | `repeated string`   | `viewId`   |    |
| 3 | `repeated Filter`   | `filter`   |    |
| 4 | `repeated Relation` | `relation` |    |
| 5 | `repeated Sort`     | `sort`     |    |
| 6 | `repeated Fields`   | `fields`   |    |

#### `Event.Block.Dataview.ViewUpdate.Fields`



| #  | 类型                                                            | 字段                      | 说明              |
| -- | ------------------------------------------------------------- | ----------------------- | --------------- |
| 1  | `repeated anytype.model.Block.Content.Dataview.View.Type`     | `type`                  |                 |
| 2  | `repeated string`                                             | `name`                  |                 |
| 3  | `repeated string`                                             | `coverRelationKey`      |                 |
| 4  | `repeated bool`                                               | `hideIcon`              |                 |
| 6  | `repeated bool`                                               | `coverFit`              |                 |
| 7  | `repeated string`                                             | `groupRelationKey`      |                 |
| 16 | `repeated string`                                             | `endRelationKey`        |                 |
| 8  | `repeated bool`                                               | `groupBackgroundColors` |                 |
| 9  | `repeated int32`                                              | `pageLimit`             |                 |
| 17 | `repeated bool`                                               | `wrapContent`           | within the view |
| 18 | `repeated anytype.model.Block.Content.Dataview.View.ListSize` | `listSize`              |                 |
| 19 | `repeated bool`                                               | `alternateRows`         |                 |

#### `Event.Block.Dataview.ViewUpdate.Filter`



| # | 类型                | 字段 | 说明 |
| - | ----------------- | -- | -- |
| — | (oneof) operation |    |    |

#### `Event.Block.Dataview.ViewUpdate.Filter.Add`



| # | 类型                                                     | 字段        | 说明 |
| - | ------------------------------------------------------ | --------- | -- |
| 1 | `repeated string`                                      | `afterId` |    |
| 2 | `repeated anytype.model.Block.Content.Dataview.Filter` | `items`   |    |

#### `Event.Block.Dataview.ViewUpdate.Filter.Move`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `afterId` |    |
| 2 | `repeated string` | `ids`     |    |

#### `Event.Block.Dataview.ViewUpdate.Filter.Remove`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Dataview.ViewUpdate.Filter.Update`



| # | 类型                                                     | 字段     | 说明 |
| - | ------------------------------------------------------ | ------ | -- |
| 1 | `repeated string`                                      | `id`   |    |
| 2 | `repeated anytype.model.Block.Content.Dataview.Filter` | `item` |    |

#### `Event.Block.Dataview.ViewUpdate.Relation`



| # | 类型                | 字段 | 说明 |
| - | ----------------- | -- | -- |
| — | (oneof) operation |    |    |

#### `Event.Block.Dataview.ViewUpdate.Relation.Add`



| # | 类型                                                       | 字段        | 说明 |
| - | -------------------------------------------------------- | --------- | -- |
| 1 | `repeated string`                                        | `afterId` |    |
| 2 | `repeated anytype.model.Block.Content.Dataview.Relation` | `items`   |    |

#### `Event.Block.Dataview.ViewUpdate.Relation.Move`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `afterId` |    |
| 2 | `repeated string` | `ids`     |    |

#### `Event.Block.Dataview.ViewUpdate.Relation.Remove`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Dataview.ViewUpdate.Relation.Update`



| # | 类型                                                       | 字段     | 说明 |
| - | -------------------------------------------------------- | ------ | -- |
| 1 | `repeated string`                                        | `id`   |    |
| 2 | `repeated anytype.model.Block.Content.Dataview.Relation` | `item` |    |

#### `Event.Block.Dataview.ViewUpdate.Sort`



| # | 类型                | 字段 | 说明 |
| - | ----------------- | -- | -- |
| — | (oneof) operation |    |    |

#### `Event.Block.Dataview.ViewUpdate.Sort.Add`



| # | 类型                                                   | 字段        | 说明 |
| - | ---------------------------------------------------- | --------- | -- |
| 1 | `repeated string`                                    | `afterId` |    |
| 2 | `repeated anytype.model.Block.Content.Dataview.Sort` | `items`   |    |

#### `Event.Block.Dataview.ViewUpdate.Sort.Move`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `afterId` |    |
| 2 | `repeated string` | `ids`     |    |

#### `Event.Block.Dataview.ViewUpdate.Sort.Remove`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Dataview.ViewUpdate.Sort.Update`



| # | 类型                                                   | 字段     | 说明 |
| - | ---------------------------------------------------- | ------ | -- |
| 1 | `repeated string`                                    | `id`   |    |
| 2 | `repeated anytype.model.Block.Content.Dataview.Sort` | `item` |    |

#### `Event.Block.Delete`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.FilesUpload`



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `blockId`  |    |
| 2 | `repeated string` | `filePath` |    |

#### `Event.Block.Fill`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Align`



| # | 类型                                   | 字段      | 说明 |
| - | ------------------------------------ | ------- | -- |
| 1 | `repeated string`                    | `id`    |    |
| 2 | `repeated anytype.model.Block.Align` | `align` |    |

#### `Event.Block.Fill.BackgroundColor`



| # | 类型                | 字段                | 说明 |
| - | ----------------- | ----------------- | -- |
| 1 | `repeated string` | `id`              |    |
| 2 | `repeated string` | `backgroundColor` |    |

#### `Event.Block.Fill.Bookmark`



| # | 类型                        | 字段               | 说明 |
| - | ------------------------- | ---------------- | -- |
| 1 | `repeated string`         | `id`             |    |
| 2 | `repeated Url`            | `url`            |    |
| 3 | `repeated Title`          | `title`          |    |
| 4 | `repeated Description`    | `description`    |    |
| 5 | `repeated ImageHash`      | `imageHash`      |    |
| 6 | `repeated FaviconHash`    | `faviconHash`    |    |
| 7 | `repeated Type`           | `type`           |    |
| 8 | `repeated TargetObjectId` | `targetObjectId` |    |

#### `Event.Block.Fill.Bookmark.Description`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Bookmark.FaviconHash`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Bookmark.ImageHash`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Bookmark.TargetObjectId`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Bookmark.Title`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Bookmark.Type`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Bookmark.Url`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.ChildrenIds`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `id`          |    |
| 2 | `repeated string` | `childrenIds` |    |

#### `Event.Block.Fill.DatabaseRecords`



| # | 类型                                | 字段        | 说明 |
| - | --------------------------------- | --------- | -- |
| 1 | `repeated string`                 | `id`      |    |
| 2 | `repeated google.protobuf.Struct` | `records` |    |

#### `Event.Block.Fill.Details`



| # | 类型                                | 字段        | 说明 |
| - | --------------------------------- | --------- | -- |
| 1 | `repeated string`                 | `id`      |    |
| 2 | `repeated google.protobuf.Struct` | `details` |    |

#### `Event.Block.Fill.Div`



| # | 类型                | 字段      | 说明 |
| - | ----------------- | ------- | -- |
| 1 | `repeated string` | `id`    |    |
| 2 | `repeated Style`  | `style` |    |

#### `Event.Block.Fill.Div.Style`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Fields`



| # | 类型                                | 字段       | 说明 |
| - | --------------------------------- | -------- | -- |
| 1 | `repeated string`                 | `id`     |    |
| 2 | `repeated google.protobuf.Struct` | `fields` |    |

#### `Event.Block.Fill.File`



| # | 类型                | 字段      | 说明 |
| - | ----------------- | ------- | -- |
| 1 | `repeated string` | `id`    |    |
| 2 | `repeated Type`   | `type`  |    |
| 3 | `repeated State`  | `state` |    |
| 4 | `repeated Mime`   | `mime`  |    |
| 5 | `repeated Hash`   | `hash`  |    |
| 6 | `repeated Name`   | `name`  |    |
| 7 | `repeated Size`   | `size`  |    |
| 8 | `repeated Style`  | `style` |    |

#### `Event.Block.Fill.File.Hash`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.File.Mime`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.File.Name`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.File.Size`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.File.State`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.File.Style`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.File.Type`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.File.Width`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Link`



| # | 类型                       | 字段              | 说明 |
| - | ------------------------ | --------------- | -- |
| 1 | `repeated string`        | `id`            |    |
| 2 | `repeated TargetBlockId` | `targetBlockId` |    |
| 3 | `repeated Style`         | `style`         |    |
| 4 | `repeated Fields`        | `fields`        |    |

#### `Event.Block.Fill.Link.Fields`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Link.Style`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Link.TargetBlockId`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Restrictions`



| # | 类型                                          | 字段             | 说明 |
| - | ------------------------------------------- | -------------- | -- |
| 1 | `repeated string`                           | `id`           |    |
| 2 | `repeated anytype.model.Block.Restrictions` | `restrictions` |    |

#### `Event.Block.Fill.Text`



| # | 类型                 | 字段        | 说明 |
| - | ------------------ | --------- | -- |
| 1 | `repeated string`  | `id`      |    |
| 2 | `repeated Text`    | `text`    |    |
| 3 | `repeated Style`   | `style`   |    |
| 4 | `repeated Marks`   | `marks`   |    |
| 5 | `repeated Checked` | `checked` |    |
| 6 | `repeated Color`   | `color`   |    |

#### `Event.Block.Fill.Text.Checked`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Text.Color`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Text.Marks`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Text.Style`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Fill.Text.Text`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.MarksInfo`



| # | 类型                                                    | 字段             | 说明 |
| - | ----------------------------------------------------- | -------------- | -- |
| 1 | `repeated anytype.model.Block.Content.Text.Mark.Type` | `marksInRange` |    |

#### `Event.Block.Set`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Align`



| # | 类型                                   | 字段      | 说明 |
| - | ------------------------------------ | ------- | -- |
| 1 | `repeated string`                    | `id`    |    |
| 2 | `repeated anytype.model.Block.Align` | `align` |    |

#### `Event.Block.Set.BackgroundColor`



| # | 类型                | 字段                | 说明 |
| - | ----------------- | ----------------- | -- |
| 1 | `repeated string` | `id`              |    |
| 2 | `repeated string` | `backgroundColor` |    |

#### `Event.Block.Set.Bookmark`



| # | 类型                        | 字段               | 说明 |
| - | ------------------------- | ---------------- | -- |
| 1 | `repeated string`         | `id`             |    |
| 2 | `repeated Url`            | `url`            |    |
| 3 | `repeated Title`          | `title`          |    |
| 4 | `repeated Description`    | `description`    |    |
| 5 | `repeated ImageHash`      | `imageHash`      |    |
| 6 | `repeated FaviconHash`    | `faviconHash`    |    |
| 7 | `repeated Type`           | `type`           |    |
| 8 | `repeated TargetObjectId` | `targetObjectId` |    |
| 9 | `repeated State`          | `state`          |    |

#### `Event.Block.Set.Bookmark.Description`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Bookmark.FaviconHash`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Bookmark.ImageHash`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Bookmark.State`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Bookmark.TargetObjectId`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Bookmark.Title`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Bookmark.Type`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Bookmark.Url`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.ChildrenIds`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `id`          |    |
| 2 | `repeated string` | `childrenIds` |    |

#### `Event.Block.Set.Div`



| # | 类型                | 字段      | 说明 |
| - | ----------------- | ------- | -- |
| 1 | `repeated string` | `id`    |    |
| 2 | `repeated Style`  | `style` |    |

#### `Event.Block.Set.Div.Style`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Fields`



| # | 类型                                | 字段       | 说明 |
| - | --------------------------------- | -------- | -- |
| 1 | `repeated string`                 | `id`     |    |
| 2 | `repeated google.protobuf.Struct` | `fields` |    |

#### `Event.Block.Set.File`



| # | 类型                        | 字段               | 说明 |
| - | ------------------------- | ---------------- | -- |
| 1 | `repeated string`         | `id`             |    |
| 2 | `repeated Type`           | `type`           |    |
| 3 | `repeated State`          | `state`          |    |
| 4 | `repeated Mime`           | `mime`           |    |
| 5 | `repeated Hash`           | `hash`           |    |
| 6 | `repeated Name`           | `name`           |    |
| 7 | `repeated Size`           | `size`           |    |
| 8 | `repeated Style`          | `style`          |    |
| 9 | `repeated TargetObjectId` | `targetObjectId` |    |

#### `Event.Block.Set.File.Hash`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.File.Mime`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.File.Name`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.File.Size`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.File.State`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.File.Style`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.File.TargetObjectId`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.File.Type`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.File.Width`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Latex`



| # | 类型                   | 字段          | 说明 |
| - | -------------------- | ----------- | -- |
| 1 | `repeated string`    | `id`        |    |
| 2 | `repeated Text`      | `text`      |    |
| 3 | `repeated Processor` | `processor` |    |

#### `Event.Block.Set.Latex.Processor`



| # | 类型                                                     | 字段      | 说明 |
| - | ------------------------------------------------------ | ------- | -- |
| 1 | `repeated anytype.model.Block.Content.Latex.Processor` | `value` |    |

#### `Event.Block.Set.Latex.Text`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Link`



| # | 类型                       | 字段              | 说明 |
| - | ------------------------ | --------------- | -- |
| 1 | `repeated string`        | `id`            |    |
| 2 | `repeated TargetBlockId` | `targetBlockId` |    |
| 3 | `repeated Style`         | `style`         |    |
| 4 | `repeated Fields`        | `fields`        |    |
| 5 | `repeated IconSize`      | `iconSize`      |    |
| 6 | `repeated CardStyle`     | `cardStyle`     |    |
| 7 | `repeated Description`   | `description`   |    |
| 8 | `repeated Relations`     | `relations`     |    |

#### `Event.Block.Set.Link.CardStyle`



| # | 类型                                                    | 字段      | 说明 |
| - | ----------------------------------------------------- | ------- | -- |
| 1 | `repeated anytype.model.Block.Content.Link.CardStyle` | `value` |    |

#### `Event.Block.Set.Link.Description`



| # | 类型                                                      | 字段      | 说明 |
| - | ------------------------------------------------------- | ------- | -- |
| 1 | `repeated anytype.model.Block.Content.Link.Description` | `value` |    |

#### `Event.Block.Set.Link.Fields`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Link.IconSize`



| # | 类型                                                   | 字段      | 说明 |
| - | ---------------------------------------------------- | ------- | -- |
| 1 | `repeated anytype.model.Block.Content.Link.IconSize` | `value` |    |

#### `Event.Block.Set.Link.Relations`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Link.Style`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Link.TargetBlockId`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Relation`



| # | 类型                | 字段    | 说明 |
| - | ----------------- | ----- | -- |
| 1 | `repeated string` | `id`  |    |
| 2 | `repeated Key`    | `key` |    |

#### `Event.Block.Set.Relation.Key`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Restrictions`



| # | 类型                                          | 字段             | 说明 |
| - | ------------------------------------------- | -------------- | -- |
| 1 | `repeated string`                           | `id`           |    |
| 2 | `repeated anytype.model.Block.Restrictions` | `restrictions` |    |

#### `Event.Block.Set.TableRow`



| # | 类型                  | 字段         | 说明 |
| - | ------------------- | ---------- | -- |
| 1 | `repeated string`   | `id`       |    |
| 2 | `repeated IsHeader` | `isHeader` |    |

#### `Event.Block.Set.TableRow.IsHeader`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Text`



| # | 类型                   | 字段          | 说明 |
| - | -------------------- | ----------- | -- |
| 1 | `repeated string`    | `id`        |    |
| 2 | `repeated Text`      | `text`      |    |
| 3 | `repeated Style`     | `style`     |    |
| 4 | `repeated Marks`     | `marks`     |    |
| 5 | `repeated Checked`   | `checked`   |    |
| 6 | `repeated Color`     | `color`     |    |
| 7 | `repeated IconEmoji` | `iconEmoji` |    |
| 8 | `repeated IconImage` | `iconImage` |    |

#### `Event.Block.Set.Text.Checked`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Text.Color`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Text.IconEmoji`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Text.IconImage`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Text.Marks`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Text.Style`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Text.Text`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.VerticalAlign`



| # | 类型                                           | 字段              | 说明 |
| - | -------------------------------------------- | --------------- | -- |
| 1 | `repeated string`                            | `id`            |    |
| 2 | `repeated anytype.model.Block.VerticalAlign` | `verticalAlign` |    |

#### `Event.Block.Set.Widget`



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `id`     |    |
| 2 | `repeated Layout` | `layout` |    |
| 3 | `repeated Limit`  | `limit`  |    |
| 4 | `repeated ViewId` | `viewId` |    |

#### `Event.Block.Set.Widget.Layout`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Widget.Limit`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Block.Set.Widget.ViewId`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Chat`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Chat.Add`



| # | 类型                                | 字段             | 说明 |
| - | --------------------------------- | -------------- | -- |
| 1 | `repeated string`                 | `id`           |    |
| 2 | `repeated string`                 | `orderId`      |    |
| 6 | `repeated string`                 | `afterOrderId` |    |
| 3 | `repeated model.ChatMessage`      | `message`      |    |
| 4 | `repeated string`                 | `subIds`       |    |
| 5 | `repeated google.protobuf.Struct` | `dependencies` |    |

#### `Event.Chat.Delete`



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `id`     |    |
| 2 | `repeated string` | `subIds` |    |

#### `Event.Chat.Update`



| # | 类型                           | 字段        | 说明 |
| - | ---------------------------- | --------- | -- |
| 1 | `repeated string`            | `id`      |    |
| 2 | `repeated model.ChatMessage` | `message` |    |
| 3 | `repeated string`            | `subIds`  |    |

#### `Event.Chat.UpdateMentionReadStatus`



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `ids`    |    |
| 2 | `repeated bool`   | `isRead` |    |
| 3 | `repeated string` | `subIds` |    |

#### `Event.Chat.UpdateMessageCount`



| # | 类型                | 字段             | 说明 |
| - | ----------------- | -------------- | -- |
| 1 | `repeated int32`  | `messageCount` |    |
| 2 | `repeated string` | `subIds`       |    |

#### `Event.Chat.UpdateMessageReadStatus`



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `ids`    |    |
| 2 | `repeated bool`   | `isRead` |    |
| 3 | `repeated string` | `subIds` |    |

#### `Event.Chat.UpdateMessageSyncStatus`



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `ids`      |    |
| 2 | `repeated bool`   | `isSynced` |    |
| 3 | `repeated string` | `subIds`   |    |

#### `Event.Chat.UpdatePinnedStatus`



| # | 类型                           | 字段         | 说明 |
| - | ---------------------------- | ---------- | -- |
| 1 | `repeated model.ChatMessage` | `message`  |    |
| 2 | `repeated bool`              | `isPinned` |    |
| 3 | `repeated string`            | `subIds`   |    |

#### `Event.Chat.UpdateReactionReadStatus`



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `ids`      |    |
| 2 | `repeated bool`   | `isUnread` |    |
| 3 | `repeated string` | `subIds`   |    |

#### `Event.Chat.UpdateReactions`



| # | 类型                                     | 字段          | 说明 |
| - | -------------------------------------- | ----------- | -- |
| 1 | `repeated string`                      | `id`        |    |
| 2 | `repeated model.ChatMessage.Reactions` | `reactions` |    |
| 3 | `repeated string`                      | `subIds`    |    |

#### `Event.Chat.UpdateState`



| # | 类型                         | 字段       | 说明 |
| - | -------------------------- | -------- | -- |
| 1 | `repeated model.ChatState` | `state`  |    |
| 2 | `repeated string`          | `subIds` |    |

#### `Event.Debug`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Debug.ProfileCreated`

> ProfileCreated is emitted whenever the middleware writes a snapshot archive on its own (e.g. the memory-growth detector), so clients can surface it or queue the archive for upload without polling the profiles directory. Archives produced as a result of a client RPC (DebugRunProfiler) are NOT re-announced via this event — the RPC response already carries the path.



| # | 类型                | 字段         | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| - | ----------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `reason`   | reason is a short, stable, UPPER\_SNAKE\_CASE label describing why the middleware produced this report. It is NOT the DebugRunProfiler Reason enum — values come from the internal call sites: - "MEMORY\_GROWTH"  : the desktop memory-growth detector tripped - "LONG\_RPC"       : an RPC exceeded the long-execution threshold - "DB\_CORRUPTION"  : an anystore/spacestore database failed to open More reasons may be added over time; clients should forward unknown values to Sentry as-is. |
| 2 | `repeated string` | `jsonInfo` | jsonInfo is JSON-encoded context produced by the middleware (reason- specific keys like "sysMemory", "method", "durationMs", "db", "code"). Clients forward it verbatim to Sentry as the event context.                                                                                                                                                                                                                                                                                             |
| 3 | `repeated string` | `path`     | path is the absolute path to the snapshot archive on disk; empty when the reason is event-only (e.g. DB\_CORRUPTION) and no artifact was produced.                                                                                                                                                                                                                                                                                                                                                  |
| 4 | `repeated bool`   | `full`     | full is true when the archive carries a timed CPU profile + trace in addition to heap and goroutines. False for fast snapshots and for event-only reports.                                                                                                                                                                                                                                                                                                                                          |

#### `Event.File`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.File.LimitReached`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated string` | `fileId`  |    |

#### `Event.File.LimitUpdated`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.File.LocalUsage`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.File.SpaceUsage`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated uint64` | `bytesUsage` |    |
| 2 | `repeated string` | `spaceId`    |    |

#### `Event.Import`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Import.Finish`



| # | 类型                           | 字段                 | 说明 |
| - | ---------------------------- | ------------------ | -- |
| 1 | `repeated string`            | `rootCollectionID` |    |
| 2 | `repeated int64`             | `objectsCount`     |    |
| 3 | `repeated model.Import.Type` | `importType`       |    |

#### `Event.Membership`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Membership.TiersUpdate`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Membership.Update`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.MembershipV2`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.MembershipV2.ProductsUpdate`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.MembershipV2.Update`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Message`



| #   | 类型                | 字段        | 说明 |
| --- | ----------------- | --------- | -- |
| 132 | `repeated string` | `spaceId` |    |
| —   | (oneof) value     |           |    |

#### `Event.Notification`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Notification.Send`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Notification.Update`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Object`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Object.AutoArchive`



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated string` | `objectIds` |    |

#### `Event.Object.AutoRestore`



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated string` | `objectIds` |    |

#### `Event.Object.CleanupSuggestion`



| # | 类型                 | 字段          | 说明                                                                               |
| - | ------------------ | ----------- | -------------------------------------------------------------------------------- |
| 1 | `repeated string`  | `objectIds` | orphan ids (objects at any level + files at level >= 2) created within contextId |
| 2 | `repeated string`  | `contextId` | the object that was archived / deleted / had a link removed                      |
| 3 | `repeated Trigger` | `trigger`   |                                                                                  |

#### `Event.Object.Close`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Object.Details`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Object.Details.Amend`

> Amend (i.e. add a new key-value pair or update an existing key-value pair) existing state



| # | 类型                  | 字段        | 说明 |
| - | ------------------- | --------- | -- |
| 1 | `repeated string`   | `id`      |    |
| 2 | `repeated KeyValue` | `details` |    |
| 3 | `repeated string`   | `subIds`  |    |

#### `Event.Object.Details.Amend.KeyValue`



| # | 类型                               | 字段      | 说明 |
| - | -------------------------------- | ------- | -- |
| 1 | `repeated string`                | `key`   |    |
| 2 | `repeated google.protobuf.Value` | `value` |    |

#### `Event.Object.Details.Set`

> Overwrite current state



| # | 类型                | 字段       | 说明    |
| - | ----------------- | -------- | ----- |
| 1 | `repeated string` | `id`     |       |
| 3 | `repeated string` | `subIds` | state |

#### `Event.Object.Details.Unset`

> Unset existing detail keys



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `id`     |    |
| 2 | `repeated string` | `keys`   |    |
| 3 | `repeated string` | `subIds` |    |

#### `Event.Object.Relations`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Object.Relations.Amend`



| # | 类型                                    | 字段              | 说明 |
| - | ------------------------------------- | --------------- | -- |
| 1 | `repeated string`                     | `id`            |    |
| 2 | `repeated anytype.model.RelationLink` | `relationLinks` |    |

#### `Event.Object.Relations.Remove`



| # | 类型                | 字段             | 说明 |
| - | ----------------- | -------------- | -- |
| 1 | `repeated string` | `id`           |    |
| 2 | `repeated string` | `relationKeys` |    |

#### `Event.Object.Remove`



| # | 类型                | 字段    | 说明                                 |
| - | ----------------- | ----- | ---------------------------------- |
| 1 | `repeated string` | `ids` | notifies that objects were removed |

#### `Event.Object.Restrictions`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Object.Restrictions.Set`



| # | 类型                                    | 字段             | 说明 |
| - | ------------------------------------- | -------------- | -- |
| 1 | `repeated string`                     | `id`           |    |
| 2 | `repeated anytype.model.Restrictions` | `restrictions` |    |

#### `Event.Object.Subscription`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Object.Subscription.Add`

> Adds new document to subscriptions



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `id`      |    |
| 2 | `repeated string` | `afterId` |    |
| 3 | `repeated string` | `subId`   |    |

#### `Event.Object.Subscription.Counters`



| # | 类型                | 字段          | 说明                                |
| - | ----------------- | ----------- | --------------------------------- |
| 1 | `repeated int64`  | `total`     | total available records           |
| 2 | `repeated int64`  | `nextCount` | how many records available after  |
| 3 | `repeated int64`  | `prevCount` | how many records available before |
| 4 | `repeated string` | `subId`     |                                   |

#### `Event.Object.Subscription.Groups`



| # | 类型                                                    | 字段       | 说明 |
| - | ----------------------------------------------------- | -------- | -- |
| 1 | `repeated string`                                     | `subId`  |    |
| 2 | `repeated anytype.model.Block.Content.Dataview.Group` | `group`  |    |
| 3 | `repeated bool`                                       | `remove` |    |

#### `Event.Object.Subscription.Position`

> Indicates new position of document



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `id`      |    |
| 2 | `repeated string` | `afterId` |    |
| 3 | `repeated string` | `subId`   |    |

#### `Event.Object.Subscription.Remove`

> Removes document from subscription



| # | 类型                | 字段      | 说明 |
| - | ----------------- | ------- | -- |
| 1 | `repeated string` | `id`    |    |
| 2 | `repeated string` | `subId` |    |

#### `Event.P2PStatus`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.P2PStatus.Update`



| # | 类型                | 字段               | 说明 |
| - | ----------------- | ---------------- | -- |
| 1 | `repeated string` | `spaceId`        |    |
| 2 | `repeated Status` | `status`         |    |
| 3 | `repeated int64`  | `devicesCounter` |    |

#### `Event.Payload`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Payload.Broadcast`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Ping`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Process`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Process.Done`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Process.New`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Process.Update`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Space`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Space.SyncStatus`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Space.SyncStatus.Update`



| # | 类型                   | 字段                      | 说明 |
| - | -------------------- | ----------------------- | -- |
| 1 | `repeated string`    | `id`                    |    |
| 2 | `repeated Status`    | `status`                |    |
| 3 | `repeated Network`   | `network`               |    |
| 4 | `repeated SyncError` | `error`                 |    |
| 5 | `repeated int64`     | `syncingObjectsCounter` |    |
| 6 | `repeated int64`     | `notSyncedFilesCounter` |    |
| 7 | `repeated int64`     | `uploadingFilesCounter` |    |

#### `Event.Status`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.Status.Thread`



| # | 类型                 | 字段         | 说明 |
| - | ------------------ | ---------- | -- |
| 1 | `repeated Summary` | `summary`  |    |
| 2 | `repeated Cafe`    | `cafe`     |    |
| 3 | `repeated Account` | `accounts` |    |

#### `Event.Status.Thread.Account`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated string` | `id`         |    |
| 2 | `repeated string` | `name`       |    |
| 3 | `repeated string` | `imageHash`  |    |
| 4 | `repeated bool`   | `online`     |    |
| 5 | `repeated int64`  | `lastPulled` |    |
| 6 | `repeated int64`  | `lastEdited` |    |
| 7 | `repeated Device` | `devices`    |    |

#### `Event.Status.Thread.Cafe`



| # | 类型                    | 字段                | 说明 |
| - | --------------------- | ----------------- | -- |
| 1 | `repeated SyncStatus` | `status`          |    |
| 2 | `repeated int64`      | `lastPulled`      |    |
| 3 | `repeated bool`       | `lastPushSucceed` |    |
| 4 | `repeated PinStatus`  | `files`           |    |

#### `Event.Status.Thread.Cafe.PinStatus`



| # | 类型               | 字段        | 说明 |
| - | ---------------- | --------- | -- |
| 1 | `repeated int32` | `pinning` |    |
| 2 | `repeated int32` | `pinned`  |    |
| 3 | `repeated int32` | `failed`  |    |
| 4 | `repeated int64` | `updated` |    |

#### `Event.Status.Thread.Device`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated string` | `name`       |    |
| 2 | `repeated bool`   | `online`     |    |
| 3 | `repeated int64`  | `lastPulled` |    |
| 4 | `repeated int64`  | `lastEdited` |    |

#### `Event.Status.Thread.Summary`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.User`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.User.Block`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Event.User.Block.Join`



| # | 类型                 | 字段        | 说明 |
| - | ------------------ | --------- | -- |
| 1 | `repeated Account` | `account` |    |

#### `Event.User.Block.Left`



| # | 类型                 | 字段        | 说明 |
| - | ------------------ | --------- | -- |
| 1 | `repeated Account` | `account` |    |

#### `Event.User.Block.SelectRange`



| # | 类型                 | 字段              | 说明 |
| - | ------------------ | --------------- | -- |
| 1 | `repeated Account` | `account`       |    |
| 2 | `repeated string`  | `blockIdsArray` |    |

#### `Event.User.Block.TextRange`



| # | 类型                             | 字段        | 说明 |
| - | ------------------------------ | --------- | -- |
| 1 | `repeated Account`             | `account` |    |
| 2 | `repeated string`              | `blockId` |    |
| 3 | `repeated anytype.model.Range` | `range`   |    |

#### `Model`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Model.Process`



| #  | 类型                  | 字段         | 说明 |
| -- | ------------------- | ---------- | -- |
| 1  | `repeated string`   | `id`       |    |
| 3  | `repeated State`    | `state`    |    |
| 4  | `repeated Progress` | `progress` |    |
| 5  | `repeated string`   | `spaceId`  |    |
| —  | (oneof) message     |            |    |
| 11 | `repeated string`   | `error`    |    |

#### `Model.Process.DropFiles`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Model.Process.Export`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Model.Process.Import`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Model.Process.Migration`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Model.Process.PreloadFile`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Model.Process.Progress`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated int64`  | `total`   |    |
| 2 | `repeated int64`  | `done`    |    |
| 3 | `repeated string` | `message` |    |

#### `Model.Process.SaveFile`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `ResponseEvent`



| # | 类型                       | 字段          | 说明 |
| - | ------------------------ | ----------- | -- |
| 1 | `repeated Event.Message` | `messages`  |    |
| 2 | `repeated string`        | `contextId` |    |
| 4 | `repeated string`        | `traceId`   |    |

### any-block/format/v1/proto/models.proto

#### `Account`



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `id`     |    |
| 4 | `repeated Config` | `config` |    |
| 5 | `repeated Status` | `status` |    |
| 6 | `repeated Info`   | `info`   |    |

#### `Account.Auth`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Account.Auth.AppInfo`



| # | 类型                       | 字段          | 说明 |
| - | ------------------------ | ----------- | -- |
| 1 | `repeated string`        | `appHash`   |    |
| 2 | `repeated string`        | `appName`   |    |
| 4 | `repeated string`        | `appKey`    |    |
| 5 | `repeated int64`         | `createdAt` |    |
| 6 | `repeated int64`         | `expireAt`  |    |
| 7 | `repeated LocalApiScope` | `scope`     |    |
| 8 | `repeated bool`          | `isActive`  |    |

#### `Account.Config`



| #   | 类型                                | 字段                        | 说明 |
| --- | --------------------------------- | ------------------------- | -- |
| 1   | `repeated bool`                   | `enableDataview`          |    |
| 2   | `repeated bool`                   | `enableDebug`             |    |
| 3   | `repeated bool`                   | `enablePrereleaseChannel` |    |
| 4   | `repeated bool`                   | `enableSpaces`            |    |
| 100 | `repeated google.protobuf.Struct` | `extra`                   |    |

#### `Account.Info`



| #   | 类型                | 字段                       | 说明 |
| --- | ----------------- | ------------------------ | -- |
| 2   | `repeated string` | `homeObjectId`           |    |
| 3   | `repeated string` | `archiveObjectId`        |    |
| 4   | `repeated string` | `profileObjectId`        |    |
| 11  | `repeated string` | `marketplaceWorkspaceId` |    |
| 15  | `repeated string` | `workspaceObjectId`      |    |
| 16  | `repeated string` | `spaceChatId`            |    |
| 8   | `repeated string` | `deviceId`               |    |
| 9   | `repeated string` | `accountSpaceId`         |    |
| 10  | `repeated string` | `widgetsId`              |    |
| 13  | `repeated string` | `spaceViewId`            |    |
| 14  | `repeated string` | `techSpaceId`            |    |
| 101 | `repeated string` | `gatewayUrl`             |    |
| 103 | `repeated string` | `localStoragePath`       |    |
| 104 | `repeated string` | `timeZone`               |    |
| 105 | `repeated string` | `analyticsId`            |    |
| 106 | `repeated string` | `networkId`              |    |
| 107 | `repeated string` | `ethereumAddress`        |    |
| 108 | `repeated string` | `metaDataKey`            |    |

#### `Account.Status`



| # | 类型                    | 字段             | 说明 |
| - | --------------------- | -------------- | -- |
| 1 | `repeated StatusType` | `statusType`   |    |
| 2 | `repeated int64`      | `deletionDate` |    |

#### `Block`



| # | 类型                                | 字段                | 说明 |
| - | --------------------------------- | ----------------- | -- |
| 1 | `repeated string`                 | `id`              |    |
| 2 | `repeated google.protobuf.Struct` | `fields`          |    |
| 3 | `repeated Restrictions`           | `restrictions`    |    |
| 4 | `repeated string`                 | `childrenIds`     |    |
| 5 | `repeated string`                 | `backgroundColor` |    |
| 6 | `repeated Align`                  | `align`           |    |
| 7 | `repeated VerticalAlign`          | `verticalAlign`   |    |
| — | (oneof) content                   |                   |    |

#### `Block.Content`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Block.Content.Bookmark`



| # | 类型                          | 字段               | 说明                                                |
| - | --------------------------- | ---------------- | ------------------------------------------------- |
| 1 | `repeated string`           | `url`            |                                                   |
| 2 | `repeated string`           | `title`          | Deprecated. Get this data from the target object. |
| 3 | `repeated string`           | `description`    | Deprecated. Get this data from the target object. |
| 4 | `repeated string`           | `imageHash`      | Deprecated. Get this data from the target object. |
| 5 | `repeated string`           | `faviconHash`    | Deprecated. Get this data from the target object. |
| 6 | `repeated LinkPreview.Type` | `type`           |                                                   |
| 7 | `repeated string`           | `targetObjectId` |                                                   |
| 8 | `repeated State`            | `state`          |                                                   |

#### `Block.Content.Chat`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Block.Content.Dataview`



| #  | 类型                                    | 字段               | 说明         |
| -- | ------------------------------------- | ---------------- | ---------- |
| 1  | `repeated string`                     | `source`         |            |
| 2  | `repeated View`                       | `views`          |            |
| 3  | `repeated string`                     | `activeView`     |            |
| 4  | `repeated model.Relation`             | `relations`      | deprecated |
| 12 | `repeated GroupOrder`                 | `groupOrders`    |            |
| 13 | `repeated ObjectOrder`                | `objectOrders`   |            |
| 5  | `repeated anytype.model.RelationLink` | `relationLinks`  |            |
| 6  | `repeated string`                     | `TargetObjectId` |            |
| 14 | `repeated bool`                       | `isCollection`   |            |

#### `Block.Content.Dataview.Checkbox`



| # | 类型              | 字段        | 说明 |
| - | --------------- | --------- | -- |
| 1 | `repeated bool` | `checked` |    |

#### `Block.Content.Dataview.Date`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Block.Content.Dataview.Filter`



| #  | 类型                               | 字段                 | 说明 |
| -- | -------------------------------- | ------------------ | -- |
| 9  | `repeated string`                | `id`               |    |
| 1  | `repeated Operator`              | `operator`         |    |
| 2  | `repeated string`                | `RelationKey`      |    |
| 5  | `repeated string`                | `relationProperty` |    |
| 3  | `repeated Condition`             | `condition`        |    |
| 4  | `repeated google.protobuf.Value` | `value`            |    |
| 6  | `repeated QuickOption`           | `quickOption`      |    |
| 7  | `repeated RelationFormat`        | `format`           |    |
| 8  | `repeated bool`                  | `includeTime`      |    |
| 10 | `repeated Filter`                | `nestedFilters`    |    |

#### `Block.Content.Dataview.Group`



| # | 类型                | 字段   | 说明 |
| - | ----------------- | ---- | -- |
| 1 | `repeated string` | `id` |    |
| — | (oneof) Value     |      |    |

#### `Block.Content.Dataview.GroupOrder`



| # | 类型                   | 字段           | 说明 |
| - | -------------------- | ------------ | -- |
| 1 | `repeated string`    | `viewId`     |    |
| 2 | `repeated ViewGroup` | `viewGroups` |    |

#### `Block.Content.Dataview.ObjectOrder`



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated string` | `viewId`    |    |
| 2 | `repeated string` | `groupId`   |    |
| 3 | `repeated string` | `objectIds` |    |

#### `Block.Content.Dataview.Relation`



| # | 类型                     | 字段                | 说明                                 |
| - | ---------------------- | ----------------- | ---------------------------------- |
| 1 | `repeated string`      | `key`             |                                    |
| 2 | `repeated bool`        | `isVisible`       |                                    |
| 3 | `repeated int32`       | `width`           |                                    |
| 5 | `repeated bool`        | `dateIncludeTime` | bool isReadOnly = 4; // deprecated |
| 6 | `repeated TimeFormat`  | `timeFormat`      |                                    |
| 7 | `repeated DateFormat`  | `dateFormat`      |                                    |
| 8 | `repeated FormulaType` | `formula`         |                                    |
| 9 | `repeated Block.Align` | `align`           |                                    |

#### `Block.Content.Dataview.Sort`



| # | 类型                               | 字段               | 说明 |
| - | -------------------------------- | ---------------- | -- |
| 1 | `repeated string`                | `RelationKey`    |    |
| 2 | `repeated Type`                  | `type`           |    |
| 3 | `repeated google.protobuf.Value` | `customOrder`    |    |
| 4 | `repeated RelationFormat`        | `format`         |    |
| 5 | `repeated bool`                  | `includeTime`    |    |
| 6 | `repeated string`                | `id`             |    |
| 7 | `repeated EmptyType`             | `emptyPlacement` |    |
| 8 | `repeated bool`                  | `noCollate`      |    |

#### `Block.Content.Dataview.Status`



| # | 类型                | 字段   | 说明 |
| - | ----------------- | ---- | -- |
| 1 | `repeated string` | `id` |    |

#### `Block.Content.Dataview.Tag`



| # | 类型                | 字段    | 说明 |
| - | ----------------- | ----- | -- |
| 1 | `repeated string` | `ids` |    |

#### `Block.Content.Dataview.View`



| #  | 类型                  | 字段                      | 说明 |
| -- | ------------------- | ----------------------- | -- |
| 1  | `repeated string`   | `id`                    |    |
| 2  | `repeated Type`     | `type`                  |    |
| 3  | `repeated string`   | `name`                  |    |
| 4  | `repeated Sort`     | `sorts`                 |    |
| 5  | `repeated Filter`   | `filters`               |    |
| 6  | `repeated Relation` | `relations`             |    |
| 7  | `repeated string`   | `coverRelationKey`      |    |
| 8  | `repeated bool`     | `hideIcon`              |    |
| 9  | `repeated Size`     | `cardSize`              |    |
| 10 | `repeated bool`     | `coverFit`              |    |
| 11 | `repeated string`   | `groupRelationKey`      |    |
| 12 | `repeated bool`     | `groupBackgroundColors` |    |
| 13 | `repeated int32`    | `pageLimit`             |    |
| 14 | `repeated string`   | `defaultTemplateId`     |    |
| 15 | `repeated string`   | `defaultObjectTypeId`   |    |
| 16 | `repeated string`   | `endRelationKey`        |    |
| 17 | `repeated bool`     | `wrapContent`           |    |
| 18 | `repeated ListSize` | `listSize`              |    |
| 19 | `repeated bool`     | `alternateRows`         |    |

#### `Block.Content.Dataview.ViewGroup`



| # | 类型                | 字段                | 说明 |
| - | ----------------- | ----------------- | -- |
| 1 | `repeated string` | `groupId`         |    |
| 2 | `repeated int32`  | `index`           |    |
| 3 | `repeated bool`   | `hidden`          |    |
| 4 | `repeated string` | `backgroundColor` |    |

#### `Block.Content.Div`



| # | 类型               | 字段      | 说明 |
| - | ---------------- | ------- | -- |
| 1 | `repeated Style` | `style` |    |

#### `Block.Content.FeaturedRelations`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Block.Content.File`



| # | 类型                | 字段               | 说明 |
| - | ----------------- | ---------------- | -- |
| 1 | `repeated string` | `hash`           |    |
| 2 | `repeated string` | `name`           |    |
| 3 | `repeated Type`   | `type`           |    |
| 4 | `repeated string` | `mime`           |    |
| 5 | `repeated int64`  | `size`           |    |
| 6 | `repeated int64`  | `addedAt`        |    |
| 9 | `repeated string` | `targetObjectId` |    |
| 7 | `repeated State`  | `state`          |    |
| 8 | `repeated Style`  | `style`          |    |

#### `Block.Content.Icon`



| # | 类型                | 字段     | 说明 |
| - | ----------------- | ------ | -- |
| 1 | `repeated string` | `name` |    |

#### `Block.Content.Latex`



| # | 类型                   | 字段          | 说明 |
| - | -------------------- | ----------- | -- |
| 1 | `repeated string`    | `text`      |    |
| 2 | `repeated Processor` | `processor` |    |

#### `Block.Content.Layout`



| # | 类型               | 字段      | 说明 |
| - | ---------------- | ------- | -- |
| 1 | `repeated Style` | `style` |    |

#### `Block.Content.Link`



| # | 类型                                | 字段              | 说明 |
| - | --------------------------------- | --------------- | -- |
| 1 | `repeated string`                 | `targetBlockId` |    |
| 2 | `repeated Style`                  | `style`         |    |
| 3 | `repeated google.protobuf.Struct` | `fields`        |    |
| 4 | `repeated IconSize`               | `iconSize`      |    |
| 5 | `repeated CardStyle`              | `cardStyle`     |    |
| 6 | `repeated Description`            | `description`   |    |
| 7 | `repeated string`                 | `relations`     |    |

#### `Block.Content.Relation`



| # | 类型                | 字段    | 说明 |
| - | ----------------- | ----- | -- |
| 1 | `repeated string` | `key` |    |

#### `Block.Content.Smartblock`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Block.Content.Table`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Block.Content.TableColumn`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Block.Content.TableOfContents`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Block.Content.TableRow`



| # | 类型              | 字段         | 说明 |
| - | --------------- | ---------- | -- |
| 1 | `repeated bool` | `isHeader` |    |

#### `Block.Content.Text`



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated string` | `text`      |    |
| 2 | `repeated Style`  | `style`     |    |
| 3 | `repeated Marks`  | `marks`     |    |
| 4 | `repeated bool`   | `checked`   |    |
| 5 | `repeated string` | `color`     |    |
| 6 | `repeated string` | `iconEmoji` |    |
| 7 | `repeated string` | `iconImage` |    |

#### `Block.Content.Text.Mark`



| # | 类型                | 字段      | 说明 |
| - | ----------------- | ------- | -- |
| 1 | `repeated Range`  | `range` |    |
| 2 | `repeated Type`   | `type`  |    |
| 3 | `repeated string` | `param` |    |

#### `Block.Content.Text.Marks`



| # | 类型              | 字段      | 说明 |
| - | --------------- | ------- | -- |
| 1 | `repeated Mark` | `marks` |    |

#### `Block.Content.Widget`



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated Layout` | `layout`    |    |
| 2 | `repeated int32`  | `limit`     |    |
| 3 | `repeated string` | `viewId`    |    |
| 4 | `repeated bool`   | `autoAdded` |    |

#### `Block.Restrictions`



| # | 类型              | 字段       | 说明 |
| - | --------------- | -------- | -- |
| 1 | `repeated bool` | `read`   |    |
| 2 | `repeated bool` | `edit`   |    |
| 3 | `repeated bool` | `remove` |    |
| 4 | `repeated bool` | `drag`   |    |
| 5 | `repeated bool` | `dropOn` |    |

#### `BlockMetaOnly`



| # | 类型                                | 字段       | 说明 |
| - | --------------------------------- | -------- | -- |
| 1 | `repeated string`                 | `id`     |    |
| 2 | `repeated google.protobuf.Struct` | `fields` |    |

#### `ChatMessage`



| #  | 类型                        | 字段                 | 说明                                                                                                                                                                                                                                                                                                                                     |
| -- | ------------------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | `repeated string`         | `id`               |                                                                                                                                                                                                                                                                                                                                        |
| 2  | `repeated string`         | `orderId`          |                                                                                                                                                                                                                                                                                                                                        |
| 3  | `repeated string`         | `creator`          |                                                                                                                                                                                                                                                                                                                                        |
| 4  | `repeated int64`          | `createdAt`        |                                                                                                                                                                                                                                                                                                                                        |
| 9  | `repeated int64`          | `modifiedAt`       |                                                                                                                                                                                                                                                                                                                                        |
| 11 | `repeated string`         | `stateId`          | stateId is ever-increasing id (BSON ObjectId) for this message. Unlike orderId, this ID is ordered by the time messages are added. For example, it's useful to prevent accidental reading of messages from the past when a ChatReadMessages request is sent: a message from the past may appear, but the client is still unaware of it |
| 5  | `repeated string`         | `replyToMessageId` |                                                                                                                                                                                                                                                                                                                                        |
| 6  | `repeated MessageContent` | `message`          |                                                                                                                                                                                                                                                                                                                                        |
| 7  | `repeated Attachment`     | `attachments`      |                                                                                                                                                                                                                                                                                                                                        |
| 8  | `repeated Reactions`      | `reactions`        |                                                                                                                                                                                                                                                                                                                                        |
| 10 | `repeated bool`           | `read`             |                                                                                                                                                                                                                                                                                                                                        |
| 12 | `repeated bool`           | `mentionRead`      |                                                                                                                                                                                                                                                                                                                                        |
| 14 | `repeated bool`           | `hasMention`       |                                                                                                                                                                                                                                                                                                                                        |
| 13 | `repeated bool`           | `synced`           |                                                                                                                                                                                                                                                                                                                                        |
| 15 | `repeated bool`           | `pinned`           |                                                                                                                                                                                                                                                                                                                                        |
| 16 | `repeated bool`           | `unreadReaction`   |                                                                                                                                                                                                                                                                                                                                        |
| 17 | `repeated MessageBlock`   | `blocks`           |                                                                                                                                                                                                                                                                                                                                        |

#### `ChatMessage.Attachment`



| # | 类型                        | 字段       | 说明 |
| - | ------------------------- | -------- | -- |
| 1 | `repeated string`         | `target` |    |
| 2 | `repeated AttachmentType` | `type`   |    |

#### `ChatMessage.MessageBlock`



| # | 类型              | 字段 | 说明 |
| - | --------------- | -- | -- |
| — | (oneof) content |    |    |

#### `ChatMessage.MessageBlockEditorQuote`



| # | 类型                          | 字段        | 说明 |
| - | --------------------------- | --------- | -- |
| 1 | `repeated string`           | `blockId` |    |
| 2 | `repeated MessageBlockText` | `content` |    |

#### `ChatMessage.MessageBlockEmbed`



| # | 类型                                       | 字段          | 说明 |
| - | ---------------------------------------- | ----------- | -- |
| 1 | `repeated string`                        | `text`      |    |
| 2 | `repeated Block.Content.Latex.Processor` | `processor` |    |

#### `ChatMessage.MessageBlockLink`



| # | 类型                  | 字段               | 说明 |
| - | ------------------- | ---------------- | -- |
| 1 | `repeated string`   | `targetObjectId` |    |
| 2 | `repeated LinkType` | `type`           |    |

#### `ChatMessage.MessageBlockMessageQuote`



| # | 类型                          | 字段              | 说明 |
| - | --------------------------- | --------------- | -- |
| 1 | `repeated string`           | `messageId`     |    |
| 2 | `repeated string`           | `participantId` |    |
| 3 | `repeated MessageBlockText` | `content`       |    |

#### `ChatMessage.MessageBlockText`



| # | 类型                                  | 字段        | 说明 |
| - | ----------------------------------- | --------- | -- |
| 1 | `repeated string`                   | `text`    |    |
| 2 | `repeated Block.Content.Text.Style` | `style`   |    |
| 3 | `repeated Block.Content.Text.Mark`  | `marks`   |    |
| 4 | `repeated bool`                     | `checked` |    |
| 5 | `repeated string`                   | `lang`    |    |

#### `ChatMessage.MessageContent`



| # | 类型                                  | 字段      | 说明 |
| - | ----------------------------------- | ------- | -- |
| 1 | `repeated string`                   | `text`  |    |
| 2 | `repeated Block.Content.Text.Style` | `style` |    |
| 3 | `repeated Block.Content.Text.Mark`  | `marks` |    |

#### `ChatMessage.Reactions`



| # | 类型                                   | 字段          | 说明 |
| - | ------------------------------------ | ----------- | -- |
| 1 | `repeated map<string, IdentityList>` | `reactions` |    |

#### `ChatMessage.Reactions.IdentityList`



| # | 类型                | 字段    | 说明 |
| - | ----------------- | ----- | -- |
| 1 | `repeated string` | `ids` |    |

#### `ChatState`



| # | 类型                     | 字段                      | 说明 |
| - | ---------------------- | ----------------------- | -- |
| 1 | `repeated UnreadState` | `messages`              |    |
| 2 | `repeated UnreadState` | `mentions`              |    |
| 3 | `repeated string`      | `lastStateId`           |    |
| 4 | `repeated int64`       | `order`                 |    |
| 5 | `repeated string`      | `unreadReactionOrderId` |    |

#### `ChatState.UnreadState`



| # | 类型                | 字段              | 说明 |
| - | ----------------- | --------------- | -- |
| 1 | `repeated string` | `oldestOrderId` |    |
| 2 | `repeated int32`  | `counter`       |    |

#### `Detail`



| # | 类型                               | 字段      | 说明 |
| - | -------------------------------- | ------- | -- |
| 1 | `repeated string`                | `key`   |    |
| 2 | `repeated google.protobuf.Value` | `value` |    |

#### `DeviceInfo`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `id`          |    |
| 2 | `repeated string` | `name`        |    |
| 3 | `repeated int64`  | `addDate`     |    |
| 4 | `repeated bool`   | `archived`    |    |
| 5 | `repeated bool`   | `isConnected` |    |

#### `Export`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `FileEncryptionKey`



| # | 类型                | 字段     | 说明 |
| - | ----------------- | ------ | -- |
| 1 | `repeated string` | `path` |    |
| 2 | `repeated string` | `key`  |    |

#### `FileInfo`



| # | 类型                           | 字段               | 说明 |
| - | ---------------------------- | ---------------- | -- |
| 1 | `repeated string`            | `fileId`         |    |
| 2 | `repeated FileEncryptionKey` | `encryptionKeys` |    |

#### `IdentityProfile`



| # | 类型                           | 字段                   | 说明 |
| - | ---------------------------- | -------------------- | -- |
| 1 | `repeated string`            | `identity`           |    |
| 2 | `repeated string`            | `name`               |    |
| 3 | `repeated string`            | `iconCid`            |    |
| 4 | `repeated FileEncryptionKey` | `iconEncryptionKeys` |    |
| 5 | `repeated string`            | `description`        |    |
| 6 | `repeated string`            | `globalName`         |    |

#### `IdentityProfileWithKey`



| # | 类型                         | 字段                | 说明 |
| - | -------------------------- | ----------------- | -- |
| 1 | `repeated IdentityProfile` | `identityProfile` |    |
| 2 | `repeated bytes`           | `requestMetadata` |    |

#### `Import`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `InternalFlag`



| # | 类型               | 字段      | 说明 |
| - | ---------------- | ------- | -- |
| 1 | `repeated Value` | `value` |    |

#### `Invite`



| # | 类型               | 字段          | 说明 |
| - | ---------------- | ----------- | -- |
| 1 | `repeated bytes` | `payload`   |    |
| 2 | `repeated bytes` | `signature` |    |

#### `InvitePayload`



| #  | 类型                           | 字段                          | 说明 |
| -- | ---------------------------- | --------------------------- | -- |
| 1  | `repeated string`            | `creatorIdentity`           |    |
| 2  | `repeated string`            | `creatorName`               |    |
| 12 | `repeated string`            | `creatorIconCid`            |    |
| 13 | `repeated FileEncryptionKey` | `creatorIconEncryptionKeys` |    |
| 3  | `repeated bytes`             | `aclKey`                    |    |
| 4  | `repeated string`            | `spaceId`                   |    |
| 5  | `repeated string`            | `spaceName`                 |    |
| 6  | `repeated string`            | `spaceIconCid`              |    |
| 10 | `repeated uint32`            | `spaceIconOption`           |    |
| 11 | `repeated uint32`            | `spaceUxType`               |    |
| 14 | `repeated uint32`            | `spaceType`                 |    |
| 7  | `repeated FileEncryptionKey` | `spaceIconEncryptionKeys`   |    |
| 8  | `repeated InviteType`        | `inviteType`                |    |
| 9  | `repeated bytes`             | `guestKey`                  |    |

#### `Layout`



| # | 类型                           | 字段                  | 说明 |
| - | ---------------------------- | ------------------- | -- |
| 1 | `repeated ObjectType.Layout` | `id`                |    |
| 2 | `repeated string`            | `name`              |    |
| 3 | `repeated Relation`          | `requiredRelations` |    |

#### `LinkPreview`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `url`         |    |
| 2 | `repeated string` | `title`       |    |
| 3 | `repeated string` | `description` |    |
| 4 | `repeated string` | `imageUrl`    |    |
| 5 | `repeated string` | `faviconUrl`  |    |
| 6 | `repeated Type`   | `type`        |    |

#### `ManifestInfo`



| #  | 类型                | 字段             | 说明 |
| -- | ----------------- | -------------- | -- |
| 2  | `repeated string` | `id`           |    |
| 3  | `repeated string` | `name`         |    |
| 4  | `repeated string` | `author`       |    |
| 5  | `repeated string` | `license`      |    |
| 6  | `repeated string` | `title`        |    |
| 7  | `repeated string` | `description`  |    |
| 8  | `repeated string` | `screenshots`  |    |
| 9  | `repeated string` | `downloadLink` |    |
| 10 | `repeated int32`  | `fileSize`     |    |
| 11 | `repeated string` | `categories`   |    |
| 12 | `repeated string` | `language`     |    |

#### `Membership`



| #  | 类型                                           | 字段                      | 说明                                                                                 |
| -- | -------------------------------------------- | ----------------------- | ---------------------------------------------------------------------------------- |
| 1  | `repeated uint32`                            | `tier`                  | it was Tier before, changed to int32 to allow dynamic values                       |
| 2  | `repeated Status`                            | `status`                |                                                                                    |
| 3  | `repeated uint64`                            | `dateStarted`           |                                                                                    |
| 4  | `repeated uint64`                            | `dateEnds`              |                                                                                    |
| 5  | `repeated bool`                              | `isAutoRenew`           |                                                                                    |
| 6  | `repeated PaymentMethod`                     | `paymentMethod`         |                                                                                    |
| 7  | `repeated string`                            | `nsName`                | can be empty if user did not ask for any name                                      |
| 8  | `repeated anytype.model.NameserviceNameType` | `nsNameType`            |                                                                                    |
| 9  | `repeated string`                            | `userEmail`             | if the email was verified by the user or set during the checkout - it will be here |
| 10 | `repeated bool`                              | `subscribeToNewsletter` |                                                                                    |

#### `MembershipTierData`



| #  | 类型                    | 字段                      | 说明                                                                                                                 |
| -- | --------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1  | `repeated uint32`     | `id`                    | this is a unique Payment Node ID of the tier WARNING: tiers can be sorted differently, not according to their IDs! |
| 2  | `repeated string`     | `name`                  | localazied name of the tier                                                                                        |
| 3  | `repeated string`     | `description`           | just a short technical description                                                                                 |
| 4  | `repeated bool`       | `isTest`                | is this tier for testing and debugging only?                                                                       |
| 5  | `repeated PeriodType` | `periodType`            | how long is the period of the subscription                                                                         |
| 6  | `repeated uint32`     | `periodValue`           | i.e. "5 days" or "3 years"                                                                                         |
| 7  | `repeated uint32`     | `priceStripeUsdCents`   | this one is a price we use ONLY on Stripe platform                                                                 |
| 8  | `repeated uint32`     | `anyNamesCountIncluded` | number of ANY NS names that this tier includes also in the "features" list (see below)                             |
| 9  | `repeated uint32`     | `anyNameMinLength`      | somename.any - is of len 8                                                                                         |
| 10 | `repeated string`     | `features`              | localized strings for the features                                                                                 |
| 11 | `repeated string`     | `colorStr`              | green, blue, red, purple, custom                                                                                   |
| 12 | `repeated string`     | `stripeProductId`       | Stripe platform-specific data:                                                                                     |
| 13 | `repeated string`     | `stripeManageUrl`       |                                                                                                                    |
| 15 | `repeated string`     | `iosProductId`          | iOS platform-specific data:                                                                                        |
| 16 | `repeated string`     | `iosManageUrl`          |                                                                                                                    |
| 17 | `repeated string`     | `androidProductId`      | Android platform-specific data:                                                                                    |
| 18 | `repeated string`     | `androidManageUrl`      |                                                                                                                    |
| 19 | `repeated string`     | `offer`                 | "limited offer" or somehing like that                                                                              |

#### `MembershipV2`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `MembershipV2.Amount`



| # | 类型                | 字段            | 说明                                                                                                    |
| - | ----------------- | ------------- | ----------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `currency`    | ISO 4217 currency code                                                                                |
| 2 | `repeated int64`  | `amountCents` | $0.01 = 1 $1.00 = 100 also supports negative amounts! some invoices can have negatice amount (refund) |

#### `MembershipV2.Cart`



| # | 类型                     | 字段                  | 说明                                                                                                                         |
| - | ---------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated CartProduct` | `products`          | if you add Nx the same product - it will be Nx in the 'products' array, i.e: each product instance has a unique index      |
| 2 | `repeated Amount`      | `total`             | total amount of the cart (including discounts, etc)                                                                        |
| 3 | `repeated Amount`      | `totalNextInvoice`  | in case you are paying in the middle of the period (for existing customers) the next invoice amount will also be generated |
| 4 | `repeated uint64`      | `nextInvoiceDate`   |                                                                                                                            |
| 5 | `repeated string`      | `appliedPromocodes` |                                                                                                                            |

#### `MembershipV2.CartProduct`



| # | 类型                 | 字段           | 说明                                                                                                                                                                                  |
| - | ------------------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated Product` | `product`    |                                                                                                                                                                                     |
| 2 | `repeated bool`    | `isYearly`   | otherwise - monthly or isLifetime                                                                                                                                                   |
| 3 | `repeated bool`    | `remove`     | set to true if you want to remove this item from the customer it's like setting -1 to some product                                                                                  |
| 4 | `repeated bool`    | `isLifetime` | if true - then this is lifetime product (no matter what isYearly above is) unfortunately we do not use Period here to keep compatibility with old versions that still use isYearly! |

#### `MembershipV2.CryptoCheckout`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `invoiceURL`  |    |
| 2 | `repeated Amount` | `total`       |    |
| 3 | `repeated bool`   | `isCanCancel` |    |

#### `MembershipV2.Data`



| # | 类型                          | 字段                  | 说明 |
| - | --------------------------- | ------------------- | -- |
| 1 | `repeated PurchasedProduct` | `products`          |    |
| 2 | `repeated Invoice`          | `nextInvoice`       |    |
| 3 | `repeated string`           | `teamOwnerID`       |    |
| 4 | `repeated PaymentProvider`  | `paymentProvider`   |    |
| 5 | `repeated string`           | `appliedPromocodes` |    |

#### `MembershipV2.Features`



| # | 类型                | 字段              | 说明 |
| - | ----------------- | --------------- | -- |
| 1 | `repeated uint64` | `storageBytes`  |    |
| 2 | `repeated uint32` | `spaceReaders`  |    |
| 3 | `repeated uint32` | `spaceWriters`  |    |
| 4 | `repeated uint32` | `sharedSpaces`  |    |
| 5 | `repeated uint32` | `teamSeats`     |    |
| 6 | `repeated uint32` | `anyNameCount`  |    |
| 7 | `repeated uint32` | `anyNameMinLen` |    |
| 8 | `repeated uint32` | `privateSpaces` |    |

#### `MembershipV2.Invoice`



| # | 类型                | 字段      | 说明 |
| - | ----------------- | ------- | -- |
| 1 | `repeated uint64` | `date`  |    |
| 2 | `repeated Amount` | `total` |    |

#### `MembershipV2.Product`



| #  | 类型                  | 字段               | 说明                                                                                                                                                                                                                                                                                                                                                                                             |
| -- | ------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | `repeated string`   | `id`             |                                                                                                                                                                                                                                                                                                                                                                                                |
| 2  | `repeated string`   | `name`           |                                                                                                                                                                                                                                                                                                                                                                                                |
| 3  | `repeated string`   | `description`    |                                                                                                                                                                                                                                                                                                                                                                                                |
| 4  | `repeated bool`     | `isTopLevel`     |                                                                                                                                                                                                                                                                                                                                                                                                |
| 5  | `repeated bool`     | `isHidden`       |                                                                                                                                                                                                                                                                                                                                                                                                |
| 6  | `repeated bool`     | `isIntro`        | isIntro flag can be used as follows:  1. if current user's top level product has isIntro flag -> then you'd rather show a FULL list of all products to enable upgrading from CURRENT product 2. but if current user's top level product has no isIntro flag -> then it means that this plan was aquired and user need to control it. then show "second screen" to control that product instead |
| 7  | `repeated bool`     | `isUpgradeable`  | isUpgradeable can be used as follows:  if current user's top level product has isUpgradeable flag -> show incentives to buy something else                                                                                                                                                                                                                                                     |
| 8  | `repeated Amount`   | `pricesYearly`   |                                                                                                                                                                                                                                                                                                                                                                                                |
| 9  | `repeated Amount`   | `pricesMonthly`  |                                                                                                                                                                                                                                                                                                                                                                                                |
| 10 | `repeated string`   | `colorStr`       | green, blue, red, purple, custom, etc                                                                                                                                                                                                                                                                                                                                                          |
| 11 | `repeated string`   | `offer`          |                                                                                                                                                                                                                                                                                                                                                                                                |
| 12 | `repeated Features` | `features`       |                                                                                                                                                                                                                                                                                                                                                                                                |
| 13 | `repeated Amount`   | `pricesLifetime` |                                                                                                                                                                                                                                                                                                                                                                                                |

#### `MembershipV2.ProductStatus`



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated Status` | `status` |    |

#### `MembershipV2.PurchaseInfo`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated uint64` | `dateStarted` |    |
| 2 | `repeated uint64` | `dateEnds`    |    |
| 3 | `repeated bool`   | `isAutoRenew` |    |
| 4 | `repeated Period` | `period`      |    |

#### `MembershipV2.PurchasedProduct`



| # | 类型                       | 字段              | 说明 |
| - | ------------------------ | --------------- | -- |
| 1 | `repeated Product`       | `product`       |    |
| 2 | `repeated PurchaseInfo`  | `purchaseInfo`  |    |
| 3 | `repeated ProductStatus` | `productStatus` |    |

#### `Metadata`



| # | 类型              | 字段 | 说明 |
| - | --------------- | -- | -- |
| — | (oneof) payload |    |    |

#### `Metadata.Payload`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Metadata.Payload.IdentityPayload`



| # | 类型               | 字段              | 说明 |
| - | ---------------- | --------------- | -- |
| 1 | `repeated bytes` | `profileSymKey` |    |

#### `Notification`



| #  | 类型                | 字段           | 说明 |
| -- | ----------------- | ------------ | -- |
| 1  | `repeated string` | `id`         |    |
| 2  | `repeated int64`  | `createTime` |    |
| 4  | `repeated Status` | `status`     |    |
| 5  | `repeated bool`   | `isLocal`    |    |
| —  | (oneof) payload   |              |    |
| 7  | `repeated string` | `space`      |    |
| 14 | `repeated string` | `aclHeadId`  |    |

#### `Notification.Export`



| # | 类型                             | 字段           | 说明 |
| - | ------------------------------ | ------------ | -- |
| 2 | `repeated Code`                | `errorCode`  |    |
| 3 | `repeated model.Export.Format` | `exportType` |    |

#### `Notification.GalleryImport`



| # | 类型                                | 字段          | 说明 |
| - | --------------------------------- | ----------- | -- |
| 1 | `repeated string`                 | `processId` |    |
| 2 | `repeated model.Import.ErrorCode` | `errorCode` |    |
| 3 | `repeated string`                 | `spaceId`   |    |
| 4 | `repeated string`                 | `name`      |    |
| 5 | `repeated string`                 | `spaceName` |    |

#### `Notification.Import`



| # | 类型                                | 字段           | 说明 |
| - | --------------------------------- | ------------ | -- |
| 1 | `repeated string`                 | `processId`  |    |
| 2 | `repeated model.Import.ErrorCode` | `errorCode`  |    |
| 3 | `repeated model.Import.Type`      | `importType` |    |
| 4 | `repeated string`                 | `spaceId`    |    |
| 5 | `repeated string`                 | `name`       |    |
| 6 | `repeated string`                 | `spaceName`  |    |

#### `Notification.ParticipantPermissionsChange`



| # | 类型                                | 字段            | 说明 |
| - | --------------------------------- | ------------- | -- |
| 1 | `repeated string`                 | `spaceId`     |    |
| 2 | `repeated ParticipantPermissions` | `permissions` |    |
| 3 | `repeated string`                 | `spaceName`   |    |

#### `Notification.ParticipantRemove`



| # | 类型                | 字段             | 说明 |
| - | ----------------- | -------------- | -- |
| 1 | `repeated string` | `identity`     |    |
| 2 | `repeated string` | `identityName` |    |
| 3 | `repeated string` | `identityIcon` |    |
| 4 | `repeated string` | `spaceId`      |    |
| 5 | `repeated string` | `spaceName`    |    |

#### `Notification.ParticipantRequestApproved`



| # | 类型                                | 字段            | 说明 |
| - | --------------------------------- | ------------- | -- |
| 1 | `repeated string`                 | `spaceId`     |    |
| 2 | `repeated ParticipantPermissions` | `permissions` |    |
| 5 | `repeated string`                 | `spaceName`   |    |

#### `Notification.ParticipantRequestDecline`



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated string` | `spaceId`   |    |
| 3 | `repeated string` | `spaceName` |    |

#### `Notification.RequestToJoin`



| # | 类型                | 字段             | 说明 |
| - | ----------------- | -------------- | -- |
| 1 | `repeated string` | `spaceId`      |    |
| 2 | `repeated string` | `identity`     |    |
| 3 | `repeated string` | `identityName` |    |
| 4 | `repeated string` | `identityIcon` |    |
| 5 | `repeated string` | `spaceName`    |    |

#### `Notification.RequestToLeave`



| # | 类型                | 字段             | 说明 |
| - | ----------------- | -------------- | -- |
| 1 | `repeated string` | `spaceId`      |    |
| 2 | `repeated string` | `identity`     |    |
| 3 | `repeated string` | `identityName` |    |
| 4 | `repeated string` | `identityIcon` |    |
| 5 | `repeated string` | `spaceName`    |    |

#### `Notification.Test`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Object`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Object.ChangePayload`



| # | 类型                        | 字段               | 说明 |
| - | ------------------------- | ---------------- | -- |
| 1 | `repeated SmartBlockType` | `smartBlockType` |    |
| 2 | `repeated string`         | `key`            |    |
| 3 | `repeated bytes`          | `data`           |    |

#### `ObjectType`



| #  | 类型                        | 字段                       | 说明 |
| -- | ------------------------- | ------------------------ | -- |
| 1  | `repeated string`         | `url`                    |    |
| 2  | `repeated string`         | `name`                   |    |
| 3  | `repeated RelationLink`   | `relationLinks`          |    |
| 4  | `repeated Layout`         | `layout`                 |    |
| 5  | `repeated string`         | `iconEmoji`              |    |
| 6  | `repeated string`         | `description`            |    |
| 7  | `repeated bool`           | `hidden`                 |    |
| 10 | `repeated bool`           | `readonly`               |    |
| 8  | `repeated SmartBlockType` | `types`                  |    |
| 9  | `repeated bool`           | `isArchived`             |    |
| 11 | `repeated bool`           | `installedByDefault`     |    |
| 12 | `repeated string`         | `key`                    |    |
| 13 | `repeated int64`          | `revision`               |    |
| 14 | `repeated bool`           | `restrictObjectCreation` |    |
| 15 | `repeated int64`          | `iconColor`              |    |
| 16 | `repeated string`         | `iconName`               |    |
| 17 | `repeated string`         | `pluralName`             |    |

#### `ObjectView`



| #  | 类型                          | 字段                  | 说明 |
| -- | --------------------------- | ------------------- | -- |
| 1  | `repeated string`           | `rootId`            |    |
| 2  | `repeated Block`            | `blocks`            |    |
| 3  | `repeated DetailsSet`       | `details`           |    |
| 4  | `repeated SmartBlockType`   | `type`              |    |
| 7  | `repeated Relation`         | `relations`         |    |
| 10 | `repeated RelationLink`     | `relationLinks`     |    |
| 8  | `repeated Restrictions`     | `restrictions`      |    |
| 9  | `repeated HistorySize`      | `history`           |    |
| 11 | `repeated BlockParticipant` | `blockParticipants` |    |

#### `ObjectView.BlockParticipant`



| # | 类型                | 字段              | 说明 |
| - | ----------------- | --------------- | -- |
| 1 | `repeated string` | `blockId`       |    |
| 2 | `repeated string` | `participantId` |    |

#### `ObjectView.DetailsSet`



| # | 类型                                | 字段        | 说明 |
| - | --------------------------------- | --------- | -- |
| 1 | `repeated string`                 | `id`      |    |
| 2 | `repeated google.protobuf.Struct` | `details` |    |
| 3 | `repeated string`                 | `subIds`  |    |

#### `ObjectView.HistorySize`



| # | 类型               | 字段     | 说明 |
| - | ---------------- | ------ | -- |
| 1 | `repeated int32` | `undo` |    |
| 2 | `repeated int32` | `redo` |    |

#### `ObjectView.RelationWithValuePerObject`



| # | 类型                           | 字段          | 说明 |
| - | ---------------------------- | ----------- | -- |
| 1 | `repeated string`            | `objectId`  |    |
| 2 | `repeated RelationWithValue` | `relations` |    |

#### `ParticipantPermissionChange`



| # | 类型                                | 字段         | 说明 |
| - | --------------------------------- | ---------- | -- |
| 1 | `repeated string`                 | `identity` |    |
| 2 | `repeated ParticipantPermissions` | `perms`    |    |

#### `Placeholder`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `relationKey` |    |
| 2 | `repeated Value`  | `values`      |    |

#### `Placeholder.Value`



| # | 类型                               | 字段      | 说明 |
| - | -------------------------------- | ------- | -- |
| 1 | `repeated Type`                  | `type`  |    |
| 2 | `repeated google.protobuf.Value` | `value` |    |

#### `Range`



| # | 类型               | 字段     | 说明 |
| - | ---------------- | ------ | -- |
| 1 | `repeated int32` | `from` |    |
| 2 | `repeated int32` | `to`   |    |

#### `Relation`

> Relation describe the human-interpreted relation type. It may be something like "Date of creation, format=date" or "Assignee, format=objectId, objectType=person"



| #   | 类型                               | 字段                 | 说明                                                                                                                                                                                        |
| --- | -------------------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 100 | `repeated string`                | `id`               |                                                                                                                                                                                           |
| 1   | `repeated string`                | `key`              | Key under which the value is stored in the map. Must be unique for the object type. It usually auto-generated bsonid, but also may be something human-readable in case of prebuilt types. |
| 2   | `repeated RelationFormat`        | `format`           |                                                                                                                                                                                           |
| 3   | `repeated string`                | `name`             |                                                                                                                                                                                           |
| 4   | `repeated google.protobuf.Value` | `defaultValue`     |                                                                                                                                                                                           |
| 5   | `repeated DataSource`            | `dataSource`       |                                                                                                                                                                                           |
| 6   | `repeated bool`                  | `hidden`           |                                                                                                                                                                                           |
| 7   | `repeated bool`                  | `readOnly`         |                                                                                                                                                                                           |
| 15  | `repeated bool`                  | `readOnlyRelation` |                                                                                                                                                                                           |
| 8   | `repeated bool`                  | `multi`            |                                                                                                                                                                                           |
| 9   | `repeated string`                | `objectTypes`      |                                                                                                                                                                                           |
| 12  | `repeated Option`                | `selectDict`       | index 10, 11 was used in internal-only builds. Can be reused, but may break some test accounts                                                                                            |
| 13  | `repeated int32`                 | `maxCount`         |                                                                                                                                                                                           |
| 14  | `repeated string`                | `description`      |                                                                                                                                                                                           |
| 20  | `repeated Scope`                 | `scope`            | on-store fields, injected only locally                                                                                                                                                    |
| 21  | `repeated string`                | `creator`          |                                                                                                                                                                                           |
| 22  | `repeated int64`                 | `revision`         |                                                                                                                                                                                           |
| 23  | `repeated bool`                  | `includeTime`      |                                                                                                                                                                                           |

#### `Relation.Option`



| # | 类型                | 字段            | 说明                                    |
| - | ----------------- | ------------- | ------------------------------------- |
| 1 | `repeated string` | `id`          |                                       |
| 2 | `repeated string` | `text`        |                                       |
| 3 | `repeated string` | `color`       |                                       |
| 5 | `repeated string` | `relationKey` | 4 is reserved for old relation format |
| 6 | `repeated string` | `orderId`     |                                       |

#### `RelationLink`



| # | 类型                        | 字段       | 说明 |
| - | ------------------------- | -------- | -- |
| 1 | `repeated string`         | `key`    |    |
| 2 | `repeated RelationFormat` | `format` |    |

#### `RelationOptions`



| # | 类型                         | 字段        | 说明 |
| - | -------------------------- | --------- | -- |
| 1 | `repeated Relation.Option` | `options` |    |

#### `RelationWithValue`



| # | 类型                               | 字段         | 说明 |
| - | -------------------------------- | ---------- | -- |
| 1 | `repeated Relation`              | `relation` |    |
| 2 | `repeated google.protobuf.Value` | `value`    |    |

#### `Relations`



| # | 类型                  | 字段          | 说明 |
| - | ------------------- | ----------- | -- |
| 1 | `repeated Relation` | `relations` |    |

#### `Restrictions`



| # | 类型                              | 字段         | 说明 |
| - | ------------------------------- | ---------- | -- |
| 1 | `repeated ObjectRestriction`    | `object`   |    |
| 2 | `repeated DataviewRestrictions` | `dataview` |    |

#### `Restrictions.DataviewRestrictions`



| # | 类型                             | 字段             | 说明 |
| - | ------------------------------ | -------------- | -- |
| 1 | `repeated string`              | `blockId`      |    |
| 2 | `repeated DataviewRestriction` | `restrictions` |    |

#### `Search`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Search.Message`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `Search.Message.Result`



| # | 类型                     | 字段                | 说明 |
| - | ---------------------- | ----------------- | -- |
| 1 | `repeated string`      | `chatId`          |    |
| 2 | `repeated string`      | `messageId`       |    |
| 3 | `repeated int64`       | `score`           |    |
| 4 | `repeated string`      | `highlight`       |    |
| 5 | `repeated Range`       | `highlightRanges` |    |
| 6 | `repeated ChatMessage` | `message`         |    |
| 7 | `repeated string`      | `spaceId`         |    |

#### `Search.Message.Sort`



| # | 类型              | 字段     | 说明 |
| - | --------------- | ------ | -- |
| 1 | `repeated Key`  | `key`  |    |
| 2 | `repeated Type` | `type` |    |

#### `Search.Meta`



| # | 类型                                | 字段                | 说明 |
| - | --------------------------------- | ----------------- | -- |
| 1 | `repeated string`                 | `highlight`       |    |
| 2 | `repeated Range`                  | `highlightRanges` |    |
| 3 | `repeated string`                 | `blockId`         |    |
| 4 | `repeated string`                 | `relationKey`     |    |
| 5 | `repeated google.protobuf.Struct` | `relationDetails` |    |

#### `Search.Result`



| # | 类型                                | 字段         | 说明 |
| - | --------------------------------- | ---------- | -- |
| 1 | `repeated string`                 | `objectId` |    |
| 2 | `repeated google.protobuf.Struct` | `details`  |    |
| 3 | `repeated Meta`                   | `meta`     |    |

#### `SmartBlockSnapshotBase`



| #  | 类型                                | 字段                         | 说明 |
| -- | --------------------------------- | -------------------------- | -- |
| 1  | `repeated Block`                  | `blocks`                   |    |
| 2  | `repeated google.protobuf.Struct` | `details`                  |    |
| 5  | `repeated string`                 | `objectTypes`              |    |
| 6  | `repeated google.protobuf.Struct` | `collections`              |    |
| 8  | `repeated string`                 | `removedCollectionKeys`    |    |
| 7  | `repeated RelationLink`           | `relationLinks`            |    |
| 9  | `repeated string`                 | `key`                      |    |
| 10 | `repeated int64`                  | `originalCreatedTimestamp` |    |
| 11 | `repeated FileInfo`               | `fileInfo`                 |    |

#### `SpaceObjectHeader`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceID` |    |

### any-block/format/v1/proto/snapshot.proto

#### `Profile`



| # | 类型                     | 字段                 | 说明 |
| - | ---------------------- | ------------------ | -- |
| 1 | `repeated string`      | `name`             |    |
| 2 | `repeated string`      | `avatar`           |    |
| 4 | `repeated string`      | `address`          |    |
| 5 | `repeated string`      | `spaceDashboardId` |    |
| 6 | `repeated string`      | `profileId`        |    |
| 7 | `repeated string`      | `analyticsId`      |    |
| 8 | `repeated string`      | `startingPage`     |    |
| 9 | `repeated WidgetBlock` | `widgets`          |    |

#### `SnapshotWithType`



| # | 类型                                      | 字段         | 说明 |
| - | --------------------------------------- | ---------- | -- |
| 1 | `repeated anytype.model.SmartBlockType` | `sbType`   |    |
| 2 | `repeated anytype.Change.Snapshot`      | `snapshot` |    |

#### `WidgetBlock`



| # | 类型                                           | 字段               | 说明 |
| - | -------------------------------------------- | ---------------- | -- |
| 1 | `repeated model.Block.Content.Widget.Layout` | `layout`         |    |
| 2 | `repeated string`                            | `targetObjectId` |    |
| 3 | `repeated int32`                             | `objectLimit`    |    |

### any-sync-filenode/index/indexproto/protos/index.proto

#### `CidEntry`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated uint64` | `size`       |    |
| 2 | `repeated int64`  | `createTime` |    |
| 3 | `repeated int64`  | `updateTime` |    |
| 4 | `repeated int32`  | `refs`       |    |
| 5 | `repeated uint32` | `version`    |    |

#### `CidList`



| # | 类型               | 字段     | 说明 |
| - | ---------------- | ------ | -- |
| 1 | `repeated bytes` | `cids` |    |

#### `FileEntry`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated string` | `cids`       |    |
| 2 | `repeated uint64` | `size`       |    |
| 3 | `repeated int64`  | `createTime` |    |
| 4 | `repeated int64`  | `updateTime` |    |

#### `GroupEntry`



| # | 类型                | 字段             | 说明 |
| - | ----------------- | -------------- | -- |
| 1 | `repeated string` | `groupId`      |    |
| 2 | `repeated int64`  | `createTime`   |    |
| 3 | `repeated int64`  | `updateTime`   |    |
| 4 | `repeated uint64` | `size`         |    |
| 5 | `repeated uint64` | `cidCount`     |    |
| 6 | `repeated string` | `spaceIds`     |    |
| 7 | `repeated uint64` | `limit`        |    |
| 8 | `repeated uint64` | `accountLimit` |    |

#### `OwnershipRecord`



| # | 类型                | 字段               | 说明 |
| - | ----------------- | ---------------- | -- |
| 1 | `repeated string` | `ownerId`        |    |
| 2 | `repeated int64`  | `aclRecordIndex` |    |

#### `SpaceEntry`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated string` | `groupId`    |    |
| 2 | `repeated int64`  | `createTime` |    |
| 3 | `repeated int64`  | `updateTime` |    |
| 4 | `repeated uint64` | `size`       |    |
| 5 | `repeated uint32` | `fileCount`  |    |
| 6 | `repeated uint64` | `cidCount`   |    |
| 7 | `repeated uint64` | `limit`      |    |

### any-sync-node/debug/nodedebugrpc/nodedebugrpcproto/protos/nodedebugrpc.proto

#### `AllSpacesRequest`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `AllSpacesResponse`



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `spaceIds` |    |

#### `AllTreesRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |

#### `AllTreesResponse`



| # | 类型              | 字段      | 说明 |
| - | --------------- | ------- | -- |
| 1 | `repeated Tree` | `trees` |    |

#### `DumpTreeRequest`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated string` | `spaceId`    |    |
| 2 | `repeated string` | `documentId` |    |

#### `DumpTreeResponse`



| # | 类型                | 字段     | 说明 |
| - | ----------------- | ------ | -- |
| 1 | `repeated string` | `dump` |    |

#### `ForceNodeSyncRequest`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `ForceNodeSyncResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `NodesAddressesBySpaceRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |

#### `NodesAddressesBySpaceResponse`



| # | 类型                | 字段              | 说明 |
| - | ----------------- | --------------- | -- |
| 1 | `repeated string` | `nodeAddresses` |    |

#### `Tree`



| # | 类型                | 字段      | 说明 |
| - | ----------------- | ------- | -- |
| 1 | `repeated string` | `id`    |    |
| 2 | `repeated string` | `heads` |    |

#### `TreeParamsRequest`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated string` | `spaceId`    |    |
| 2 | `repeated string` | `documentId` |    |

#### `TreeParamsResponse`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `rootId`  |    |
| 2 | `repeated string` | `headIds` |    |

### any-sync-node/nodesync/nodesyncproto/protos/nodesync.proto

#### `AdoptArchiveRequest`



| # | 类型                | 字段                 | 说明                                                                                        |
| - | ----------------- | ------------------ | ----------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `spaceId`          |                                                                                           |
| 2 | `repeated string` | `srcKey`           | srcKey is the full key of the gzipped snapshot within the shared bucket (sender's prefix) |
| 3 | `repeated string` | `oldHash`          | heads hashes of the space at snapshot time, as stored in the sender's index               |
| 4 | `repeated string` | `newHash`          |                                                                                           |
| 5 | `repeated bool`   | `eager`            | eager asks the receiver to restore the space in background right away                     |
| 6 | `repeated int64`  | `compressedSize`   |                                                                                           |
| 7 | `repeated int64`  | `uncompressedSize` |                                                                                           |

#### `AdoptArchiveResponse`



| # | 类型                            | 字段       | 说明 |
| - | ----------------------------- | -------- | -- |
| 1 | `repeated AdoptArchiveResult` | `result` |    |

#### `ColdSyncRequest`



| # | 类型                              | 字段             | 说明 |
| - | ------------------------------- | -------------- | -- |
| 1 | `repeated string`               | `spaceId`      |    |
| 2 | `repeated ColdSyncProtocolType` | `protocolType` |    |

#### `ColdSyncResponse`



| # | 类型                              | 字段             | 说明 |
| - | ------------------------------- | -------------- | -- |
| 2 | `repeated string`               | `filename`     |    |
| 3 | `repeated bytes`                | `data`         |    |
| 4 | `repeated uint32`               | `crc32`        |    |
| 5 | `repeated ColdSyncProtocolType` | `protocolType` |    |

#### `PartitionSyncRange`

> PartitionSyncRange presenting a request for one range



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated uint64` | `from`     |    |
| 2 | `repeated uint64` | `to`       |    |
| 3 | `repeated uint32` | `limit`    |    |
| 4 | `repeated bool`   | `elements` |    |

#### `PartitionSyncRequest`

> HeadSyncRequest is a request for HeadSync



| # | 类型                            | 字段            | 说明 |
| - | ----------------------------- | ------------- | -- |
| 1 | `repeated uint64`             | `partitionId` |    |
| 2 | `repeated PartitionSyncRange` | `ranges`      |    |

#### `PartitionSyncResponse`

> PartitionSyncResponse is a response for HeadSync



| # | 类型                             | 字段        | 说明 |
| - | ------------------------------ | --------- | -- |
| 1 | `repeated PartitionSyncResult` | `results` |    |

#### `PartitionSyncResult`

> PartitionSyncResult presenting a response for one range



| # | 类型                                    | 字段         | 说明 |
| - | ------------------------------------- | ---------- | -- |
| 1 | `repeated bytes`                      | `hash`     |    |
| 2 | `repeated PartitionSyncResultElement` | `elements` |    |
| 3 | `repeated uint32`                     | `count`    |    |

#### `PartitionSyncResultElement`

> PartitionSyncResultElement presenting state of one object



| # | 类型                | 字段     | 说明 |
| - | ----------------- | ------ | -- |
| 1 | `repeated string` | `id`   |    |
| 2 | `repeated string` | `head` |    |

### any-sync/commonfile/fileproto/filep2p/protos/filep2p.proto

#### `FileAvailability`



| # | 类型                      | 字段        | 说明 |
| - | ----------------------- | --------- | -- |
| 1 | `repeated bytes`        | `rootCid` |    |
| 2 | `repeated Availability` | `have`    |    |

#### `FileCheckRequest`

> \---- FileCheck (availability) ---------------------------------------------



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `spaceId`  |    |
| 2 | `repeated bytes`  | `rootCids` |    |

#### `FileCheckResponse`



| # | 类型                          | 字段      | 说明 |
| - | --------------------------- | ------- | -- |
| 1 | `repeated FileAvailability` | `files` |    |

#### `ObjectReadRequest`

> \---- ObjectRead (ranged CAR bytes) ----------------------------------------



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated bytes`  | `rootCid` |    |
| 3 | `repeated uint64` | `offset`  |    |
| 4 | `repeated uint32` | `length`  |    |

#### `ObjectReadResponse`



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated bytes`  | `data`      |    |
| 2 | `repeated uint64` | `totalSize` |    |

### any-sync/commonfile/fileproto/fileprotov2/protos/filev2.proto

#### `InfoRequest`

> \---- Info (node-level metadata) --------------------------------------------- InfoRequest is deliberately empty: Info is static node metadata, extensible later (capabilities, limits) without a wire break.



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `InfoResponse`



| # | 类型                | 字段                  | 说明                                                                                                                                                                                                                         |
| - | ----------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `publicReadBaseUrl` | publicReadBaseUrl, when non-empty, lets clients construct durable object URLs as {publicReadBaseUrl}/blob/{spaceId}/{rootCid} with zero broker round-trips; clients cache it. Empty = no public read: use RequestDownload. |

#### `NetworkSignReceipt`

> NetworkSignReceipt mirrors coordinator SpaceReceiptWithSignature: an opaque protobuf-encoded payload plus the network-key signature over it. The payload schema is intentionally not defined here (opaque blob forwarded verbatim).



| # | 类型               | 字段               | 说明 |
| - | ---------------- | ---------------- | -- |
| 1 | `repeated bytes` | `receiptPayload` |    |
| 2 | `repeated bytes` | `signature`      |    |

#### `PresignField`



| # | 类型                | 字段      | 说明 |
| - | ----------------- | ------- | -- |
| 1 | `repeated string` | `key`   |    |
| 2 | `repeated string` | `value` |    |

#### `PresignedUpload`

> PresignedUpload is an OPAQUE presigned upload target. No S3 vendor structs leak into the shared proto: the client POSTs 
>
> `fields`
>
>  \+ the object body to 
>
> `url`
>
>  verbatim. Modeled as a presigned POST form (fields are ordered key/value pairs rather than a map) so the signing order is deterministic and reproducible.



| # | 类型                      | 字段                 | 说明 |
| - | ----------------------- | ------------------ | -- |
| 1 | `repeated string`       | `url`              |    |
| 2 | `repeated PresignField` | `fields`           |    |
| 3 | `repeated uint64`       | `maxContentLength` |    |
| 4 | `repeated int64`        | `expiry`           |    |

#### `RequestDownloadRequest`

> \---- RequestDownload ------------------------------------------------------



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `spaceId`  |    |
| 2 | `repeated bytes`  | `rootCids` |    |

#### `RequestDownloadResponse`



| # | 类型                               | 字段        | 说明 |
| - | -------------------------------- | --------- | -- |
| 1 | `repeated RequestDownloadResult` | `results` |    |

#### `RequestDownloadResult`



| # | 类型                        | 字段         | 说明 |
| - | ------------------------- | ---------- | -- |
| 1 | `repeated bytes`          | `rootCid`  |    |
| 2 | `repeated ErrCode`        | `code`     |    |
| 3 | `repeated SignedDownload` | `download` |    |

#### `RequestSignRequest`

> \---- RequestSign ----------------------------------------------------------



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `spaceId`  |    |
| 2 | `repeated bytes`  | `rootCids` |    |

#### `RequestSignResponse`



| # | 类型                           | 字段        | 说明 |
| - | ---------------------------- | --------- | -- |
| 1 | `repeated RequestSignResult` | `results` |    |

#### `RequestSignResult`



| # | 类型                            | 字段        | 说明 |
| - | ----------------------------- | --------- | -- |
| 1 | `repeated bytes`              | `rootCid` |    |
| 2 | `repeated ErrCode`            | `code`    |    |
| 3 | `repeated NetworkSignReceipt` | `receipt` |    |

#### `SignedDownload`

> SignedDownload is an OPAQUE signed GET target (kept as a message, symmetric with PresignedUpload, so download can grow response headers etc. without a wire break on the result envelope).



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `url`    |    |
| 2 | `repeated int64`  | `expiry` |    |

#### `SpaceInfoRequest`

> \---- SpaceInfo (batch quota-info) -----------------------------------------



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `spaceIds` |    |

#### `SpaceInfoResponse`



| # | 类型                         | 字段        | 说明 |
| - | -------------------------- | --------- | -- |
| 1 | `repeated SpaceInfoResult` | `results` |    |

#### `SpaceInfoResult`



| # | 类型                    | 字段        | 说明 |
| - | --------------------- | --------- | -- |
| 1 | `repeated string`     | `spaceId` |    |
| 2 | `repeated ErrCode`    | `code`    |    |
| 3 | `repeated SpaceQuota` | `quota`   |    |

#### `SpaceQuota`



| # | 类型                | 字段                   | 说明                                                                                                                                                                                                         |
| - | ----------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated uint64` | `limitBytes`         |                                                                                                                                                                                                            |
| 2 | `repeated uint64` | `totalUsageBytes`    |                                                                                                                                                                                                            |
| 3 | `repeated uint64` | `durableUsageBytes`  |                                                                                                                                                                                                            |
| 4 | `repeated uint64` | `inflightUsageBytes` |                                                                                                                                                                                                            |
| 5 | `repeated uint64` | `filesCount`         |                                                                                                                                                                                                            |
| 6 | `repeated uint64` | `accountLimitBytes`  | account-pool view for the requesting identity (files are charged to their uploader; all the identity's spaces share one pool). Zero when the node has no coordinator-backed limits (self-hosted fallback). |
| 7 | `repeated uint64` | `accountUsageBytes`  |                                                                                                                                                                                                            |

#### `UploadRequest`

> \---- Upload ---------------------------------------------------------------



| # | 类型                           | 字段        | 说明 |
| - | ---------------------------- | --------- | -- |
| 1 | `repeated string`            | `spaceId` |    |
| 2 | `repeated UploadRequestItem` | `items`   |    |

#### `UploadRequestItem`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated bytes`  | `rootCid` |    |
| 2 | `repeated uint64` | `size`    |    |

#### `UploadResponse`



| # | 类型                      | 字段        | 说明 |
| - | ----------------------- | --------- | -- |
| 1 | `repeated UploadResult` | `results` |    |

#### `UploadResult`



| # | 类型                         | 字段        | 说明 |
| - | -------------------------- | --------- | -- |
| 1 | `repeated bytes`           | `rootCid` |    |
| 2 | `repeated ErrCode`         | `code`    |    |
| 3 | `repeated PresignedUpload` | `upload`  |    |

### any-sync/commonfile/fileproto/protos/file.proto

#### `AccountInfoRequest`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `AccountInfoResponse`



| # | 类型                           | 字段                  | 说明                                         |
| - | ---------------------------- | ------------------- | ------------------------------------------ |
| 1 | `repeated uint64`            | `limitBytes`        | the shared limit excluding isolated spaces |
| 2 | `repeated uint64`            | `totalUsageBytes`   |                                            |
| 3 | `repeated uint64`            | `totalCidsCount`    |                                            |
| 4 | `repeated SpaceInfoResponse` | `spaces`            |                                            |
| 5 | `repeated uint64`            | `accountLimitBytes` | the total limit including isolated spaces  |

#### `AccountLimitSetRequest`



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `identity` |    |
| 2 | `repeated uint64` | `limit`    |    |

#### `Block`



| # | 类型               | 字段     | 说明 |
| - | ---------------- | ------ | -- |
| 2 | `repeated bytes` | `cid`  |    |
| 3 | `repeated bytes` | `data` |    |

#### `BlockAvailability`



| # | 类型                            | 字段       | 说明 |
| - | ----------------------------- | -------- | -- |
| 1 | `repeated bytes`              | `cid`    |    |
| 2 | `repeated AvailabilityStatus` | `status` |    |

#### `BlockDeleteUnboundRequest`



| # | 类型               | 字段    | 说明 |
| - | ---------------- | ----- | -- |
| 1 | `repeated bytes` | `cid` |    |

#### `BlockGetRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated bytes`  | `cid`     |    |
| 3 | `repeated bool`   | `wait`    |    |

#### `BlockGetResponse`



| # | 类型               | 字段     | 说明 |
| - | ---------------- | ------ | -- |
| 1 | `repeated bytes` | `cid`  |    |
| 2 | `repeated bytes` | `data` |    |

#### `BlockPushManyRequest`



| # | 类型                    | 字段           | 说明 |
| - | --------------------- | ------------ | -- |
| 1 | `repeated FileBlocks` | `fileBlocks` |    |

#### `BlockPushRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated string` | `fileId`  |    |
| 3 | `repeated bytes`  | `cid`     |    |
| 4 | `repeated bytes`  | `data`    |    |

#### `BlocksBindRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated string` | `fileId`  |    |
| 3 | `repeated bytes`  | `cids`    |    |

#### `BlocksCheckRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated bytes`  | `cids`    |    |

#### `BlocksCheckResponse`



| # | 类型                           | 字段                   | 说明 |
| - | ---------------------------- | -------------------- | -- |
| 1 | `repeated BlockAvailability` | `blocksAvailability` |    |

#### `CheckRequest`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `CheckResponse`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated string` | `spaceIds`   |    |
| 2 | `repeated bool`   | `allowWrite` |    |

#### `FileBlocks`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `fileId`  |    |
| 2 | `repeated string` | `spaceId` |    |
| 3 | `repeated Block`  | `blocks`  |    |

#### `FileInfo`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated string` | `fileId`     |    |
| 2 | `repeated uint64` | `usageBytes` |    |
| 3 | `repeated uint32` | `cidsCount`  |    |

#### `FilesDeleteRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated string` | `fileIds` |    |

#### `FilesDeleteResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `FilesGetRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |

#### `FilesGetResponse`



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `fileId` |    |

#### `FilesInfoRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated string` | `fileIds` |    |

#### `FilesInfoResponse`



| # | 类型                  | 字段          | 说明 |
| - | ------------------- | ----------- | -- |
| 1 | `repeated FileInfo` | `filesInfo` |    |

#### `Ok`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `SpaceInfoRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |

#### `SpaceInfoResponse`



| # | 类型                | 字段                | 说明 |
| - | ----------------- | ----------------- | -- |
| 1 | `repeated uint64` | `limitBytes`      |    |
| 2 | `repeated uint64` | `totalUsageBytes` |    |
| 3 | `repeated uint64` | `cidsCount`       |    |
| 4 | `repeated uint64` | `filesCount`      |    |
| 5 | `repeated uint64` | `spaceUsageBytes` |    |
| 6 | `repeated string` | `spaceId`         |    |

#### `SpaceLimitSetRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated uint64` | `limit`   |    |

### any-sync/commonspace/clientspaceproto/protos/clientspace.proto

#### `LocalServer`



| # | 类型                | 字段     | 说明 |
| - | ----------------- | ------ | -- |
| 1 | `repeated string` | `Ips`  |    |
| 2 | `repeated int32`  | `port` |    |

#### `SpaceExchangeRequest`



| # | 类型                     | 字段            | 说明 |
| - | ---------------------- | ------------- | -- |
| 1 | `repeated string`      | `spaceIds`    |    |
| 2 | `repeated LocalServer` | `localServer` |    |

#### `SpaceExchangeResponse`



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `spaceIds` |    |

#### `SpaceExchangeV2Request`



| # | 类型                     | 字段            | 说明                                                                                                                                            |
| - | ---------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated bytes`       | `nonce`       | nonce is 32 random bytes chosen by the caller; it challenges both request and response tokens                                                 |
| 2 | `repeated bytes`       | `spaceTokens` | spaceTokens holds one 32-byte request token per caller space, padded with random tokens up to a bucket size and sorted to hide the true count |
| 3 | `repeated LocalServer` | `localServer` |                                                                                                                                               |

#### `SpaceExchangeV2Response`



| # | 类型               | 字段            | 说明                                                                                                                                     |
| - | ---------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated bytes` | `spaceTokens` | spaceTokens holds one 32-byte response token per intersecting space — the responder's proof of membership, keyed by the caller's nonce |

### any-sync/commonspace/object/acl/aclrecordproto/protos/aclrecord.proto

#### `AclAccountAdd`

> AclAccountAdd contains new account to be added



| # | 类型                            | 字段                 | 说明 |
| - | ----------------------------- | ------------------ | -- |
| 1 | `repeated bytes`              | `identity`         |    |
| 2 | `repeated AclUserPermissions` | `permissions`      |    |
| 3 | `repeated bytes`              | `metadata`         |    |
| 4 | `repeated bytes`              | `encryptedReadKey` |    |

#### `AclAccountInvite`

> AclAccountInvite contains the public invite key, the private part of which is sent to the user directly



| # | 类型                            | 字段                 | 说明                                                                                                                                                                                          |
| - | ----------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated bytes`              | `inviteKey`        |                                                                                                                                                                                             |
| 2 | `repeated AclInviteType`      | `inviteType`       |                                                                                                                                                                                             |
| 3 | `repeated AclUserPermissions` | `permissions`      | permissions tells with which permissions the user joins the space. Used only for invites without approve.                                                                                   |
| 4 | `repeated bytes`              | `encryptedReadKey` | encryptedReadKey is used when the user creates an invite without approve. So everyone having the invite can join the space immediately. The key could only be decrypted using the inviteKey |

#### `AclAccountInviteChange`



| # | 类型                            | 字段               | 说明 |
| - | ----------------------------- | ---------------- | -- |
| 1 | `repeated string`             | `inviteRecordId` |    |
| 2 | `repeated AclUserPermissions` | `permissions`    |    |

#### `AclAccountInviteJoin`

> AclInviteJoin contains the reference to the invite record and the data of the person who wants to join, confirmed by the private invite key The person must encrypt the key with its own public key



| # | 类型                            | 字段                        | 说明                                                                              |
| - | ----------------------------- | ------------------------- | ------------------------------------------------------------------------------- |
| 1 | `repeated bytes`              | `identity`                |                                                                                 |
| 2 | `repeated string`             | `inviteRecordId`          |                                                                                 |
| 3 | `repeated bytes`              | `inviteIdentitySignature` |                                                                                 |
| 4 | `repeated bytes`              | `metadata`                | Metadata is encrypted with metadata key of the space                            |
| 5 | `repeated bytes`              | `encryptedReadKey`        | encryptedReadKey is the read key of a space encrypted using person's public key |
| 6 | `repeated AclUserPermissions` | `permissions`             |                                                                                 |

#### `AclAccountInviteRevoke`

> AclAccountInviteRevoke revokes the invite record



| # | 类型                | 字段               | 说明 |
| - | ----------------- | ---------------- | -- |
| 1 | `repeated string` | `inviteRecordId` |    |

#### `AclAccountPermissionChange`

> AclAccountPermissionChange changes permissions of specific account



| # | 类型                            | 字段            | 说明 |
| - | ----------------------------- | ------------- | -- |
| 1 | `repeated bytes`              | `identity`    |    |
| 2 | `repeated AclUserPermissions` | `permissions` |    |

#### `AclAccountPermissionChanges`

> AclAccountPermissionChanges contains permission changes for certain identities



| # | 类型                                    | 字段        | 说明 |
| - | ------------------------------------- | --------- | -- |
| 1 | `repeated AclAccountPermissionChange` | `changes` |    |

#### `AclAccountRemove`

> AclAccountRemove removes an account and changes read key for space



| # | 类型                          | 字段              | 说明 |
| - | --------------------------- | --------------- | -- |
| 1 | `repeated bytes`            | `identities`    |    |
| 2 | `repeated AclReadKeyChange` | `readKeyChange` |    |

#### `AclAccountRequestAccept`

> AclAccountRequestAccept contains the reference to join record and all read keys, encrypted with the identity of the requestor



| # | 类型                            | 字段                 | 说明 |
| - | ----------------------------- | ------------------ | -- |
| 1 | `repeated bytes`              | `identity`         |    |
| 2 | `repeated string`             | `requestRecordId`  |    |
| 3 | `repeated bytes`              | `encryptedReadKey` |    |
| 4 | `repeated AclUserPermissions` | `permissions`      |    |

#### `AclAccountRequestCancel`

> AclRequestCancel contains reference to the request that is canceled by the account



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `recordId` |    |

#### `AclAccountRequestDecline`

> AclAccountRequestDecline contains the reference to join record



| # | 类型                | 字段                | 说明 |
| - | ----------------- | ----------------- | -- |
| 1 | `repeated string` | `requestRecordId` |    |

#### `AclAccountRequestJoin`

> AclAccountRequestJoin contains the reference to the invite record and the data of the person who wants to join, confirmed by the private invite key



| # | 类型                | 字段                        | 说明                                                   |
| - | ----------------- | ------------------------- | ---------------------------------------------------- |
| 1 | `repeated bytes`  | `inviteIdentity`          |                                                      |
| 2 | `repeated string` | `inviteRecordId`          |                                                      |
| 3 | `repeated bytes`  | `inviteIdentitySignature` |                                                      |
| 4 | `repeated bytes`  | `metadata`                | Metadata is encrypted with metadata key of the space |

#### `AclAccountRequestRemove`

> AclAccountRequestRemove adds a request to remove an account



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `AclAccountsAdd`

> AclAccountsAdd contains new accounts to be added



| # | 类型                       | 字段          | 说明 |
| - | ------------------------ | ----------- | -- |
| 1 | `repeated AclAccountAdd` | `additions` |    |

#### `AclContentValue`

> AclContentValue contains possible values for Acl



| # | 类型            | 字段 | 说明 |
| - | ------------- | -- | -- |
| — | (oneof) value |    |    |

#### `AclData`

> AclData contains different acl content



| # | 类型                         | 字段           | 说明 |
| - | -------------------------- | ------------ | -- |
| 1 | `repeated AclContentValue` | `aclContent` |    |

#### `AclEncryptedReadKey`

> AclEncryptedReadKeys are new key for specific identity



| # | 类型               | 字段                 | 说明 |
| - | ---------------- | ------------------ | -- |
| 1 | `repeated bytes` | `identity`         |    |
| 2 | `repeated bytes` | `encryptedReadKey` |    |

#### `AclOneToOneInfo`

> AclOneToOneInfo exists if its one-to-one space acl record



| # | 类型               | 字段        | 说明 |
| - | ---------------- | --------- | -- |
| 1 | `repeated bytes` | `owner`   |    |
| 2 | `repeated bytes` | `writers` |    |

#### `AclOwnershipChange`

> AclOwnershipChange contains the new owner identity



| # | 类型                            | 字段                    | 说明 |
| - | ----------------------------- | --------------------- | -- |
| 1 | `repeated bytes`              | `newOwnerIdentity`    |    |
| 2 | `repeated AclUserPermissions` | `oldOwnerPermissions` |    |

#### `AclReadKeyChange`

> AclReadKeyChange changes the key for a space



| # | 类型                             | 字段                         | 说明                                                      |
| - | ------------------------------ | -------------------------- | ------------------------------------------------------- |
| 1 | `repeated AclEncryptedReadKey` | `accountKeys`              |                                                         |
| 2 | `repeated bytes`               | `metadataPubKey`           |                                                         |
| 3 | `repeated bytes`               | `encryptedMetadataPrivKey` | EncryptedMetadataPrivKey is encrypted with new read key |
| 4 | `repeated bytes`               | `encryptedOldReadKey`      | EncryptedOldReadKey is encrypted with new read key      |
| 5 | `repeated AclEncryptedReadKey` | `inviteKeys`               |                                                         |

#### `AclRoot`

> AclRoot is a root of access control list



| #  | 类型                         | 字段                         | 说明 |
| -- | -------------------------- | -------------------------- | -- |
| 1  | `repeated bytes`           | `identity`                 |    |
| 2  | `repeated bytes`           | `masterKey`                |    |
| 3  | `repeated string`          | `spaceId`                  |    |
| 4  | `repeated bytes`           | `encryptedReadKey`         |    |
| 5  | `repeated int64`           | `timestamp`                |    |
| 6  | `repeated bytes`           | `identitySignature`        |    |
| 7  | `repeated bytes`           | `metadataPubKey`           |    |
| 8  | `repeated bytes`           | `encryptedMetadataPrivKey` |    |
| 9  | `repeated bytes`           | `encryptedOwnerMetadata`   |    |
| 10 | `repeated AclOneToOneInfo` | `oneToOneInfo`             |    |
| 11 | `repeated AclSpaceOptions` | `options`                  |    |

#### `AclSpaceOptions`

> AclSpaceOptions contains space-level toggles/options



| # | 类型              | 字段                 | 说明 |
| - | --------------- | ------------------ | -- |
| 1 | `repeated bool` | `deleteRestricted` |    |

#### `AclSpaceOptionsChange`

> AclSpaceOptionsChange changes space options (owner-only)



| # | 类型                         | 字段        | 说明 |
| - | -------------------------- | --------- | -- |
| 1 | `repeated AclSpaceOptions` | `options` |    |

### any-sync/commonspace/object/tree/treechangeproto/protos/treechange.proto

#### `NoDataTreeChange`

> TreeChange is a change of a tree



| # | 类型                | 字段               | 说明                                                                           |
| - | ----------------- | ---------------- | ---------------------------------------------------------------------------- |
| 1 | `repeated string` | `treeHeadIds`    | TreeHeadIds are previous ids for this TreeChange                             |
| 2 | `repeated string` | `aclHeadId`      | AclHeadId is a cid of latest acl record at the time of this change           |
| 3 | `repeated string` | `snapshotBaseId` | SnapshotBaseId is a snapshot (root) of the tree where this change is added   |
| 5 | `repeated string` | `readKeyId`      | ReadKeyId is the id of the read key                                          |
| 6 | `repeated int64`  | `timestamp`      | Timestamp is this change creation timestamp                                  |
| 7 | `repeated bytes`  | `identity`       | Identity is a public key with which the raw payload of this change is signed |
| 8 | `repeated bool`   | `isSnapshot`     | IsSnapshot indicates whether this change contains a snapshot of state        |
| 9 | `repeated string` | `dataType`       | DataType indicates some special parameters of data for the client            |

#### `RawTreeChange`

> RawTreeChange is a marshalled TreeChange (or RootChange) payload and a signature of this payload



| # | 类型               | 字段          | 说明                                                                            |
| - | ---------------- | ----------- | ----------------------------------------------------------------------------- |
| 1 | `repeated bytes` | `payload`   | Payload is a byte payload containing TreeChange                               |
| 2 | `repeated bytes` | `signature` | Signature is a signature made by identity indicated in the TreeChange payload |

#### `RawTreeChangeWithId`

> RawTreeChangeWithId is a marshalled RawTreeChange with CID



| # | 类型                | 字段          | 说明                                           |
| - | ----------------- | ----------- | -------------------------------------------- |
| 1 | `repeated bytes`  | `rawChange` | RawChange is a byte payload of RawTreeChange |
| 2 | `repeated string` | `id`        | Id is a cid made from rawChange payload      |

#### `ReducedTreeChange`



| # | 类型                | 字段            | 说明                                               |
| - | ----------------- | ------------- | ------------------------------------------------ |
| 1 | `repeated string` | `treeHeadIds` | TreeHeadIds are previous ids for this TreeChange |

#### `RootChange`

> RootChange is a root of a tree



| # | 类型                | 字段              | 说明                                                                   |
| - | ----------------- | --------------- | -------------------------------------------------------------------- |
| 1 | `repeated string` | `aclHeadId`     | AclHeadId is a cid of latest acl record at the time of tree creation |
| 2 | `repeated string` | `spaceId`       | SpaceId is an id of space where the document is placed               |
| 3 | `repeated string` | `changeType`    | ChangeType is a type of tree which this RootChange is a root of      |
| 4 | `repeated int64`  | `timestamp`     | Timestamp is this change creation timestamp                          |
| 5 | `repeated bytes`  | `seed`          | Seed is a random bytes to make root change unique                    |
| 6 | `repeated bytes`  | `identity`      | Identity is a public key of the tree's creator                       |
| 7 | `repeated bytes`  | `changePayload` | ChangePayload is a payload related to ChangeType                     |
| 8 | `repeated bool`   | `isDerived`     | IsDerived tells if the tree is derived                               |
| 9 | `repeated string` | `parentId`      | ParentId is the id of the parent object for bound derived objects    |

#### `TreeChange`

> TreeChange is a change of a tree



| # | 类型                | 字段               | 说明                                                                           |
| - | ----------------- | ---------------- | ---------------------------------------------------------------------------- |
| 1 | `repeated string` | `treeHeadIds`    | TreeHeadIds are previous ids for this TreeChange                             |
| 2 | `repeated string` | `aclHeadId`      | AclHeadId is a cid of latest acl record at the time of this change           |
| 3 | `repeated string` | `snapshotBaseId` | SnapshotBaseId is a snapshot (root) of the tree where this change is added   |
| 4 | `repeated bytes`  | `changesData`    | ChangesData is an arbitrary payload to be read by the client                 |
| 5 | `repeated string` | `readKeyId`      | ReadKeyId is the id of the read key                                          |
| 6 | `repeated int64`  | `timestamp`      | Timestamp is this change creation timestamp                                  |
| 7 | `repeated bytes`  | `identity`       | Identity is a public key with which the raw payload of this change is signed |
| 8 | `repeated bool`   | `isSnapshot`     | IsSnapshot indicates whether this change contains a snapshot of state        |
| 9 | `repeated string` | `dataType`       | DataType indicates some special parameters of data for the client            |

#### `TreeChangeInfo`

> TreeChangeInfo is used internally in Tree implementation for ease of marshalling



| # | 类型                | 字段              | 说明 |
| - | ----------------- | --------------- | -- |
| 1 | `repeated string` | `changeType`    |    |
| 2 | `repeated bytes`  | `changePayload` |    |

#### `TreeErrorResponse`

> TreeErrorResponse is an error sent as a response for a full sync request



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `error`   |    |
| 2 | `repeated uint64` | `errCode` |    |

#### `TreeFullSyncRequest`

> TreeHeadUpdate is a message sent when document needs full sync



| # | 类型                             | 字段             | 说明                                                                                                                                                                                                         |
| - | ------------------------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string`              | `heads`        |                                                                                                                                                                                                            |
| 2 | `repeated RawTreeChangeWithId` | `changes`      |                                                                                                                                                                                                            |
| 3 | `repeated string`              | `snapshotPath` |                                                                                                                                                                                                            |
| 4 | `repeated bool`                | `probe`        | probe asks the responder for the tree's root and current heads only, with no change bodies. Old responders ignore it and stream the full tree; a probing requester must be ready for both response shapes. |

#### `TreeFullSyncResponse`

> TreeFullSyncResponse is a message sent as a response for a specific full sync



| # | 类型                             | 字段             | 说明 |
| - | ------------------------------ | -------------- | -- |
| 1 | `repeated string`              | `heads`        |    |
| 2 | `repeated RawTreeChangeWithId` | `changes`      |    |
| 3 | `repeated string`              | `snapshotPath` |    |

#### `TreeHeadUpdate`

> TreeHeadUpdate is a message sent on document head update



| # | 类型                             | 字段             | 说明 |
| - | ------------------------------ | -------------- | -- |
| 1 | `repeated string`              | `heads`        |    |
| 2 | `repeated RawTreeChangeWithId` | `changes`      |    |
| 3 | `repeated string`              | `snapshotPath` |    |

#### `TreeSyncContentValue`

> TreeSyncContentValue provides different types for tree sync



| # | 类型            | 字段 | 说明 |
| - | ------------- | -- | -- |
| — | (oneof) value |    |    |

#### `TreeSyncMessage`



| # | 类型                              | 字段           | 说明 |
| - | ------------------------------- | ------------ | -- |
| 1 | `repeated TreeSyncContentValue` | `content`    |    |
| 2 | `repeated RawTreeChangeWithId`  | `rootChange` |    |

### any-sync/commonspace/pubsub/pubsubproto/protos/pubsub.proto

#### `PubSubMessage`

> PubSubMessage is the single frame type carried by PubSubStream



| # | 类型              | 字段 | 说明 |
| - | --------------- | -- | -- |
| — | (oneof) content |    |    |

#### `Publish`

> Publish carries one ephemeral fire-and-forget message to a fully-qualified topic



| # | 类型                | 字段               | 说明                                                                                                                                       |
| - | ----------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `spaceId`        |                                                                                                                                          |
| 2 | `repeated string` | `topic`          | topic is a fully-qualified '/'-separated topic; wildcards are not allowed                                                                |
| 3 | `repeated bytes`  | `msgId`          | msgId is 16 random bytes generated by the publisher, used for duplicate suppression                                                      |
| 4 | `repeated string` | `keyId`          | keyId is the space ReadKey id used to encrypt the payload; empty means plaintext (keyless spaces)                                        |
| 5 | `repeated bytes`  | `payload`        | payload is ciphertext, or plaintext iff keyId is empty                                                                                   |
| 6 | `repeated bytes`  | `identity`       | identity is the sender's marshalled account public key                                                                                   |
| 7 | `repeated bytes`  | `signature`      | signature is the account-key signature over "anysync:pubsub:v1" \| spaceId \| topic \| msgId \| keyId \| le64(timestampMilli) \| payload |
| 8 | `repeated int64`  | `timestampMilli` | timestampMilli is the sender's wall clock, informational                                                                                 |
| 9 | `repeated bool`   | `relayed`        | relayed is set by a node when forwarding node-to-node; a relayed message is never forwarded again; excluded from the signature           |

#### `Status`

> Status is sent by the serving peer on a rejected subscribe or publish; success is silent



| # | 类型                  | 字段        | 说明                                                                                                                                   |
| - | ------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 1 | `repeated string`   | `spaceId` |                                                                                                                                      |
| 2 | `repeated string`   | `topics`  | topics echoes the offending patterns (or the topic of a rejected publish)                                                            |
| 3 | `repeated ErrCodes` | `code`    |                                                                                                                                      |
| 4 | `repeated bytes`    | `msgId`   | msgId echoes a rejected publish's id so the caller can correlate the rejection to a specific Publish; empty for subscribe rejections |

#### `Subscribe`

> Subscribe adds topic patterns to the stream's interest set for the space. Patterns may contain wildcards: '*' matches exactly one segment, '>' matches one-or-more trailing segments (tail-only)



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated string` | `topics`  |    |

#### `Unsubscribe`

> Unsubscribe removes patterns from the stream's interest set, matched verbatim (not expanded); empty topics means remove all patterns of the space



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated string` | `topics`  |    |

### any-sync/commonspace/spacesyncproto/protos/spacesync.proto

#### `AclAddRecordRequest`

> AclAddRecordRequest contains marshaled consensusproto.RawRecord



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated bytes`  | `payload` |    |

#### `AclAddRecordResponse`

> AclAddRecordResponse contains created record id and marshaled consensusproto.RawRecord



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `recordId` |    |
| 2 | `repeated bytes`  | `payload`  |    |

#### `AclGetRecordsRequest`

> AclGetRecordsRequest can optionally contain the last known aclHead, the server will return only new records or an empty list if there are no new records. If aclHead is not provided the whole list will be returned.



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated string` | `aclHead` |    |

#### `AclGetRecordsResponse`

> AclGetRecordsResponse contains list of marshaled consensusproto.RawRecordWithId



| # | 类型               | 字段        | 说明 |
| - | ---------------- | --------- | -- |
| 1 | `repeated bytes` | `records` |    |

#### `AclRecord`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated bytes`  | `aclPayload` |    |
| 2 | `repeated string` | `id`         |    |

#### `HeadSyncRange`

> HeadSyncRange presenting a request for one range



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated uint64` | `from`     |    |
| 2 | `repeated uint64` | `to`       |    |
| 3 | `repeated uint32` | `limit`    |    |
| 4 | `repeated bool`   | `elements` |    |

#### `HeadSyncRequest`

> HeadSyncRequest is a request for HeadSync



| # | 类型                       | 字段         | 说明 |
| - | ------------------------ | ---------- | -- |
| 1 | `repeated string`        | `spaceId`  |    |
| 2 | `repeated HeadSyncRange` | `ranges`   |    |
| 3 | `repeated DiffType`      | `diffType` |    |

#### `HeadSyncResponse`

> HeadSyncResponse is a response for HeadSync



| # | 类型                        | 字段         | 说明 |
| - | ------------------------- | ---------- | -- |
| 1 | `repeated HeadSyncResult` | `results`  |    |
| 2 | `repeated DiffType`       | `diffType` |    |

#### `HeadSyncResult`

> HeadSyncResult presenting a response for one range



| # | 类型                               | 字段         | 说明 |
| - | -------------------------------- | ---------- | -- |
| 1 | `repeated bytes`                 | `hash`     |    |
| 2 | `repeated HeadSyncResultElement` | `elements` |    |
| 3 | `repeated uint32`                | `count`    |    |

#### `HeadSyncResultElement`

> HeadSyncResultElement presenting state of one object



| # | 类型                | 字段     | 说明 |
| - | ----------------- | ------ | -- |
| 1 | `repeated string` | `id`   |    |
| 2 | `repeated string` | `head` |    |

#### `ObjectDelete`

> ObjectDelete is a message containing an object id which should be deleted



| # | 类型                | 字段   | 说明 |
| - | ----------------- | ---- | -- |
| 1 | `repeated string` | `id` |    |

#### `ObjectSyncMessage`

> ObjectSyncMessage is a message sent on object sync



| # | 类型                    | 字段           | 说明 |
| - | --------------------- | ------------ | -- |
| 1 | `repeated string`     | `spaceId`    |    |
| 2 | `repeated string`     | `requestId`  |    |
| 3 | `repeated string`     | `replyId`    |    |
| 4 | `repeated bytes`      | `payload`    |    |
| 5 | `repeated string`     | `objectId`   |    |
| 6 | `repeated ObjectType` | `objectType` |    |

#### `RawSpaceHeader`

> RawSpaceHeader is raw header for SpaceHeader



| # | 类型               | 字段            | 说明 |
| - | ---------------- | ------------- | -- |
| 1 | `repeated bytes` | `spaceHeader` |    |
| 2 | `repeated bytes` | `signature`   |    |

#### `RawSpaceHeaderWithId`

> RawSpaceHeaderWithId is a marshalled RawSpaceHeader with its content id



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated bytes`  | `rawHeader` |    |
| 2 | `repeated string` | `id`        |    |

#### `SettingsData`

> SettingsData contains ObjectTree change payload



| # | 类型                               | 字段         | 说明 |
| - | -------------------------------- | ---------- | -- |
| 1 | `repeated SpaceSettingsContent`  | `content`  |    |
| 2 | `repeated SpaceSettingsSnapshot` | `snapshot` |    |

#### `SpaceDelete`

> SpaceDelete is a message containing deleter peer id



| # | 类型                | 字段              | 说明 |
| - | ----------------- | --------------- | -- |
| 1 | `repeated string` | `deleterPeerId` |    |

#### `SpaceHeader`

> SpaceHeader is a header for a space



| #   | 类型                               | 字段                   | 说明                                                                                    |
| --- | -------------------------------- | -------------------- | ------------------------------------------------------------------------------------- |
| 1   | `repeated bytes`                 | `identity`           |                                                                                       |
| 2   | `repeated int64`                 | `timestamp`          |                                                                                       |
| 3   | `repeated string`                | `spaceType`          |                                                                                       |
| 4   | `repeated uint64`                | `replicationKey`     |                                                                                       |
| 5   | `repeated bytes`                 | `seed`               |                                                                                       |
| 6   | `repeated bytes`                 | `spaceHeaderPayload` |                                                                                       |
| 7   | `repeated bytes`                 | `aclPayload`         | since v1 fields                                                                       |
| 8   | `repeated bytes`                 | `settingPayload`     |                                                                                       |
| 9   | `repeated SpaceFileProtoVersion` | `fileprotoVersion`   | fileprotoVersion gates the file protocol (v2 = filenode v2 + S3-direct + networkSign) |
| 100 | `repeated SpaceHeaderVersion`    | `version`            |                                                                                       |

#### `SpacePayload`

> SpacePayload is a payload for pushing a space



| # | 类型                              | 字段                       | 说明 |
| - | ------------------------------- | ------------------------ | -- |
| 1 | `repeated RawSpaceHeaderWithId` | `spaceHeader`            |    |
| 2 | `repeated bytes`                | `aclPayload`             |    |
| 3 | `repeated string`               | `aclPayloadId`           |    |
| 4 | `repeated bytes`                | `spaceSettingsPayload`   |    |
| 5 | `repeated string`               | `spaceSettingsPayloadId` |    |

#### `SpacePullRequest`

> SpacePullRequest is a request to request a space on a node that doesn't have it



| # | 类型                | 字段   | 说明 |
| - | ----------------- | ---- | -- |
| 1 | `repeated string` | `id` |    |

#### `SpacePullResponse`

> SpacePullResponse is a response with header and acl root



| # | 类型                      | 字段           | 说明 |
| - | ----------------------- | ------------ | -- |
| 1 | `repeated SpacePayload` | `payload`    |    |
| 2 | `repeated AclRecord`    | `aclRecords` |    |

#### `SpacePushRequest`

> SpacePushRequest is a request to add space on a node containing only one acl record



| # | 类型                      | 字段           | 说明 |
| - | ----------------------- | ------------ | -- |
| 1 | `repeated SpacePayload` | `payload`    |    |
| 2 | `repeated bytes`        | `Credential` |    |

#### `SpacePushResponse`

> SpacePushResponse is an empty response



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `SpaceSettingsContent`

> SpaceSettingsContent is a payload for a space settings object



| # | 类型            | 字段 | 说明 |
| - | ------------- | -- | -- |
| — | (oneof) value |    |    |

#### `SpaceSettingsSnapshot`

> SpaceSettingsSnapshot contains all the deleted ids in a snapshot



| # | 类型                | 字段              | 说明 |
| - | ----------------- | --------------- | -- |
| 1 | `repeated string` | `deletedIds`    |    |
| 2 | `repeated string` | `deleterPeerId` |    |

#### `SpaceSubscription`



| # | 类型                                 | 字段         | 说明 |
| - | ---------------------------------- | ---------- | -- |
| 1 | `repeated string`                  | `spaceIds` |    |
| 2 | `repeated SpaceSubscriptionAction` | `action`   |    |

#### `StorageHeader`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `spaceId`     |    |
| 2 | `repeated string` | `storageName` |    |

#### `StoreDeletePrefix`

> StoreDeletePrefix is the deletion watermark operation: applying the row carrying it physically removes every stored row whose key starts with the prefix and whose timestamp is older than the watermark's, and rejects such rows arriving later. The watermark row itself is the only retained state. It lives inside the signed StoreKeyInner so the operation type cannot be forged, and rides the ordinary element sync so it reaches every replica — including devices restoring from old snapshots.



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `prefix` |    |

#### `StoreDiffRequest`



| # | 类型                       | 字段        | 说明 |
| - | ------------------------ | --------- | -- |
| 1 | `repeated string`        | `spaceId` |    |
| 2 | `repeated HeadSyncRange` | `ranges`  |    |

#### `StoreDiffResponse`



| # | 类型                        | 字段        | 说明 |
| - | ------------------------- | --------- | -- |
| 1 | `repeated HeadSyncResult` | `results` |    |

#### `StoreHeader`

> StoreHeader is a header for a store



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `spaceId`     |    |
| 2 | `repeated string` | `storageName` |    |

#### `StoreKeyInner`



| # | 类型                           | 字段               | 说明                                                                                                                                     |
| - | ---------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated bytes`             | `peer`           |                                                                                                                                        |
| 2 | `repeated bytes`             | `identity`       |                                                                                                                                        |
| 3 | `repeated bytes`             | `value`          |                                                                                                                                        |
| 4 | `repeated int64`             | `timestampMicro` |                                                                                                                                        |
| 5 | `repeated string`            | `aclHeadId`      |                                                                                                                                        |
| 6 | `repeated string`            | `key`            |                                                                                                                                        |
| 7 | `repeated StoreDeletePrefix` | `delete`         | delete turns this row into a deletion watermark instead of a value (see StoreDeletePrefix). key mirrors the prefix; value stays empty. |

#### `StoreKeyValue`



| # | 类型                | 字段                  | 说明 |
| - | ----------------- | ------------------- | -- |
| 1 | `repeated string` | `keyPeerId`         |    |
| 2 | `repeated bytes`  | `value`             |    |
| 3 | `repeated bytes`  | `identitySignature` |    |
| 4 | `repeated bytes`  | `peerSignature`     |    |
| 5 | `repeated string` | `spaceId`           |    |

#### `StoreKeyValues`



| # | 类型                       | 字段          | 说明 |
| - | ------------------------ | ----------- | -- |
| 1 | `repeated StoreKeyValue` | `keyValues` |    |

### any-sync/consensus/consensusproto/protos/consensus.proto

#### `Err`



| # | 类型                  | 字段      | 说明 |
| - | ------------------- | ------- | -- |
| 1 | `repeated ErrCodes` | `error` |    |

#### `Log`



| # | 类型                         | 字段        | 说明 |
| - | -------------------------- | --------- | -- |
| 1 | `repeated string`          | `id`      |    |
| 3 | `repeated RawRecordWithId` | `records` |    |

#### `LogAddRequest`



| # | 类型                         | 字段       | 说明                                                  |
| - | -------------------------- | -------- | --------------------------------------------------- |
| 1 | `repeated string`          | `logId`  |                                                     |
| 2 | `repeated RawRecordWithId` | `record` | first record in the log, consensus node not sign it |

#### `LogDeleteRequest`



| # | 类型                | 字段      | 说明 |
| - | ----------------- | ------- | -- |
| 1 | `repeated string` | `logId` |    |

#### `LogFullSyncRequest`

> LogFullSyncRequest is a message sent when consensus log needs full sync



| # | 类型                         | 字段        | 说明 |
| - | -------------------------- | --------- | -- |
| 1 | `repeated string`          | `head`    |    |
| 2 | `repeated RawRecordWithId` | `records` |    |

#### `LogFullSyncResponse`

> LogFullSyncResponse is a message sent as a response for a specific full sync



| # | 类型                         | 字段        | 说明 |
| - | -------------------------- | --------- | -- |
| 1 | `repeated string`          | `head`    |    |
| 2 | `repeated RawRecordWithId` | `records` |    |

#### `LogHeadUpdate`

> LogHeadUpdate is a message sent on consensus log head update



| # | 类型                         | 字段        | 说明 |
| - | -------------------------- | --------- | -- |
| 1 | `repeated string`          | `head`    |    |
| 2 | `repeated RawRecordWithId` | `records` |    |

#### `LogSyncContentValue`

> LogSyncContentValue provides different types for log sync



| # | 类型            | 字段 | 说明 |
| - | ------------- | -- | -- |
| — | (oneof) value |    |    |

#### `LogSyncMessage`

> LogSyncMessage is a message sent when we are syncing logs



| # | 类型                             | 字段        | 说明 |
| - | ------------------------------ | --------- | -- |
| 1 | `repeated string`              | `id`      |    |
| 2 | `repeated bytes`               | `payload` |    |
| 3 | `repeated LogSyncContentValue` | `content` |    |

#### `LogWatchEvent`



| # | 类型                         | 字段        | 说明 |
| - | -------------------------- | --------- | -- |
| 1 | `repeated string`          | `logId`   |    |
| 2 | `repeated RawRecordWithId` | `records` |    |
| 3 | `repeated Err`             | `error`   |    |

#### `LogWatchRequest`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated string` | `watchIds`   |    |
| 2 | `repeated string` | `unwatchIds` |    |

#### `Ok`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `RawRecord`

> RawRecord is a proto message containing the payload in bytes, signature of the account who added it and signature of the acceptor



| # | 类型               | 字段                  | 说明 |
| - | ---------------- | ------------------- | -- |
| 1 | `repeated bytes` | `payload`           |    |
| 2 | `repeated bytes` | `signature`         |    |
| 3 | `repeated bytes` | `acceptorIdentity`  |    |
| 4 | `repeated bytes` | `acceptorSignature` |    |
| 5 | `repeated int64` | `acceptorTimestamp` |    |

#### `RawRecordWithId`

> RawRecordWithId is a raw record and the id for convenience



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated bytes`  | `payload` |    |
| 2 | `repeated string` | `id`      |    |

#### `Record`

> Record is a record containing a data



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated string` | `prevId`    |    |
| 2 | `repeated bytes`  | `identity`  |    |
| 3 | `repeated bytes`  | `data`      |    |
| 4 | `repeated int64`  | `timestamp` |    |

#### `RecordAddRequest`



| # | 类型                   | 字段       | 说明 |
| - | -------------------- | -------- | -- |
| 1 | `repeated string`    | `logId`  |    |
| 2 | `repeated RawRecord` | `record` |    |

### any-sync/coordinator/coordinatorproto/protos/coordinator.proto

#### `AccountDeleteRequest`

> AccountDeleteRequest contains payload for account deletion



| # | 类型                | 字段                  | 说明 |
| - | ----------------- | ------------------- | -- |
| 1 | `repeated string` | `deletionPayloadId` |    |
| 2 | `repeated bytes`  | `deletionPayload`   |    |

#### `AccountDeleteResponse`

> AccountDeleteResponse contains timestamp when the account is finally deleted



| # | 类型               | 字段                     | 说明 |
| - | ---------------- | ---------------------- | -- |
| 1 | `repeated int64` | `toBeDeletedTimestamp` |    |

#### `AccountDeletionConfirmPayload`

> AccountDeletionConfirmPayload contains payload for deletion confirmation



| # | 类型                | 字段                | 说明                                                                |
| - | ----------------- | ----------------- | ----------------------------------------------------------------- |
| 1 | `repeated string` | `peerId`          | PeerId of receipt requester                                       |
| 2 | `repeated bytes`  | `accountIdentity` | AccountIdentity is an identity of a space owner                   |
| 3 | `repeated string` | `networkId`       | NetworkId is the id of a network where the deletion was requested |
| 4 | `repeated int64`  | `timestamp`       | Timestamp is a timestamp when the deletion was requested          |

#### `AccountLimits`

> AccountLimits describes account level limit



| # | 类型                | 字段                  | 说明 |
| - | ----------------- | ------------------- | -- |
| 1 | `repeated uint32` | `sharedSpacesLimit` |    |

#### `AccountLimitsSetRequest`



| # | 类型                | 字段                      | 说明 |
| - | ----------------- | ----------------------- | -- |
| 1 | `repeated string` | `identity`              |    |
| 2 | `repeated string` | `reason`                |    |
| 3 | `repeated uint64` | `fileStorageLimitBytes` |    |
| 4 | `repeated uint32` | `spaceMembersRead`      |    |
| 5 | `repeated uint32` | `spaceMembersWrite`     |    |
| 6 | `repeated uint32` | `sharedSpacesLimit`     |    |

#### `AccountLimitsSetResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `AccountRevertDeletionRequest`

> AccountRevertDeletionRequest is a request to revert an account deletion



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `AccountRevertDeletionResponse`

> AccountRevertDeletionResponse is an empty response confirming that the deletion is reverted



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `AclAddRecordRequest`

> AclAddRecordRequest contains marshaled consensusproto.RawRecord



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated bytes`  | `payload` |    |

#### `AclAddRecordResponse`

> AclAddRecordResponse contains created record id and marshaled consensusproto.RawRecord



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `recordId` |    |
| 2 | `repeated bytes`  | `payload`  |    |

#### `AclDeleteInviteRequest`

> AclDeleteInviteRequest asks the coordinator to remove a revoked invite's file from the filenodes. The coordinator resolves the cid to its invite through the binding made by AclUploadInvite and refuses to remove one that still grants access.



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated string` | `spaceId`   |    |
| 2 | `repeated bytes`  | `inviteCid` |    |

#### `AclDeleteInviteResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `AclEventLogRecord`



| # | 类型                               | 字段            | 说明                                              |
| - | -------------------------------- | ------------- | ----------------------------------------------- |
| 1 | `repeated string`                | `id`          | Id is a record id                               |
| 2 | `repeated string`                | `spaceId`     | SpaceId is a space identifier                   |
| 3 | `repeated int64`                 | `timestamp`   | Timestamp is a unixtimestamp of record creation |
| 4 | `repeated AclEventLogRecordType` | `type`        | Type of current event                           |
| 5 | `repeated string`                | `aclChangeId` | only for RecordTypeSpaceAclAddRecord            |

#### `AclEventLogRequest`



| # | 类型                | 字段                | 说明                                                                                                                           |
| - | ----------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `accountIdentity` |                                                                                                                              |
| 2 | `repeated string` | `afterId`         | AfterId is the last known logId to request records after this id. If it is empty will be returned a list from the beginning. |
| 3 | `repeated uint32` | `limit`           | Limit is a desired record count in response                                                                                  |

#### `AclEventLogResponse`



| # | 类型                           | 字段        | 说明                                                                           |
| - | ---------------------------- | --------- | ---------------------------------------------------------------------------- |
| 1 | `repeated AclEventLogRecord` | `records` | AclEventLogRecord list of records, if there are no new records will be empty |
| 2 | `repeated bool`              | `hasMore` | HasMore indicates if there are records left                                  |

#### `AclGetRecordsRequest`

> AclGetRecordsRequest can optionally contain the last known aclHead, the server will return only new records or an empty list if there are no new records. If aclHead is not provided the whole list will be returned.



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated string` | `aclHead` |    |

#### `AclGetRecordsResponse`

> AclGetRecordsResponse contains list of marshaled consensusproto.RawRecordWithId



| # | 类型               | 字段        | 说明 |
| - | ---------------- | --------- | -- |
| 1 | `repeated bytes` | `records` |    |

#### `AclUploadInviteRequest`



| # | 类型                | 字段             | 说明                                                                                                            |
| - | ----------------- | -------------- | ------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated bytes`  | `cid`          |                                                                                                               |
| 2 | `repeated bytes`  | `data`         |                                                                                                               |
| 3 | `repeated string` | `spaceId`      | spaceId and invitePubKey bind the uploaded file to its invite, so that AclDeleteInvite can later remove it.   |
| 4 | `repeated bytes`  | `invitePubKey` | invitePubKey is the PUBLIC part of the invite key. For a guest invite it is the public part of the guest key. |

#### `AclUploadInviteResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `DeletionConfirmPayload`

> DeletionConfirmPayload contains payload for deletion confirmation



| # | 类型                | 字段                | 说明                                                                |
| - | ----------------- | ----------------- | ----------------------------------------------------------------- |
| 1 | `repeated string` | `spaceId`         | SpaceId is the identifier of space                                |
| 2 | `repeated string` | `peerId`          | PeerId of receipt requester                                       |
| 3 | `repeated bytes`  | `accountIdentity` | AccountIdentity is an identity of a space owner                   |
| 4 | `repeated string` | `networkId`       | NetworkId is the id of a network where the deletion was requested |
| 5 | `repeated int64`  | `timestamp`       | Timestamp is a timestamp when the deletion was requested          |

#### `DeletionConfirmPayloadWithSignature`

> DeletionConfirmPayloadWithSignature contains protobuf encoded deletion payload and its signature



| # | 类型               | 字段                | 说明 |
| - | ---------------- | ----------------- | -- |
| 1 | `repeated bytes` | `deletionPayload` |    |
| 2 | `repeated bytes` | `signature`       |    |

#### `DeletionLogRecord`



| # | 类型                                 | 字段            | 说明                                              |
| - | ---------------------------------- | ------------- | ----------------------------------------------- |
| 1 | `repeated string`                  | `id`          | Id is a record id                               |
| 2 | `repeated string`                  | `spaceId`     | SpaceId is a space identifier                   |
| 3 | `repeated DeletionLogRecordStatus` | `status`      | DeletionLogRecordStatus is a space status       |
| 4 | `repeated int64`                   | `timestamp`   | Timestamp is a unixtimestamp of record creation |
| 5 | `repeated string`                  | `fileGroup`   | FileGroup is a key of group for file nodes      |
| 6 | `repeated string`                  | `aclRecordId` | AclRecordId (optional)                          |

#### `DeletionLogRequest`



| # | 类型                | 字段        | 说明                                                                                                                           |
| - | ----------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `afterId` | AfterId is the last known logId to request records after this id. If it is empty will be returned a list from the beginning. |
| 2 | `repeated uint32` | `limit`   | Limit is a desired record count in response                                                                                  |

#### `DeletionLogResponse`



| # | 类型                           | 字段        | 说明                                                                           |
| - | ---------------------------- | --------- | ---------------------------------------------------------------------------- |
| 1 | `repeated DeletionLogRecord` | `records` | DeletionLogRecord list of records, if there are no new records will be empty |
| 2 | `repeated bool`              | `hasMore` | HasMore indicates if there are records left                                  |

#### `FileLimitsGetRequest`



| # | 类型                | 字段         | 说明                                                                        |
| - | ----------------- | ---------- | ------------------------------------------------------------------------- |
| 1 | `repeated string` | `spaceId`  |                                                                           |
| 2 | `repeated string` | `identity` | Identity is the uploader account identity whose pool bounds are requested |

#### `FileLimitsGetResponse`



| # | 类型                | 字段                       | 说明                                                                                                  |
| - | ----------------- | ------------------------ | --------------------------------------------------------------------------------------------------- |
| 1 | `repeated uint64` | `accountLimitBytes`      | AccountLimitBytes is the identity's total file-storage cap (the common account pool)                |
| 2 | `repeated uint64` | `accountTotalUsageBytes` | AccountTotalUsageBytes is the coordinator-aggregated durable usage across all the identity's spaces |
| 3 | `repeated uint64` | `spaceLimitBytes`        | SpaceLimitBytes is an optional space-scoped cap; 0 = unset                                          |

#### `FileUsageReportRequest`



| # | 类型                      | 字段     | 说明 |
| - | ----------------------- | ------ | -- |
| 1 | `repeated FileUsageRow` | `rows` |    |

#### `FileUsageReportResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `FileUsageRow`



| # | 类型                | 字段                  | 说明                                                                                                           |
| - | ----------------- | ------------------- | ------------------------------------------------------------------------------------------------------------ |
| 1 | `repeated string` | `spaceId`           |                                                                                                              |
| 2 | `repeated string` | `identity`          | Identity is the charged uploader identity (the author of the root's earliest bind row)                       |
| 3 | `repeated uint64` | `durableBytes`      | DurableBytes is the HEAD-measured durable usage of this (space, identity) slice; in-flight is never reported |
| 4 | `repeated uint64` | `durableFilesCount` |                                                                                                              |

#### `InboxAddMessageRequest`



| # | 类型                      | 字段        | 说明 |
| - | ----------------------- | --------- | -- |
| 1 | `repeated InboxMessage` | `message` |    |

#### `InboxAddMessageResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `InboxFetchRequest`



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated string` | `offset` |    |

#### `InboxFetchResponse`



| # | 类型                      | 字段         | 说明 |
| - | ----------------------- | ---------- | -- |
| 1 | `repeated InboxMessage` | `messages` |    |
| 2 | `repeated bool`         | `hasMore`  |    |

#### `InboxMessage`



| # | 类型                         | 字段           | 说明 |
| - | -------------------------- | ------------ | -- |
| 1 | `repeated string`          | `id`         |    |
| 2 | `repeated InboxPacketType` | `packetType` |    |
| 3 | `repeated InboxPacket`     | `packet`     |    |

#### `InboxPacket`



| # | 类型                      | 字段                 | 说明 |
| - | ----------------------- | ------------------ | -- |
| 1 | `repeated InboxKeyType` | `keyType`          |    |
| 2 | `repeated string`       | `senderIdentity`   |    |
| 3 | `repeated string`       | `receiverIdentity` |    |
| 4 | `repeated bytes`        | `senderSignature`  |    |
| 5 | `repeated InboxPayload` | `payload`          |    |

#### `InboxPayload`



| # | 类型                          | 字段            | 说明 |
| - | --------------------------- | ------------- | -- |
| 1 | `repeated InboxPayloadType` | `payloadType` |    |
| 2 | `repeated int64`            | `timestamp`   |    |
| 3 | `repeated bytes`            | `body`        |    |

#### `NetworkConfigurationRequest`

> NetworkConfigurationRequest contains currenId of the client configuration, it can be empty



| # | 类型                | 字段          | 说明                                                                                                                                            |
| - | ----------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `currentId` | currenId of the client configuration if the currentId is equal to the latest configuration id then the response will not contain a nodes list |

#### `NetworkConfigurationResponse`

> NetworkConfigurationResponse contains list of nodes



| # | 类型                | 字段                 | 说明                                                                                                                            |
| - | ----------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `configurationId`  | id of current configuration                                                                                                   |
| 2 | `repeated string` | `networkId`        | network id                                                                                                                    |
| 3 | `repeated Node`   | `nodes`            | nodes list - it will be empty if the client's currentId is equal configurationId                                              |
| 4 | `repeated uint64` | `creationTimeUnix` | unix timestamp of the creation time of configuration                                                                          |
| 5 | `repeated uint64` | `epoch`            | monotonically increasing version of the configuration, 0 if the coordinator predates epoch support                            |
| 6 | `repeated string` | `fileNetworkId`    | identity of the fileV2 fleet's shared receipt-signing key (network string encoding); empty if the network has no fileV2 fleet |

#### `Node`

> Node describes one node in the network



| # | 类型                  | 字段          | 说明                                                                                  |
| - | ------------------- | ----------- | ----------------------------------------------------------------------------------- |
| 1 | `repeated string`   | `peerId`    | peerId - it's a peer identifier (libp2p format string) so it's an encoded publicKey |
| 2 | `repeated string`   | `addresses` | list of node addresses                                                              |
| 3 | `repeated NodeType` | `types`     | list of supported APIs                                                              |

#### `NotifySubscribeEvent`



| # | 类型                         | 字段          | 说明 |
| - | -------------------------- | ----------- | -- |
| 1 | `repeated NotifyEventType` | `eventType` |    |
| 2 | `repeated bytes`           | `payload`   |    |

#### `NotifySubscribeRequest`

> Request to subscribe to notifications



| # | 类型                         | 字段          | 说明 |
| - | -------------------------- | ----------- | -- |
| 1 | `repeated NotifyEventType` | `eventType` |    |

#### `SpaceDeleteRequest`

> SpaceDeleteRequest contains the deletion confirmation for the space to be deleted



| # | 类型                | 字段                  | 说明 |
| - | ----------------- | ------------------- | -- |
| 1 | `repeated string` | `spaceId`           |    |
| 2 | `repeated string` | `deletionPayloadId` |    |
| 3 | `repeated bytes`  | `deletionPayload`   |    |
| 4 | `repeated int64`  | `deletionDuration`  |    |

#### `SpaceDeleteResponse`

> SpaceDeleteResponse contains timestamp when the space is finally deleted



| # | 类型               | 字段                     | 说明 |
| - | ---------------- | ---------------------- | -- |
| 1 | `repeated int64` | `toBeDeletedTimestamp` |    |

#### `SpaceLimits`



| # | 类型                | 字段             | 说明 |
| - | ----------------- | -------------- | -- |
| 1 | `repeated uint32` | `readMembers`  |    |
| 2 | `repeated uint32` | `writeMembers` |    |

#### `SpaceMakeShareableRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |

#### `SpaceMakeShareableResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `SpaceMakeUnshareableRequest`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |
| 2 | `repeated string` | `aclHead` |    |

#### `SpaceMakeUnshareableResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `SpaceReceipt`

> SpaceReceipt contains permission to SpacePush operation



| # | 类型                | 字段                | 说明                                                                      |
| - | ----------------- | ----------------- | ----------------------------------------------------------------------- |
| 1 | `repeated string` | `spaceId`         | SpaceId is the identifier of space                                      |
| 2 | `repeated string` | `peerId`          | PeerId of receipt requester                                             |
| 3 | `repeated bytes`  | `accountIdentity` | AccountIdentity is an identity of a space owner                         |
| 4 | `repeated string` | `networkId`       | NetworkId is the id of a network where the receipt is issued            |
| 5 | `repeated uint64` | `validUntil`      | ValidUntil is a unix-timestamp with a deadline time of receipt validity |

#### `SpaceReceiptWithSignature`

> SpaceReceiptWithSignature contains protobuf encoded receipt and its signature



| # | 类型               | 字段                    | 说明 |
| - | ---------------- | --------------------- | -- |
| 1 | `repeated bytes` | `spaceReceiptPayload` |    |
| 2 | `repeated bytes` | `signature`           |    |

#### `SpaceSignRequest`



| # | 类型                | 字段             | 说明                                                                                                                                                                                       |
| - | ----------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `spaceId`      | SpaceId is the id of the signed space                                                                                                                                                    |
| 2 | `repeated bytes`  | `header`       | Header is the header of the signed space                                                                                                                                                 |
| 5 | `repeated bool`   | `forceRequest` | Deprecated: OldIdentity is no longer used Deprecated: NewIdentitySignature is no longer used ForceRequest if true, forces the creating space receipt even if the space is deleted before |

#### `SpaceSignResponse`



| # | 类型                                   | 字段        | 说明 |
| - | ------------------------------------ | --------- | -- |
| 1 | `repeated SpaceReceiptWithSignature` | `receipt` |    |

#### `SpaceStatusChangeRequest`

> SpaceStatusChangeRequest contains the deletionChange if we want to delete space, or it is empty otherwise



| # | 类型                             | 字段                    | 说明 |
| - | ------------------------------ | --------------------- | -- |
| 1 | `repeated string`              | `spaceId`             |    |
| 2 | `repeated string`              | `deletionPayloadId`   |    |
| 3 | `repeated bytes`               | `deletionPayload`     |    |
| 4 | `repeated DeletionPayloadType` | `deletionPayloadType` |    |

#### `SpaceStatusChangeResponse`

> SpaceStatusChangeResponse contains changed status of space



| # | 类型                            | 字段        | 说明 |
| - | ----------------------------- | --------- | -- |
| 1 | `repeated SpaceStatusPayload` | `payload` |    |

#### `SpaceStatusCheckManyRequest`

> SpaceStatusCheckManyRequest contains the spaceIds of requested spaces



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `spaceIds` |    |

#### `SpaceStatusCheckManyResponse`

> SpaceStatusCheckManyResponse contains the current statuses of spaces



| # | 类型                            | 字段              | 说明 |
| - | ----------------------------- | --------------- | -- |
| 1 | `repeated SpaceStatusPayload` | `payloads`      |    |
| 2 | `repeated AccountLimits`      | `accountLimits` |    |

#### `SpaceStatusCheckRequest`

> SpaceStatusCheckRequest contains the spaceId of requested space



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `spaceId` |    |

#### `SpaceStatusCheckResponse`

> SpaceStatusCheckResponse contains the current status of space



| # | 类型                            | 字段        | 说明 |
| - | ----------------------------- | --------- | -- |
| 1 | `repeated SpaceStatusPayload` | `payload` |    |

#### `SpaceStatusPayload`



| # | 类型                          | 字段                  | 说明 |
| - | --------------------------- | ------------------- | -- |
| 1 | `repeated SpaceStatus`      | `status`            |    |
| 2 | `repeated int64`            | `deletionTimestamp` |    |
| 3 | `repeated SpacePermissions` | `permissions`       |    |
| 4 | `repeated SpaceLimits`      | `limits`            |    |
| 5 | `repeated bool`             | `isShared`          |    |

### any-sync/identityrepo/identityrepoproto/protos/identityrepo.proto

#### `Data`



| # | 类型                | 字段          | 说明                                             |
| - | ----------------- | ----------- | ---------------------------------------------- |
| 1 | `repeated string` | `kind`      | kind is a string representing the kind of data |
| 2 | `repeated bytes`  | `data`      | data is a byte payload                         |
| 3 | `repeated bytes`  | `signature` | data signature                                 |

#### `DataDeleteRequest`



| # | 类型                | 字段         | 说明                                                                |
| - | ----------------- | ---------- | ----------------------------------------------------------------- |
| 1 | `repeated string` | `identity` | string representation of identity, must be equal handshake result |
| 2 | `repeated string` | `kinds`    | kinds of data to delete, if empty all kinds will be deleted       |

#### `DataPullRequest`



| # | 类型                | 字段           | 说明                                   |
| - | ----------------- | ------------ | ------------------------------------ |
| 1 | `repeated string` | `identities` | list of identities wanted to request |
| 2 | `repeated string` | `kinds`      | kinds of data wanted to request      |

#### `DataPullResponse`



| # | 类型                          | 字段     | 说明 |
| - | --------------------------- | ------ | -- |
| 1 | `repeated DataWithIdentity` | `data` |    |

#### `DataPutRequest`



| # | 类型                | 字段         | 说明                                                                |
| - | ----------------- | ---------- | ----------------------------------------------------------------- |
| 1 | `repeated string` | `identity` | string representation of identity, must be equal handshake result |
| 2 | `repeated Data`   | `data`     | data to save                                                      |

#### `DataWithIdentity`



| # | 类型                | 字段         | 说明 |
| - | ----------------- | ---------- | -- |
| 1 | `repeated string` | `identity` |    |
| 2 | `repeated Data`   | `data`     |    |

#### `Ok`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

### any-sync/nameservice/nameserviceproto/protos/nameservice.proto

#### `BatchNameAvailableRequest`



| # | 类型                | 字段          | 说明                          |
| - | ----------------- | ----------- | --------------------------- |
| 1 | `repeated string` | `fullNames` | Names including .any suffix |

#### `BatchNameAvailableResponse`



| # | 类型                               | 字段        | 说明 |
| - | -------------------------------- | --------- | -- |
| 1 | `repeated NameAvailableResponse` | `results` |    |

#### `BatchNameByAddressRequest`



| # | 类型                | 字段                     | 说明                                                            |
| - | ----------------- | ---------------------- | ------------------------------------------------------------- |
| 1 | `repeated string` | `ownerScwEthAddresses` | EOA -> SCW -> name A SCW Ethereum address that owns that name |

#### `BatchNameByAddressResponse`



| # | 类型                               | 字段        | 说明 |
| - | -------------------------------- | --------- | -- |
| 1 | `repeated NameByAddressResponse` | `results` |    |

#### `BatchNameByAnyIdRequest`



| # | 类型                | 字段             | 说明 |
| - | ----------------- | -------------- | -- |
| 1 | `repeated string` | `anyAddresses` |    |

#### `NameAvailableRequest`

> import "google/protobuf/timestamp.proto";



| # | 类型                | 字段         | 说明                         |
| - | ----------------- | ---------- | -------------------------- |
| 1 | `repeated string` | `fullName` | Name including .any suffix |

#### `NameAvailableResponse`



| # | 类型                | 字段                   | 说明                                                                                                                    |
| - | ----------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated bool`   | `available`          |                                                                                                                       |
| 2 | `repeated string` | `ownerScwEthAddress` | EOA -> SCW -> name This field is non-empty only if name is "already registered"                                       |
| 3 | `repeated string` | `ownerEthAddress`    | This field is non-empty only if name is "already registered"                                                          |
| 4 | `repeated string` | `ownerAnyAddress`    | A content hash attached to this name This field is non-empty only if name is "already registered"                     |
| 5 | `repeated string` | `spaceId`            | A SpaceID attached to this name This field is non-empty only if name is "already registered"                          |
| 6 | `repeated int64`  | `nameExpires`        | doesn't work with marashalling/unmarshalling google.protobuf.Timestamp nameExpires = 5 \[(gogoproto.stdtime) = true]; |

#### `NameByAddressRequest`



| # | 类型                | 字段                   | 说明                                                            |
| - | ----------------- | -------------------- | ------------------------------------------------------------- |
| 1 | `repeated string` | `ownerScwEthAddress` | EOA -> SCW -> name A SCW Ethereum address that owns that name |

#### `NameByAddressResponse`



| # | 类型                | 字段      | 说明 |
| - | ----------------- | ------- | -- |
| 1 | `repeated bool`   | `found` |    |
| 2 | `repeated string` | `name`  |    |

#### `NameByAnyIdRequest`



| # | 类型                | 字段           | 说明 |
| - | ----------------- | ------------ | -- |
| 1 | `repeated string` | `anyAddress` |    |

### any-sync/nameservice/nameserviceproto/protos/nameservice\_aa.proto

#### `AdminFundGasOperationsRequest`



| # | 类型                | 字段                | 说明                                                       |
| - | ----------------- | ----------------- | -------------------------------------------------------- |
| 1 | `repeated string` | `ownerEthAddress` | An Ethereum address that owns that name                  |
| 2 | `repeated string` | `ownerAnyID`      |                                                          |
| 3 | `repeated uint64` | `operationsCount` | Number of gas operations: update name, add new data, etc |

#### `AdminFundGasOperationsRequestSigned`



| # | 类型               | 字段          | 说明                                      |
| - | ---------------- | ----------- | --------------------------------------- |
| 1 | `repeated bytes` | `payload`   | AdminFundGasOperationsRequest struct    |
| 2 | `repeated bytes` | `signature` | payload signed by Admin of this service |

#### `AdminFundUserAccountRequest`



| # | 类型                | 字段                | 说明                                                                                                           |
| - | ----------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ |
| 1 | `repeated string` | `ownerEthAddress` | An Ethereum address that owns that name                                                                      |
| 2 | `repeated uint64` | `namesCount`      | Number of names that user can buy. We will mint him tokens that he can use to buy names (one token per name) |

#### `AdminFundUserAccountRequestSigned`



| # | 类型               | 字段          | 说明                                      |
| - | ---------------- | ----------- | --------------------------------------- |
| 1 | `repeated bytes` | `payload`   | AdminFundUserAccountRequest struct      |
| 2 | `repeated bytes` | `signature` | payload signed by Admin of this service |

#### `CreateUserOperationRequest`



| # | 类型                | 字段                | 说明                                                                                                                                      |
| - | ----------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated bytes`  | `data`            |                                                                                                                                         |
| 2 | `repeated bytes`  | `signedData`      | "data" signed with Ethereum private key                                                                                                 |
| 3 | `repeated bytes`  | `context`         |                                                                                                                                         |
| 4 | `repeated string` | `ownerEthAddress` |                                                                                                                                         |
| 5 | `repeated string` | `ownerAnyID`      | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 6 | `repeated string` | `fullName`        | all operations currently are towards single name, please specify it we can use it for caching, etc purps.                               |

#### `CreateUserOperationRequestSigned`



| # | 类型               | 字段          | 说明                                   |
| - | ---------------- | ----------- | ------------------------------------ |
| 1 | `repeated bytes` | `payload`   | CreateUserOperationRequest struct    |
| 2 | `repeated bytes` | `signature` | payload signed with Anytype identity |

#### `GetDataNameRegisterResponse`



| # | 类型               | 字段        | 说明 |
| - | ---------------- | --------- | -- |
| 1 | `repeated bytes` | `data`    |    |
| 2 | `repeated bytes` | `context` |    |

#### `GetOperationStatusRequest`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `operationId` |    |

#### `GetUserAccountRequest`

> no signature required here



| # | 类型                | 字段                | 说明                                         |
| - | ----------------- | ----------------- | ------------------------------------------ |
| 1 | `repeated string` | `ownerEthAddress` | An Ethereum address that owns that account |

#### `NameRegisterForSpaceRequest`



| # | 类型                | 字段                     | 说明                                                                                                                                                                                                     |
| - | ----------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1 | `repeated string` | `fullName`             |                                                                                                                                                                                                        |
| 2 | `repeated string` | `ownerAnyAddress`      | A content hash attached to this name This should not be empty! in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 3 | `repeated string` | `ownerEthAddress`      | An Ethereum address that owns that name                                                                                                                                                                |
| 4 | `repeated string` | `spaceId`              | A SpaceID attached to this name                                                                                                                                                                        |
| 5 | `repeated uint32` | `registerPeriodMonths` | How many months to register the name for                                                                                                                                                               |

#### `NameRegisterRequest`



| # | 类型                | 字段                              | 说明                                                                                                                                                                                                     |
| - | ----------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1 | `repeated string` | `fullName`                      |                                                                                                                                                                                                        |
| 2 | `repeated string` | `ownerAnyAddress`               | A content hash attached to this name This should not be empty! in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 3 | `repeated string` | `ownerEthAddress`               | An Ethereum address that owns that name                                                                                                                                                                |
| 4 | `repeated bool`   | `registerToSmartContractWallet` | if false -> name ownership will belong to ownerEthAddress if true -> name ownership will belong to SCW of ownerEthAddress (AccountAbstraction)                                                         |
| 5 | `repeated uint32` | `registerPeriodMonths`          | How many months to register the name for                                                                                                                                                               |

#### `NameRegisterRequestSigned`

> Example: 1 - register alice.any -> ANYID123123 2 - register xxxx.any -> ANYID123123 reverse resolve ANYID123123 will return xxxx.any  TODO: currently by default "true" bool updateReverseResolver = 4;



| # | 类型               | 字段          | 说明                                        |
| - | ---------------- | ----------- | ----------------------------------------- |
| 1 | `repeated bytes` | `payload`   | NameRegisterRequest struct                |
| 2 | `repeated bytes` | `signature` | payload signed by payload.ownerEthAddress |

#### `NameRenewRequest`



| # | 类型                | 字段                           | 说明                                                                                                                                                                                                     |
| - | ----------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1 | `repeated string` | `fullName`                   |                                                                                                                                                                                                        |
| 2 | `repeated string` | `ownerAnyAddress`            | A content hash attached to this name This should not be empty! in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 3 | `repeated string` | `ownerEthAddress`            | An Ethereum address that owns that name                                                                                                                                                                |
| 4 | `repeated bool`   | `renewToSmartContractWallet` | if false -> name ownership will belong to ownerEthAddress if true -> name ownership will belong to SCW of ownerEthAddress (AccountAbstraction)                                                         |
| 5 | `repeated uint32` | `renewPeriodMonths`          | How many months to register the name for                                                                                                                                                               |

#### `NameRenewRequestSigned`



| # | 类型               | 字段          | 说明                                        |
| - | ---------------- | ----------- | ----------------------------------------- |
| 1 | `repeated bytes` | `payload`   | NameRenewRequest struct                   |
| 2 | `repeated bytes` | `signature` | payload signed by payload.ownerEthAddress |

#### `OperationResponse`



| # | 类型                        | 字段               | 说明 |
| - | ------------------------- | ---------------- | -- |
| 1 | `repeated string`         | `operationId`    |    |
| 2 | `repeated OperationState` | `operationState` |    |

#### `UserAccount`



| # | 类型                | 字段                                | 说明                                                                                                                                                                            |
| - | ----------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `ownerEthAddress`                 | An Ethereum address that owns that account                                                                                                                                    |
| 2 | `repeated string` | `ownerSmartContracWalletAddress`  | This smart contract really controls all names you can ask .owner() method to get 'ownerEthAddress'                                                                            |
| 3 | `repeated bool`   | `ownerSmartContracWalletDeployed` | The ownerSmartContracWalletAddress field is calculated automatically from ownerEthAddress even if SCW is not deployed yet SCW is deployed automatically after first operation |
| 4 | `repeated uint64` | `namesCountLeft`                  | Number of names that the user can buy. We will mint him tokens that he can use to buy names (one token per name)                                                              |
| 5 | `repeated uint64` | `operationsCountLeft`             | Number of gas operations: update name, add new data, etc                                                                                                                      |

### any-sync/net/endtoendtest/testpeer/testproto/protos/testservice.proto

#### `StreamMessage`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `reqData` |    |
| 2 | `repeated int64`  | `repeat`  |    |
| 3 | `repeated int64`  | `n`       |    |

### any-sync/net/rpc/limiter/limiterproto/protos/limiter.proto

### any-sync/net/secureservice/handshake/handshakeproto/protos/handshake.proto

#### `Ack`



| # | 类型               | 字段      | 说明 |
| - | ---------------- | ------- | -- |
| 1 | `repeated Error` | `error` |    |

#### `Credentials`



| # | 类型                         | 字段              | 说明 |
| - | -------------------------- | --------------- | -- |
| 1 | `repeated CredentialsType` | `type`          |    |
| 2 | `repeated bytes`           | `payload`       |    |
| 3 | `repeated uint32`          | `version`       |    |
| 4 | `repeated string`          | `clientVersion` |    |

#### `PayloadSignedPeerIds`



| # | 类型               | 字段         | 说明                                   |
| - | ---------------- | ---------- | ------------------------------------ |
| 1 | `repeated bytes` | `identity` | account identity                     |
| 2 | `repeated bytes` | `sign`     | sign of (localPeerId + remotePeerId) |

#### `Proto`



| # | 类型                   | 字段          | 说明 |
| - | -------------------- | ----------- | -- |
| 1 | `repeated ProtoType` | `proto`     |    |
| 2 | `repeated Encoding`  | `encodings` |    |

### any-sync/net/streampool/testservice/protos/testservice.proto

#### `StreamMessage`



| # | 类型                | 字段        | 说明 |
| - | ----------------- | --------- | -- |
| 1 | `repeated string` | `reqData` |    |
| 2 | `repeated int64`  | `repeat`  |    |

### any-sync/paymentservice/paymentserviceproto/protos/paymentservice.proto

#### `BuySubscriptionRequest`



| # | 类型                       | 字段                 | 说明                                                                                                                                                                                                                                                                                |
| - | ------------------------ | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string`        | `ownerAnyId`       | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account()                                                                                                                                           |
| 2 | `repeated string`        | `ownerEthAddress`  | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |
| 3 | `repeated uint32`        | `requestedTier`    | was SubscriptionTier before, changed to uint32 to allow us to use dynamic tiers                                                                                                                                                                                                   |
| 4 | `repeated PaymentMethod` | `paymentMethod`    |                                                                                                                                                                                                                                                                                   |
| 5 | `repeated string`        | `requestedAnyName` | if empty - then no name requested if non-empty - PP node will register that name on behalf of the user                                                                                                                                                                            |
| 6 | `repeated string`        | `userEmail`        | for some payment methods we need to know the user's email                                                                                                                                                                                                                         |

#### `BuySubscriptionRequestSigned`



| # | 类型               | 字段          | 说明                                             |
| - | ---------------- | ----------- | ---------------------------------------------- |
| 1 | `repeated bytes` | `payload`   | BuySubscriptionRequest                         |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `BuySubscriptionResponse`



| # | 类型                | 字段           | 说明                                                                                                                     |
| - | ----------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `paymentUrl` | will feature current billing ID [stripe.com/?client\_reference\_id=1234](https://stripe.com/?client_reference_id=1234) |
| 2 | `repeated string` | `billingID`  | billingID is passed via mobile client to payment platform                                                              |

#### `CodeGetInfoRequest`



| # | 类型                | 字段                | 说明                                                                                                                                                                                                                                                                                |
| - | ----------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `ownerAnyId`      | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account()                                                                                                                                           |
| 2 | `repeated string` | `ownerEthAddress` | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |
| 3 | `repeated string` | `code`            | code received in the email                                                                                                                                                                                                                                                        |

#### `CodeGetInfoRequestSigned`



| # | 类型               | 字段          | 说明                                             |
| - | ---------------- | ----------- | ---------------------------------------------- |
| 1 | `repeated bytes` | `payload`   | CodeGetInfoRequest                             |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `CodeGetInfoResponse`



| # | 类型                | 字段     | 说明 |
| - | ----------------- | ------ | -- |
| 1 | `repeated uint32` | `tier` |    |

#### `CodeRedeemRequest`



| # | 类型                | 字段                 | 说明                                                                                                                                                                                                                                                                                |
| - | ----------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `ownerAnyId`       | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account()                                                                                                                                           |
| 2 | `repeated string` | `ownerEthAddress`  | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |
| 3 | `repeated string` | `requestedAnyName` | if empty - then no name requested                                                                                                                                                                                                                                                 |
| 4 | `repeated string` | `code`             | code received in the email                                                                                                                                                                                                                                                        |

#### `CodeRedeemRequestSigned`



| # | 类型               | 字段          | 说明                                             |
| - | ---------------- | ----------- | ---------------------------------------------- |
| 1 | `repeated bytes` | `payload`   | CodeRedeemRequest                              |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `CodeRedeemResponse`



| # | 类型              | 字段        | 说明 |
| - | --------------- | --------- | -- |
| 1 | `repeated bool` | `success` |    |

#### `FinalizeSubscriptionRequest`



| # | 类型                | 字段                 | 说明                                                                                                                                                                                                                                                                                |
| - | ----------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `ownerAnyId`       | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account()                                                                                                                                           |
| 2 | `repeated string` | `ownerEthAddress`  | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |
| 3 | `repeated string` | `requestedAnyName` | if empty - then no name requested                                                                                                                                                                                                                                                 |

#### `FinalizeSubscriptionRequestSigned`



| # | 类型               | 字段          | 说明                                             |
| - | ---------------- | ----------- | ---------------------------------------------- |
| 1 | `repeated bytes` | `payload`   | VerifyEmailRequest                             |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `FinalizeSubscriptionResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `GetSubscriptionPortalLinkRequest`



| # | 类型                | 字段           | 说明                                                                                                                                      |
| - | ----------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |

#### `GetSubscriptionPortalLinkRequestSigned`



| # | 类型               | 字段          | 说明                                             |
| - | ---------------- | ----------- | ---------------------------------------------- |
| 1 | `repeated bytes` | `payload`   | GetSubscriptionPortalLinkRequest               |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `GetSubscriptionPortalLinkResponse`



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated string` | `portalUrl` |    |

#### `GetSubscriptionRequest`



| # | 类型                | 字段           | 说明                                                                                                                                      |
| - | ----------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `ownerAnyID` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |

#### `GetSubscriptionRequestSigned`



| # | 类型               | 字段          | 说明                                             |
| - | ---------------- | ----------- | ---------------------------------------------- |
| 1 | `repeated bytes` | `payload`   | GetSubscriptionRequest                         |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `GetSubscriptionResponse`



| # | 类型                            | 字段                      | 说明                                                                                     |
| - | ----------------------------- | ----------------------- | -------------------------------------------------------------------------------------- |
| 1 | `repeated uint32`             | `tier`                  | was SubscriptionTier before, changed to uint32 to allow us to use dynamic tiers        |
| 2 | `repeated SubscriptionStatus` | `status`                |                                                                                        |
| 3 | `repeated uint64`             | `dateStarted`           |                                                                                        |
| 4 | `repeated uint64`             | `dateEnds`              |                                                                                        |
| 5 | `repeated bool`               | `isAutoRenew`           |                                                                                        |
| 6 | `repeated PaymentMethod`      | `paymentMethod`         |                                                                                        |
| 7 | `repeated string`             | `requestedAnyName`      |                                                                                        |
| 8 | `repeated string`             | `userEmail`             | if user verified her email OR provided it while buying a subscription, it will be here |
| 9 | `repeated bool`               | `subscribeToNewsletter` |                                                                                        |

#### `GetVerificationEmailRequest`



| # | 类型                | 字段                        | 说明                                                                                                                                      |
| - | ----------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `ownerAnyId`              | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 2 | `repeated string` | `email`                   |                                                                                                                                         |
| 3 | `repeated bool`   | `subscribeToNewsletter`   |                                                                                                                                         |
| 4 | `repeated bool`   | `insiderTipsAndTutorials` |                                                                                                                                         |
| 5 | `repeated bool`   | `isOnboardingList`        | if we are coming from the onboarding screen                                                                                             |

#### `GetVerificationEmailRequestSigned`



| # | 类型               | 字段          | 说明                                             |
| - | ---------------- | ----------- | ---------------------------------------------- |
| 1 | `repeated bytes` | `payload`   | GetVerificationEmailRequest                    |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `GetVerificationEmailResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `IsNameValidRequest`



| # | 类型                | 字段                 | 说明 |
| - | ----------------- | ------------------ | -- |
| 1 | `repeated uint32` | `requestedTier`    |    |
| 2 | `repeated string` | `requestedAnyName` |    |

#### `IsNameValidResponse`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated Code`   | `code`        |    |
| 2 | `repeated string` | `description` |    |

#### `VerifyAppStoreReceiptRequest`



| # | 类型                | 字段           | 说明                                                                                                                                      |
| - | ----------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 2 | `repeated string` | `receipt`    | receipt is a JWT-encoded information about subscription purchase                                                                        |

#### `VerifyAppStoreReceiptRequestSigned`



| # | 类型               | 字段          | 说明                                             |
| - | ---------------- | ----------- | ---------------------------------------------- |
| 1 | `repeated bytes` | `payload`   | VerifyAppStoreReceiptRequest                   |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `VerifyAppStoreReceiptResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `VerifyEmailRequest`



| # | 类型                | 字段                | 说明                                                                                                                                                                                                                                                                                |
| - | ----------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `ownerAnyId`      | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account()                                                                                                                                           |
| 2 | `repeated string` | `ownerEthAddress` | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |
| 3 | `repeated string` | `code`            | code received in the email                                                                                                                                                                                                                                                        |

#### `VerifyEmailRequestSigned`



| # | 类型               | 字段          | 说明                                             |
| - | ---------------- | ----------- | ---------------------------------------------- |
| 1 | `repeated bytes` | `payload`   | VerifyEmailRequest                             |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `VerifyEmailResponse`



| # | 类型              | 字段        | 说明 |
| - | --------------- | --------- | -- |
| 1 | `repeated bool` | `success` |    |

### any-sync/paymentservice/paymentserviceproto/protos/paymentservice2.proto

#### `MembershipV2`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `MembershipV2.Amount`



| # | 类型                | 字段            | 说明                                     |
| - | ----------------- | ------------- | -------------------------------------- |
| 1 | `repeated string` | `currency`    |                                        |
| 2 | `repeated int64`  | `amountCents` | $0.01 = 1 $1.00 = 100 negative amounts |

#### `MembershipV2.AnyNameAllocateRequest`



| # | 类型                | 字段                 | 说明                                                                                                                                                                                                                                                                                |
| - | ----------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `requestedAnyName` |                                                                                                                                                                                                                                                                                   |
| 2 | `repeated string` | `ownerEthAddress`  | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |

#### `MembershipV2.AnyNameAllocateResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `MembershipV2.AnyNameIsValidRequest`



| # | 类型                | 字段                 | 说明 |
| - | ----------------- | ------------------ | -- |
| 1 | `repeated string` | `requestedAnyName` |    |

#### `MembershipV2.AnyNameIsValidResponse`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated Code`   | `code`        |    |
| 2 | `repeated string` | `description` |    |

#### `MembershipV2.Cart`



| # | 类型                     | 字段                  | 说明                                                                                                                         |
| - | ---------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated CartProduct` | `products`          | if you add Nx the same product - it will be Nx in the 'products' array, i.e: each product instance has a unique index      |
| 2 | `repeated Amount`      | `total`             | total amount of the cart (including discounts, etc)                                                                        |
| 3 | `repeated Amount`      | `totalNextInvoice`  | in case you are paying in the middle of the period (for existing customers) the next invoice amount will also be generated |
| 4 | `repeated uint64`      | `nextInvoiceDate`   |                                                                                                                            |
| 5 | `repeated string`      | `appliedPromocodes` |                                                                                                                            |

#### `MembershipV2.CartProduct`



| # | 类型                 | 字段           | 说明                                                                                                                                                                                  |
| - | ------------------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated Product` | `product`    |                                                                                                                                                                                     |
| 2 | `repeated bool`    | `isYearly`   | otherwise - monthly or isLifetime                                                                                                                                                   |
| 3 | `repeated bool`    | `remove`     | set to true if you want to remove this item from the customer it's like setting -1 to some product                                                                                  |
| 4 | `repeated bool`    | `isLifetime` | if true - then this is lifetime product (no matter what isYearly above is) unfortunately we do not use Period here to keep compatibility with old versions that still use isYearly! |

#### `MembershipV2.CryptoCheckout`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `invoiceURL`  |    |
| 2 | `repeated Amount` | `total`       |    |
| 3 | `repeated bool`   | `isCanCancel` |    |

#### `MembershipV2.Features`



| # | 类型                | 字段              | 说明 |
| - | ----------------- | --------------- | -- |
| 1 | `repeated uint64` | `storageBytes`  |    |
| 2 | `repeated uint32` | `spaceReaders`  |    |
| 3 | `repeated uint32` | `spaceWriters`  |    |
| 4 | `repeated uint32` | `sharedSpaces`  |    |
| 5 | `repeated uint32` | `teamSeats`     |    |
| 6 | `repeated uint32` | `anyNameCount`  |    |
| 7 | `repeated uint32` | `anyNameMinLen` |    |

#### `MembershipV2.GetProductsRequest`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `MembershipV2.GetProductsResponse`



| # | 类型                 | 字段         | 说明 |
| - | ------------------ | ---------- | -- |
| 1 | `repeated Product` | `products` |    |

#### `MembershipV2.GetStatusRequest`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `MembershipV2.GetStatusResponse`



| # | 类型                                       | 字段                  | 说明                               |
| - | ---------------------------------------- | ------------------- | -------------------------------- |
| 1 | `repeated MembershipV2.PurchasedProduct` | `products`          |                                  |
| 2 | `repeated MembershipV2.Invoice`          | `nextInvoice`       |                                  |
| 3 | `repeated string`                        | `teamOwnerID`       |                                  |
| 4 | `repeated MembershipV2.PaymentProvider`  | `paymentProvider`   |                                  |
| 5 | `repeated string`                        | `appliedPromocodes` |                                  |
| 6 | `repeated MembershipV2.CryptoCheckout`   | `cryptoCheckout`    | if crypto checkout is in process |

#### `MembershipV2.Invoice`



| # | 类型                | 字段              | 说明                                                                                                                                                                                                                                                                                                                                                                      |
| - | ----------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `id`            |                                                                                                                                                                                                                                                                                                                                                                         |
| 2 | `repeated uint64` | `date`          |                                                                                                                                                                                                                                                                                                                                                                         |
| 3 | `repeated Amount` | `total`         |                                                                                                                                                                                                                                                                                                                                                                         |
| 4 | `repeated Status` | `status`        |                                                                                                                                                                                                                                                                                                                                                                         |
| 5 | `repeated string` | `paymentUrl`    | Stripe hosted-invoice payment page for an OPEN (unpaid) invoice the user must pay to keep access — set during the reverse-trial grace period. Empty when no action is required.                                                                                                                                                                                         |
| 6 | `repeated string` | `billingReason` | Stripe billing\_reason of the OPEN invoice this record describes, verbatim (e.g. "subscription\_cycle" for the first post-trial invoice, "subscription\_update"/"subscription\_threshold" for later renewal dunning). Lets a consumer tell a trial-ended grace invoice from a failed-renewal one exactly, instead of inferring it from period math. Empty when unknown. |

#### `MembershipV2.Product`



| #  | 类型                  | 字段               | 说明                                                                                                                                                                                                                                                                                                                                                                                             |
| -- | ------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | `repeated string`   | `id`             | this is a unique Payment Node ID adding 2 same products to a cart means we will have 2 items with same ID                                                                                                                                                                                                                                                                                      |
| 2  | `repeated string`   | `name`           |                                                                                                                                                                                                                                                                                                                                                                                                |
| 3  | `repeated string`   | `description`    |                                                                                                                                                                                                                                                                                                                                                                                                |
| 4  | `repeated bool`     | `isTopLevel`     |                                                                                                                                                                                                                                                                                                                                                                                                |
| 5  | `repeated bool`     | `isHidden`       |                                                                                                                                                                                                                                                                                                                                                                                                |
| 6  | `repeated bool`     | `isIntro`        | isIntro flag can be used as follows:  1. if current user's top level product has isIntro flag -> then you'd rather show a FULL list of all products to enable upgrading from CURRENT product 2. but if current user's top level product has no isIntro flag -> then it means that this plan was aquired and user need to control it. then show "second screen" to control that product instead |
| 7  | `repeated bool`     | `isUpgradeable`  | isUpgradeable can be used as follows:  if current user's top level product has isUpgradeable flag -> show incentives to buy something else                                                                                                                                                                                                                                                     |
| 8  | `repeated Amount`   | `pricesYearly`   |                                                                                                                                                                                                                                                                                                                                                                                                |
| 9  | `repeated Amount`   | `pricesMonthly`  |                                                                                                                                                                                                                                                                                                                                                                                                |
| 10 | `repeated string`   | `colorStr`       | green, blue, red, purple, custom, etc                                                                                                                                                                                                                                                                                                                                                          |
| 11 | `repeated string`   | `offer`          |                                                                                                                                                                                                                                                                                                                                                                                                |
| 12 | `repeated Features` | `features`       |                                                                                                                                                                                                                                                                                                                                                                                                |
| 13 | `repeated Amount`   | `pricesLifetime` |                                                                                                                                                                                                                                                                                                                                                                                                |

#### `MembershipV2.ProductStatus`



| # | 类型                | 字段       | 说明 |
| - | ----------------- | -------- | -- |
| 1 | `repeated Status` | `status` |    |

#### `MembershipV2.PurchaseInfo`



| # | 类型                | 字段              | 说明                                                                                                                               |
| - | ----------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated uint64` | `dateStarted`   |                                                                                                                                  |
| 2 | `repeated uint64` | `dateEnds`      |                                                                                                                                  |
| 3 | `repeated bool`   | `isAutoRenew`   |                                                                                                                                  |
| 4 | `repeated Period` | `period`        |                                                                                                                                  |
| 5 | `repeated uint64` | `dateTrialEnds` | 0 = not in a trial. Otherwise the Unix timestamp when the free trial ends, which is also when the first real invoice is charged. |

#### `MembershipV2.PurchasedProduct`



| # | 类型                       | 字段              | 说明 |
| - | ------------------------ | --------------- | -- |
| 1 | `repeated Product`       | `product`       |    |
| 2 | `repeated PurchaseInfo`  | `purchaseInfo`  |    |
| 3 | `repeated ProductStatus` | `productStatus` |    |

#### `MembershipV2.StoreCartCheckoutRequest`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `MembershipV2.StoreCartCheckoutResponse`



| # | 类型                | 字段           | 说明                                                                                                                                                              |
| - | ----------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `paymentUrl` | for new customers - will contain a payment URL (new Stripe session)  if this is empty - then this is existing customer and we are trying to process the payment |

#### `MembershipV2.StoreCartClearRequest`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `MembershipV2.StoreCartGetRequest`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `MembershipV2.StoreCartGetResponse`



| # | 类型                           | 字段     | 说明 |
| - | ---------------------------- | ------ | -- |
| 1 | `repeated MembershipV2.Cart` | `cart` |    |

#### `MembershipV2.StoreCartPromocodeApplyRequest`



| # | 类型                | 字段          | 说明 |
| - | ----------------- | ----------- | -- |
| 1 | `repeated string` | `promocode` |    |

#### `MembershipV2.StoreCartUpdateRequest`



| # | 类型                     | 字段                | 说明 |
| - | ---------------------- | ----------------- | -- |
| 1 | `repeated CartProduct` | `products`        |    |
| 2 | `repeated string`      | `ownerEthAddress` |    |
| 3 | `repeated string`      | `promocodes`      |    |

#### `MembershipV2.StoreCartUpdateResponse`



| # | 类型                           | 字段     | 说明 |
| - | ---------------------------- | ------ | -- |
| 1 | `repeated MembershipV2.Cart` | `cart` |    |

#### `MembershipV2.SubscribeToUpdatesRequest`



| # | 类型                  | 字段          | 说明                     |
| - | ------------------- | ----------- | ---------------------- |
| 1 | `repeated string`   | `email`     |                        |
| 2 | `repeated Platform` | `platform`  |                        |
| 3 | `repeated bool`     | `subscribe` | if false - unsubscribe |
| 4 | `repeated string`   | `context`   | additional data        |

#### `MembershipV2.SubscribeToUpdatesResponse`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `MembershipV2.WebAuthRequest`



| # | 类型 | 字段 | 说明 |
| - | -- | -- | -- |

#### `MembershipV2.WebAuthResponse`



| # | 类型                | 字段    | 说明                                      |
| - | ----------------- | ----- | --------------------------------------- |
| 1 | `repeated string` | `jwt` |                                         |
| 2 | `repeated string` | `url` | (optional) redirect here after the auth |

### any-sync/paymentservice/paymentserviceproto/protos/paymentservice\_tiers.proto

#### `Feature`



| # | 类型                | 字段            | 说明 |
| - | ----------------- | ------------- | -- |
| 1 | `repeated string` | `description` |    |

#### `GetTiersRequest`



| # | 类型                | 字段           | 说明                                                                                                                                      |
| - | ----------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 2 | `repeated string` | `locale`     |                                                                                                                                         |
| 3 | `repeated string` | `version`    |                                                                                                                                         |

#### `GetTiersRequestSigned`



| # | 类型               | 字段          | 说明                                             |
| - | ---------------- | ----------- | ---------------------------------------------- |
| 1 | `repeated bytes` | `payload`   | GetTiersRequest struct                         |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `GetTiersResponse`



| # | 类型                  | 字段      | 说明                          |
| - | ------------------- | ------- | --------------------------- |
| 1 | `repeated TierData` | `tiers` | list of all available tiers |

#### `TierData`



| #  | 类型                    | 字段                      | 说明                                                                                                                                                                 |
| -- | --------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1  | `repeated uint32`     | `id`                    | this is a unique ID of the tier you should hardcode this in your app and provide icon, graphics, etc for each tier (even for old/historical/inactive/hidden tiers) |
| 2  | `repeated string`     | `name`                  | localazied name of the tier                                                                                                                                        |
| 3  | `repeated string`     | `description`           | just a short technical description you don't have to use it, you can use your own UI-friendly texts                                                                |
| 4  | `repeated bool`       | `isActive`              | can you buy it (ON ALL PLATFORMS, without clarification)?                                                                                                          |
| 5  | `repeated bool`       | `isTest`                | is this tier for debugging only?                                                                                                                                   |
| 6  | `repeated bool`       | `isHiddenTier`          | hidden tiers are only visible once user got them                                                                                                                   |
| 7  | `repeated PeriodType` | `periodType`            | how long is the period of the subscription                                                                                                                         |
| 8  | `repeated uint32`     | `periodValue`           | i.e. "5 days" or "3 years"                                                                                                                                         |
| 9  | `repeated uint32`     | `priceStripeUsdCents`   | this one is a price we use ONLY on Stripe platform                                                                                                                 |
| 10 | `repeated uint32`     | `anyNamesCountIncluded` | number of ANY NS names that this tier includes (not counted as a "feature" and not in the features list)                                                           |
| 11 | `repeated uint32`     | `anyNameMinLength`      | somename.any - len of 8                                                                                                                                            |
| 12 | `repeated Feature`    | `features`              | each tier has a set of features                                                                                                                                    |
| 13 | `repeated string`     | `colorStr`              | green, blue, red, purple or custom color in string format #ff00ff                                                                                                  |
| 14 | `repeated string`     | `stripeProductId`       | Stripe platform-specific data:                                                                                                                                     |
| 15 | `repeated string`     | `stripeManageUrl`       |                                                                                                                                                                    |
| 16 | `repeated string`     | `iosProductId`          | iOS platform-specific data:                                                                                                                                        |
| 17 | `repeated string`     | `iosManageUrl`          |                                                                                                                                                                    |
| 18 | `repeated string`     | `androidProductId`      | Android platform-specific data:                                                                                                                                    |
| 19 | `repeated string`     | `androidManageUrl`      |                                                                                                                                                                    |
| 20 | `repeated string`     | `offer`                 | something like "limited offer", etc                                                                                                                                |

### any-sync/util/crypto/cryptoproto/protos/crypto.proto

#### `Key`



| # | 类型                 | 字段     | 说明 |
| - | ------------------ | ------ | -- |
| 1 | `repeated KeyType` | `Type` |    |
| 2 | `repeated bytes`   | `Data` |    |

## 四、枚举

> 按文件分组；嵌套枚举用点路径表示。

### any-block/format/v1/proto/changes.proto

#### `ModifyOp`



| 值          | 编号 |
| ---------- | -- |
| `Set`      | 0  |
| `Unset`    | 1  |
| `Inc`      | 2  |
| `AddToSet` | 3  |
| `Pull`     | 4  |

### any-block/format/v1/proto/events.proto

#### `Event.Block.Dataview.SliceOperation`



| 值                       | 编号 |
| ----------------------- | -- |
| `SliceOperationNone`    | 0  |
| `SliceOperationAdd`     | 1  |
| `SliceOperationMove`    | 2  |
| `SliceOperationRemove`  | 3  |
| `SliceOperationReplace` | 4  |

#### `Event.Object.CleanupSuggestion.Trigger`



| 值             | 编号 |
| ------------- | -- |
| `archive`     | 0  |
| `delete`      | 1  |
| `linkRemoval` | 2  |

#### `Event.P2PStatus.Status`



| 值              | 编号 |
| -------------- | -- |
| `NotConnected` | 0  |
| `NotPossible`  | 1  |
| `Connected`    | 2  |
| `Restricted`   | 3  |

#### `Event.Space.Network`



| 值           | 编号 |
| ----------- | -- |
| `Anytype`   | 0  |
| `SelfHost`  | 1  |
| `LocalOnly` | 2  |

#### `Event.Space.Status`



| 值                    | 编号 |
| -------------------- | -- |
| `Synced`             | 0  |
| `Syncing`            | 1  |
| `Error`              | 2  |
| `Offline`            | 3  |
| `NetworkNeedsUpdate` | 4  |

#### `Event.Space.SyncError`



| 值                     | 编号 |
| --------------------- | -- |
| `Null`                | 0  |
| `StorageLimitExceed`  | 1  |
| `IncompatibleVersion` | 2  |
| `NetworkError`        | 3  |

#### `Event.Status.Thread.SyncStatus`



| 值                     | 编号 |
| --------------------- | -- |
| `Unknown`             | 0  |
| `Offline`             | 1  |
| `Syncing`             | 2  |
| `Synced`              | 3  |
| `Failed`              | 4  |
| `IncompatibleVersion` | 5  |
| `NetworkNeedsUpdate`  | 6  |

#### `Model.Process.State`



| 值          | 编号 |
| ---------- | -- |
| `None`     | 0  |
| `Running`  | 1  |
| `Done`     | 2  |
| `Canceled` | 3  |
| `Error`    | 4  |

### any-block/format/v1/proto/models.proto

#### `Account.Auth.LocalApiScope`



| 值         | 编号 |
| --------- | -- |
| `Limited` | 0  |
| `JsonAPI` | 1  |
| `Full`    | 2  |

#### `Account.StatusType`



| 值                 | 编号 |
| ----------------- | -- |
| `Active`          | 0  |
| `PendingDeletion` | 1  |
| `StartedDeletion` | 2  |
| `Deleted`         | 3  |

#### `Block.Align`



| 值              | 编号 |
| -------------- | -- |
| `AlignLeft`    | 0  |
| `AlignCenter`  | 1  |
| `AlignRight`   | 2  |
| `AlignJustify` | 3  |

#### `Block.Content.Bookmark.State`



| 值          | 编号 |
| ---------- | -- |
| `Empty`    | 0  |
| `Fetching` | 1  |
| `Done`     | 2  |
| `Error`    | 3  |

#### `Block.Content.Dataview.Filter.Condition`



| 值                | 编号 |
| ---------------- | -- |
| `None`           | 0  |
| `Equal`          | 1  |
| `NotEqual`       | 2  |
| `Greater`        | 3  |
| `Less`           | 4  |
| `GreaterOrEqual` | 5  |
| `LessOrEqual`    | 6  |
| `Like`           | 7  |
| `NotLike`        | 8  |
| `In`             | 9  |
| `NotIn`          | 10 |
| `Empty`          | 11 |
| `NotEmpty`       | 12 |
| `AllIn`          | 13 |
| `NotAllIn`       | 14 |
| `ExactIn`        | 15 |
| `NotExactIn`     | 16 |
| `Exists`         | 17 |

#### `Block.Content.Dataview.Filter.Operator`



| 值     | 编号 |
| ----- | -- |
| `No`  | 0  |
| `Or`  | 1  |
| `And` | 2  |

#### `Block.Content.Dataview.Filter.QuickOption`



| 值                 | 编号 |
| ----------------- | -- |
| `ExactDate`       | 0  |
| `Yesterday`       | 1  |
| `Today`           | 2  |
| `Tomorrow`        | 3  |
| `LastWeek`        | 4  |
| `CurrentWeek`     | 5  |
| `NextWeek`        | 6  |
| `LastMonth`       | 7  |
| `CurrentMonth`    | 8  |
| `NextMonth`       | 9  |
| `NumberOfDaysAgo` | 10 |
| `NumberOfDaysNow` | 11 |
| `LastYear`        | 12 |
| `CurrentYear`     | 13 |
| `NextYear`        | 14 |

#### `Block.Content.Dataview.Relation.DateFormat`



| 值                    | 编号 |
| -------------------- | -- |
| `MonthAbbrBeforeDay` | 0  |
| `MonthAbbrAfterDay`  | 1  |
| `Short`              | 2  |
| `ShortUS`            | 3  |
| `ISO`                | 4  |

#### `Block.Content.Dataview.Relation.FormulaType`



| 值                 | 编号 |
| ----------------- | -- |
| `None`            | 0  |
| `Count`           | 1  |
| `CountValue`      | 2  |
| `CountDistinct`   | 3  |
| `CountEmpty`      | 4  |
| `CountNotEmpty`   | 5  |
| `PercentEmpty`    | 6  |
| `PercentNotEmpty` | 7  |
| `MathSum`         | 8  |
| `MathAverage`     | 9  |
| `MathMedian`      | 10 |
| `MathMin`         | 11 |
| `MathMax`         | 12 |
| `Range`           | 13 |

#### `Block.Content.Dataview.Relation.TimeFormat`



| 值          | 编号 |
| ---------- | -- |
| `Format12` | 0  |
| `Format24` | 1  |

#### `Block.Content.Dataview.Sort.EmptyType`



| 值              | 编号 |
| -------------- | -- |
| `NotSpecified` | 0  |
| `Start`        | 1  |
| `End`          | 2  |

#### `Block.Content.Dataview.Sort.Type`



| 值        | 编号 |
| -------- | -- |
| `Asc`    | 0  |
| `Desc`   | 1  |
| `Custom` | 2  |

#### `Block.Content.Dataview.View.ListSize`



| 值         | 编号 |
| --------- | -- |
| `Compact` | 0  |
| `Regular` | 1  |

#### `Block.Content.Dataview.View.Size`



| 值        | 编号 |
| -------- | -- |
| `Small`  | 0  |
| `Medium` | 1  |
| `Large`  | 2  |

#### `Block.Content.Dataview.View.Type`



| 值          | 编号 |
| ---------- | -- |
| `Table`    | 0  |
| `List`     | 1  |
| `Gallery`  | 2  |
| `Kanban`   | 3  |
| `Calendar` | 4  |
| `Graph`    | 5  |

#### `Block.Content.Div.Style`



| 值      | 编号 |
| ------ | -- |
| `Line` | 0  |
| `Dots` | 1  |

#### `Block.Content.File.State`



| 值           | 编号 |
| ----------- | -- |
| `Empty`     | 0  |
| `Uploading` | 1  |
| `Done`      | 2  |
| `Error`     | 3  |

#### `Block.Content.File.Style`



| 值       | 编号 |
| ------- | -- |
| `Auto`  | 0  |
| `Link`  | 1  |
| `Embed` | 2  |

#### `Block.Content.File.Type`



| 值       | 编号 |
| ------- | -- |
| `None`  | 0  |
| `File`  | 1  |
| `Image` | 2  |
| `Video` | 3  |
| `Audio` | 4  |
| `PDF`   | 5  |

#### `Block.Content.Latex.Processor`



| 值               | 编号 |
| --------------- | -- |
| `Latex`         | 0  |
| `Mermaid`       | 1  |
| `Chart`         | 2  |
| `Youtube`       | 3  |
| `Vimeo`         | 4  |
| `Soundcloud`    | 5  |
| `GoogleMaps`    | 6  |
| `Miro`          | 7  |
| `Figma`         | 8  |
| `Twitter`       | 9  |
| `OpenStreetMap` | 10 |
| `Reddit`        | 11 |
| `Facebook`      | 12 |
| `Instagram`     | 13 |
| `Telegram`      | 14 |
| `GithubGist`    | 15 |
| `Codepen`       | 16 |
| `Bilibili`      | 17 |
| `Excalidraw`    | 18 |
| `Kroki`         | 19 |
| `Graphviz`      | 20 |
| `Sketchfab`     | 21 |
| `Image`         | 22 |
| `Drawio`        | 23 |
| `Spotify`       | 24 |

#### `Block.Content.Layout.Style`



| 值              | 编号 |
| -------------- | -- |
| `Row`          | 0  |
| `Column`       | 1  |
| `Div`          | 2  |
| `Header`       | 3  |
| `TableRows`    | 4  |
| `TableColumns` | 5  |

#### `Block.Content.Link.CardStyle`



| 值        | 编号 |
| -------- | -- |
| `Text`   | 0  |
| `Card`   | 1  |
| `Inline` | 2  |

#### `Block.Content.Link.Description`



| 值         | 编号 |
| --------- | -- |
| `None`    | 0  |
| `Added`   | 1  |
| `Content` | 2  |

#### `Block.Content.Link.IconSize`



| 值            | 编号 |
| ------------ | -- |
| `SizeNone`   | 0  |
| `SizeSmall`  | 1  |
| `SizeMedium` | 2  |

#### `Block.Content.Link.Style`



| 值           | 编号 |
| ----------- | -- |
| `Page`      | 0  |
| `Dataview`  | 1  |
| `Dashboard` | 2  |
| `Archive`   | 3  |

#### `Block.Content.Text.Mark.Type`



| 值                 | 编号 |
| ----------------- | -- |
| `Strikethrough`   | 0  |
| `Keyboard`        | 1  |
| `Italic`          | 2  |
| `Bold`            | 3  |
| `Underscored`     | 4  |
| `Link`            | 5  |
| `TextColor`       | 6  |
| `BackgroundColor` | 7  |
| `Mention`         | 8  |
| `Emoji`           | 9  |
| `Object`          | 10 |

#### `Block.Content.Text.Style`



| 值               | 编号 |
| --------------- | -- |
| `Paragraph`     | 0  |
| `Header1`       | 1  |
| `Header2`       | 2  |
| `Header3`       | 3  |
| `Header4`       | 4  |
| `Quote`         | 5  |
| `Code`          | 6  |
| `Title`         | 7  |
| `Checkbox`      | 8  |
| `Marked`        | 9  |
| `Numbered`      | 10 |
| `Toggle`        | 11 |
| `Description`   | 12 |
| `Callout`       | 13 |
| `ToggleHeader1` | 14 |
| `ToggleHeader2` | 15 |
| `ToggleHeader3` | 16 |

#### `Block.Content.Widget.Layout`



| 值             | 编号 |
| ------------- | -- |
| `Link`        | 0  |
| `Tree`        | 1  |
| `List`        | 2  |
| `CompactList` | 3  |
| `View`        | 4  |

#### `Block.Position`



| 值            | 编号 |
| ------------ | -- |
| `None`       | 0  |
| `Top`        | 1  |
| `Bottom`     | 2  |
| `Left`       | 3  |
| `Right`      | 4  |
| `Inner`      | 5  |
| `Replace`    | 6  |
| `InnerFirst` | 7  |

#### `Block.VerticalAlign`



| 值                     | 编号 |
| --------------------- | -- |
| `VerticalAlignTop`    | 0  |
| `VerticalAlignMiddle` | 1  |
| `VerticalAlignBottom` | 2  |

#### `ChatMessage.Attachment.AttachmentType`



| 值       | 编号 |
| ------- | -- |
| `FILE`  | 0  |
| `IMAGE` | 1  |
| `LINK`  | 2  |

#### `ChatMessage.MessageBlockLink.LinkType`



| 值          | 编号 |
| ---------- | -- |
| `Object`   | 0  |
| `File`     | 1  |
| `Image`    | 2  |
| `Bookmark` | 3  |

#### `DeviceNetworkType`



| 值               | 编号 |
| --------------- | -- |
| `WIFI`          | 0  |
| `CELLULAR`      | 1  |
| `NOT_CONNECTED` | 2  |

#### `Export.Format`



| 值            | 编号 |
| ------------ | -- |
| `Markdown`   | 0  |
| `Protobuf`   | 1  |
| `JSON`       | 2  |
| `DOT`        | 3  |
| `SVG`        | 4  |
| `GRAPH_JSON` | 5  |
| `AnyBlockV2` | 6  |

#### `FileIndexingStatus`



| 值            | 编号 |
| ------------ | -- |
| `NotIndexed` | 0  |
| `Indexed`    | 1  |
| `NotFound`   | 2  |

#### `ImageKind`



| 值                    | 编号 |
| -------------------- | -- |
| `Basic`              | 0  |
| `Cover`              | 1  |
| `Icon`               | 2  |
| `AutomaticallyAdded` | 3  |

#### `Import.ErrorCode`



| 值                                         | 编号 |
| ----------------------------------------- | -- |
| `NULL`                                    | 0  |
| `UNKNOWN_ERROR`                           | 1  |
| `BAD_INPUT`                               | 2  |
| `INTERNAL_ERROR`                          | 3  |
| `FILE_LOAD_ERROR`                         | 8  |
| `IMPORT_IS_CANCELED`                      | 6  |
| `NOTION_NO_OBJECTS_IN_INTEGRATION`        | 5  |
| `NOTION_SERVER_IS_UNAVAILABLE`            | 12 |
| `NOTION_RATE_LIMIT_EXCEEDED`              | 13 |
| `FILE_IMPORT_NO_OBJECTS_IN_ZIP_ARCHIVE`   | 14 |
| `FILE_IMPORT_NO_OBJECTS_IN_DIRECTORY`     | 17 |
| `HTML_WRONG_HTML_STRUCTURE`               | 10 |
| `PB_NOT_ANYBLOCK_FORMAT`                  | 11 |
| `CSV_LIMIT_OF_ROWS_OR_RELATIONS_EXCEEDED` | 7  |
| `INSUFFICIENT_PERMISSIONS`                | 9  |

#### `Import.Type`



| 值          | 编号 |
| ---------- | -- |
| `Notion`   | 0  |
| `Markdown` | 1  |
| `External` | 2  |
| `Pb`       | 3  |
| `Html`     | 4  |
| `Txt`      | 5  |
| `Csv`      | 6  |
| `Obsidian` | 7  |

#### `InternalFlag.Value`

> Use such a weird construction due to the issue with imported repeated enum type Look 
>
> [https://github.com/golang/protobuf/issues/1135](https://github.com/golang/protobuf/issues/1135)
>
>  for more information.



| 值                          | 编号 |
| -------------------------- | -- |
| `editorDeleteEmpty`        | 0  |
| `editorSelectType`         | 1  |
| `editorSelectTemplate`     | 2  |
| `collectionDontIndexLinks` | 3  |

#### `InviteType`



| 值                | 编号 |
| ---------------- | -- |
| `Member`         | 0  |
| `Guest`          | 1  |
| `WithoutApprove` | 2  |

#### `LinkPreview.Type`



| 值         | 编号 |
| --------- | -- |
| `Unknown` | 0  |
| `Page`    | 1  |
| `Image`   | 2  |
| `Text`    | 3  |

#### `Membership.EmailVerificationStatus`



| 值                   | 编号 |
| ------------------- | -- |
| `StatusNotVerified` | 0  |
| `StatusCodeSent`    | 1  |
| `StatusVerified`    | 2  |

#### `Membership.PaymentMethod`



| 值                   | 编号 |
| ------------------- | -- |
| `MethodNone`        | 0  |
| `MethodStripe`      | 1  |
| `MethodCrypto`      | 2  |
| `MethodInappApple`  | 3  |
| `MethodInappGoogle` | 4  |

#### `Membership.Status`



| 值                                   | 编号 |
| ----------------------------------- | -- |
| `StatusUnknown`                     | 0  |
| `StatusPending`                     | 1  |
| `StatusActive`                      | 2  |
| `StatusPendingRequiresFinalization` | 3  |

#### `MembershipTierData.PeriodType`



| 值                     | 编号 |
| --------------------- | -- |
| `PeriodTypeUnknown`   | 0  |
| `PeriodTypeUnlimited` | 1  |
| `PeriodTypeDays`      | 2  |
| `PeriodTypeWeeks`     | 3  |
| `PeriodTypeMonths`    | 4  |
| `PeriodTypeYears`     | 5  |

#### `MembershipV2.PaymentProvider`



| 值               | 编号 |
| --------------- | -- |
| `None`          | 0  |
| `Stripe`        | 1  |
| `Crypto`        | 2  |
| `BillingPortal` | 3  |
| `AppStore`      | 4  |
| `GooglePlay`    | 5  |

#### `MembershipV2.Period`



| 值            | 编号 |
| ------------ | -- |
| `Monthly`    | 1  |
| `Yearly`     | 2  |
| `ThreeYears` | 3  |
| `Lifetime`   | 4  |

#### `MembershipV2.Platform`



| 值               | 编号 |
| --------------- | -- |
| `Unknown`       | 0  |
| `Desktop`       | 1  |
| `MobileIOS`     | 2  |
| `MobileAndroid` | 3  |
| `Web`           | 4  |

#### `MembershipV2.ProductStatus.Status`



| 值                                        | 编号 |
| ---------------------------------------- | -- |
| `StatusUnknown`                          | 0  |
| `StatusPending`                          | 1  |
| `StatusActive`                           | 2  |
| `StatusPendingRequiresAnyNameAllocation` | 3  |

#### `NameserviceNameType`



| 值         | 编号 |
| --------- | -- |
| `AnyName` | 0  |

#### `Notification.ActionType`



| 值       | 编号 |
| ------- | -- |
| `CLOSE` | 0  |

#### `Notification.Export.Code`



| 值               | 编号 |
| --------------- | -- |
| `NULL`          | 0  |
| `UNKNOWN_ERROR` | 1  |
| `BAD_INPUT`     | 2  |

#### `Notification.Status`



| 值         | 编号 |
| --------- | -- |
| `Created` | 0  |
| `Shown`   | 1  |
| `Read`    | 2  |
| `Replied` | 3  |

#### `ObjectOrigin`



| 值                  | 编号 |
| ------------------ | -- |
| `none`             | 0  |
| `clipboard`        | 1  |
| `dragAndDrop`      | 2  |
| `import`           | 3  |
| `webclipper`       | 4  |
| `sharingExtension` | 5  |
| `usecase`          | 6  |
| `builtin`          | 7  |
| `bookmark`         | 8  |
| `api`              | 9  |

#### `ObjectType.Layout`



| 值                     | 编号 |
| --------------------- | -- |
| `basic`               | 0  |
| `profile`             | 1  |
| `todo`                | 2  |
| `set`                 | 3  |
| `objectType`          | 4  |
| `relation`            | 5  |
| `file`                | 6  |
| `dashboard`           | 7  |
| `image`               | 8  |
| `note`                | 9  |
| `space`               | 10 |
| `bookmark`            | 11 |
| `relationOptionsList` | 12 |
| `relationOption`      | 13 |
| `collection`          | 14 |
| `audio`               | 15 |
| `video`               | 16 |
| `date`                | 17 |
| `spaceView`           | 18 |
| `participant`         | 19 |
| `pdf`                 | 20 |
| `chatDeprecated`      | 21 |
| `chatDerived`         | 22 |
| `tag`                 | 23 |
| `notification`        | 24 |
| `missingObject`       | 25 |
| `devices`             | 26 |
| `discussion`          | 27 |

#### `ParticipantPermissions`



| 值               | 编号 |
| --------------- | -- |
| `Reader`        | 0  |
| `Writer`        | 1  |
| `Owner`         | 2  |
| `NoPermissions` | 3  |
| `Admin`         | 4  |

#### `ParticipantStatus`



| 值          | 编号 |
| ---------- | -- |
| `Joining`  | 0  |
| `Active`   | 1  |
| `Removed`  | 2  |
| `Declined` | 3  |
| `Removing` | 4  |
| `Canceled` | 5  |

#### `Placeholder.Type`



| 值                        | 编号 |
| ------------------------ | -- |
| `PlaceholderValue`       | 0  |
| `PlaceholderToday`       | 1  |
| `PlaceholderCurrentUser` | 2  |

#### `Relation.DataSource`



| 值         | 编号 |
| --------- | -- |
| `details` | 0  |
| `derived` | 1  |
| `account` | 2  |
| `local`   | 3  |

#### `Relation.Scope`



| 值                      | 编号 |
| ---------------------- | -- |
| `object`               | 0  |
| `type`                 | 1  |
| `setOfTheSameType`     | 2  |
| `objectsOfTheSameType` | 3  |
| `library`              | 4  |

#### `RelationFormat`

> RelationFormat describes how the underlying data is stored in the google.protobuf.Value and how it should be validated/sanitized



| 值           | 编号  |
| ----------- | --- |
| `longtext`  | 0   |
| `shorttext` | 1   |
| `number`    | 2   |
| `status`    | 3   |
| `tag`       | 11  |
| `date`      | 4   |
| `file`      | 5   |
| `checkbox`  | 6   |
| `url`       | 7   |
| `email`     | 8   |
| `phone`     | 9   |
| `emoji`     | 10  |
| `object`    | 100 |
| `relations` | 101 |
| `map`       | 102 |

#### `Restrictions.DataviewRestriction`



| 值                | 编号 |
| ---------------- | -- |
| `DVNone`         | 0  |
| `DVRelation`     | 1  |
| `DVCreateObject` | 2  |
| `DVViews`        | 3  |

#### `Restrictions.ObjectRestriction`



| 值                        | 编号 |
| ------------------------ | -- |
| `None`                   | 0  |
| `Delete`                 | 1  |
| `Relations`              | 2  |
| `Blocks`                 | 3  |
| `Details`                | 4  |
| `TypeChange`             | 5  |
| `LayoutChange`           | 6  |
| `Template`               | 7  |
| `Duplicate`              | 8  |
| `CreateObjectOfThisType` | 9  |
| `Publish`                | 10 |

#### `Search.Message.Sort.Key`



| 值             | 编号 |
| ------------- | -- |
| `ORDER_ID`    | 0  |
| `SCORE`       | 1  |
| `CREATED_AT`  | 2  |
| `MODIFIED_AT` | 3  |

#### `Search.Message.Sort.Type`



| 值      | 编号 |
| ------ | -- |
| `Asc`  | 0  |
| `Desc` | 1  |

#### `SmartBlockType`



| 值            | 编号 |
| ------------ | -- |
| `AccountOld` | 0  |

#### `SpaceAccessType`



| 值          | 编号 |
| ---------- | -- |
| `Private`  | 0  |
| `Personal` | 1  |
| `Shared`   | 2  |

#### `SpaceShareableStatus`



| 值                    | 编号 |
| -------------------- | -- |
| `StatusUnknown`      | 0  |
| `StatusShareable`    | 1  |
| `StatusNotShareable` | 2  |

#### `SpaceStatus`



| 值                       | 编号 |
| ----------------------- | -- |
| `Unknown`               | 0  |
| `Loading`               | 1  |
| `Ok`                    | 2  |
| `Missing`               | 3  |
| `Error`                 | 4  |
| `RemoteWaitingDeletion` | 5  |
| `RemoteDeleted`         | 6  |
| `SpaceDeleted`          | 7  |
| `SpaceActive`           | 8  |
| `SpaceJoining`          | 9  |
| `SpaceRemoving`         | 10 |

#### `SpaceType`



| 值                   | 编号 |
| ------------------- | -- |
| `SpaceTypeUnknown`  | 0  |
| `SpaceTypeRegular`  | 1  |
| `SpaceTypeTech`     | 2  |
| `SpaceTypeChat`     | 3  |
| `SpaceTypeOneToOne` | 4  |

#### `SpaceUxType`



| 值          | 编号 |
| ---------- | -- |
| `None`     | 0  |
| `Data`     | 1  |
| `Stream`   | 2  |
| `Chat`     | 3  |
| `OneToOne` | 4  |

#### `SyncError`



| 值                              | 编号 |
| ------------------------------ | -- |
| `SyncErrorNull`                | 0  |
| `SyncErrorIncompatibleVersion` | 2  |
| `SyncErrorNetworkError`        | 3  |
| `SyncErrorOversized`           | 4  |

#### `SyncStatus`



| 值                   | 编号 |
| ------------------- | -- |
| `SyncStatusSynced`  | 0  |
| `SyncStatusSyncing` | 1  |
| `SyncStatusError`   | 2  |
| `SyncStatusQueued`  | 3  |

#### `TemplateNamePrefillType`



| 值                  | 编号 |
| ------------------ | -- |
| `Empty`            | 0  |
| `FromTemplateName` | 1  |

### any-sync-node/nodesync/nodesyncproto/protos/nodesync.proto

#### `AdoptArchiveResult`



| 值                                 | 编号 |
| --------------------------------- | -- |
| `AdoptArchiveOk`                  | 0  |
| `AdoptArchiveAlreadyHaveSame`     | 1  |
| `AdoptArchiveAlreadyHaveDiverged` | 2  |

#### `ColdSyncProtocolType`



| 值                | 编号 |
| ---------------- | -- |
| `Pogreb`         | 0  |
| `AnystoreSqlite` | 1  |

#### `ErrCodes`



| 值                      | 编号   |
| ---------------------- | ---- |
| `Unexpected`           | 0    |
| `ExpectedCoordinator`  | 1    |
| `UnsupportedStorage`   | 2    |
| `SpaceDeleted`         | 3    |
| `ArchiveUnavailable`   | 4    |
| `ArchiveObjectMissing` | 5    |
| `PeerIsNotNode`        | 6    |
| `NotResponsible`       | 7    |
| `SpacePendingDeletion` | 8    |
| `ErrorOffset`          | 1000 |

### any-sync/commonfile/fileproto/filep2p/protos/filep2p.proto

#### `Availability`



| 值         | 编号 |
| --------- | -- |
| `None`    | 0  |
| `Partial` | 1  |
| `Full`    | 2  |

#### `ErrCodes`

> ErrCodes are WHOLE-RPC (drpc-level) errors, mirroring v1 filesync.ErrCodes and v2's fileprotov2.ErrCodes. Wired through rpcerr.ErrGroup(ErrorOffset) in the filep2perr package. Offset 900 is the next free rpcerr block (v1=200, v2=800). Zero value Unexpected=0 registers at offset+0 so an uncoded fault reads as Unexpected.



| 值                | 编号  |
| ---------------- | --- |
| `Unexpected`     | 0   |
| `Forbidden`      | 1   |
| `InvalidRequest` | 2   |
| `FileNotFound`   | 3   |
| `ErrorOffset`    | 900 |

### any-sync/commonfile/fileproto/fileprotov2/protos/filev2.proto

#### `ErrCode`

> ErrCode is the PER-ITEM, in-body business outcome (err == nil at the RPC layer). Flat status enum with an explicit success sentinel Ok=0. The typed payload on a *Result is valid ONLY when code == Ok. Deliberately a SEPARATE enum from ErrCodes: its zero value means success (not error), it never flows through rpcerr, and its value short-names are kept disjoint from ErrCodes so proto3's package-level enum-value scoping stays clean. Servers MUST set 
>
> `code`
>
>  explicitly on every result (Ok is the proto3 default, so an unset code would be misread as a success with an empty payload).



| 值                   | 编号 |
| ------------------- | -- |
| `Ok`                | 0  |
| `ErrUnexpected`     | 1  |
| `ErrCidNotFound`    | 2  |
| `ErrForbidden`      | 3  |
| `ErrLimitExceeded`  | 4  |
| `ErrSpaceNotFound`  | 5  |
| `ErrNotResponsible` | 6  |

#### `ErrCodes`

> ErrCodes are WHOLE-RPC (drpc-level) errors, mirroring v1 filesync.ErrCodes. Wired through rpcerr.ErrGroup(ErrCodes_ErrorOffset) in the fileprotov2err package. Returned as a NON-nil drpc error ONLY for auth / malformed / batch-too-large / misrouted. Never used to report the outcome of an individual item (that is the per-item ErrCode below). Zero value Unexpected=0 registers at offset+0 (=800), so an uncoded server fault reads as Unexpected — exactly as v1 does at 200. Offset 800 is the only free rpcerr block (v1=200, 100/300/400/500/600/700 are taken).



| 值                   | 编号  |
| ------------------- | --- |
| `Unexpected`        | 0   |
| `Forbidden`         | 1   |
| `InvalidRequest`    | 2   |
| `QuerySizeExceeded` | 3   |
| `NotResponsible`    | 4   |
| `ErrorOffset`       | 800 |

### any-sync/commonfile/fileproto/protos/file.proto

#### `AvailabilityStatus`



| 值               | 编号 |
| --------------- | -- |
| `NotExists`     | 0  |
| `Exists`        | 1  |
| `ExistsInSpace` | 2  |

#### `ErrCodes`



| 值                          | 编号  |
| -------------------------- | --- |
| `Unexpected`               | 0   |
| `CIDNotFound`              | 1   |
| `Forbidden`                | 2   |
| `_DeprecatedLimitExceeded` | 3   |
| `QuerySizeExceeded`        | 4   |
| `WrongHash`                | 5   |
| `NotEnoughSpace`           | 6   |
| `AclRecordNotFound`        | 7   |
| `LimitExceeded`            | 8   |
| `ErrorOffset`              | 200 |

### any-sync/commonspace/object/acl/aclrecordproto/protos/aclrecord.proto

#### `AclInviteType`



| 值               | 编号 |
| --------------- | -- |
| `RequestToJoin` | 0  |
| `AnyoneCanJoin` | 1  |

#### `AclUserPermissions`

> AclUserPermissions contains different possible user roles



| 值        | 编号 |
| -------- | -- |
| `None`   | 0  |
| `Owner`  | 1  |
| `Admin`  | 2  |
| `Writer` | 3  |
| `Reader` | 4  |
| `Guest`  | 5  |

### any-sync/commonspace/object/tree/treechangeproto/protos/treechange.proto

#### `ErrorCodes`



| 值                      | 编号  |
| ---------------------- | --- |
| `Unexpected`           | 0   |
| `GetTreeError`         | 1   |
| `FullSyncRequestError` | 2   |
| `ErrorOffset`          | 400 |

### any-sync/commonspace/pubsub/pubsubproto/protos/pubsub.proto

#### `ErrCodes`



| 值                | 编号   |
| ---------------- | ---- |
| `Unexpected`     | 0    |
| `NotAMember`     | 1    |
| `NotResponsible` | 2    |
| `RateLimited`    | 3    |
| `TooManyTopics`  | 4    |
| `InvalidMessage` | 5    |
| `TopicNotOwned`  | 6    |
| `InvalidTopic`   | 7    |
| `ErrorOffset`    | 1100 |

### any-sync/commonspace/spacesyncproto/protos/spacesync.proto

#### `DiffType`

> DiffType is a type of diff



| 值         | 编号 |
| --------- | -- |
| `Initial` | 0  |
| `V1`      | 1  |
| `V2`      | 2  |
| `V3`      | 3  |

#### `ErrCodes`



| 值                         | 编号  |
| ------------------------- | --- |
| `Unexpected`              | 0   |
| `SpaceMissing`            | 1   |
| `SpaceExists`             | 2   |
| `SpaceNotInCache`         | 3   |
| `SpaceIsDeleted`          | 4   |
| `PeerIsNotResponsible`    | 5   |
| `ReceiptIsInvalid`        | 6   |
| `InvalidPayload`          | 7   |
| `DuplicateRequest`        | 8   |
| `TooManyRequestsFromPeer` | 9   |
| `ErrorOffset`             | 100 |

#### `ObjectType`

> ObjectType is a type of object



| 值          | 编号 |
| ---------- | -- |
| `Tree`     | 0  |
| `Acl`      | 1  |
| `KeyValue` | 2  |

#### `SpaceFileProtoVersion`

> SpaceFileProtoVersion gates the file protocol a space uses. It lives in the signed, immutable header so it can't be stripped/downgraded without invalidating the owner signature.



| 值                                  | 编号 |
| ---------------------------------- | -- |
| `SpaceFileProtoVersionUnspecified` | 0  |
| `SpaceFileProtoVersionV2`          | 2  |

#### `SpaceHeaderVersion`



| 值                     | 编号 |
| --------------------- | -- |
| `SpaceHeaderVersion0` | 0  |
| `SpaceHeaderVersion1` | 1  |

#### `SpaceSubscriptionAction`

> SpaceSubscription contains in ObjectSyncMessage.Payload and indicates that we need to subscribe or unsubscribe the current stream to this space



| 值             | 编号 |
| ------------- | -- |
| `Subscribe`   | 0  |
| `Unsubscribe` | 1  |

### any-sync/consensus/consensusproto/protos/consensus.proto

#### `ErrCodes`



| 值                | 编号  |
| ---------------- | --- |
| `Unexpected`     | 0   |
| `LogExists`      | 1   |
| `LogNotFound`    | 2   |
| `RecordConflict` | 3   |
| `Forbidden`      | 4   |
| `InvalidPayload` | 5   |
| `ErrorOffset`    | 500 |

### any-sync/coordinator/coordinatorproto/protos/coordinator.proto

#### `AclEventLogRecordType`



| 值                             | 编号 |
| ----------------------------- | -- |
| `RecordTypeSpaceReceipt`      | 0  |
| `RecordTypeSpaceShared`       | 1  |
| `RecordTypeSpaceUnshared`     | 2  |
| `RecordTypeSpaceAclAddRecord` | 3  |

#### `DeletionLogRecordStatus`



| 值                 | 编号 |
| ----------------- | -- |
| `Ok`              | 0  |
| `RemovePrepare`   | 1  |
| `Remove`          | 2  |
| `OwnershipChange` | 3  |

#### `DeletionPayloadType`

> DeletionChangeType determines the type of deletion payload



| 值         | 编号 |
| --------- | -- |
| `Tree`    | 0  |
| `Confirm` | 1  |
| `Account` | 2  |

#### `ErrorCodes`



| 值                                | 编号  |
| -------------------------------- | --- |
| `Unexpected`                     | 0   |
| `SpaceDeleted`                   | 1   |
| `SpaceDeletionPending`           | 2   |
| `SpaceCreated`                   | 3   |
| `SpaceNotExists`                 | 4   |
| `SpaceLimitReached`              | 5   |
| `AccountDeleted`                 | 6   |
| `Forbidden`                      | 7   |
| `AclHeadIsMissing`               | 8   |
| `AclNonEmpty`                    | 9   |
| `SpaceNotShareable`              | 10  |
| `InboxMessageVerifyFailed`       | 11  |
| `SubscribePeerAlreadySubscribed` | 12  |
| `InviteStillActive`              | 13  |
| `ErrorOffset`                    | 300 |

#### `InboxKeyType`



| 值         | 编号 |
| --------- | -- |
| `ed25519` | 0  |

#### `InboxPacketType`

> Inbox Message



| 值         | 编号 |
| --------- | -- |
| `Default` | 0  |

#### `InboxPayloadType`



| 值                            | 编号 |
| ---------------------------- | -- |
| `InboxPayloadOneToOneInvite` | 0  |
| `InboxPayloadRegularInvite`  | 1  |

#### `NodeType`

> NodeType determines the type of API that a node supports



| 值                      | 编号 |
| ---------------------- | -- |
| `TreeAPI`              | 0  |
| `FileAPI`              | 1  |
| `CoordinatorAPI`       | 2  |
| `ConsensusAPI`         | 3  |
| `NamingNodeAPI`        | 4  |
| `PaymentProcessingAPI` | 5  |
| `FileV2API`            | 6  |

#### `NotifyEventType`

> Enum for event types



| 值                           | 编号 |
| --------------------------- | -- |
| `UnspecifiedEvent`          | 0  |
| `InboxNewMessageEvent`      | 1  |
| `NetworkConfigChangedEvent` | 2  |

#### `SpacePermissions`



| 值                         | 编号 |
| ------------------------- | -- |
| `SpacePermissionsUnknown` | 0  |
| `SpacePermissionsOwner`   | 1  |

#### `SpaceStatus`



| 值                            | 编号 |
| ---------------------------- | -- |
| `SpaceStatusCreated`         | 0  |
| `SpaceStatusPendingDeletion` | 1  |
| `SpaceStatusDeletionStarted` | 2  |
| `SpaceStatusDeleted`         | 3  |
| `SpaceStatusNotExists`       | 4  |

### any-sync/nameservice/nameserviceproto/protos/nameservice\_aa.proto

#### `OperationState`



| 值                   | 编号 |
| ------------------- | -- |
| `OpUnknown`         | 0  |
| `Pending`           | 1  |
| `PendingOrNotFound` | 2  |
| `Completed`         | 3  |
| `Error`             | 4  |

### any-sync/net/rpc/limiter/limiterproto/protos/limiter.proto

#### `ErrCodes`



| 值                   | 编号  |
| ------------------- | --- |
| `RateLimitExceeded` | 0   |
| `ErrorOffset`       | 700 |

### any-sync/net/secureservice/handshake/handshakeproto/protos/handshake.proto

#### `CredentialsType`



| 值               | 编号 |
| --------------- | -- |
| `SkipVerify`    | 0  |
| `SignedPeerIds` | 1  |

#### `Encoding`



| 值        | 编号 |
| -------- | -- |
| `None`   | 0  |
| `Snappy` | 1  |

#### `Error`



| 值                      | 编号 |
| ---------------------- | -- |
| `Null`                 | 0  |
| `Unexpected`           | 1  |
| `InvalidCredentials`   | 2  |
| `UnexpectedPayload`    | 3  |
| `SkipVerifyNotAllowed` | 4  |
| `DeadlineExceeded`     | 5  |
| `IncompatibleVersion`  | 6  |
| `IncompatibleProto`    | 7  |

#### `ProtoType`



| 值      | 编号 |
| ------ | -- |
| `DRPC` | 0  |

### any-sync/paymentservice/paymentserviceproto/protos/paymentservice.proto

#### `ErrorCodes`



| 值                           | 编号  |
| --------------------------- | --- |
| `Unexpected`                | 0   |
| `EthAddressEmpty`           | 1   |
| `InvalidSignature`          | 2   |
| `TierWrong`                 | 3   |
| `TierNotFound`              | 4   |
| `TierInactive`              | 5   |
| `PaymentMethodWrong`        | 6   |
| `BadAnyName`                | 7   |
| `Unknown`                   | 8   |
| `SubsAlreadyActive`         | 9   |
| `SubsNotFound`              | 10  |
| `SubsWrongState`            | 11  |
| `EmailWrongFormat`          | 12  |
| `EmailAlreadyVerified`      | 13  |
| `EmailAlreadySent`          | 14  |
| `EmailFailedToSend`         | 15  |
| `EmailExpired`              | 16  |
| `EmailWrongCode`            | 17  |
| `AppleInvalidReceipt`       | 18  |
| `ApplePurchaseRegistration` | 19  |
| `AppleSubscriptionRenew`    | 20  |
| `CodeNotFound`              | 21  |
| `CodeAlreadyUsed`           | 22  |
| `ErrorOffset`               | 600 |

#### `IsNameValidResponse.Code`



| 值                   | 编号 |
| ------------------- | -- |
| `Valid`             | 0  |
| `NoDotAny`          | 1  |
| `TooShort`          | 2  |
| `TooLong`           | 3  |
| `HasInvalidChars`   | 4  |
| `TierFeatureNoName` | 5  |
| `CanNotReserve`     | 6  |

#### `PaymentMethod`



| 值                   | 编号 |
| ------------------- | -- |
| `MethodCard`        | 0  |
| `MethodCrypto`      | 1  |
| `MethodApplePay`    | 2  |
| `MethodGooglePay`   | 3  |
| `MethodAppleInapp`  | 4  |
| `MethodGoogleInapp` | 5  |
| `MethodNone`        | 6  |

#### `SubscriptionStatus`



| 值                                   | 编号 |
| ----------------------------------- | -- |
| `StatusUnknown`                     | 0  |
| `StatusPending`                     | 1  |
| `StatusActive`                      | 2  |
| `StatusPendingRequiresFinalization` | 3  |

#### `SubscriptionTier`

> TODO: later we will have an interface to enumerate all available tiers it's a bad idea to list them here, because interface will be changed often



| 值                        | 编号 |
| ------------------------ | -- |
| `TierUnknown`            | 0  |
| `TierExplorer`           | 1  |
| `TierBuilder1WeekTEST`   | 2  |
| `TierCoCreator1WeekTEST` | 3  |
| `TierBuilder1Year`       | 4  |
| `TierCoCreator1Year`     | 5  |
| `TierBuilderPlus`        | 6  |
| `TierAnytypeTeam`        | 7  |

### any-sync/paymentservice/paymentserviceproto/protos/paymentservice2.proto

#### `MembershipV2.AnyNameIsValidResponse.Code`



| 值                  | 编号 |
| ------------------ | -- |
| `Valid`            | 0  |
| `NoDotAny`         | 1  |
| `TooShort`         | 2  |
| `TooLong`          | 3  |
| `HasInvalidChars`  | 4  |
| `AccountHasNoName` | 5  |
| `CanNotReserve`    | 6  |

#### `MembershipV2.Invoice.Status`



| 值        | 编号 |
| -------- | -- |
| `Unpaid` | 0  |
| `Paid`   | 1  |

#### `MembershipV2.PaymentProvider`



| 值               | 编号 |
| --------------- | -- |
| `None`          | 0  |
| `Stripe`        | 1  |
| `Crypto`        | 2  |
| `BillingPortal` | 3  |
| `AppStore`      | 4  |
| `GooglePlay`    | 5  |

#### `MembershipV2.Period`



| 值            | 编号 |
| ------------ | -- |
| `Monthly`    | 1  |
| `Yearly`     | 2  |
| `ThreeYears` | 3  |
| `Lifetime`   | 4  |

#### `MembershipV2.Platform`



| 值               | 编号 |
| --------------- | -- |
| `Unknown`       | 0  |
| `Desktop`       | 1  |
| `MobileIOS`     | 2  |
| `MobileAndroid` | 3  |
| `Web`           | 4  |

#### `MembershipV2.ProductStatus.Status`



| 值                                   | 编号 |
| ----------------------------------- | -- |
| `StatusUnknown`                     | 0  |
| `StatusPending`                     | 1  |
| `StatusActive`                      | 2  |
| `StatusPendingRequiresFinalization` | 3  |

### any-sync/paymentservice/paymentserviceproto/protos/paymentservice\_tiers.proto

#### `PeriodType`



| 值                     | 编号 |
| --------------------- | -- |
| `PeriodTypeUnknown`   | 0  |
| `PeriodTypeUnlimited` | 1  |
| `PeriodTypeDays`      | 2  |
| `PeriodTypeWeeks`     | 3  |
| `PeriodTypeMonths`    | 4  |
| `PeriodTypeYears`     | 5  |

### any-sync/util/crypto/cryptoproto/protos/crypto.proto

#### `KeyType`



| 值                | 编号 |
| ---------------- | -- |
| `Ed25519Public`  | 0  |
| `Ed25519Private` | 1  |
| `AES`            | 2  |

## 五、附录

### 5.1 测试服务



* `net/endtoendtest/testpeer/testproto/protos/testservice.proto`（pkg `testService`，`Test` 4 个方法）：端到端测试用。

* `net/streampool/testservice/protos/testservice.proto`（pkg `testService`，`Test` 2 个方法）：streampool 压力测试用。

### 5.2 与客户端学习路径的关系



* **你自研客户端实际要打交道的服务**（按通信对象）：


  * coordinator → `Coordinator`（22 方法：空间路由、网络配置、空间操作）

  * sync node → `SpaceSync`（10）、`PubSub`（1）、`ClientSpace`（2）

  * filenode → `File`（14）、`FileV2`（5）

  * 其他客户端 → `FileP2P`（2）

  * 可选：`IdentityRepo`（3）、`Anyns`（8）、`AnynsAccountAbstraction`（7）、`AnyPaymentProcessing`（11）、`AnyPaymentProcessingV2`（8）

* **节点间服务（你一般不需要直接实现，但理解协议需要）**：`Consensus`（4）、`NodeSync`（3）。

* 消息结构章节里标 `aclrecord` / `treechange` 的包是**变更日志与 ACL 记录的格式定义**，是理解 "追加式变更日志 + 版本溯源" 的关键，虽然它们没有 RPC。

### 5.3 数据格式（any-block）

`any-block/format/v1/proto/` 是对象数据格式定义（`models.proto` 125 消息 / `events.proto` 226 消息 / `changes.proto` 34 消息 / `snapshot.proto` 3 消息），已含在上述消息统计中。它定义 "一条变更长什么样、对象状态如何序列化"，是你自研客户端存储层的基础。