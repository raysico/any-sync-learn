
> 📌 本文档为《any-sync 协议 Protobuf 接口参考》系列第 3 篇：消息结构 · 协议层（文件 / 空间 / 共识 / 协调器 / 名称 / 支付等）。

### any-block/format/v1/proto/snapshot.proto

#### `Profile`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `name` |  |
| 2 | `repeated string` | `avatar` |  |
| 4 | `repeated string` | `address` |  |
| 5 | `repeated string` | `spaceDashboardId` |  |
| 6 | `repeated string` | `profileId` |  |
| 7 | `repeated string` | `analyticsId` |  |
| 8 | `repeated string` | `startingPage` |  |
| 9 | `repeated WidgetBlock` | `widgets` |  |

#### `SnapshotWithType`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated anytype.model.SmartBlockType` | `sbType` |  |
| 2 | `repeated anytype.Change.Snapshot` | `snapshot` |  |

#### `WidgetBlock`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated model.Block.Content.Widget.Layout` | `layout` |  |
| 2 | `repeated string` | `targetObjectId` |  |
| 3 | `repeated int32` | `objectLimit` |  |


### any-sync-filenode/index/indexproto/protos/index.proto

#### `CidEntry`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `size` |  |
| 2 | `repeated int64` | `createTime` |  |
| 3 | `repeated int64` | `updateTime` |  |
| 4 | `repeated int32` | `refs` |  |
| 5 | `repeated uint32` | `version` |  |

#### `CidList`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `cids` |  |

#### `FileEntry`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `cids` |  |
| 2 | `repeated uint64` | `size` |  |
| 3 | `repeated int64` | `createTime` |  |
| 4 | `repeated int64` | `updateTime` |  |

#### `GroupEntry`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `groupId` |  |
| 2 | `repeated int64` | `createTime` |  |
| 3 | `repeated int64` | `updateTime` |  |
| 4 | `repeated uint64` | `size` |  |
| 5 | `repeated uint64` | `cidCount` |  |
| 6 | `repeated string` | `spaceIds` |  |
| 7 | `repeated uint64` | `limit` |  |
| 8 | `repeated uint64` | `accountLimit` |  |

#### `OwnershipRecord`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerId` |  |
| 2 | `repeated int64` | `aclRecordIndex` |  |

#### `SpaceEntry`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `groupId` |  |
| 2 | `repeated int64` | `createTime` |  |
| 3 | `repeated int64` | `updateTime` |  |
| 4 | `repeated uint64` | `size` |  |
| 5 | `repeated uint32` | `fileCount` |  |
| 6 | `repeated uint64` | `cidCount` |  |
| 7 | `repeated uint64` | `limit` |  |


### any-sync-node/debug/nodedebugrpc/nodedebugrpcproto/protos/nodedebugrpc.proto

#### `AllSpacesRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `AllSpacesResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceIds` |  |

#### `AllTreesRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |

#### `AllTreesResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Tree` | `trees` |  |

#### `DumpTreeRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `documentId` |  |

#### `DumpTreeResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `dump` |  |

#### `ForceNodeSyncRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `ForceNodeSyncResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `NodesAddressesBySpaceRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |

#### `NodesAddressesBySpaceResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `nodeAddresses` |  |

#### `Tree`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `heads` |  |

#### `TreeParamsRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `documentId` |  |

#### `TreeParamsResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `rootId` |  |
| 2 | `repeated string` | `headIds` |  |


### any-sync-node/nodesync/nodesyncproto/protos/nodesync.proto

#### `AdoptArchiveRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `srcKey` | srcKey is the full key of the gzipped snapshot within the shared bucket (sender's prefix) |
| 3 | `repeated string` | `oldHash` | heads hashes of the space at snapshot time, as stored in the sender's index |
| 4 | `repeated string` | `newHash` |  |
| 5 | `repeated bool` | `eager` | eager asks the receiver to restore the space in background right away |
| 6 | `repeated int64` | `compressedSize` |  |
| 7 | `repeated int64` | `uncompressedSize` |  |

#### `AdoptArchiveResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated AdoptArchiveResult` | `result` |  |

#### `ColdSyncRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated ColdSyncProtocolType` | `protocolType` |  |

#### `ColdSyncResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 2 | `repeated string` | `filename` |  |
| 3 | `repeated bytes` | `data` |  |
| 4 | `repeated uint32` | `crc32` |  |
| 5 | `repeated ColdSyncProtocolType` | `protocolType` |  |

#### `PartitionSyncRange`

> PartitionSyncRange presenting a request for one range

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `from` |  |
| 2 | `repeated uint64` | `to` |  |
| 3 | `repeated uint32` | `limit` |  |
| 4 | `repeated bool` | `elements` |  |

#### `PartitionSyncRequest`

> HeadSyncRequest is a request for HeadSync

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `partitionId` |  |
| 2 | `repeated PartitionSyncRange` | `ranges` |  |

#### `PartitionSyncResponse`

> PartitionSyncResponse is a response for HeadSync

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated PartitionSyncResult` | `results` |  |

#### `PartitionSyncResult`

> PartitionSyncResult presenting a response for one range

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `hash` |  |
| 2 | `repeated PartitionSyncResultElement` | `elements` |  |
| 3 | `repeated uint32` | `count` |  |

#### `PartitionSyncResultElement`

> PartitionSyncResultElement presenting state of one object

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `head` |  |


### any-sync/commonfile/fileproto/filep2p/protos/filep2p.proto

#### `FileAvailability`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `rootCid` |  |
| 2 | `repeated Availability` | `have` |  |

#### `FileCheckRequest`

> ---- FileCheck (availability) ---------------------------------------------

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated bytes` | `rootCids` |  |

#### `FileCheckResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated FileAvailability` | `files` |  |

#### `ObjectReadRequest`

> ---- ObjectRead (ranged CAR bytes) ----------------------------------------

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated bytes` | `rootCid` |  |
| 3 | `repeated uint64` | `offset` |  |
| 4 | `repeated uint32` | `length` |  |

#### `ObjectReadResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `data` |  |
| 2 | `repeated uint64` | `totalSize` |  |


### any-sync/commonfile/fileproto/fileprotov2/protos/filev2.proto

#### `InfoRequest`

> ---- Info (node-level metadata) --------------------------------------------- InfoRequest is deliberately empty: Info is static node metadata, extensible later (capabilities, limits) without a wire break.

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `InfoResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `publicReadBaseUrl` | publicReadBaseUrl, when non-empty, lets clients construct durable object URLs as {publicReadBaseUrl}/blob/{spaceId}/{rootCid} with zero broker round-trips; clients cache it. Empty = no public read: use RequestDownload. |

#### `NetworkSignReceipt`

> NetworkSignReceipt mirrors coordinator SpaceReceiptWithSignature: an opaque protobuf-encoded payload plus the network-key signature over it. The payload schema is intentionally not defined here (opaque blob forwarded verbatim).

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `receiptPayload` |  |
| 2 | `repeated bytes` | `signature` |  |

#### `PresignField`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `key` |  |
| 2 | `repeated string` | `value` |  |

#### `PresignedUpload`

> PresignedUpload is an OPAQUE presigned upload target. No S3 vendor structs leak into the shared proto: the client POSTs `fields` + the object body to `url` verbatim. Modeled as a presigned POST form (fields are ordered key/value pairs rather than a map) so the signing order is deterministic and reproducible.

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `url` |  |
| 2 | `repeated PresignField` | `fields` |  |
| 3 | `repeated uint64` | `maxContentLength` |  |
| 4 | `repeated int64` | `expiry` |  |

#### `RequestDownloadRequest`

> ---- RequestDownload ------------------------------------------------------

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated bytes` | `rootCids` |  |

#### `RequestDownloadResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated RequestDownloadResult` | `results` |  |

#### `RequestDownloadResult`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `rootCid` |  |
| 2 | `repeated ErrCode` | `code` |  |
| 3 | `repeated SignedDownload` | `download` |  |

#### `RequestSignRequest`

> ---- RequestSign ----------------------------------------------------------

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated bytes` | `rootCids` |  |

#### `RequestSignResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated RequestSignResult` | `results` |  |

#### `RequestSignResult`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `rootCid` |  |
| 2 | `repeated ErrCode` | `code` |  |
| 3 | `repeated NetworkSignReceipt` | `receipt` |  |

#### `SignedDownload`

> SignedDownload is an OPAQUE signed GET target (kept as a message, symmetric with PresignedUpload, so download can grow response headers etc. without a wire break on the result envelope).

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `url` |  |
| 2 | `repeated int64` | `expiry` |  |

#### `SpaceInfoRequest`

> ---- SpaceInfo (batch quota-info) -----------------------------------------

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceIds` |  |

#### `SpaceInfoResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SpaceInfoResult` | `results` |  |

#### `SpaceInfoResult`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated ErrCode` | `code` |  |
| 3 | `repeated SpaceQuota` | `quota` |  |

#### `SpaceQuota`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `limitBytes` |  |
| 2 | `repeated uint64` | `totalUsageBytes` |  |
| 3 | `repeated uint64` | `durableUsageBytes` |  |
| 4 | `repeated uint64` | `inflightUsageBytes` |  |
| 5 | `repeated uint64` | `filesCount` |  |
| 6 | `repeated uint64` | `accountLimitBytes` | account-pool view for the requesting identity (files are charged to their uploader; all the identity's spaces share one pool). Zero when the node has no coordinator-backed limits (self-hosted fallback). |
| 7 | `repeated uint64` | `accountUsageBytes` |  |

#### `UploadRequest`

> ---- Upload ---------------------------------------------------------------

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated UploadRequestItem` | `items` |  |

#### `UploadRequestItem`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `rootCid` |  |
| 2 | `repeated uint64` | `size` |  |

#### `UploadResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated UploadResult` | `results` |  |

#### `UploadResult`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `rootCid` |  |
| 2 | `repeated ErrCode` | `code` |  |
| 3 | `repeated PresignedUpload` | `upload` |  |


### any-sync/commonfile/fileproto/protos/file.proto

#### `AccountInfoRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `AccountInfoResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `limitBytes` | the shared limit excluding isolated spaces |
| 2 | `repeated uint64` | `totalUsageBytes` |  |
| 3 | `repeated uint64` | `totalCidsCount` |  |
| 4 | `repeated SpaceInfoResponse` | `spaces` |  |
| 5 | `repeated uint64` | `accountLimitBytes` | the total limit including isolated spaces |

#### `AccountLimitSetRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `identity` |  |
| 2 | `repeated uint64` | `limit` |  |

#### `Block`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 2 | `repeated bytes` | `cid` |  |
| 3 | `repeated bytes` | `data` |  |

#### `BlockAvailability`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `cid` |  |
| 2 | `repeated AvailabilityStatus` | `status` |  |

#### `BlockDeleteUnboundRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `cid` |  |

#### `BlockGetRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated bytes` | `cid` |  |
| 3 | `repeated bool` | `wait` |  |

#### `BlockGetResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `cid` |  |
| 2 | `repeated bytes` | `data` |  |

#### `BlockPushManyRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated FileBlocks` | `fileBlocks` |  |

#### `BlockPushRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `fileId` |  |
| 3 | `repeated bytes` | `cid` |  |
| 4 | `repeated bytes` | `data` |  |

#### `BlocksBindRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `fileId` |  |
| 3 | `repeated bytes` | `cids` |  |

#### `BlocksCheckRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated bytes` | `cids` |  |

#### `BlocksCheckResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated BlockAvailability` | `blocksAvailability` |  |

#### `CheckRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `CheckResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceIds` |  |
| 2 | `repeated bool` | `allowWrite` |  |

#### `FileBlocks`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `fileId` |  |
| 2 | `repeated string` | `spaceId` |  |
| 3 | `repeated Block` | `blocks` |  |

#### `FileInfo`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `fileId` |  |
| 2 | `repeated uint64` | `usageBytes` |  |
| 3 | `repeated uint32` | `cidsCount` |  |

#### `FilesDeleteRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `fileIds` |  |

#### `FilesDeleteResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `FilesGetRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |

#### `FilesGetResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `fileId` |  |

#### `FilesInfoRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `fileIds` |  |

#### `FilesInfoResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated FileInfo` | `filesInfo` |  |

#### `Ok`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `SpaceInfoRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |

#### `SpaceInfoResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `limitBytes` |  |
| 2 | `repeated uint64` | `totalUsageBytes` |  |
| 3 | `repeated uint64` | `cidsCount` |  |
| 4 | `repeated uint64` | `filesCount` |  |
| 5 | `repeated uint64` | `spaceUsageBytes` |  |
| 6 | `repeated string` | `spaceId` |  |

#### `SpaceLimitSetRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated uint64` | `limit` |  |


### any-sync/commonspace/clientspaceproto/protos/clientspace.proto

#### `LocalServer`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `Ips` |  |
| 2 | `repeated int32` | `port` |  |

#### `SpaceExchangeRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceIds` |  |
| 2 | `repeated LocalServer` | `localServer` |  |

#### `SpaceExchangeResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceIds` |  |

#### `SpaceExchangeV2Request`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `nonce` | nonce is 32 random bytes chosen by the caller; it challenges both request and response tokens |
| 2 | `repeated bytes` | `spaceTokens` | spaceTokens holds one 32-byte request token per caller space, padded with random tokens up to a bucket size and sorted to hide the true count |
| 3 | `repeated LocalServer` | `localServer` |  |

#### `SpaceExchangeV2Response`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `spaceTokens` | spaceTokens holds one 32-byte response token per intersecting space — the responder's proof of membership, keyed by the caller's nonce |


### any-sync/commonspace/object/acl/aclrecordproto/protos/aclrecord.proto

#### `AclAccountAdd`

> AclAccountAdd contains new account to be added

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `identity` |  |
| 2 | `repeated AclUserPermissions` | `permissions` |  |
| 3 | `repeated bytes` | `metadata` |  |
| 4 | `repeated bytes` | `encryptedReadKey` |  |

#### `AclAccountInvite`

> AclAccountInvite contains the public invite key, the private part of which is sent to the user directly

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `inviteKey` |  |
| 2 | `repeated AclInviteType` | `inviteType` |  |
| 3 | `repeated AclUserPermissions` | `permissions` | permissions tells with which permissions the user joins the space. Used only for invites without approve. |
| 4 | `repeated bytes` | `encryptedReadKey` | encryptedReadKey is used when the user creates an invite without approve. So everyone having the invite can join the space immediately. The key could only be decrypted using the inviteKey |

#### `AclAccountInviteChange`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `inviteRecordId` |  |
| 2 | `repeated AclUserPermissions` | `permissions` |  |

#### `AclAccountInviteJoin`

> AclInviteJoin contains the reference to the invite record and the data of the person who wants to join, confirmed by the private invite key The person must encrypt the key with its own public key

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `identity` |  |
| 2 | `repeated string` | `inviteRecordId` |  |
| 3 | `repeated bytes` | `inviteIdentitySignature` |  |
| 4 | `repeated bytes` | `metadata` | Metadata is encrypted with metadata key of the space |
| 5 | `repeated bytes` | `encryptedReadKey` | encryptedReadKey is the read key of a space encrypted using person's public key |
| 6 | `repeated AclUserPermissions` | `permissions` |  |

#### `AclAccountInviteRevoke`

> AclAccountInviteRevoke revokes the invite record

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `inviteRecordId` |  |

#### `AclAccountPermissionChange`

> AclAccountPermissionChange changes permissions of specific account

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `identity` |  |
| 2 | `repeated AclUserPermissions` | `permissions` |  |

#### `AclAccountPermissionChanges`

> AclAccountPermissionChanges contains permission changes for certain identities

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated AclAccountPermissionChange` | `changes` |  |

#### `AclAccountRemove`

> AclAccountRemove removes an account and changes read key for space

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `identities` |  |
| 2 | `repeated AclReadKeyChange` | `readKeyChange` |  |

#### `AclAccountRequestAccept`

> AclAccountRequestAccept contains the reference to join record and all read keys, encrypted with the identity of the requestor

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `identity` |  |
| 2 | `repeated string` | `requestRecordId` |  |
| 3 | `repeated bytes` | `encryptedReadKey` |  |
| 4 | `repeated AclUserPermissions` | `permissions` |  |

#### `AclAccountRequestCancel`

> AclRequestCancel contains reference to the request that is canceled by the account

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `recordId` |  |

#### `AclAccountRequestDecline`

> AclAccountRequestDecline contains the reference to join record

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `requestRecordId` |  |

#### `AclAccountRequestJoin`

> AclAccountRequestJoin contains the reference to the invite record and the data of the person who wants to join, confirmed by the private invite key

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `inviteIdentity` |  |
| 2 | `repeated string` | `inviteRecordId` |  |
| 3 | `repeated bytes` | `inviteIdentitySignature` |  |
| 4 | `repeated bytes` | `metadata` | Metadata is encrypted with metadata key of the space |

#### `AclAccountRequestRemove`

> AclAccountRequestRemove adds a request to remove an account

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `AclAccountsAdd`

> AclAccountsAdd contains new accounts to be added

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated AclAccountAdd` | `additions` |  |

#### `AclContentValue`

> AclContentValue contains possible values for Acl

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) value | |  |

#### `AclData`

> AclData contains different acl content

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated AclContentValue` | `aclContent` |  |

#### `AclEncryptedReadKey`

> AclEncryptedReadKeys are new key for specific identity

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `identity` |  |
| 2 | `repeated bytes` | `encryptedReadKey` |  |

#### `AclOneToOneInfo`

> AclOneToOneInfo exists if its one-to-one space acl record

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `owner` |  |
| 2 | `repeated bytes` | `writers` |  |

#### `AclOwnershipChange`

> AclOwnershipChange contains the new owner identity

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `newOwnerIdentity` |  |
| 2 | `repeated AclUserPermissions` | `oldOwnerPermissions` |  |

#### `AclReadKeyChange`

> AclReadKeyChange changes the key for a space

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated AclEncryptedReadKey` | `accountKeys` |  |
| 2 | `repeated bytes` | `metadataPubKey` |  |
| 3 | `repeated bytes` | `encryptedMetadataPrivKey` | EncryptedMetadataPrivKey is encrypted with new read key |
| 4 | `repeated bytes` | `encryptedOldReadKey` | EncryptedOldReadKey is encrypted with new read key |
| 5 | `repeated AclEncryptedReadKey` | `inviteKeys` |  |

#### `AclRoot`

> AclRoot is a root of access control list

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `identity` |  |
| 2 | `repeated bytes` | `masterKey` |  |
| 3 | `repeated string` | `spaceId` |  |
| 4 | `repeated bytes` | `encryptedReadKey` |  |
| 5 | `repeated int64` | `timestamp` |  |
| 6 | `repeated bytes` | `identitySignature` |  |
| 7 | `repeated bytes` | `metadataPubKey` |  |
| 8 | `repeated bytes` | `encryptedMetadataPrivKey` |  |
| 9 | `repeated bytes` | `encryptedOwnerMetadata` |  |
| 10 | `repeated AclOneToOneInfo` | `oneToOneInfo` |  |
| 11 | `repeated AclSpaceOptions` | `options` |  |

#### `AclSpaceOptions`

> AclSpaceOptions contains space-level toggles/options

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bool` | `deleteRestricted` |  |

#### `AclSpaceOptionsChange`

> AclSpaceOptionsChange changes space options (owner-only)

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated AclSpaceOptions` | `options` |  |


### any-sync/commonspace/object/tree/treechangeproto/protos/treechange.proto

#### `NoDataTreeChange`

> TreeChange is a change of a tree

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `treeHeadIds` | TreeHeadIds are previous ids for this TreeChange |
| 2 | `repeated string` | `aclHeadId` | AclHeadId is a cid of latest acl record at the time of this change |
| 3 | `repeated string` | `snapshotBaseId` | SnapshotBaseId is a snapshot (root) of the tree where this change is added |
| 5 | `repeated string` | `readKeyId` | ReadKeyId is the id of the read key |
| 6 | `repeated int64` | `timestamp` | Timestamp is this change creation timestamp |
| 7 | `repeated bytes` | `identity` | Identity is a public key with which the raw payload of this change is signed |
| 8 | `repeated bool` | `isSnapshot` | IsSnapshot indicates whether this change contains a snapshot of state |
| 9 | `repeated string` | `dataType` | DataType indicates some special parameters of data for the client |

#### `RawTreeChange`

> RawTreeChange is a marshalled TreeChange (or RootChange) payload and a signature of this payload

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | Payload is a byte payload containing TreeChange |
| 2 | `repeated bytes` | `signature` | Signature is a signature made by identity indicated in the TreeChange payload |

#### `RawTreeChangeWithId`

> RawTreeChangeWithId is a marshalled RawTreeChange with CID

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `rawChange` | RawChange is a byte payload of RawTreeChange |
| 2 | `repeated string` | `id` | Id is a cid made from rawChange payload |

#### `ReducedTreeChange`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `treeHeadIds` | TreeHeadIds are previous ids for this TreeChange |

#### `RootChange`

> RootChange is a root of a tree

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `aclHeadId` | AclHeadId is a cid of latest acl record at the time of tree creation |
| 2 | `repeated string` | `spaceId` | SpaceId is an id of space where the document is placed |
| 3 | `repeated string` | `changeType` | ChangeType is a type of tree which this RootChange is a root of |
| 4 | `repeated int64` | `timestamp` | Timestamp is this change creation timestamp |
| 5 | `repeated bytes` | `seed` | Seed is a random bytes to make root change unique |
| 6 | `repeated bytes` | `identity` | Identity is a public key of the tree's creator |
| 7 | `repeated bytes` | `changePayload` | ChangePayload is a payload related to ChangeType |
| 8 | `repeated bool` | `isDerived` | IsDerived tells if the tree is derived |
| 9 | `repeated string` | `parentId` | ParentId is the id of the parent object for bound derived objects |

#### `TreeChange`

> TreeChange is a change of a tree

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `treeHeadIds` | TreeHeadIds are previous ids for this TreeChange |
| 2 | `repeated string` | `aclHeadId` | AclHeadId is a cid of latest acl record at the time of this change |
| 3 | `repeated string` | `snapshotBaseId` | SnapshotBaseId is a snapshot (root) of the tree where this change is added |
| 4 | `repeated bytes` | `changesData` | ChangesData is an arbitrary payload to be read by the client |
| 5 | `repeated string` | `readKeyId` | ReadKeyId is the id of the read key |
| 6 | `repeated int64` | `timestamp` | Timestamp is this change creation timestamp |
| 7 | `repeated bytes` | `identity` | Identity is a public key with which the raw payload of this change is signed |
| 8 | `repeated bool` | `isSnapshot` | IsSnapshot indicates whether this change contains a snapshot of state |
| 9 | `repeated string` | `dataType` | DataType indicates some special parameters of data for the client |

#### `TreeChangeInfo`

> TreeChangeInfo is used internally in Tree implementation for ease of marshalling

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `changeType` |  |
| 2 | `repeated bytes` | `changePayload` |  |

#### `TreeErrorResponse`

> TreeErrorResponse is an error sent as a response for a full sync request

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `error` |  |
| 2 | `repeated uint64` | `errCode` |  |

#### `TreeFullSyncRequest`

> TreeHeadUpdate is a message sent when document needs full sync

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `heads` |  |
| 2 | `repeated RawTreeChangeWithId` | `changes` |  |
| 3 | `repeated string` | `snapshotPath` |  |
| 4 | `repeated bool` | `probe` | probe asks the responder for the tree's root and current heads only, with no change bodies. Old responders ignore it and stream the full tree; a probing requester must be ready for both response shapes. |

#### `TreeFullSyncResponse`

> TreeFullSyncResponse is a message sent as a response for a specific full sync

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `heads` |  |
| 2 | `repeated RawTreeChangeWithId` | `changes` |  |
| 3 | `repeated string` | `snapshotPath` |  |

#### `TreeHeadUpdate`

> TreeHeadUpdate is a message sent on document head update

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `heads` |  |
| 2 | `repeated RawTreeChangeWithId` | `changes` |  |
| 3 | `repeated string` | `snapshotPath` |  |

#### `TreeSyncContentValue`

> TreeSyncContentValue provides different types for tree sync

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) value | |  |

#### `TreeSyncMessage`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated TreeSyncContentValue` | `content` |  |
| 2 | `repeated RawTreeChangeWithId` | `rootChange` |  |


### any-sync/commonspace/pubsub/pubsubproto/protos/pubsub.proto

#### `PubSubMessage`

> PubSubMessage is the single frame type carried by PubSubStream

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) content | |  |

#### `Publish`

> Publish carries one ephemeral fire-and-forget message to a fully-qualified topic

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `topic` | topic is a fully-qualified '/'-separated topic; wildcards are not allowed |
| 3 | `repeated bytes` | `msgId` | msgId is 16 random bytes generated by the publisher, used for duplicate suppression |
| 4 | `repeated string` | `keyId` | keyId is the space ReadKey id used to encrypt the payload; empty means plaintext (keyless spaces) |
| 5 | `repeated bytes` | `payload` | payload is ciphertext, or plaintext iff keyId is empty |
| 6 | `repeated bytes` | `identity` | identity is the sender's marshalled account public key |
| 7 | `repeated bytes` | `signature` | signature is the account-key signature over "anysync:pubsub:v1" \| spaceId \| topic \| msgId \| keyId \| le64(timestampMilli) \| payload |
| 8 | `repeated int64` | `timestampMilli` | timestampMilli is the sender's wall clock, informational |
| 9 | `repeated bool` | `relayed` | relayed is set by a node when forwarding node-to-node; a relayed message is never forwarded again; excluded from the signature |

#### `Status`

> Status is sent by the serving peer on a rejected subscribe or publish; success is silent

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `topics` | topics echoes the offending patterns (or the topic of a rejected publish) |
| 3 | `repeated ErrCodes` | `code` |  |
| 4 | `repeated bytes` | `msgId` | msgId echoes a rejected publish's id so the caller can correlate the rejection to a specific Publish; empty for subscribe rejections |

#### `Subscribe`

> Subscribe adds topic patterns to the stream's interest set for the space. Patterns may contain wildcards: '*' matches exactly one segment, '>' matches one-or-more trailing segments (tail-only)

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `topics` |  |

#### `Unsubscribe`

> Unsubscribe removes patterns from the stream's interest set, matched verbatim (not expanded); empty topics means remove all patterns of the space

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `topics` |  |


### any-sync/commonspace/spacesyncproto/protos/spacesync.proto

#### `AclAddRecordRequest`

> AclAddRecordRequest contains marshaled consensusproto.RawRecord

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated bytes` | `payload` |  |

#### `AclAddRecordResponse`

> AclAddRecordResponse contains created record id and marshaled consensusproto.RawRecord

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `recordId` |  |
| 2 | `repeated bytes` | `payload` |  |

#### `AclGetRecordsRequest`

> AclGetRecordsRequest can optionally contain the last known aclHead, the server will return only new records or an empty list if there are no new records. If aclHead is not provided the whole list will be returned.

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `aclHead` |  |

#### `AclGetRecordsResponse`

> AclGetRecordsResponse contains list of marshaled consensusproto.RawRecordWithId

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `records` |  |

#### `AclRecord`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `aclPayload` |  |
| 2 | `repeated string` | `id` |  |

#### `HeadSyncRange`

> HeadSyncRange presenting a request for one range

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `from` |  |
| 2 | `repeated uint64` | `to` |  |
| 3 | `repeated uint32` | `limit` |  |
| 4 | `repeated bool` | `elements` |  |

#### `HeadSyncRequest`

> HeadSyncRequest is a request for HeadSync

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated HeadSyncRange` | `ranges` |  |
| 3 | `repeated DiffType` | `diffType` |  |

#### `HeadSyncResponse`

> HeadSyncResponse is a response for HeadSync

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated HeadSyncResult` | `results` |  |
| 2 | `repeated DiffType` | `diffType` |  |

#### `HeadSyncResult`

> HeadSyncResult presenting a response for one range

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `hash` |  |
| 2 | `repeated HeadSyncResultElement` | `elements` |  |
| 3 | `repeated uint32` | `count` |  |

#### `HeadSyncResultElement`

> HeadSyncResultElement presenting state of one object

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated string` | `head` |  |

#### `ObjectDelete`

> ObjectDelete is a message containing an object id which should be deleted

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |

#### `ObjectSyncMessage`

> ObjectSyncMessage is a message sent on object sync

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `requestId` |  |
| 3 | `repeated string` | `replyId` |  |
| 4 | `repeated bytes` | `payload` |  |
| 5 | `repeated string` | `objectId` |  |
| 6 | `repeated ObjectType` | `objectType` |  |

#### `RawSpaceHeader`

> RawSpaceHeader is raw header for SpaceHeader

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `spaceHeader` |  |
| 2 | `repeated bytes` | `signature` |  |

#### `RawSpaceHeaderWithId`

> RawSpaceHeaderWithId is a marshalled RawSpaceHeader with its content id

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `rawHeader` |  |
| 2 | `repeated string` | `id` |  |

#### `SettingsData`

> SettingsData contains ObjectTree change payload

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SpaceSettingsContent` | `content` |  |
| 2 | `repeated SpaceSettingsSnapshot` | `snapshot` |  |

#### `SpaceDelete`

> SpaceDelete is a message containing deleter peer id

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `deleterPeerId` |  |

#### `SpaceHeader`

> SpaceHeader is a header for a space

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `identity` |  |
| 2 | `repeated int64` | `timestamp` |  |
| 3 | `repeated string` | `spaceType` |  |
| 4 | `repeated uint64` | `replicationKey` |  |
| 5 | `repeated bytes` | `seed` |  |
| 6 | `repeated bytes` | `spaceHeaderPayload` |  |
| 7 | `repeated bytes` | `aclPayload` | since v1 fields |
| 8 | `repeated bytes` | `settingPayload` |  |
| 9 | `repeated SpaceFileProtoVersion` | `fileprotoVersion` | fileprotoVersion gates the file protocol (v2 = filenode v2 + S3-direct + networkSign) |
| 100 | `repeated SpaceHeaderVersion` | `version` |  |

#### `SpacePayload`

> SpacePayload is a payload for pushing a space

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated RawSpaceHeaderWithId` | `spaceHeader` |  |
| 2 | `repeated bytes` | `aclPayload` |  |
| 3 | `repeated string` | `aclPayloadId` |  |
| 4 | `repeated bytes` | `spaceSettingsPayload` |  |
| 5 | `repeated string` | `spaceSettingsPayloadId` |  |

#### `SpacePullRequest`

> SpacePullRequest is a request to request a space on a node that doesn't have it

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |

#### `SpacePullResponse`

> SpacePullResponse is a response with header and acl root

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SpacePayload` | `payload` |  |
| 2 | `repeated AclRecord` | `aclRecords` |  |

#### `SpacePushRequest`

> SpacePushRequest is a request to add space on a node containing only one acl record

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SpacePayload` | `payload` |  |
| 2 | `repeated bytes` | `Credential` |  |

#### `SpacePushResponse`

> SpacePushResponse is an empty response

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `SpaceSettingsContent`

> SpaceSettingsContent is a payload for a space settings object

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) value | |  |

#### `SpaceSettingsSnapshot`

> SpaceSettingsSnapshot contains all the deleted ids in a snapshot

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `deletedIds` |  |
| 2 | `repeated string` | `deleterPeerId` |  |

#### `SpaceSubscription`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceIds` |  |
| 2 | `repeated SpaceSubscriptionAction` | `action` |  |

#### `StorageHeader`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `storageName` |  |

#### `StoreDeletePrefix`

> StoreDeletePrefix is the deletion watermark operation: applying the row carrying it physically removes every stored row whose key starts with the prefix and whose timestamp is older than the watermark's, and rejects such rows arriving later. The watermark row itself is the only retained state. It lives inside the signed StoreKeyInner so the operation type cannot be forged, and rides the ordinary element sync so it reaches every replica — including devices restoring from old snapshots.

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `prefix` |  |

#### `StoreDiffRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated HeadSyncRange` | `ranges` |  |

#### `StoreDiffResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated HeadSyncResult` | `results` |  |

#### `StoreHeader`

> StoreHeader is a header for a store

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `storageName` |  |

#### `StoreKeyInner`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `peer` |  |
| 2 | `repeated bytes` | `identity` |  |
| 3 | `repeated bytes` | `value` |  |
| 4 | `repeated int64` | `timestampMicro` |  |
| 5 | `repeated string` | `aclHeadId` |  |
| 6 | `repeated string` | `key` |  |
| 7 | `repeated StoreDeletePrefix` | `delete` | delete turns this row into a deletion watermark instead of a value (see StoreDeletePrefix). key mirrors the prefix; value stays empty. |

#### `StoreKeyValue`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `keyPeerId` |  |
| 2 | `repeated bytes` | `value` |  |
| 3 | `repeated bytes` | `identitySignature` |  |
| 4 | `repeated bytes` | `peerSignature` |  |
| 5 | `repeated string` | `spaceId` |  |

#### `StoreKeyValues`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated StoreKeyValue` | `keyValues` |  |


### any-sync/consensus/consensusproto/protos/consensus.proto

#### `Err`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated ErrCodes` | `error` |  |

#### `Log`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 3 | `repeated RawRecordWithId` | `records` |  |

#### `LogAddRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `logId` |  |
| 2 | `repeated RawRecordWithId` | `record` | first record in the log, consensus node not sign it |

#### `LogDeleteRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `logId` |  |

#### `LogFullSyncRequest`

> LogFullSyncRequest is a message sent when consensus log needs full sync

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `head` |  |
| 2 | `repeated RawRecordWithId` | `records` |  |

#### `LogFullSyncResponse`

> LogFullSyncResponse is a message sent as a response for a specific full sync

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `head` |  |
| 2 | `repeated RawRecordWithId` | `records` |  |

#### `LogHeadUpdate`

> LogHeadUpdate is a message sent on consensus log head update

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `head` |  |
| 2 | `repeated RawRecordWithId` | `records` |  |

#### `LogSyncContentValue`

> LogSyncContentValue provides different types for log sync

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| — | (oneof) value | |  |

#### `LogSyncMessage`

> LogSyncMessage is a message sent when we are syncing logs

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated bytes` | `payload` |  |
| 3 | `repeated LogSyncContentValue` | `content` |  |

#### `LogWatchEvent`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `logId` |  |
| 2 | `repeated RawRecordWithId` | `records` |  |
| 3 | `repeated Err` | `error` |  |

#### `LogWatchRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `watchIds` |  |
| 2 | `repeated string` | `unwatchIds` |  |

#### `Ok`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `RawRecord`

> RawRecord is a proto message containing the payload in bytes, signature of the account who added it and signature of the acceptor

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` |  |
| 2 | `repeated bytes` | `signature` |  |
| 3 | `repeated bytes` | `acceptorIdentity` |  |
| 4 | `repeated bytes` | `acceptorSignature` |  |
| 5 | `repeated int64` | `acceptorTimestamp` |  |

#### `RawRecordWithId`

> RawRecordWithId is a raw record and the id for convenience

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` |  |
| 2 | `repeated string` | `id` |  |

#### `Record`

> Record is a record containing a data

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `prevId` |  |
| 2 | `repeated bytes` | `identity` |  |
| 3 | `repeated bytes` | `data` |  |
| 4 | `repeated int64` | `timestamp` |  |

#### `RecordAddRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `logId` |  |
| 2 | `repeated RawRecord` | `record` |  |


### any-sync/coordinator/coordinatorproto/protos/coordinator.proto

#### `AccountDeleteRequest`

> AccountDeleteRequest contains payload for account deletion

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `deletionPayloadId` |  |
| 2 | `repeated bytes` | `deletionPayload` |  |

#### `AccountDeleteResponse`

> AccountDeleteResponse contains timestamp when the account is finally deleted

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated int64` | `toBeDeletedTimestamp` |  |

#### `AccountDeletionConfirmPayload`

> AccountDeletionConfirmPayload contains payload for deletion confirmation

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `peerId` | PeerId of receipt requester |
| 2 | `repeated bytes` | `accountIdentity` | AccountIdentity is an identity of a space owner |
| 3 | `repeated string` | `networkId` | NetworkId is the id of a network where the deletion was requested |
| 4 | `repeated int64` | `timestamp` | Timestamp is a timestamp when the deletion was requested |

#### `AccountLimits`

> AccountLimits describes account level limit

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint32` | `sharedSpacesLimit` |  |

#### `AccountLimitsSetRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `identity` |  |
| 2 | `repeated string` | `reason` |  |
| 3 | `repeated uint64` | `fileStorageLimitBytes` |  |
| 4 | `repeated uint32` | `spaceMembersRead` |  |
| 5 | `repeated uint32` | `spaceMembersWrite` |  |
| 6 | `repeated uint32` | `sharedSpacesLimit` |  |

#### `AccountLimitsSetResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `AccountRevertDeletionRequest`

> AccountRevertDeletionRequest is a request to revert an account deletion

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `AccountRevertDeletionResponse`

> AccountRevertDeletionResponse is an empty response confirming that the deletion is reverted

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `AclAddRecordRequest`

> AclAddRecordRequest contains marshaled consensusproto.RawRecord

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated bytes` | `payload` |  |

#### `AclAddRecordResponse`

> AclAddRecordResponse contains created record id and marshaled consensusproto.RawRecord

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `recordId` |  |
| 2 | `repeated bytes` | `payload` |  |

#### `AclDeleteInviteRequest`

> AclDeleteInviteRequest asks the coordinator to remove a revoked invite's file from the filenodes. The coordinator resolves the cid to its invite through the binding made by AclUploadInvite and refuses to remove one that still grants access.

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated bytes` | `inviteCid` |  |

#### `AclDeleteInviteResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `AclEventLogRecord`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` | Id is a record id |
| 2 | `repeated string` | `spaceId` | SpaceId is a space identifier |
| 3 | `repeated int64` | `timestamp` | Timestamp is a unixtimestamp of record creation |
| 4 | `repeated AclEventLogRecordType` | `type` | Type of current event |
| 5 | `repeated string` | `aclChangeId` | only for RecordTypeSpaceAclAddRecord |

#### `AclEventLogRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `accountIdentity` |  |
| 2 | `repeated string` | `afterId` | AfterId is the last known logId to request records after this id. If it is empty will be returned a list from the beginning. |
| 3 | `repeated uint32` | `limit` | Limit is a desired record count in response |

#### `AclEventLogResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated AclEventLogRecord` | `records` | AclEventLogRecord list of records, if there are no new records will be empty |
| 2 | `repeated bool` | `hasMore` | HasMore indicates if there are records left |

#### `AclGetRecordsRequest`

> AclGetRecordsRequest can optionally contain the last known aclHead, the server will return only new records or an empty list if there are no new records. If aclHead is not provided the whole list will be returned.

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `aclHead` |  |

#### `AclGetRecordsResponse`

> AclGetRecordsResponse contains list of marshaled consensusproto.RawRecordWithId

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `records` |  |

#### `AclUploadInviteRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `cid` |  |
| 2 | `repeated bytes` | `data` |  |
| 3 | `repeated string` | `spaceId` | spaceId and invitePubKey bind the uploaded file to its invite, so that AclDeleteInvite can later remove it. |
| 4 | `repeated bytes` | `invitePubKey` | invitePubKey is the PUBLIC part of the invite key. For a guest invite it is the public part of the guest key. |

#### `AclUploadInviteResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `DeletionConfirmPayload`

> DeletionConfirmPayload contains payload for deletion confirmation

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` | SpaceId is the identifier of space |
| 2 | `repeated string` | `peerId` | PeerId of receipt requester |
| 3 | `repeated bytes` | `accountIdentity` | AccountIdentity is an identity of a space owner |
| 4 | `repeated string` | `networkId` | NetworkId is the id of a network where the deletion was requested |
| 5 | `repeated int64` | `timestamp` | Timestamp is a timestamp when the deletion was requested |

#### `DeletionConfirmPayloadWithSignature`

> DeletionConfirmPayloadWithSignature contains protobuf encoded deletion payload and its signature

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `deletionPayload` |  |
| 2 | `repeated bytes` | `signature` |  |

#### `DeletionLogRecord`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` | Id is a record id |
| 2 | `repeated string` | `spaceId` | SpaceId is a space identifier |
| 3 | `repeated DeletionLogRecordStatus` | `status` | DeletionLogRecordStatus is a space status |
| 4 | `repeated int64` | `timestamp` | Timestamp is a unixtimestamp of record creation |
| 5 | `repeated string` | `fileGroup` | FileGroup is a key of group for file nodes |
| 6 | `repeated string` | `aclRecordId` | AclRecordId (optional) |

#### `DeletionLogRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `afterId` | AfterId is the last known logId to request records after this id. If it is empty will be returned a list from the beginning. |
| 2 | `repeated uint32` | `limit` | Limit is a desired record count in response |

#### `DeletionLogResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated DeletionLogRecord` | `records` | DeletionLogRecord list of records, if there are no new records will be empty |
| 2 | `repeated bool` | `hasMore` | HasMore indicates if there are records left |

#### `FileLimitsGetRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `identity` | Identity is the uploader account identity whose pool bounds are requested |

#### `FileLimitsGetResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `accountLimitBytes` | AccountLimitBytes is the identity's total file-storage cap (the common account pool) |
| 2 | `repeated uint64` | `accountTotalUsageBytes` | AccountTotalUsageBytes is the coordinator-aggregated durable usage across all the identity's spaces |
| 3 | `repeated uint64` | `spaceLimitBytes` | SpaceLimitBytes is an optional space-scoped cap; 0 = unset |

#### `FileUsageReportRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated FileUsageRow` | `rows` |  |

#### `FileUsageReportResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `FileUsageRow`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `identity` | Identity is the charged uploader identity (the author of the root's earliest bind row) |
| 3 | `repeated uint64` | `durableBytes` | DurableBytes is the HEAD-measured durable usage of this (space, identity) slice; in-flight is never reported |
| 4 | `repeated uint64` | `durableFilesCount` |  |

#### `InboxAddMessageRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated InboxMessage` | `message` |  |

#### `InboxAddMessageResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `InboxFetchRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `offset` |  |

#### `InboxFetchResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated InboxMessage` | `messages` |  |
| 2 | `repeated bool` | `hasMore` |  |

#### `InboxMessage`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated InboxPacketType` | `packetType` |  |
| 3 | `repeated InboxPacket` | `packet` |  |

#### `InboxPacket`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated InboxKeyType` | `keyType` |  |
| 2 | `repeated string` | `senderIdentity` |  |
| 3 | `repeated string` | `receiverIdentity` |  |
| 4 | `repeated bytes` | `senderSignature` |  |
| 5 | `repeated InboxPayload` | `payload` |  |

#### `InboxPayload`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated InboxPayloadType` | `payloadType` |  |
| 2 | `repeated int64` | `timestamp` |  |
| 3 | `repeated bytes` | `body` |  |

#### `NetworkConfigurationRequest`

> NetworkConfigurationRequest contains currenId of the client configuration, it can be empty

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `currentId` | currenId of the client configuration if the currentId is equal to the latest configuration id then the response will not contain a nodes list |

#### `NetworkConfigurationResponse`

> NetworkConfigurationResponse contains list of nodes

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `configurationId` | id of current configuration |
| 2 | `repeated string` | `networkId` | network id |
| 3 | `repeated Node` | `nodes` | nodes list - it will be empty if the client's currentId is equal configurationId |
| 4 | `repeated uint64` | `creationTimeUnix` | unix timestamp of the creation time of configuration |
| 5 | `repeated uint64` | `epoch` | monotonically increasing version of the configuration, 0 if the coordinator predates epoch support |
| 6 | `repeated string` | `fileNetworkId` | identity of the fileV2 fleet's shared receipt-signing key (network string encoding); empty if the network has no fileV2 fleet |

#### `Node`

> Node describes one node in the network

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `peerId` | peerId - it's a peer identifier (libp2p format string) so it's an encoded publicKey |
| 2 | `repeated string` | `addresses` | list of node addresses |
| 3 | `repeated NodeType` | `types` | list of supported APIs |

#### `NotifySubscribeEvent`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated NotifyEventType` | `eventType` |  |
| 2 | `repeated bytes` | `payload` |  |

#### `NotifySubscribeRequest`

> Request to subscribe to notifications

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated NotifyEventType` | `eventType` |  |

#### `SpaceDeleteRequest`

> SpaceDeleteRequest contains the deletion confirmation for the space to be deleted

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `deletionPayloadId` |  |
| 3 | `repeated bytes` | `deletionPayload` |  |
| 4 | `repeated int64` | `deletionDuration` |  |

#### `SpaceDeleteResponse`

> SpaceDeleteResponse contains timestamp when the space is finally deleted

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated int64` | `toBeDeletedTimestamp` |  |

#### `SpaceLimits`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint32` | `readMembers` |  |
| 2 | `repeated uint32` | `writeMembers` |  |

#### `SpaceMakeShareableRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |

#### `SpaceMakeShareableResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `SpaceMakeUnshareableRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `aclHead` |  |

#### `SpaceMakeUnshareableResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `SpaceReceipt`

> SpaceReceipt contains permission to SpacePush operation

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` | SpaceId is the identifier of space |
| 2 | `repeated string` | `peerId` | PeerId of receipt requester |
| 3 | `repeated bytes` | `accountIdentity` | AccountIdentity is an identity of a space owner |
| 4 | `repeated string` | `networkId` | NetworkId is the id of a network where the receipt is issued |
| 5 | `repeated uint64` | `validUntil` | ValidUntil is a unix-timestamp with a deadline time of receipt validity |

#### `SpaceReceiptWithSignature`

> SpaceReceiptWithSignature contains protobuf encoded receipt and its signature

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `spaceReceiptPayload` |  |
| 2 | `repeated bytes` | `signature` |  |

#### `SpaceSignRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` | SpaceId is the id of the signed space |
| 2 | `repeated bytes` | `header` | Header is the header of the signed space |
| 5 | `repeated bool` | `forceRequest` | Deprecated: OldIdentity is no longer used Deprecated: NewIdentitySignature is no longer used ForceRequest if true, forces the creating space receipt even if the space is deleted before |

#### `SpaceSignResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SpaceReceiptWithSignature` | `receipt` |  |

#### `SpaceStatusChangeRequest`

> SpaceStatusChangeRequest contains the deletionChange if we want to delete space, or it is empty otherwise

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |
| 2 | `repeated string` | `deletionPayloadId` |  |
| 3 | `repeated bytes` | `deletionPayload` |  |
| 4 | `repeated DeletionPayloadType` | `deletionPayloadType` |  |

#### `SpaceStatusChangeResponse`

> SpaceStatusChangeResponse contains changed status of space

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SpaceStatusPayload` | `payload` |  |

#### `SpaceStatusCheckManyRequest`

> SpaceStatusCheckManyRequest contains the spaceIds of requested spaces

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceIds` |  |

#### `SpaceStatusCheckManyResponse`

> SpaceStatusCheckManyResponse contains the current statuses of spaces

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SpaceStatusPayload` | `payloads` |  |
| 2 | `repeated AccountLimits` | `accountLimits` |  |

#### `SpaceStatusCheckRequest`

> SpaceStatusCheckRequest contains the spaceId of requested space

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `spaceId` |  |

#### `SpaceStatusCheckResponse`

> SpaceStatusCheckResponse contains the current status of space

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SpaceStatusPayload` | `payload` |  |

#### `SpaceStatusPayload`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated SpaceStatus` | `status` |  |
| 2 | `repeated int64` | `deletionTimestamp` |  |
| 3 | `repeated SpacePermissions` | `permissions` |  |
| 4 | `repeated SpaceLimits` | `limits` |  |
| 5 | `repeated bool` | `isShared` |  |


### any-sync/identityrepo/identityrepoproto/protos/identityrepo.proto

#### `Data`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `kind` | kind is a string representing the kind of data |
| 2 | `repeated bytes` | `data` | data is a byte payload |
| 3 | `repeated bytes` | `signature` | data signature |

#### `DataDeleteRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `identity` | string representation of identity, must be equal handshake result |
| 2 | `repeated string` | `kinds` | kinds of data to delete, if empty all kinds will be deleted |

#### `DataPullRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `identities` | list of identities wanted to request |
| 2 | `repeated string` | `kinds` | kinds of data wanted to request |

#### `DataPullResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated DataWithIdentity` | `data` |  |

#### `DataPutRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `identity` | string representation of identity, must be equal handshake result |
| 2 | `repeated Data` | `data` | data to save |

#### `DataWithIdentity`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `identity` |  |
| 2 | `repeated Data` | `data` |  |

#### `Ok`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|


### any-sync/nameservice/nameserviceproto/protos/nameservice.proto

#### `BatchNameAvailableRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `fullNames` | Names including .any suffix |

#### `BatchNameAvailableResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated NameAvailableResponse` | `results` |  |

#### `BatchNameByAddressRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerScwEthAddresses` | EOA -> SCW -> name A SCW Ethereum address that owns that name |

#### `BatchNameByAddressResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated NameByAddressResponse` | `results` |  |

#### `BatchNameByAnyIdRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `anyAddresses` |  |

#### `NameAvailableRequest`

> import "google/protobuf/timestamp.proto";

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `fullName` | Name including .any suffix |

#### `NameAvailableResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bool` | `available` |  |
| 2 | `repeated string` | `ownerScwEthAddress` | EOA -> SCW -> name This field is non-empty only if name is "already registered" |
| 3 | `repeated string` | `ownerEthAddress` | This field is non-empty only if name is "already registered" |
| 4 | `repeated string` | `ownerAnyAddress` | A content hash attached to this name This field is non-empty only if name is "already registered" |
| 5 | `repeated string` | `spaceId` | A SpaceID attached to this name This field is non-empty only if name is "already registered" |
| 6 | `repeated int64` | `nameExpires` | doesn't work with marashalling/unmarshalling google.protobuf.Timestamp nameExpires = 5 [(gogoproto.stdtime) = true]; |

#### `NameByAddressRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerScwEthAddress` | EOA -> SCW -> name A SCW Ethereum address that owns that name |

#### `NameByAddressResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bool` | `found` |  |
| 2 | `repeated string` | `name` |  |

#### `NameByAnyIdRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `anyAddress` |  |


### any-sync/nameservice/nameserviceproto/protos/nameservice_aa.proto

#### `AdminFundGasOperationsRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerEthAddress` | An Ethereum address that owns that name |
| 2 | `repeated string` | `ownerAnyID` |  |
| 3 | `repeated uint64` | `operationsCount` | Number of gas operations: update name, add new data, etc |

#### `AdminFundGasOperationsRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | AdminFundGasOperationsRequest struct |
| 2 | `repeated bytes` | `signature` | payload signed by Admin of this service |

#### `AdminFundUserAccountRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerEthAddress` | An Ethereum address that owns that name |
| 2 | `repeated uint64` | `namesCount` | Number of names that user can buy. We will mint him tokens that he can use to buy names (one token per name) |

#### `AdminFundUserAccountRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | AdminFundUserAccountRequest struct |
| 2 | `repeated bytes` | `signature` | payload signed by Admin of this service |

#### `CreateUserOperationRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `data` |  |
| 2 | `repeated bytes` | `signedData` | "data" signed with Ethereum private key |
| 3 | `repeated bytes` | `context` |  |
| 4 | `repeated string` | `ownerEthAddress` |  |
| 5 | `repeated string` | `ownerAnyID` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 6 | `repeated string` | `fullName` | all operations currently are towards single name, please specify it we can use it for caching, etc purps. |

#### `CreateUserOperationRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | CreateUserOperationRequest struct |
| 2 | `repeated bytes` | `signature` | payload signed with Anytype identity |

#### `GetDataNameRegisterResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `data` |  |
| 2 | `repeated bytes` | `context` |  |

#### `GetOperationStatusRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `operationId` |  |

#### `GetUserAccountRequest`

> no signature required here

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerEthAddress` | An Ethereum address that owns that account |

#### `NameRegisterForSpaceRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `fullName` |  |
| 2 | `repeated string` | `ownerAnyAddress` | A content hash attached to this name This should not be empty! in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 3 | `repeated string` | `ownerEthAddress` | An Ethereum address that owns that name |
| 4 | `repeated string` | `spaceId` | A SpaceID attached to this name |
| 5 | `repeated uint32` | `registerPeriodMonths` | How many months to register the name for |

#### `NameRegisterRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `fullName` |  |
| 2 | `repeated string` | `ownerAnyAddress` | A content hash attached to this name This should not be empty! in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 3 | `repeated string` | `ownerEthAddress` | An Ethereum address that owns that name |
| 4 | `repeated bool` | `registerToSmartContractWallet` | if false -> name ownership will belong to ownerEthAddress if true -> name ownership will belong to SCW of ownerEthAddress (AccountAbstraction) |
| 5 | `repeated uint32` | `registerPeriodMonths` | How many months to register the name for |

#### `NameRegisterRequestSigned`

> Example: 1 - register alice.any -> ANYID123123 2 - register xxxx.any -> ANYID123123 reverse resolve ANYID123123 will return xxxx.any  TODO: currently by default "true" bool updateReverseResolver = 4;

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | NameRegisterRequest struct |
| 2 | `repeated bytes` | `signature` | payload signed by payload.ownerEthAddress |

#### `NameRenewRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `fullName` |  |
| 2 | `repeated string` | `ownerAnyAddress` | A content hash attached to this name This should not be empty! in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 3 | `repeated string` | `ownerEthAddress` | An Ethereum address that owns that name |
| 4 | `repeated bool` | `renewToSmartContractWallet` | if false -> name ownership will belong to ownerEthAddress if true -> name ownership will belong to SCW of ownerEthAddress (AccountAbstraction) |
| 5 | `repeated uint32` | `renewPeriodMonths` | How many months to register the name for |

#### `NameRenewRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | NameRenewRequest struct |
| 2 | `repeated bytes` | `signature` | payload signed by payload.ownerEthAddress |

#### `OperationResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `operationId` |  |
| 2 | `repeated OperationState` | `operationState` |  |

#### `UserAccount`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerEthAddress` | An Ethereum address that owns that account |
| 2 | `repeated string` | `ownerSmartContracWalletAddress` | This smart contract really controls all names you can ask .owner() method to get 'ownerEthAddress' |
| 3 | `repeated bool` | `ownerSmartContracWalletDeployed` | The ownerSmartContracWalletAddress field is calculated automatically from ownerEthAddress even if SCW is not deployed yet SCW is deployed automatically after first operation |
| 4 | `repeated uint64` | `namesCountLeft` | Number of names that the user can buy. We will mint him tokens that he can use to buy names (one token per name) |
| 5 | `repeated uint64` | `operationsCountLeft` | Number of gas operations: update name, add new data, etc |


### any-sync/net/endtoendtest/testpeer/testproto/protos/testservice.proto

#### `StreamMessage`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `reqData` |  |
| 2 | `repeated int64` | `repeat` |  |
| 3 | `repeated int64` | `n` |  |


### any-sync/net/rpc/limiter/limiterproto/protos/limiter.proto


### any-sync/net/secureservice/handshake/handshakeproto/protos/handshake.proto

#### `Ack`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Error` | `error` |  |

#### `Credentials`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated CredentialsType` | `type` |  |
| 2 | `repeated bytes` | `payload` |  |
| 3 | `repeated uint32` | `version` |  |
| 4 | `repeated string` | `clientVersion` |  |

#### `PayloadSignedPeerIds`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `identity` | account identity |
| 2 | `repeated bytes` | `sign` | sign of (localPeerId + remotePeerId) |

#### `Proto`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated ProtoType` | `proto` |  |
| 2 | `repeated Encoding` | `encodings` |  |


### any-sync/net/streampool/testservice/protos/testservice.proto

#### `StreamMessage`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `reqData` |  |
| 2 | `repeated int64` | `repeat` |  |


### any-sync/paymentservice/paymentserviceproto/protos/paymentservice.proto

#### `BuySubscriptionRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 2 | `repeated string` | `ownerEthAddress` | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |
| 3 | `repeated uint32` | `requestedTier` | was SubscriptionTier before, changed to uint32 to allow us to use dynamic tiers |
| 4 | `repeated PaymentMethod` | `paymentMethod` |  |
| 5 | `repeated string` | `requestedAnyName` | if empty - then no name requested if non-empty - PP node will register that name on behalf of the user |
| 6 | `repeated string` | `userEmail` | for some payment methods we need to know the user's email |

#### `BuySubscriptionRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | BuySubscriptionRequest |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `BuySubscriptionResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `paymentUrl` | will feature current billing ID stripe.com/?client_reference_id=1234 |
| 2 | `repeated string` | `billingID` | billingID is passed via mobile client to payment platform |

#### `CodeGetInfoRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 2 | `repeated string` | `ownerEthAddress` | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |
| 3 | `repeated string` | `code` | code received in the email |

#### `CodeGetInfoRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | CodeGetInfoRequest |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `CodeGetInfoResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint32` | `tier` |  |

#### `CodeRedeemRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 2 | `repeated string` | `ownerEthAddress` | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |
| 3 | `repeated string` | `requestedAnyName` | if empty - then no name requested |
| 4 | `repeated string` | `code` | code received in the email |

#### `CodeRedeemRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | CodeRedeemRequest |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `CodeRedeemResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bool` | `success` |  |

#### `FinalizeSubscriptionRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 2 | `repeated string` | `ownerEthAddress` | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |
| 3 | `repeated string` | `requestedAnyName` | if empty - then no name requested |

#### `FinalizeSubscriptionRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | VerifyEmailRequest |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `FinalizeSubscriptionResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `GetSubscriptionPortalLinkRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |

#### `GetSubscriptionPortalLinkRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | GetSubscriptionPortalLinkRequest |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `GetSubscriptionPortalLinkResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `portalUrl` |  |

#### `GetSubscriptionRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerAnyID` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |

#### `GetSubscriptionRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | GetSubscriptionRequest |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `GetSubscriptionResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint32` | `tier` | was SubscriptionTier before, changed to uint32 to allow us to use dynamic tiers |
| 2 | `repeated SubscriptionStatus` | `status` |  |
| 3 | `repeated uint64` | `dateStarted` |  |
| 4 | `repeated uint64` | `dateEnds` |  |
| 5 | `repeated bool` | `isAutoRenew` |  |
| 6 | `repeated PaymentMethod` | `paymentMethod` |  |
| 7 | `repeated string` | `requestedAnyName` |  |
| 8 | `repeated string` | `userEmail` | if user verified her email OR provided it while buying a subscription, it will be here |
| 9 | `repeated bool` | `subscribeToNewsletter` |  |

#### `GetVerificationEmailRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 2 | `repeated string` | `email` |  |
| 3 | `repeated bool` | `subscribeToNewsletter` |  |
| 4 | `repeated bool` | `insiderTipsAndTutorials` |  |
| 5 | `repeated bool` | `isOnboardingList` | if we are coming from the onboarding screen |

#### `GetVerificationEmailRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | GetVerificationEmailRequest |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `GetVerificationEmailResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `IsNameValidRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint32` | `requestedTier` |  |
| 2 | `repeated string` | `requestedAnyName` |  |

#### `IsNameValidResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Code` | `code` |  |
| 2 | `repeated string` | `description` |  |

#### `VerifyAppStoreReceiptRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 2 | `repeated string` | `receipt` | receipt is a JWT-encoded information about subscription purchase |

#### `VerifyAppStoreReceiptRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | VerifyAppStoreReceiptRequest |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `VerifyAppStoreReceiptResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `VerifyEmailRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 2 | `repeated string` | `ownerEthAddress` | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |
| 3 | `repeated string` | `code` | code received in the email |

#### `VerifyEmailRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | VerifyEmailRequest |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `VerifyEmailResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bool` | `success` |  |


### any-sync/paymentservice/paymentserviceproto/protos/paymentservice2.proto

#### `MembershipV2`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `MembershipV2.Amount`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `currency` |  |
| 2 | `repeated int64` | `amountCents` | $0.01 = 1 $1.00 = 100 negative amounts |

#### `MembershipV2.AnyNameAllocateRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `requestedAnyName` |  |
| 2 | `repeated string` | `ownerEthAddress` | this is the owner's main EOA (Externally Owned Account) address not AccountAbstraction's SCW (Smart Contract Wallet) address! this is required to reserve a name for the owner (later that is done by user) in the following format: "0x7a250d5630b4cf539739df2c5dacb4c659f2488d" |

#### `MembershipV2.AnyNameAllocateResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `MembershipV2.AnyNameIsValidRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `requestedAnyName` |  |

#### `MembershipV2.AnyNameIsValidResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Code` | `code` |  |
| 2 | `repeated string` | `description` |  |

#### `MembershipV2.Cart`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated CartProduct` | `products` | if you add Nx the same product - it will be Nx in the 'products' array, i.e: each product instance has a unique index |
| 2 | `repeated Amount` | `total` | total amount of the cart (including discounts, etc) |
| 3 | `repeated Amount` | `totalNextInvoice` | in case you are paying in the middle of the period (for existing customers) the next invoice amount will also be generated |
| 4 | `repeated uint64` | `nextInvoiceDate` |  |
| 5 | `repeated string` | `appliedPromocodes` |  |

#### `MembershipV2.CartProduct`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Product` | `product` |  |
| 2 | `repeated bool` | `isYearly` | otherwise - monthly or isLifetime |
| 3 | `repeated bool` | `remove` | set to true if you want to remove this item from the customer it's like setting -1 to some product |
| 4 | `repeated bool` | `isLifetime` | if true - then this is lifetime product (no matter what isYearly above is) unfortunately we do not use Period here to keep compatibility with old versions that still use isYearly! |

#### `MembershipV2.CryptoCheckout`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `invoiceURL` |  |
| 2 | `repeated Amount` | `total` |  |
| 3 | `repeated bool` | `isCanCancel` |  |

#### `MembershipV2.Features`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `storageBytes` |  |
| 2 | `repeated uint32` | `spaceReaders` |  |
| 3 | `repeated uint32` | `spaceWriters` |  |
| 4 | `repeated uint32` | `sharedSpaces` |  |
| 5 | `repeated uint32` | `teamSeats` |  |
| 6 | `repeated uint32` | `anyNameCount` |  |
| 7 | `repeated uint32` | `anyNameMinLen` |  |

#### `MembershipV2.GetProductsRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `MembershipV2.GetProductsResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Product` | `products` |  |

#### `MembershipV2.GetStatusRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `MembershipV2.GetStatusResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated MembershipV2.PurchasedProduct` | `products` |  |
| 2 | `repeated MembershipV2.Invoice` | `nextInvoice` |  |
| 3 | `repeated string` | `teamOwnerID` |  |
| 4 | `repeated MembershipV2.PaymentProvider` | `paymentProvider` |  |
| 5 | `repeated string` | `appliedPromocodes` |  |
| 6 | `repeated MembershipV2.CryptoCheckout` | `cryptoCheckout` | if crypto checkout is in process |

#### `MembershipV2.Invoice`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` |  |
| 2 | `repeated uint64` | `date` |  |
| 3 | `repeated Amount` | `total` |  |
| 4 | `repeated Status` | `status` |  |
| 5 | `repeated string` | `paymentUrl` | Stripe hosted-invoice payment page for an OPEN (unpaid) invoice the user must pay to keep access — set during the reverse-trial grace period. Empty when no action is required. |
| 6 | `repeated string` | `billingReason` | Stripe billing_reason of the OPEN invoice this record describes, verbatim (e.g. "subscription_cycle" for the first post-trial invoice, "subscription_update"/"subscription_threshold" for later renewal dunning). Lets a consumer tell a trial-ended grace invoice from a failed-renewal one exactly, instead of inferring it from period math. Empty when unknown. |

#### `MembershipV2.Product`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `id` | this is a unique Payment Node ID adding 2 same products to a cart means we will have 2 items with same ID |
| 2 | `repeated string` | `name` |  |
| 3 | `repeated string` | `description` |  |
| 4 | `repeated bool` | `isTopLevel` |  |
| 5 | `repeated bool` | `isHidden` |  |
| 6 | `repeated bool` | `isIntro` | isIntro flag can be used as follows:  1. if current user's top level product has isIntro flag -> then you'd rather show a FULL list of all products to enable upgrading from CURRENT product 2. but if current user's top level product has no isIntro flag -> then it means that this plan was aquired and user need to control it. then show "second screen" to control that product instead |
| 7 | `repeated bool` | `isUpgradeable` | isUpgradeable can be used as follows:  if current user's top level product has isUpgradeable flag -> show incentives to buy something else |
| 8 | `repeated Amount` | `pricesYearly` |  |
| 9 | `repeated Amount` | `pricesMonthly` |  |
| 10 | `repeated string` | `colorStr` | green, blue, red, purple, custom, etc |
| 11 | `repeated string` | `offer` |  |
| 12 | `repeated Features` | `features` |  |
| 13 | `repeated Amount` | `pricesLifetime` |  |

#### `MembershipV2.ProductStatus`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Status` | `status` |  |

#### `MembershipV2.PurchaseInfo`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint64` | `dateStarted` |  |
| 2 | `repeated uint64` | `dateEnds` |  |
| 3 | `repeated bool` | `isAutoRenew` |  |
| 4 | `repeated Period` | `period` |  |
| 5 | `repeated uint64` | `dateTrialEnds` | 0 = not in a trial. Otherwise the Unix timestamp when the free trial ends, which is also when the first real invoice is charged. |

#### `MembershipV2.PurchasedProduct`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated Product` | `product` |  |
| 2 | `repeated PurchaseInfo` | `purchaseInfo` |  |
| 3 | `repeated ProductStatus` | `productStatus` |  |

#### `MembershipV2.StoreCartCheckoutRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `MembershipV2.StoreCartCheckoutResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `paymentUrl` | for new customers - will contain a payment URL (new Stripe session)  if this is empty - then this is existing customer and we are trying to process the payment |

#### `MembershipV2.StoreCartClearRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `MembershipV2.StoreCartGetRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `MembershipV2.StoreCartGetResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated MembershipV2.Cart` | `cart` |  |

#### `MembershipV2.StoreCartPromocodeApplyRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `promocode` |  |

#### `MembershipV2.StoreCartUpdateRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated CartProduct` | `products` |  |
| 2 | `repeated string` | `ownerEthAddress` |  |
| 3 | `repeated string` | `promocodes` |  |

#### `MembershipV2.StoreCartUpdateResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated MembershipV2.Cart` | `cart` |  |

#### `MembershipV2.SubscribeToUpdatesRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `email` |  |
| 2 | `repeated Platform` | `platform` |  |
| 3 | `repeated bool` | `subscribe` | if false - unsubscribe |
| 4 | `repeated string` | `context` | additional data |

#### `MembershipV2.SubscribeToUpdatesResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `MembershipV2.WebAuthRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|

#### `MembershipV2.WebAuthResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `jwt` |  |
| 2 | `repeated string` | `url` | (optional) redirect here after the auth |


### any-sync/paymentservice/paymentserviceproto/protos/paymentservice_tiers.proto

#### `Feature`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `description` |  |

#### `GetTiersRequest`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated string` | `ownerAnyId` | in the following format: "A5k2d9sFZw84yisTxRnz2bPRd1YPfVfhxqymZ6yESprFTG65" you can get it with Account().SignKey.GetPublic().Account() |
| 2 | `repeated string` | `locale` |  |
| 3 | `repeated string` | `version` |  |

#### `GetTiersRequestSigned`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated bytes` | `payload` | GetTiersRequest struct |
| 2 | `repeated bytes` | `signature` | this is payload signed with payload.ownerAnyID |

#### `GetTiersResponse`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated TierData` | `tiers` | list of all available tiers |

#### `TierData`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated uint32` | `id` | this is a unique ID of the tier you should hardcode this in your app and provide icon, graphics, etc for each tier (even for old/historical/inactive/hidden tiers) |
| 2 | `repeated string` | `name` | localazied name of the tier |
| 3 | `repeated string` | `description` | just a short technical description you don't have to use it, you can use your own UI-friendly texts |
| 4 | `repeated bool` | `isActive` | can you buy it (ON ALL PLATFORMS, without clarification)? |
| 5 | `repeated bool` | `isTest` | is this tier for debugging only? |
| 6 | `repeated bool` | `isHiddenTier` | hidden tiers are only visible once user got them |
| 7 | `repeated PeriodType` | `periodType` | how long is the period of the subscription |
| 8 | `repeated uint32` | `periodValue` | i.e. "5 days" or "3 years" |
| 9 | `repeated uint32` | `priceStripeUsdCents` | this one is a price we use ONLY on Stripe platform |
| 10 | `repeated uint32` | `anyNamesCountIncluded` | number of ANY NS names that this tier includes (not counted as a "feature" and not in the features list) |
| 11 | `repeated uint32` | `anyNameMinLength` | somename.any - len of 8 |
| 12 | `repeated Feature` | `features` | each tier has a set of features |
| 13 | `repeated string` | `colorStr` | green, blue, red, purple or custom color in string format #ff00ff |
| 14 | `repeated string` | `stripeProductId` | Stripe platform-specific data: |
| 15 | `repeated string` | `stripeManageUrl` |  |
| 16 | `repeated string` | `iosProductId` | iOS platform-specific data: |
| 17 | `repeated string` | `iosManageUrl` |  |
| 18 | `repeated string` | `androidProductId` | Android platform-specific data: |
| 19 | `repeated string` | `androidManageUrl` |  |
| 20 | `repeated string` | `offer` | something like "limited offer", etc |


### any-sync/util/crypto/cryptoproto/protos/crypto.proto

#### `Key`

| # | 类型 | 字段 | 说明 |
|---|---|---|---|
| 1 | `repeated KeyType` | `Type` |  |
| 2 | `repeated bytes` | `Data` |  |


