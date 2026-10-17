# any-sync 生态 .proto 中文注释版

> 本目录收录 `src/` 下 5 个仓库共 **38 个 .proto** 的中文注释版。
> 字段名、字段编号、类型、枚举值全部保持原样（可直接与源码对照），仅注释译为中文。

## 生成方式

- 核心 10 个协议文件（spacesync / treechange / aclrecord / consensus / coordinator / pubsub / identityrepo / handshake / clientspace / crypto）由人工精翻；
- 其余文件由 `scripts/translate-proto.py` 词典式翻译，标注 `【原文】` 的注释是词典未覆盖的句子，保留英文待复核；
- 重新生成：`python3 scripts/translate-proto.py`（不会覆盖上述人工精翻文件）。

## 文件清单

| 仓库 | 文件数 |
| --- | --- |
| any-sync | 21 |
| any-sync-node | 2 |
| any-sync-filenode | 1 |
| anytype-heart | 9（仅参考，本项目不使用） |
| any-block | 5（仅参考） |

## 必须先读的四份

| 文件 | 为什么重要 |
| --- | --- |
| `any-sync/commonspace/spacesyncproto/protos/spacesync.proto` | 网络侧全部 RPC：SpacePush / SpacePull / HeadSync / ObjectSync* / AclAddRecord |
| `any-sync/commonspace/object/tree/treechangeproto/protos/treechange.proto` | 对象模型：根 + 变更链、头更新、全量同步请求/响应 |
| `any-sync/commonspace/object/acl/aclrecordproto/protos/aclrecord.proto` | 权限模型：读密钥分发、邀请、移除、密钥轮换 |
| `any-sync/commonspace/pubsub/pubsubproto/protos/pubsub.proto` | 空间内无状态发布订阅（独立于对象同步流） |

## 错误码区间（来自 `src/any-sync/docs/rpc-error-offsets.md`）

wire code = 区间基准 + 本地码；两组撞码会导致进程启动 panic。

| 区间 | 服务 | 包 |
| --- | --- | --- |
| 1 / 2 | `Unexpected` / `Closed` | `net/rpc/rpcerr` 全局保留 |
| 100–199 | `spacesync` | `commonspace/spacesyncproto` |
| 200–299 | `filesync`（File v1） | `commonfile/fileproto` |
| 300–399 | `coordinator` | `coordinator/coordinatorproto` |
| 400–499 | `treechange` | `commonspace/object/tree/treechangeproto` |
| 500–599 | `consensus` | `consensus/consensusproto` |
| 600–699 | `payment` | `paymentservice/paymentserviceproto` |
| 700–799 | `limiter` | `net/rpc/limiter/limiterproto` |
| 800–899 | `filesyncv2` | `commonfile/fileproto/fileprotov2` |
| 900–999 | `filesyncp2p` | `commonfile/fileproto/filep2p` |
| 1000–1099 | `nodesync` | `any-sync-node` · `nodesync/nodesyncproto` |
| 1100–1199 | `pubsub` | `commonspace/pubsub/pubsubproto` |

## 读这些 proto 时容易踩的坑

1. **不是 gRPC**：所有服务都是 DRPC（shturl.cc），编码默认 `None`，握手阶段协商。
2. **`changeType` 是任意字符串**：网络不解释它；库 / 记录 / 空间设置都靠它区分，由应用自己定义。
3. **对象 = 一个根 + 变更链**：对象 ID 由根算出，所以“往已有对象追加变更”不会产生新对象。
4. **`ObjectSyncRequestStream` 是拉取**：请求必须是 `TreeSyncMessage` 里的 `fullSyncRequest`，否则节点返回 `tree not found`。
5. **写入用 `ObjectSyncStream`（双向长连接）**：发 `headUpdate` 通知节点有新对象，节点回拉后再通过请求流提交数据。
6. **`Credential` 是 coordinator 回执**：`SpacePush` 时必须携带 `SpaceReceiptWithSignature`，节点会校验签名与有效期。
