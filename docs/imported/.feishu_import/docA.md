
> 📌 本文档为《any-sync 协议 Protobuf 接口参考》系列第 1 篇（总览 · RPC 方法 · 枚举 · 附录）。
> 消息结构见第 2 篇《数据格式（any-block）》、第 3 篇《协议消息结构》。

# any-sync 协议 Protobuf 接口参考

> **固定版本学习底稿** —— 由本地 `any-sync-ecosystem` 快照中的 `.proto` 源码自动解析生成（2026-09-16 快照）。
> 协议核心 any-sync v0.13.2；本文档锁定的就是当前这份快照，后续学习、测试、自研客户端均以此为准。

## 范围与统计

| 项 | 值 |
|---|---|
| 覆盖仓库 | `any-sync`（协议核心）、`any-sync-node`、`any-sync-filenode`、`any-block`（format/v1 数据格式） |
| 文件数 | 28 个 `.proto` |
| 服务（service） | 17 个 |
| RPC 方法 | 112 个 |
| 消息（message） | 727 个（含嵌套消息） |
| 枚举（enum） | 133 个 |
| 明确排除 | `anytype-heart`（官方客户端 API，本学习路径不使用）；`any-block` 根目录旧副本（以 `format/v1/proto` 为准） |

> 注：`nameservice`、`paymentservice` 系列文件无 `package` 声明，本文档按 `go_package` 目录归组。

## 目录

1. [协议总览](#一协议总览)
2. [RPC 方法详表](#二rpc-方法详表)
3. [消息结构](#三消息结构)
4. [枚举](#四枚举)
5. [附录](#五附录)


## 一、协议总览

### 1.1 服务全景

| 包 | 服务 | RPC 数 | 职责 | 调用关系 |
|---|---|---|---|---|
| `anyNodeSync` | `NodeSync` | 3 | sync node 之间的空间数据同步（节点间复制、对账） | sync node ↔ sync node |
| `clientspace` | `ClientSpace` | 2 | 客户端空间辅助：space 级轻量远程调用（会话/存储信息获取） | 客户端 ↔ sync node |
| `consensusProto` | `Consensus` | 4 | ACL 共识校验：成员/权限变更记录的校验与批准（sync node 间由 RAFT 承载） | sync node ↔ consensus node |
| `coordinator` | `Coordinator` | 22 | 协调器：空间注册/路由、网络配置下发、空间列表与配置查询 | 客户端 ↔ coordinator |
| `filesync` | `File` | 14 | 文件同步 v1：CID 寻址的文件块上传/下载/校验（客户端↔filenode） | 客户端 ↔ filenode |
| `filesyncp2p` | `FileP2P` | 2 | P2P 文件传输：客户端之间直接传输文件块（不经 filenode） | 客户端 ↔ 客户端 |
| `filesyncv2` | `FileV2` | 5 | 文件同步 v2：文件组/文件快照粒度的同步接口（客户端↔filenode） | 客户端 ↔ filenode |
| `identityRepo` | `IdentityRepo` | 3 | 身份仓库：identity 元数据的注册、查询、删除 | 客户端 ↔ identity node |
| `nodeapi` | `NodeApi` | 6 | 节点调试/管理 API：仅用于调试运维，非业务协议 | 运维工具 ↔ sync node |
| `pubsub` | `PubSub` | 1 | 空间事件发布订阅：推送空间内对象变更事件 | 客户端 ↔ sync node |
| `spacesync` | `SpaceSync` | 10 | 空间同步核心：对象变更同步、空间存储操作、对象拉取/订阅（客户端↔sync node 主协议） | 客户端 ↔ sync node |
| `testService` | `Test` | 4 | 协议测试服务：仅用于框架自测（endtoendtest / streampool） | 测试 |
| `testService` | `Test` | 2 | 协议测试服务：仅用于框架自测（endtoendtest / streampool） | 测试 |
| `（无 package）` | `AnyPaymentProcessing` | 11 | 支付处理 v1：套餐/订阅/支付意图、余额查询 | 客户端 ↔ payment service |
| `（无 package）` | `AnyPaymentProcessingV2` | 8 | 支付处理 v2：会话支付、订阅管理、发票、权益 | 客户端 ↔ payment service |
| `（无 package）` | `Anyns` | 8 | 名字服务：.any 名称的可用性查询、注册、解析、续期、转移 | 客户端 ↔ name service |
| `（无 package）` | `AnynsAccountAbstraction` | 7 | 名字服务账户抽象：链上交易/账户相关的名称操作 | 客户端 ↔ name service |

### 1.2 文件清单

| 相对路径 | package | 服务 | RPC | 消息 | 枚举 |
|---|---|---|---|---|---|
| `any-block/format/v1/proto/changes.proto` | `anytype` | — | 0 | 34 | 1 |
| `any-block/format/v1/proto/events.proto` | `anytype` | — | 0 | 226 | 8 |
| `any-block/format/v1/proto/models.proto` | `anytype.model` | — | 0 | 125 | 74 |
| `any-block/format/v1/proto/snapshot.proto` | `anytype` | — | 0 | 3 | 0 |
| `any-sync-filenode/index/indexproto/protos/index.proto` | `fileIndexProto` | — | 0 | 6 | 0 |
| `any-sync-node/debug/nodedebugrpc/nodedebugrpcproto/protos/nodedebugrpc.proto` | `nodeapi` | NodeApi | 6 | 13 | 0 |
| `any-sync-node/nodesync/nodesyncproto/protos/nodesync.proto` | `anyNodeSync` | NodeSync | 3 | 9 | 3 |
| `any-sync/commonfile/fileproto/filep2p/protos/filep2p.proto` | `filesyncp2p` | FileP2P | 2 | 5 | 2 |
| `any-sync/commonfile/fileproto/fileprotov2/protos/filev2.proto` | `filesyncv2` | FileV2 | 5 | 20 | 2 |
| `any-sync/commonfile/fileproto/protos/file.proto` | `filesync` | File | 14 | 27 | 2 |
| `any-sync/commonspace/clientspaceproto/protos/clientspace.proto` | `clientspace` | ClientSpace | 2 | 5 | 0 |
| `any-sync/commonspace/object/acl/aclrecordproto/protos/aclrecord.proto` | `aclrecord` | — | 0 | 23 | 2 |
| `any-sync/commonspace/object/tree/treechangeproto/protos/treechange.proto` | `treechange` | — | 0 | 13 | 1 |
| `any-sync/commonspace/pubsub/pubsubproto/protos/pubsub.proto` | `pubsub` | PubSub | 1 | 5 | 1 |
| `any-sync/commonspace/spacesyncproto/protos/spacesync.proto` | `spacesync` | SpaceSync | 10 | 33 | 6 |
| `any-sync/consensus/consensusproto/protos/consensus.proto` | `consensusProto` | Consensus | 4 | 16 | 1 |
| `any-sync/coordinator/coordinatorproto/protos/coordinator.proto` | `coordinator` | Coordinator | 22 | 59 | 11 |
| `any-sync/identityrepo/identityrepoproto/protos/identityrepo.proto` | `identityRepo` | IdentityRepo | 3 | 7 | 0 |
| `any-sync/nameservice/nameserviceproto/protos/nameservice.proto` | `—` | Anyns | 8 | 10 | 0 |
| `any-sync/nameservice/nameserviceproto/protos/nameservice_aa.proto` | `—` | AnynsAccountAbstraction | 7 | 16 | 1 |
| `any-sync/net/endtoendtest/testpeer/testproto/protos/testservice.proto` | `testService` | Test | 4 | 1 | 0 |
| `any-sync/net/rpc/limiter/limiterproto/protos/limiter.proto` | `limiter` | — | 0 | 0 | 1 |
| `any-sync/net/secureservice/handshake/handshakeproto/protos/handshake.proto` | `anyHandshake` | — | 0 | 4 | 4 |
| `any-sync/net/streampool/testservice/protos/testservice.proto` | `testService` | Test | 2 | 1 | 0 |
| `any-sync/paymentservice/paymentserviceproto/protos/paymentservice.proto` | `—` | AnyPaymentProcessing | 11 | 29 | 5 |
| `any-sync/paymentservice/paymentserviceproto/protos/paymentservice2.proto` | `—` | AnyPaymentProcessingV2 | 8 | 31 | 6 |
| `any-sync/paymentservice/paymentserviceproto/protos/paymentservice_tiers.proto` | `—` | — | 0 | 5 | 1 |
| `any-sync/util/crypto/cryptoproto/protos/crypto.proto` | `crypto` | — | 0 | 1 | 1 |


## 二、RPC 方法详表

> 流式列：`R`=请求流式，`S`=响应流式，`RS`=双向流式，空=普通一元调用。


### NodeApi · `nodeapi`

**文件**：`any-sync-node/debug/nodedebugrpc/nodedebugrpcproto/protos/nodedebugrpc.proto`　　**职责**：节点调试/管理 API：仅用于调试运维，非业务协议

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `DumpTree` | — | `DumpTreeRequest` | `DumpTreeResponse` |  |
| `TreeParams` | — | `TreeParamsRequest` | `TreeParamsResponse` |  |
| `AllTrees` | — | `AllTreesRequest` | `AllTreesResponse` |  |
| `AllSpaces` | — | `AllSpacesRequest` | `AllSpacesResponse` |  |
| `ForceNodeSync` | — | `ForceNodeSyncRequest` | `ForceNodeSyncResponse` |  |
| `NodesAddressesBySpace` | — | `NodesAddressesBySpaceRequest` | `NodesAddressesBySpaceResponse` |  |


### NodeSync · `anyNodeSync`

**文件**：`any-sync-node/nodesync/nodesyncproto/protos/nodesync.proto`　　**职责**：sync node 之间的空间数据同步（节点间复制、对账）

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `PartitionSync` | — | `PartitionSyncRequest` | `PartitionSyncResponse` | PartitionSync compares all spaces by given c-hash partition |
| `ColdSync` | S | `ColdSyncRequest` | `ColdSyncResponse` | ColdSync requests cold sync stream for fast space download |
| `AdoptArchive` | — | `AdoptArchiveRequest` | `AdoptArchiveResponse` | AdoptArchive offers the receiver an archived space snapshot parked in the shared archive store; the receiver copies the object into its own prefix and registers the space as archived without materializing it |


### FileP2P · `filesyncp2p`

**文件**：`any-sync/commonfile/fileproto/filep2p/protos/filep2p.proto`　　**职责**：P2P 文件传输：客户端之间直接传输文件块（不经 filenode）

> FileP2P is the peer-to-peer file transfer service. It is served READ-ONLY by a client to other LAN peers so a device can fetch a file's encrypted CAR object directly from a nearby peer that already holds it, instead of the file-node / object-storage path — enabling local-network file sync, offline (no reachable node) reads, and durability takeover (a peer re-uploading a file whose creator never made it durable).  drpc route prefix is "/filesyncp2p.FileP2P/..." — DISTINCT from v1 "/filesync.File/..." and v2 "/filesyncv2.FileV2/...", so all three can be mounted on one drpc mux. Names are load-bearing: method paths derive from `package filesyncp2p` + `service FileP2P`.  Model: a client stores one immutable, content-addressed CARv2 object per file, byte-identical to the object the S3/public-read path serves. So a peer is simply an ALTERNATE SOURCE of that same object: ObjectRead returns object byte RANGES exactly like an HTTP Range GET, and the fetcher's existing seed/verify path (parse header+index, then verify every block against its cid) is reused unchanged. Because a partial local copy has holes, ObjectRead is served only by peers that hold the file in FULL; FileCheck reports which.  Conventions: * requests are ROOT-SCOPED (rootCid) — the store is one CAR per root, keyed by rootCid, with no global block-CID index; * identity is NEVER a request field — it is the authenticated connection; authorization (may this peer read this space) is the server's job; * object bytes are CIPHERTEXT (the file layer is encrypted before the DAG is built), so serving them discloses no plaintext; the FETCHER verifies every block against its cid (nothing on this wire does).

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `FileCheck` | — | `FileCheckRequest` | `FileCheckResponse` | FileCheck reports, per requested rootCid, whether the server holds the file fully, partially, or not at all — so a client can pick a FULL peer to ObjectRead from without first knowing the object geometry. |
| `ObjectRead` | — | `ObjectReadRequest` | `ObjectReadResponse` | ObjectRead returns a byte range of the file's CARv2 object. Mirrors an HTTP Range GET: totalSize echoes the whole-object size (for the head probe / index-tail read). Served only when the file is held in full. |


### FileV2 · `filesyncv2`

**文件**：`any-sync/commonfile/fileproto/fileprotov2/protos/filev2.proto`　　**职责**：文件同步 v2：文件组/文件快照粒度的同步接口（客户端↔filenode）

> FileV2 is the v2 filenode broker (S3-direct uploads/downloads).  drpc route prefix is "/filesyncv2.FileV2/..." — DISTINCT from v1 "/filesync.File/..." so both services can be mounted on the same drpc mux without a Register() panic. The package/service names are load-bearing: method paths are derived from `package filesyncv2` + `service FileV2`.  Conventions (all four SPACE-SCOPED RPCs are BATCH; Info is node-level): * request carries a single shared spaceId (or repeated spaceIds for SpaceInfo) + a repeated list of items; * identity is NEVER a request field — it is taken from the authenticated connection, and all per-space/per-cid authorization derives from it; * rootCid is bytes (raw self-describing CID, as in v1's `bytes cid`); * every result echoes its own key (rootCid bytes, or spaceId string) so clients build map[string(key)]->result in one pass — results are matched by key, NEVER by positional index; the server may reorder/dedupe; * per-item result = flat status enum (ErrCode, Ok=0) + exactly one typed payload message that is valid ONLY when code == Ok; * one bad/forbidden item never fails the whole batch.  Two error layers: 1. whole-RPC drpc error (err != nil), carrying an ErrCodes value from the offset-800 rpcerr registry, returned ONLY for cross-cutting failures: failed/absent auth (Forbidden), malformed input (InvalidRequest), an over-sized batch (QuerySizeExceeded), or a misrouted single-space request (NotResponsible — retry against the space's responsible pair); 2. per-item business outcome lives in the in-body ErrCode `code` field (err == nil for the RPC as a whole).

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `Upload` | — | `UploadRequest` | `UploadResponse` | Upload issues a presigned upload target per requested file root. |
| `RequestSign` | — | `RequestSignRequest` | `RequestSignResponse` | RequestSign returns a network-signed durable-custody receipt per rootCid. |
| `RequestDownload` | — | `RequestDownloadRequest` | `RequestDownloadResponse` | RequestDownload returns a signed GET target per rootCid. |
| `SpaceInfo` | — | `SpaceInfoRequest` | `SpaceInfoResponse` | SpaceInfo returns quota/usage per requested space (batch quota-info). |
| `Info` | — | `InfoRequest` | `InfoResponse` | Info returns static node-level metadata (no spaceId, no responsibility gate, no auth beyond the connection); clients cache it. |


### File · `filesync`

**文件**：`any-sync/commonfile/fileproto/protos/file.proto`　　**职责**：文件同步 v1：CID 寻址的文件块上传/下载/校验（客户端↔filenode）

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `BlockGet` | — | `BlockGetRequest` | `BlockGetResponse` | BlockGet gets one block from a server |
| `BlockPush` | — | `BlockPushRequest` | `Ok` | BlockPush pushes one block to a server |
| `BlockPushMany` | — | `BlockPushManyRequest` | `Ok` | BlockPushMany pushes many blocks to a server |
| `BlocksCheck` | — | `BlocksCheckRequest` | `BlocksCheckResponse` | BlocksCheck checks is CIDs exists |
| `BlocksBind` | — | `BlocksBindRequest` | `Ok` | BlocksBind binds CIDs to space |
| `FilesDelete` | — | `FilesDeleteRequest` | `FilesDeleteResponse` | FilesDelete deletes files by id |
| `FilesInfo` | — | `FilesInfoRequest` | `FilesInfoResponse` | FilesInfo return info by given files id |
| `FilesGet` | S | `FilesGetRequest` | `FilesGetResponse` | FilesGet returns a stream that streams all file ids in the space |
| `Check` | — | `CheckRequest` | `CheckResponse` | Check checks the connection and credentials |
| `SpaceInfo` | — | `SpaceInfoRequest` | `SpaceInfoResponse` | SpaceInfo returns usage, limit, etc about space |
| `AccountInfo` | — | `AccountInfoRequest` | `AccountInfoResponse` | AccountInfo returns usage, limit, etc by all spaces |
| `AccountLimitSet` | — | `AccountLimitSetRequest` | `Ok` | AccountLimitSet sets the account file storage limit (available only for nodeconf members) |
| `SpaceLimitSet` | — | `SpaceLimitSetRequest` | `Ok` | SpaceLimitSet sets the space limit. Limit 0 means space will use account limits. |
| `BlockDeleteUnbound` | — | `BlockDeleteUnboundRequest` | `Ok` | BlockDeleteUnbound permanently deletes a block that is not bound to any space (refs == 0). Available only for coordinator nodes; intended for invite-file cleanup. |


### ClientSpace · `clientspace`

**文件**：`any-sync/commonspace/clientspaceproto/protos/clientspace.proto`　　**职责**：客户端空间辅助：space 级轻量远程调用（会话/存储信息获取）

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `SpaceExchange` | — | `SpaceExchangeRequest` | `SpaceExchangeResponse` | SpaceExchange sends plaintext space id lists to any LAN peer. Deprecated: leaks the full space set to unauthenticated strangers; use SpaceExchangeV2. |
| `SpaceExchangeV2` | — | `SpaceExchangeV2Request` | `SpaceExchangeV2Response` | SpaceExchangeV2 lets two LAN peers learn only the intersection of their space sets. Instead of space ids, peers exchange per-space HMAC tokens keyed by a discovery key derived from the space's first ACL read key — a secret only members hold. A valid token both hides the space from non-members and proves the sender's membership. See clientspaceproto/exchange2.go for token derivation. |


### PubSub · `pubsub`

**文件**：`any-sync/commonspace/pubsub/pubsubproto/protos/pubsub.proto`　　**职责**：空间事件发布订阅：推送空间内对象变更事件

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `PubSubStream` | RS | `PubSubMessage` | `PubSubMessage` | PubSubStream is a long-lived bidirectional stream multiplexing all spaces and topics between two peers |


### SpaceSync · `spacesync`

**文件**：`any-sync/commonspace/spacesyncproto/protos/spacesync.proto`　　**职责**：空间同步核心：对象变更同步、空间存储操作、对象拉取/订阅（客户端↔sync node 主协议）

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `HeadSync` | — | `HeadSyncRequest` | `HeadSyncResponse` | HeadSync compares all objects and their hashes in a space |
| `StoreDiff` | — | `StoreDiffRequest` | `StoreDiffResponse` | StoreDiff compares all objects and their hashes in a space |
| `StoreElements` | RS | `StoreKeyValue` | `StoreKeyValue` | StoreElements exchanges elements between peers |
| `SpacePush` | — | `SpacePushRequest` | `SpacePushResponse` | SpacePush sends new space to the node |
| `SpacePull` | — | `SpacePullRequest` | `SpacePullResponse` | SpacePull gets space from the remote peer |
| `ObjectSyncStream` | RS | `ObjectSyncMessage` | `ObjectSyncMessage` | ObjectSyncStream opens object sync stream with node or client |
| `ObjectSync` | — | `ObjectSyncMessage` | `ObjectSyncMessage` | ObjectSync sends object sync message and synchronously gets response message |
| `ObjectSyncRequestStream` | S | `ObjectSyncMessage` | `ObjectSyncMessage` | ObjectSyncRequestStream opens sends a request and gets streamed response |
| `AclAddRecord` | — | `AclAddRecordRequest` | `AclAddRecordResponse` | AclAddRecord adds a new record to acl log. Works only with any-sync-node deprecated: use coordinator api |
| `AclGetRecords` | — | `AclGetRecordsRequest` | `AclGetRecordsResponse` | AclGetRecords gets acl records deprecated: use coordinator api |


### Consensus · `consensusProto`

**文件**：`any-sync/consensus/consensusproto/protos/consensus.proto`　　**职责**：ACL 共识校验：成员/权限变更记录的校验与批准（sync node 间由 RAFT 承载）

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `LogAdd` | — | `LogAddRequest` | `Ok` | LogAdd adds new log to consensus |
| `RecordAdd` | — | `RecordAddRequest` | `RawRecordWithId` | RecordAdd adds new record to log |
| `LogWatch` | RS | `LogWatchRequest` | `LogWatchEvent` | LogWatch fetches log and subscribes for a changes |
| `LogDelete` | — | `LogDeleteRequest` | `Ok` | LogDelete deletes the log from the consensus |


### Coordinator · `coordinator`

**文件**：`any-sync/coordinator/coordinatorproto/protos/coordinator.proto`　　**职责**：协调器：空间注册/路由、网络配置下发、空间列表与配置查询

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `SpaceSign` | — | `SpaceSignRequest` | `SpaceSignResponse` | SpaceSign signs a space creation operation |
| `SpaceStatusCheck` | — | `SpaceStatusCheckRequest` | `SpaceStatusCheckResponse` | SpaceStatusCheck checks the status of space and tells if it is deleted or not |
| `SpaceStatusCheckMany` | — | `SpaceStatusCheckManyRequest` | `SpaceStatusCheckManyResponse` | SpaceStatusCheckMany checks the statuses of spaces and tells if they are deleted or not |
| `SpaceStatusChange` | — | `SpaceStatusChangeRequest` | `SpaceStatusChangeResponse` | SpaceStatusChange changes the status of space - Deprecated |
| `SpaceMakeShareable` | — | `SpaceMakeShareableRequest` | `SpaceMakeShareableResponse` | SpaceMakeShareable makes space shareable |
| `SpaceMakeUnshareable` | — | `SpaceMakeUnshareableRequest` | `SpaceMakeUnshareableResponse` | SpaceMakeUnshareable marks space unshareable |
| `NetworkConfiguration` | — | `NetworkConfigurationRequest` | `NetworkConfigurationResponse` | NetworkConfiguration retrieves the latest network configuration |
| `DeletionLog` | — | `DeletionLogRequest` | `DeletionLogResponse` | DeletionLog gets the latest deletion log records |
| `SpaceDelete` | — | `SpaceDeleteRequest` | `SpaceDeleteResponse` | SpaceDelete deletes a space |
| `AccountDelete` | — | `AccountDeleteRequest` | `AccountDeleteResponse` | AccountDelete deletes an account |
| `AccountRevertDeletion` | — | `AccountRevertDeletionRequest` | `AccountRevertDeletionResponse` | AccountRevertDeletion reverts an account deletion |
| `AclAddRecord` | — | `AclAddRecordRequest` | `AclAddRecordResponse` | AclAddRecord adds a new record to acl log. Works only with any-sync-node |
| `AclGetRecords` | — | `AclGetRecordsRequest` | `AclGetRecordsResponse` | AclGetRecords gets acl records |
| `AccountLimitsSet` | — | `AccountLimitsSetRequest` | `AccountLimitsSetResponse` | AccountLimitsSet sets limits to the account. Can be used only by a network config member |
| `AclEventLog` | — | `AclEventLogRequest` | `AclEventLogResponse` | EventLog gets the latest event log records |
| `InboxFetch` | — | `InboxFetchRequest` | `InboxFetchResponse` | InboxFetch returns a set of (new) messages starting from a given offset |
| `InboxAddMessage` | — | `InboxAddMessageRequest` | `InboxAddMessageResponse` | InboxFetch returns a set of (new) messages starting from a given offset |
| `NotifySubscribe` | S | `NotifySubscribeRequest` | `NotifySubscribeEvent` | NotifySubscribe returns a subscription to new inbox msg |
| `AclUploadInvite` | — | `AclUploadInviteRequest` | `AclUploadInviteResponse` | AclUploadInvite uploads invite binary data to the filenodes |
| `AclDeleteInvite` | — | `AclDeleteInviteRequest` | `AclDeleteInviteResponse` | AclDeleteInvite permanently removes an invite file from the filenodes. The caller must be the space owner and the invite must be revoked in the acl. |
| `FileLimitsGet` | — | `FileLimitsGetRequest` | `FileLimitsGetResponse` | FileLimitsGet returns the file-storage pool bounds for an uploader identity in a space (files v2; fileV2 nodes only). The response carries absolute bounds — the caller computes effective headroom locally. |
| `FileUsageReport` | — | `FileUsageReportRequest` | `FileUsageReportResponse` | FileUsageReport accepts per-(space, identity) durable file usage reports from fileV2 nodes. The reporting node is taken from the authenticated peer context. Values are absolute (idempotent re-reports). |


### IdentityRepo · `identityRepo`

**文件**：`any-sync/identityrepo/identityrepoproto/protos/identityrepo.proto`　　**职责**：身份仓库：identity 元数据的注册、查询、删除

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `DataPut` | — | `DataPutRequest` | `Ok` | DataPut puts client data to a repository |
| `DataDelete` | — | `DataDeleteRequest` | `Ok` | DataDelete deletes client data from a repository |
| `DataPull` | — | `DataPullRequest` | `DataPullResponse` | DataPull pulls client data from a repository |


### Anyns · `（无 package）`

**文件**：`any-sync/nameservice/nameserviceproto/protos/nameservice.proto`　　**职责**：名字服务：.any 名称的可用性查询、注册、解析、续期、转移

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `IsNameAvailable` | — | `NameAvailableRequest` | `NameAvailableResponse` | Lookup: name -> address |
| `BatchIsNameAvailable` | — | `BatchNameAvailableRequest` | `BatchNameAvailableResponse` |  |
| `GetNameByAddress` | — | `NameByAddressRequest` | `NameByAddressResponse` | Reverse lookup: address -> name |
| `BatchGetNameByAddress` | — | `BatchNameByAddressRequest` | `BatchNameByAddressResponse` |  |
| `GetNameByAnyId` | — | `NameByAnyIdRequest` | `NameByAddressResponse` | Reverse lookup: ANY ID -> name |
| `BatchGetNameByAnyId` | — | `BatchNameByAnyIdRequest` | `BatchNameByAddressResponse` |  |
| `AdminNameRegisterSigned` | — | `NameRegisterRequestSigned` | `OperationResponse` | Register new name for the user (on behalf of the user) Anytype CAN only register names for users, but can not transfer! |
| `AdminNameRenewSigned` | — | `NameRenewRequestSigned` | `OperationResponse` |  |


### AnynsAccountAbstraction · `（无 package）`

**文件**：`any-sync/nameservice/nameserviceproto/protos/nameservice_aa.proto`　　**职责**：名字服务账户抽象：链上交易/账户相关的名称操作

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `GetOperation` | — | `GetOperationStatusRequest` | `OperationResponse` | COMMON METHODS: |
| `AdminFundUserAccount` | — | `AdminFundUserAccountRequestSigned` | `OperationResponse` | ADMIN METHODS: Will send "access tokens" to the user's account (to his SmartContractWallet). User will be able to use these "access tokens" to register his name later directly.  Blocking, will send TX to EVM chain If finished without error -> please use GetUserAccount to get updated info |
| `AdminFundGasOperations` | — | `AdminFundGasOperationsRequestSigned` | `OperationResponse` | Each operation is a single blockchain TX like "name update". User will be able to send operations without having any gas in his wallet later |
| `GetUserAccount` | — | `GetUserAccountRequest` | `UserAccount` | USER METHODS: Use it to: 1 - get your SmartContractWallet address 2 - get how many operations you still have |
| `GetDataNameRegister` | — | `NameRegisterRequest` | `GetDataNameRegisterResponse` | Example usage: 1. get data + context 2. sign it with your Ethereum private key 3. send it using CreateUserOperation 4. check operation status using GetOperation  Register new name for my Any identity |
| `GetDataNameRegisterForSpace` | — | `NameRegisterForSpaceRequest` | `GetDataNameRegisterResponse` | Register new name and attach Space ID to it |
| `CreateUserOperation` | — | `CreateUserOperationRequestSigned` | `OperationResponse` | TODO rpc GetDataNameUpdate(NameUpdateRequest) returns (GetDataNameRegisterResponse) {} |


### Test · `testService`

**文件**：`any-sync/net/endtoendtest/testpeer/testproto/protos/testservice.proto`　　**职责**：协议测试服务：仅用于框架自测（endtoendtest / streampool）

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `BiDirectionalStream` | RS | `StreamMessage` | `StreamMessage` |  |
| `ServerStream` | S | `StreamMessage` | `StreamMessage` |  |
| `ClientStream` | R | `StreamMessage` | `StreamMessage` |  |
| `Unary` | — | `StreamMessage` | `StreamMessage` |  |


### Test · `testService`

**文件**：`any-sync/net/streampool/testservice/protos/testservice.proto`　　**职责**：协议测试服务：仅用于框架自测（endtoendtest / streampool）

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `TestStream` | RS | `StreamMessage` | `StreamMessage` |  |
| `TestStream2` | S | `StreamMessage` | `StreamMessage` |  |


### AnyPaymentProcessing · `（无 package）`

**文件**：`any-sync/paymentservice/paymentserviceproto/protos/paymentservice.proto`　　**职责**：支付处理 v1：套餐/订阅/支付意图、余额查询

> NOTICE: 1 - User can not ask for a payment/other links on behalf of another user (a signature is required) 2 - Admin can do that on behalf of any user

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `GetSubscriptionStatus` | — | `GetSubscriptionRequestSigned` | `GetSubscriptionResponse` |  |
| `IsNameValid` | — | `IsNameValidRequest` | `IsNameValidResponse` | Check if the requested name is valid for the requested tier before requesting a payment link and paying |
| `BuySubscription` | — | `BuySubscriptionRequestSigned` | `BuySubscriptionResponse` | Save a new BillingID to DB, and return a payment link. You can call BuySubscription multiple times even if current payment is not processed yet (to get new payment link). If user has already an active subscription, then this will return an error. |
| `FinalizeSubscription` | — | `FinalizeSubscriptionRequestSigned` | `FinalizeSubscriptionResponse` | If your subscription is in StatusPendingRequiresFinalization, then you need to call this method |
| `GetSubscriptionPortalLink` | — | `GetSubscriptionPortalLinkRequestSigned` | `GetSubscriptionPortalLinkResponse` | Generate a link to the portal where user can: a) change her billing details b) see payment info, invoices, etc c) cancel/renew the subscription |
| `GetVerificationEmail` | — | `GetVerificationEmailRequestSigned` | `GetVerificationEmailResponse` | Verify user's email: 1st step - get a verification link to the email Will fail if already verified, i.e. you can not change your email |
| `VerifyEmail` | — | `VerifyEmailRequestSigned` | `VerifyEmailResponse` | Enter the code from the email Will fail if: link was not requested, link is expired, if email is already verified |
| `GetAllTiers` | — | `GetTiersRequestSigned` | `GetTiersResponse` | Returns all available application tiers, including inactive 1 - this list does not depend on the current platform (iOS, Android, Desktop) 2 - this list can be different for different users, based on their account ID 3 - user can not buy stripe 4 - some tiers are custom () |
| `VerifyAppStoreReceipt` | — | `VerifyAppStoreReceiptRequestSigned` | `VerifyAppStoreReceiptResponse` | Verify purchase in case subscription was bought via AppStore Incoming receipt contains all information to register purchase on Payment Node |
| `CodeGetInfo` | — | `CodeGetInfoRequestSigned` | `CodeGetInfoResponse` |  |
| `CodeRedeem` | — | `CodeRedeemRequestSigned` | `CodeRedeemResponse` |  |


### AnyPaymentProcessingV2 · `（无 package）`

**文件**：`any-sync/paymentservice/paymentserviceproto/protos/paymentservice2.proto`　　**职责**：支付处理 v2：会话支付、订阅管理、发票、权益

| 方法 | 流式 | 请求 | 响应 | 说明 |
|---|---|---|---|---|
| `SubscribeToUpdates` | — | `MembershipV2.SubscribeToUpdatesRequest` | `MembershipV2.SubscribeToUpdatesResponse` |  |
| `GetProducts` | — | `MembershipV2.GetProductsRequest` | `MembershipV2.GetProductsResponse` |  |
| `GetStatus` | — | `MembershipV2.GetStatusRequest` | `MembershipV2.GetStatusResponse` |  |
| `WebAuth` | — | `MembershipV2.WebAuthRequest` | `MembershipV2.WebAuthResponse` |  |
| `AnyNameIsValid` | — | `MembershipV2.AnyNameIsValidRequest` | `MembershipV2.AnyNameIsValidResponse` |  |
| `AnyNameAllocate` | — | `MembershipV2.AnyNameAllocateRequest` | `MembershipV2.AnyNameAllocateResponse` |  |
| `StoreCartGet` | — | `MembershipV2.StoreCartGetRequest` | `MembershipV2.StoreCartGetResponse` |  |
| `StoreCartUpdate` | — | `MembershipV2.StoreCartUpdateRequest` | `MembershipV2.StoreCartUpdateResponse` |  |




## 四、枚举

> 按文件分组；嵌套枚举用点路径表示。


### any-block/format/v1/proto/changes.proto

#### `ModifyOp`

| 值 | 编号 |
|---|---|
| `Set` | 0 |
| `Unset` | 1 |
| `Inc` | 2 |
| `AddToSet` | 3 |
| `Pull` | 4 |


### any-block/format/v1/proto/events.proto

#### `Event.Block.Dataview.SliceOperation`

| 值 | 编号 |
|---|---|
| `SliceOperationNone` | 0 |
| `SliceOperationAdd` | 1 |
| `SliceOperationMove` | 2 |
| `SliceOperationRemove` | 3 |
| `SliceOperationReplace` | 4 |

#### `Event.Object.CleanupSuggestion.Trigger`

| 值 | 编号 |
|---|---|
| `archive` | 0 |
| `delete` | 1 |
| `linkRemoval` | 2 |

#### `Event.P2PStatus.Status`

| 值 | 编号 |
|---|---|
| `NotConnected` | 0 |
| `NotPossible` | 1 |
| `Connected` | 2 |
| `Restricted` | 3 |

#### `Event.Space.Network`

| 值 | 编号 |
|---|---|
| `Anytype` | 0 |
| `SelfHost` | 1 |
| `LocalOnly` | 2 |

#### `Event.Space.Status`

| 值 | 编号 |
|---|---|
| `Synced` | 0 |
| `Syncing` | 1 |
| `Error` | 2 |
| `Offline` | 3 |
| `NetworkNeedsUpdate` | 4 |

#### `Event.Space.SyncError`

| 值 | 编号 |
|---|---|
| `Null` | 0 |
| `StorageLimitExceed` | 1 |
| `IncompatibleVersion` | 2 |
| `NetworkError` | 3 |

#### `Event.Status.Thread.SyncStatus`

| 值 | 编号 |
|---|---|
| `Unknown` | 0 |
| `Offline` | 1 |
| `Syncing` | 2 |
| `Synced` | 3 |
| `Failed` | 4 |
| `IncompatibleVersion` | 5 |
| `NetworkNeedsUpdate` | 6 |

#### `Model.Process.State`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Running` | 1 |
| `Done` | 2 |
| `Canceled` | 3 |
| `Error` | 4 |


### any-block/format/v1/proto/models.proto

#### `Account.Auth.LocalApiScope`

| 值 | 编号 |
|---|---|
| `Limited` | 0 |
| `JsonAPI` | 1 |
| `Full` | 2 |

#### `Account.StatusType`

| 值 | 编号 |
|---|---|
| `Active` | 0 |
| `PendingDeletion` | 1 |
| `StartedDeletion` | 2 |
| `Deleted` | 3 |

#### `Block.Align`

| 值 | 编号 |
|---|---|
| `AlignLeft` | 0 |
| `AlignCenter` | 1 |
| `AlignRight` | 2 |
| `AlignJustify` | 3 |

#### `Block.Content.Bookmark.State`

| 值 | 编号 |
|---|---|
| `Empty` | 0 |
| `Fetching` | 1 |
| `Done` | 2 |
| `Error` | 3 |

#### `Block.Content.Dataview.Filter.Condition`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Equal` | 1 |
| `NotEqual` | 2 |
| `Greater` | 3 |
| `Less` | 4 |
| `GreaterOrEqual` | 5 |
| `LessOrEqual` | 6 |
| `Like` | 7 |
| `NotLike` | 8 |
| `In` | 9 |
| `NotIn` | 10 |
| `Empty` | 11 |
| `NotEmpty` | 12 |
| `AllIn` | 13 |
| `NotAllIn` | 14 |
| `ExactIn` | 15 |
| `NotExactIn` | 16 |
| `Exists` | 17 |

#### `Block.Content.Dataview.Filter.Operator`

| 值 | 编号 |
|---|---|
| `No` | 0 |
| `Or` | 1 |
| `And` | 2 |

#### `Block.Content.Dataview.Filter.QuickOption`

| 值 | 编号 |
|---|---|
| `ExactDate` | 0 |
| `Yesterday` | 1 |
| `Today` | 2 |
| `Tomorrow` | 3 |
| `LastWeek` | 4 |
| `CurrentWeek` | 5 |
| `NextWeek` | 6 |
| `LastMonth` | 7 |
| `CurrentMonth` | 8 |
| `NextMonth` | 9 |
| `NumberOfDaysAgo` | 10 |
| `NumberOfDaysNow` | 11 |
| `LastYear` | 12 |
| `CurrentYear` | 13 |
| `NextYear` | 14 |

#### `Block.Content.Dataview.Relation.DateFormat`

| 值 | 编号 |
|---|---|
| `MonthAbbrBeforeDay` | 0 |
| `MonthAbbrAfterDay` | 1 |
| `Short` | 2 |
| `ShortUS` | 3 |
| `ISO` | 4 |

#### `Block.Content.Dataview.Relation.FormulaType`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Count` | 1 |
| `CountValue` | 2 |
| `CountDistinct` | 3 |
| `CountEmpty` | 4 |
| `CountNotEmpty` | 5 |
| `PercentEmpty` | 6 |
| `PercentNotEmpty` | 7 |
| `MathSum` | 8 |
| `MathAverage` | 9 |
| `MathMedian` | 10 |
| `MathMin` | 11 |
| `MathMax` | 12 |
| `Range` | 13 |

#### `Block.Content.Dataview.Relation.TimeFormat`

| 值 | 编号 |
|---|---|
| `Format12` | 0 |
| `Format24` | 1 |

#### `Block.Content.Dataview.Sort.EmptyType`

| 值 | 编号 |
|---|---|
| `NotSpecified` | 0 |
| `Start` | 1 |
| `End` | 2 |

#### `Block.Content.Dataview.Sort.Type`

| 值 | 编号 |
|---|---|
| `Asc` | 0 |
| `Desc` | 1 |
| `Custom` | 2 |

#### `Block.Content.Dataview.View.ListSize`

| 值 | 编号 |
|---|---|
| `Compact` | 0 |
| `Regular` | 1 |

#### `Block.Content.Dataview.View.Size`

| 值 | 编号 |
|---|---|
| `Small` | 0 |
| `Medium` | 1 |
| `Large` | 2 |

#### `Block.Content.Dataview.View.Type`

| 值 | 编号 |
|---|---|
| `Table` | 0 |
| `List` | 1 |
| `Gallery` | 2 |
| `Kanban` | 3 |
| `Calendar` | 4 |
| `Graph` | 5 |

#### `Block.Content.Div.Style`

| 值 | 编号 |
|---|---|
| `Line` | 0 |
| `Dots` | 1 |

#### `Block.Content.File.State`

| 值 | 编号 |
|---|---|
| `Empty` | 0 |
| `Uploading` | 1 |
| `Done` | 2 |
| `Error` | 3 |

#### `Block.Content.File.Style`

| 值 | 编号 |
|---|---|
| `Auto` | 0 |
| `Link` | 1 |
| `Embed` | 2 |

#### `Block.Content.File.Type`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `File` | 1 |
| `Image` | 2 |
| `Video` | 3 |
| `Audio` | 4 |
| `PDF` | 5 |

#### `Block.Content.Latex.Processor`

| 值 | 编号 |
|---|---|
| `Latex` | 0 |
| `Mermaid` | 1 |
| `Chart` | 2 |
| `Youtube` | 3 |
| `Vimeo` | 4 |
| `Soundcloud` | 5 |
| `GoogleMaps` | 6 |
| `Miro` | 7 |
| `Figma` | 8 |
| `Twitter` | 9 |
| `OpenStreetMap` | 10 |
| `Reddit` | 11 |
| `Facebook` | 12 |
| `Instagram` | 13 |
| `Telegram` | 14 |
| `GithubGist` | 15 |
| `Codepen` | 16 |
| `Bilibili` | 17 |
| `Excalidraw` | 18 |
| `Kroki` | 19 |
| `Graphviz` | 20 |
| `Sketchfab` | 21 |
| `Image` | 22 |
| `Drawio` | 23 |
| `Spotify` | 24 |

#### `Block.Content.Layout.Style`

| 值 | 编号 |
|---|---|
| `Row` | 0 |
| `Column` | 1 |
| `Div` | 2 |
| `Header` | 3 |
| `TableRows` | 4 |
| `TableColumns` | 5 |

#### `Block.Content.Link.CardStyle`

| 值 | 编号 |
|---|---|
| `Text` | 0 |
| `Card` | 1 |
| `Inline` | 2 |

#### `Block.Content.Link.Description`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Added` | 1 |
| `Content` | 2 |

#### `Block.Content.Link.IconSize`

| 值 | 编号 |
|---|---|
| `SizeNone` | 0 |
| `SizeSmall` | 1 |
| `SizeMedium` | 2 |

#### `Block.Content.Link.Style`

| 值 | 编号 |
|---|---|
| `Page` | 0 |
| `Dataview` | 1 |
| `Dashboard` | 2 |
| `Archive` | 3 |

#### `Block.Content.Text.Mark.Type`

| 值 | 编号 |
|---|---|
| `Strikethrough` | 0 |
| `Keyboard` | 1 |
| `Italic` | 2 |
| `Bold` | 3 |
| `Underscored` | 4 |
| `Link` | 5 |
| `TextColor` | 6 |
| `BackgroundColor` | 7 |
| `Mention` | 8 |
| `Emoji` | 9 |
| `Object` | 10 |

#### `Block.Content.Text.Style`

| 值 | 编号 |
|---|---|
| `Paragraph` | 0 |
| `Header1` | 1 |
| `Header2` | 2 |
| `Header3` | 3 |
| `Header4` | 4 |
| `Quote` | 5 |
| `Code` | 6 |
| `Title` | 7 |
| `Checkbox` | 8 |
| `Marked` | 9 |
| `Numbered` | 10 |
| `Toggle` | 11 |
| `Description` | 12 |
| `Callout` | 13 |
| `ToggleHeader1` | 14 |
| `ToggleHeader2` | 15 |
| `ToggleHeader3` | 16 |

#### `Block.Content.Widget.Layout`

| 值 | 编号 |
|---|---|
| `Link` | 0 |
| `Tree` | 1 |
| `List` | 2 |
| `CompactList` | 3 |
| `View` | 4 |

#### `Block.Position`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Top` | 1 |
| `Bottom` | 2 |
| `Left` | 3 |
| `Right` | 4 |
| `Inner` | 5 |
| `Replace` | 6 |
| `InnerFirst` | 7 |

#### `Block.VerticalAlign`

| 值 | 编号 |
|---|---|
| `VerticalAlignTop` | 0 |
| `VerticalAlignMiddle` | 1 |
| `VerticalAlignBottom` | 2 |

#### `ChatMessage.Attachment.AttachmentType`

| 值 | 编号 |
|---|---|
| `FILE` | 0 |
| `IMAGE` | 1 |
| `LINK` | 2 |

#### `ChatMessage.MessageBlockLink.LinkType`

| 值 | 编号 |
|---|---|
| `Object` | 0 |
| `File` | 1 |
| `Image` | 2 |
| `Bookmark` | 3 |

#### `DeviceNetworkType`

| 值 | 编号 |
|---|---|
| `WIFI` | 0 |
| `CELLULAR` | 1 |
| `NOT_CONNECTED` | 2 |

#### `Export.Format`

| 值 | 编号 |
|---|---|
| `Markdown` | 0 |
| `Protobuf` | 1 |
| `JSON` | 2 |
| `DOT` | 3 |
| `SVG` | 4 |
| `GRAPH_JSON` | 5 |
| `AnyBlockV2` | 6 |

#### `FileIndexingStatus`

| 值 | 编号 |
|---|---|
| `NotIndexed` | 0 |
| `Indexed` | 1 |
| `NotFound` | 2 |

#### `ImageKind`

| 值 | 编号 |
|---|---|
| `Basic` | 0 |
| `Cover` | 1 |
| `Icon` | 2 |
| `AutomaticallyAdded` | 3 |

#### `Import.ErrorCode`

| 值 | 编号 |
|---|---|
| `NULL` | 0 |
| `UNKNOWN_ERROR` | 1 |
| `BAD_INPUT` | 2 |
| `INTERNAL_ERROR` | 3 |
| `FILE_LOAD_ERROR` | 8 |
| `IMPORT_IS_CANCELED` | 6 |
| `NOTION_NO_OBJECTS_IN_INTEGRATION` | 5 |
| `NOTION_SERVER_IS_UNAVAILABLE` | 12 |
| `NOTION_RATE_LIMIT_EXCEEDED` | 13 |
| `FILE_IMPORT_NO_OBJECTS_IN_ZIP_ARCHIVE` | 14 |
| `FILE_IMPORT_NO_OBJECTS_IN_DIRECTORY` | 17 |
| `HTML_WRONG_HTML_STRUCTURE` | 10 |
| `PB_NOT_ANYBLOCK_FORMAT` | 11 |
| `CSV_LIMIT_OF_ROWS_OR_RELATIONS_EXCEEDED` | 7 |
| `INSUFFICIENT_PERMISSIONS` | 9 |

#### `Import.Type`

| 值 | 编号 |
|---|---|
| `Notion` | 0 |
| `Markdown` | 1 |
| `External` | 2 |
| `Pb` | 3 |
| `Html` | 4 |
| `Txt` | 5 |
| `Csv` | 6 |
| `Obsidian` | 7 |

#### `InternalFlag.Value`

> Use such a weird construction due to the issue with imported repeated enum type Look https://github.com/golang/protobuf/issues/1135 for more information.

| 值 | 编号 |
|---|---|
| `editorDeleteEmpty` | 0 |
| `editorSelectType` | 1 |
| `editorSelectTemplate` | 2 |
| `collectionDontIndexLinks` | 3 |

#### `InviteType`

| 值 | 编号 |
|---|---|
| `Member` | 0 |
| `Guest` | 1 |
| `WithoutApprove` | 2 |

#### `LinkPreview.Type`

| 值 | 编号 |
|---|---|
| `Unknown` | 0 |
| `Page` | 1 |
| `Image` | 2 |
| `Text` | 3 |

#### `Membership.EmailVerificationStatus`

| 值 | 编号 |
|---|---|
| `StatusNotVerified` | 0 |
| `StatusCodeSent` | 1 |
| `StatusVerified` | 2 |

#### `Membership.PaymentMethod`

| 值 | 编号 |
|---|---|
| `MethodNone` | 0 |
| `MethodStripe` | 1 |
| `MethodCrypto` | 2 |
| `MethodInappApple` | 3 |
| `MethodInappGoogle` | 4 |

#### `Membership.Status`

| 值 | 编号 |
|---|---|
| `StatusUnknown` | 0 |
| `StatusPending` | 1 |
| `StatusActive` | 2 |
| `StatusPendingRequiresFinalization` | 3 |

#### `MembershipTierData.PeriodType`

| 值 | 编号 |
|---|---|
| `PeriodTypeUnknown` | 0 |
| `PeriodTypeUnlimited` | 1 |
| `PeriodTypeDays` | 2 |
| `PeriodTypeWeeks` | 3 |
| `PeriodTypeMonths` | 4 |
| `PeriodTypeYears` | 5 |

#### `MembershipV2.PaymentProvider`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Stripe` | 1 |
| `Crypto` | 2 |
| `BillingPortal` | 3 |
| `AppStore` | 4 |
| `GooglePlay` | 5 |

#### `MembershipV2.Period`

| 值 | 编号 |
|---|---|
| `Monthly` | 1 |
| `Yearly` | 2 |
| `ThreeYears` | 3 |
| `Lifetime` | 4 |

#### `MembershipV2.Platform`

| 值 | 编号 |
|---|---|
| `Unknown` | 0 |
| `Desktop` | 1 |
| `MobileIOS` | 2 |
| `MobileAndroid` | 3 |
| `Web` | 4 |

#### `MembershipV2.ProductStatus.Status`

| 值 | 编号 |
|---|---|
| `StatusUnknown` | 0 |
| `StatusPending` | 1 |
| `StatusActive` | 2 |
| `StatusPendingRequiresAnyNameAllocation` | 3 |

#### `NameserviceNameType`

| 值 | 编号 |
|---|---|
| `AnyName` | 0 |

#### `Notification.ActionType`

| 值 | 编号 |
|---|---|
| `CLOSE` | 0 |

#### `Notification.Export.Code`

| 值 | 编号 |
|---|---|
| `NULL` | 0 |
| `UNKNOWN_ERROR` | 1 |
| `BAD_INPUT` | 2 |

#### `Notification.Status`

| 值 | 编号 |
|---|---|
| `Created` | 0 |
| `Shown` | 1 |
| `Read` | 2 |
| `Replied` | 3 |

#### `ObjectOrigin`

| 值 | 编号 |
|---|---|
| `none` | 0 |
| `clipboard` | 1 |
| `dragAndDrop` | 2 |
| `import` | 3 |
| `webclipper` | 4 |
| `sharingExtension` | 5 |
| `usecase` | 6 |
| `builtin` | 7 |
| `bookmark` | 8 |
| `api` | 9 |

#### `ObjectType.Layout`

| 值 | 编号 |
|---|---|
| `basic` | 0 |
| `profile` | 1 |
| `todo` | 2 |
| `set` | 3 |
| `objectType` | 4 |
| `relation` | 5 |
| `file` | 6 |
| `dashboard` | 7 |
| `image` | 8 |
| `note` | 9 |
| `space` | 10 |
| `bookmark` | 11 |
| `relationOptionsList` | 12 |
| `relationOption` | 13 |
| `collection` | 14 |
| `audio` | 15 |
| `video` | 16 |
| `date` | 17 |
| `spaceView` | 18 |
| `participant` | 19 |
| `pdf` | 20 |
| `chatDeprecated` | 21 |
| `chatDerived` | 22 |
| `tag` | 23 |
| `notification` | 24 |
| `missingObject` | 25 |
| `devices` | 26 |
| `discussion` | 27 |

#### `ParticipantPermissions`

| 值 | 编号 |
|---|---|
| `Reader` | 0 |
| `Writer` | 1 |
| `Owner` | 2 |
| `NoPermissions` | 3 |
| `Admin` | 4 |

#### `ParticipantStatus`

| 值 | 编号 |
|---|---|
| `Joining` | 0 |
| `Active` | 1 |
| `Removed` | 2 |
| `Declined` | 3 |
| `Removing` | 4 |
| `Canceled` | 5 |

#### `Placeholder.Type`

| 值 | 编号 |
|---|---|
| `PlaceholderValue` | 0 |
| `PlaceholderToday` | 1 |
| `PlaceholderCurrentUser` | 2 |

#### `Relation.DataSource`

| 值 | 编号 |
|---|---|
| `details` | 0 |
| `derived` | 1 |
| `account` | 2 |
| `local` | 3 |

#### `Relation.Scope`

| 值 | 编号 |
|---|---|
| `object` | 0 |
| `type` | 1 |
| `setOfTheSameType` | 2 |
| `objectsOfTheSameType` | 3 |
| `library` | 4 |

#### `RelationFormat`

> RelationFormat describes how the underlying data is stored in the google.protobuf.Value and how it should be validated/sanitized

| 值 | 编号 |
|---|---|
| `longtext` | 0 |
| `shorttext` | 1 |
| `number` | 2 |
| `status` | 3 |
| `tag` | 11 |
| `date` | 4 |
| `file` | 5 |
| `checkbox` | 6 |
| `url` | 7 |
| `email` | 8 |
| `phone` | 9 |
| `emoji` | 10 |
| `object` | 100 |
| `relations` | 101 |
| `map` | 102 |

#### `Restrictions.DataviewRestriction`

| 值 | 编号 |
|---|---|
| `DVNone` | 0 |
| `DVRelation` | 1 |
| `DVCreateObject` | 2 |
| `DVViews` | 3 |

#### `Restrictions.ObjectRestriction`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Delete` | 1 |
| `Relations` | 2 |
| `Blocks` | 3 |
| `Details` | 4 |
| `TypeChange` | 5 |
| `LayoutChange` | 6 |
| `Template` | 7 |
| `Duplicate` | 8 |
| `CreateObjectOfThisType` | 9 |
| `Publish` | 10 |

#### `Search.Message.Sort.Key`

| 值 | 编号 |
|---|---|
| `ORDER_ID` | 0 |
| `SCORE` | 1 |
| `CREATED_AT` | 2 |
| `MODIFIED_AT` | 3 |

#### `Search.Message.Sort.Type`

| 值 | 编号 |
|---|---|
| `Asc` | 0 |
| `Desc` | 1 |

#### `SmartBlockType`

| 值 | 编号 |
|---|---|
| `AccountOld` | 0 |

#### `SpaceAccessType`

| 值 | 编号 |
|---|---|
| `Private` | 0 |
| `Personal` | 1 |
| `Shared` | 2 |

#### `SpaceShareableStatus`

| 值 | 编号 |
|---|---|
| `StatusUnknown` | 0 |
| `StatusShareable` | 1 |
| `StatusNotShareable` | 2 |

#### `SpaceStatus`

| 值 | 编号 |
|---|---|
| `Unknown` | 0 |
| `Loading` | 1 |
| `Ok` | 2 |
| `Missing` | 3 |
| `Error` | 4 |
| `RemoteWaitingDeletion` | 5 |
| `RemoteDeleted` | 6 |
| `SpaceDeleted` | 7 |
| `SpaceActive` | 8 |
| `SpaceJoining` | 9 |
| `SpaceRemoving` | 10 |

#### `SpaceType`

| 值 | 编号 |
|---|---|
| `SpaceTypeUnknown` | 0 |
| `SpaceTypeRegular` | 1 |
| `SpaceTypeTech` | 2 |
| `SpaceTypeChat` | 3 |
| `SpaceTypeOneToOne` | 4 |

#### `SpaceUxType`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Data` | 1 |
| `Stream` | 2 |
| `Chat` | 3 |
| `OneToOne` | 4 |

#### `SyncError`

| 值 | 编号 |
|---|---|
| `SyncErrorNull` | 0 |
| `SyncErrorIncompatibleVersion` | 2 |
| `SyncErrorNetworkError` | 3 |
| `SyncErrorOversized` | 4 |

#### `SyncStatus`

| 值 | 编号 |
|---|---|
| `SyncStatusSynced` | 0 |
| `SyncStatusSyncing` | 1 |
| `SyncStatusError` | 2 |
| `SyncStatusQueued` | 3 |

#### `TemplateNamePrefillType`

| 值 | 编号 |
|---|---|
| `Empty` | 0 |
| `FromTemplateName` | 1 |


### any-sync-node/nodesync/nodesyncproto/protos/nodesync.proto

#### `AdoptArchiveResult`

| 值 | 编号 |
|---|---|
| `AdoptArchiveOk` | 0 |
| `AdoptArchiveAlreadyHaveSame` | 1 |
| `AdoptArchiveAlreadyHaveDiverged` | 2 |

#### `ColdSyncProtocolType`

| 值 | 编号 |
|---|---|
| `Pogreb` | 0 |
| `AnystoreSqlite` | 1 |

#### `ErrCodes`

| 值 | 编号 |
|---|---|
| `Unexpected` | 0 |
| `ExpectedCoordinator` | 1 |
| `UnsupportedStorage` | 2 |
| `SpaceDeleted` | 3 |
| `ArchiveUnavailable` | 4 |
| `ArchiveObjectMissing` | 5 |
| `PeerIsNotNode` | 6 |
| `NotResponsible` | 7 |
| `SpacePendingDeletion` | 8 |
| `ErrorOffset` | 1000 |


### any-sync/commonfile/fileproto/filep2p/protos/filep2p.proto

#### `Availability`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Partial` | 1 |
| `Full` | 2 |

#### `ErrCodes`

> ErrCodes are WHOLE-RPC (drpc-level) errors, mirroring v1 filesync.ErrCodes and v2's fileprotov2.ErrCodes. Wired through rpcerr.ErrGroup(ErrorOffset) in the filep2perr package. Offset 900 is the next free rpcerr block (v1=200, v2=800). Zero value Unexpected=0 registers at offset+0 so an uncoded fault reads as Unexpected.

| 值 | 编号 |
|---|---|
| `Unexpected` | 0 |
| `Forbidden` | 1 |
| `InvalidRequest` | 2 |
| `FileNotFound` | 3 |
| `ErrorOffset` | 900 |


### any-sync/commonfile/fileproto/fileprotov2/protos/filev2.proto

#### `ErrCode`

> ErrCode is the PER-ITEM, in-body business outcome (err == nil at the RPC layer). Flat status enum with an explicit success sentinel Ok=0. The typed payload on a *Result is valid ONLY when code == Ok. Deliberately a SEPARATE enum from ErrCodes: its zero value means success (not error), it never flows through rpcerr, and its value short-names are kept disjoint from ErrCodes so proto3's package-level enum-value scoping stays clean. Servers MUST set `code` explicitly on every result (Ok is the proto3 default, so an unset code would be misread as a success with an empty payload).

| 值 | 编号 |
|---|---|
| `Ok` | 0 |
| `ErrUnexpected` | 1 |
| `ErrCidNotFound` | 2 |
| `ErrForbidden` | 3 |
| `ErrLimitExceeded` | 4 |
| `ErrSpaceNotFound` | 5 |
| `ErrNotResponsible` | 6 |

#### `ErrCodes`

> ErrCodes are WHOLE-RPC (drpc-level) errors, mirroring v1 filesync.ErrCodes. Wired through rpcerr.ErrGroup(ErrCodes_ErrorOffset) in the fileprotov2err package. Returned as a NON-nil drpc error ONLY for auth / malformed / batch-too-large / misrouted. Never used to report the outcome of an individual item (that is the per-item ErrCode below). Zero value Unexpected=0 registers at offset+0 (=800), so an uncoded server fault reads as Unexpected — exactly as v1 does at 200. Offset 800 is the only free rpcerr block (v1=200, 100/300/400/500/600/700 are taken).

| 值 | 编号 |
|---|---|
| `Unexpected` | 0 |
| `Forbidden` | 1 |
| `InvalidRequest` | 2 |
| `QuerySizeExceeded` | 3 |
| `NotResponsible` | 4 |
| `ErrorOffset` | 800 |


### any-sync/commonfile/fileproto/protos/file.proto

#### `AvailabilityStatus`

| 值 | 编号 |
|---|---|
| `NotExists` | 0 |
| `Exists` | 1 |
| `ExistsInSpace` | 2 |

#### `ErrCodes`

| 值 | 编号 |
|---|---|
| `Unexpected` | 0 |
| `CIDNotFound` | 1 |
| `Forbidden` | 2 |
| `_DeprecatedLimitExceeded` | 3 |
| `QuerySizeExceeded` | 4 |
| `WrongHash` | 5 |
| `NotEnoughSpace` | 6 |
| `AclRecordNotFound` | 7 |
| `LimitExceeded` | 8 |
| `ErrorOffset` | 200 |


### any-sync/commonspace/object/acl/aclrecordproto/protos/aclrecord.proto

#### `AclInviteType`

| 值 | 编号 |
|---|---|
| `RequestToJoin` | 0 |
| `AnyoneCanJoin` | 1 |

#### `AclUserPermissions`

> AclUserPermissions contains different possible user roles

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Owner` | 1 |
| `Admin` | 2 |
| `Writer` | 3 |
| `Reader` | 4 |
| `Guest` | 5 |


### any-sync/commonspace/object/tree/treechangeproto/protos/treechange.proto

#### `ErrorCodes`

| 值 | 编号 |
|---|---|
| `Unexpected` | 0 |
| `GetTreeError` | 1 |
| `FullSyncRequestError` | 2 |
| `ErrorOffset` | 400 |


### any-sync/commonspace/pubsub/pubsubproto/protos/pubsub.proto

#### `ErrCodes`

| 值 | 编号 |
|---|---|
| `Unexpected` | 0 |
| `NotAMember` | 1 |
| `NotResponsible` | 2 |
| `RateLimited` | 3 |
| `TooManyTopics` | 4 |
| `InvalidMessage` | 5 |
| `TopicNotOwned` | 6 |
| `InvalidTopic` | 7 |
| `ErrorOffset` | 1100 |


### any-sync/commonspace/spacesyncproto/protos/spacesync.proto

#### `DiffType`

> DiffType is a type of diff

| 值 | 编号 |
|---|---|
| `Initial` | 0 |
| `V1` | 1 |
| `V2` | 2 |
| `V3` | 3 |

#### `ErrCodes`

| 值 | 编号 |
|---|---|
| `Unexpected` | 0 |
| `SpaceMissing` | 1 |
| `SpaceExists` | 2 |
| `SpaceNotInCache` | 3 |
| `SpaceIsDeleted` | 4 |
| `PeerIsNotResponsible` | 5 |
| `ReceiptIsInvalid` | 6 |
| `InvalidPayload` | 7 |
| `DuplicateRequest` | 8 |
| `TooManyRequestsFromPeer` | 9 |
| `ErrorOffset` | 100 |

#### `ObjectType`

> ObjectType is a type of object

| 值 | 编号 |
|---|---|
| `Tree` | 0 |
| `Acl` | 1 |
| `KeyValue` | 2 |

#### `SpaceFileProtoVersion`

> SpaceFileProtoVersion gates the file protocol a space uses. It lives in the signed, immutable header so it can't be stripped/downgraded without invalidating the owner signature.

| 值 | 编号 |
|---|---|
| `SpaceFileProtoVersionUnspecified` | 0 |
| `SpaceFileProtoVersionV2` | 2 |

#### `SpaceHeaderVersion`

| 值 | 编号 |
|---|---|
| `SpaceHeaderVersion0` | 0 |
| `SpaceHeaderVersion1` | 1 |

#### `SpaceSubscriptionAction`

> SpaceSubscription contains in ObjectSyncMessage.Payload and indicates that we need to subscribe or unsubscribe the current stream to this space

| 值 | 编号 |
|---|---|
| `Subscribe` | 0 |
| `Unsubscribe` | 1 |


### any-sync/consensus/consensusproto/protos/consensus.proto

#### `ErrCodes`

| 值 | 编号 |
|---|---|
| `Unexpected` | 0 |
| `LogExists` | 1 |
| `LogNotFound` | 2 |
| `RecordConflict` | 3 |
| `Forbidden` | 4 |
| `InvalidPayload` | 5 |
| `ErrorOffset` | 500 |


### any-sync/coordinator/coordinatorproto/protos/coordinator.proto

#### `AclEventLogRecordType`

| 值 | 编号 |
|---|---|
| `RecordTypeSpaceReceipt` | 0 |
| `RecordTypeSpaceShared` | 1 |
| `RecordTypeSpaceUnshared` | 2 |
| `RecordTypeSpaceAclAddRecord` | 3 |

#### `DeletionLogRecordStatus`

| 值 | 编号 |
|---|---|
| `Ok` | 0 |
| `RemovePrepare` | 1 |
| `Remove` | 2 |
| `OwnershipChange` | 3 |

#### `DeletionPayloadType`

> DeletionChangeType determines the type of deletion payload

| 值 | 编号 |
|---|---|
| `Tree` | 0 |
| `Confirm` | 1 |
| `Account` | 2 |

#### `ErrorCodes`

| 值 | 编号 |
|---|---|
| `Unexpected` | 0 |
| `SpaceDeleted` | 1 |
| `SpaceDeletionPending` | 2 |
| `SpaceCreated` | 3 |
| `SpaceNotExists` | 4 |
| `SpaceLimitReached` | 5 |
| `AccountDeleted` | 6 |
| `Forbidden` | 7 |
| `AclHeadIsMissing` | 8 |
| `AclNonEmpty` | 9 |
| `SpaceNotShareable` | 10 |
| `InboxMessageVerifyFailed` | 11 |
| `SubscribePeerAlreadySubscribed` | 12 |
| `InviteStillActive` | 13 |
| `ErrorOffset` | 300 |

#### `InboxKeyType`

| 值 | 编号 |
|---|---|
| `ed25519` | 0 |

#### `InboxPacketType`

> Inbox Message

| 值 | 编号 |
|---|---|
| `Default` | 0 |

#### `InboxPayloadType`

| 值 | 编号 |
|---|---|
| `InboxPayloadOneToOneInvite` | 0 |
| `InboxPayloadRegularInvite` | 1 |

#### `NodeType`

> NodeType determines the type of API that a node supports

| 值 | 编号 |
|---|---|
| `TreeAPI` | 0 |
| `FileAPI` | 1 |
| `CoordinatorAPI` | 2 |
| `ConsensusAPI` | 3 |
| `NamingNodeAPI` | 4 |
| `PaymentProcessingAPI` | 5 |
| `FileV2API` | 6 |

#### `NotifyEventType`

> Enum for event types

| 值 | 编号 |
|---|---|
| `UnspecifiedEvent` | 0 |
| `InboxNewMessageEvent` | 1 |
| `NetworkConfigChangedEvent` | 2 |

#### `SpacePermissions`

| 值 | 编号 |
|---|---|
| `SpacePermissionsUnknown` | 0 |
| `SpacePermissionsOwner` | 1 |

#### `SpaceStatus`

| 值 | 编号 |
|---|---|
| `SpaceStatusCreated` | 0 |
| `SpaceStatusPendingDeletion` | 1 |
| `SpaceStatusDeletionStarted` | 2 |
| `SpaceStatusDeleted` | 3 |
| `SpaceStatusNotExists` | 4 |


### any-sync/nameservice/nameserviceproto/protos/nameservice_aa.proto

#### `OperationState`

| 值 | 编号 |
|---|---|
| `OpUnknown` | 0 |
| `Pending` | 1 |
| `PendingOrNotFound` | 2 |
| `Completed` | 3 |
| `Error` | 4 |


### any-sync/net/rpc/limiter/limiterproto/protos/limiter.proto

#### `ErrCodes`

| 值 | 编号 |
|---|---|
| `RateLimitExceeded` | 0 |
| `ErrorOffset` | 700 |


### any-sync/net/secureservice/handshake/handshakeproto/protos/handshake.proto

#### `CredentialsType`

| 值 | 编号 |
|---|---|
| `SkipVerify` | 0 |
| `SignedPeerIds` | 1 |

#### `Encoding`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Snappy` | 1 |

#### `Error`

| 值 | 编号 |
|---|---|
| `Null` | 0 |
| `Unexpected` | 1 |
| `InvalidCredentials` | 2 |
| `UnexpectedPayload` | 3 |
| `SkipVerifyNotAllowed` | 4 |
| `DeadlineExceeded` | 5 |
| `IncompatibleVersion` | 6 |
| `IncompatibleProto` | 7 |

#### `ProtoType`

| 值 | 编号 |
|---|---|
| `DRPC` | 0 |


### any-sync/paymentservice/paymentserviceproto/protos/paymentservice.proto

#### `ErrorCodes`

| 值 | 编号 |
|---|---|
| `Unexpected` | 0 |
| `EthAddressEmpty` | 1 |
| `InvalidSignature` | 2 |
| `TierWrong` | 3 |
| `TierNotFound` | 4 |
| `TierInactive` | 5 |
| `PaymentMethodWrong` | 6 |
| `BadAnyName` | 7 |
| `Unknown` | 8 |
| `SubsAlreadyActive` | 9 |
| `SubsNotFound` | 10 |
| `SubsWrongState` | 11 |
| `EmailWrongFormat` | 12 |
| `EmailAlreadyVerified` | 13 |
| `EmailAlreadySent` | 14 |
| `EmailFailedToSend` | 15 |
| `EmailExpired` | 16 |
| `EmailWrongCode` | 17 |
| `AppleInvalidReceipt` | 18 |
| `ApplePurchaseRegistration` | 19 |
| `AppleSubscriptionRenew` | 20 |
| `CodeNotFound` | 21 |
| `CodeAlreadyUsed` | 22 |
| `ErrorOffset` | 600 |

#### `IsNameValidResponse.Code`

| 值 | 编号 |
|---|---|
| `Valid` | 0 |
| `NoDotAny` | 1 |
| `TooShort` | 2 |
| `TooLong` | 3 |
| `HasInvalidChars` | 4 |
| `TierFeatureNoName` | 5 |
| `CanNotReserve` | 6 |

#### `PaymentMethod`

| 值 | 编号 |
|---|---|
| `MethodCard` | 0 |
| `MethodCrypto` | 1 |
| `MethodApplePay` | 2 |
| `MethodGooglePay` | 3 |
| `MethodAppleInapp` | 4 |
| `MethodGoogleInapp` | 5 |
| `MethodNone` | 6 |

#### `SubscriptionStatus`

| 值 | 编号 |
|---|---|
| `StatusUnknown` | 0 |
| `StatusPending` | 1 |
| `StatusActive` | 2 |
| `StatusPendingRequiresFinalization` | 3 |

#### `SubscriptionTier`

> TODO: later we will have an interface to enumerate all available tiers it's a bad idea to list them here, because interface will be changed often

| 值 | 编号 |
|---|---|
| `TierUnknown` | 0 |
| `TierExplorer` | 1 |
| `TierBuilder1WeekTEST` | 2 |
| `TierCoCreator1WeekTEST` | 3 |
| `TierBuilder1Year` | 4 |
| `TierCoCreator1Year` | 5 |
| `TierBuilderPlus` | 6 |
| `TierAnytypeTeam` | 7 |


### any-sync/paymentservice/paymentserviceproto/protos/paymentservice2.proto

#### `MembershipV2.AnyNameIsValidResponse.Code`

| 值 | 编号 |
|---|---|
| `Valid` | 0 |
| `NoDotAny` | 1 |
| `TooShort` | 2 |
| `TooLong` | 3 |
| `HasInvalidChars` | 4 |
| `AccountHasNoName` | 5 |
| `CanNotReserve` | 6 |

#### `MembershipV2.Invoice.Status`

| 值 | 编号 |
|---|---|
| `Unpaid` | 0 |
| `Paid` | 1 |

#### `MembershipV2.PaymentProvider`

| 值 | 编号 |
|---|---|
| `None` | 0 |
| `Stripe` | 1 |
| `Crypto` | 2 |
| `BillingPortal` | 3 |
| `AppStore` | 4 |
| `GooglePlay` | 5 |

#### `MembershipV2.Period`

| 值 | 编号 |
|---|---|
| `Monthly` | 1 |
| `Yearly` | 2 |
| `ThreeYears` | 3 |
| `Lifetime` | 4 |

#### `MembershipV2.Platform`

| 值 | 编号 |
|---|---|
| `Unknown` | 0 |
| `Desktop` | 1 |
| `MobileIOS` | 2 |
| `MobileAndroid` | 3 |
| `Web` | 4 |

#### `MembershipV2.ProductStatus.Status`

| 值 | 编号 |
|---|---|
| `StatusUnknown` | 0 |
| `StatusPending` | 1 |
| `StatusActive` | 2 |
| `StatusPendingRequiresFinalization` | 3 |


### any-sync/paymentservice/paymentserviceproto/protos/paymentservice_tiers.proto

#### `PeriodType`

| 值 | 编号 |
|---|---|
| `PeriodTypeUnknown` | 0 |
| `PeriodTypeUnlimited` | 1 |
| `PeriodTypeDays` | 2 |
| `PeriodTypeWeeks` | 3 |
| `PeriodTypeMonths` | 4 |
| `PeriodTypeYears` | 5 |


### any-sync/util/crypto/cryptoproto/protos/crypto.proto

#### `KeyType`

| 值 | 编号 |
|---|---|
| `Ed25519Public` | 0 |
| `Ed25519Private` | 1 |
| `AES` | 2 |


## 五、附录

### 5.1 测试服务

- `net/endtoendtest/testpeer/testproto/protos/testservice.proto`（pkg `testService`，`Test` 4 个方法）：端到端测试用。
- `net/streampool/testservice/protos/testservice.proto`（pkg `testService`，`Test` 2 个方法）：streampool 压力测试用。

### 5.2 与客户端学习路径的关系

- **你自研客户端实际要打交道的服务**（按通信对象）：
  - coordinator → `Coordinator`（22 方法：空间路由、网络配置、空间操作）
  - sync node → `SpaceSync`（10）、`PubSub`（1）、`ClientSpace`（2）
  - filenode → `File`（14）、`FileV2`（5）
  - 其他客户端 → `FileP2P`（2）
  - 可选：`IdentityRepo`（3）、`Anyns`（8）、`AnynsAccountAbstraction`（7）、`AnyPaymentProcessing`（11）、`AnyPaymentProcessingV2`（8）
- **节点间服务（你一般不需要直接实现，但理解协议需要）**：`Consensus`（4）、`NodeSync`（3）。
- 消息结构章节里标 `aclrecord` / `treechange` 的包是**变更日志与 ACL 记录的格式定义**，是理解"追加式变更日志 + 版本溯源"的关键，虽然它们没有 RPC。

### 5.3 数据格式（any-block）

`any-block/format/v1/proto/` 是对象数据格式定义（`models.proto` 125 消息 / `events.proto` 226 消息 / `changes.proto` 34 消息 / `snapshot.proto` 3 消息），已含在上述消息统计中。它定义"一条变更长什么样、对象状态如何序列化"，是你自研客户端存储层的基础。
