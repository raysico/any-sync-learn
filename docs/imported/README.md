# 导入的调研资料索引

> 来源：原 `whynownote/any-sync-ecosystem/docs/`（该目录已于 2026-10-17 迁移拆除）
> 本目录为**完整副本**，共 42 个文件 / 1.5MB，迁移时逐项 md5 校验一致。

## 核心资料

| 文件 | 大小 | 内容 |
| --- | --- | --- |
| [any-sync-protobuf-接口参考.md](any-sync-protobuf-接口参考.md) | 387KB / 9342 行 | **最重要的资产**。28 个 proto、17 个 service、112 个 RPC、727 个 message、133 个 enum 的全量中文参考（4366 行表格） |
| [_compare.md](_compare.md) | 232KB / 7548 行 | 同上的对照版底稿 |
| [any-sync-vault-key-derivation.html](any-sync-vault-key-derivation.html) | 5.9KB | 密钥派生体系可视化（助记词 → SLED/BIP39 → Ed25519/ECDSA） |
| [any-sync-two-layer-hashing.html](any-sync-two-layer-hashing.html) | 5.8KB | 两层哈希机制可视化 |
| [any-sync-read-key-rotation.html](any-sync-read-key-rotation.html) | 6.3KB | ReadKey 轮换机制可视化 |
| [any-sync-node-topology.html](any-sync-node-topology.html) | 4.6KB | 节点拓扑可视化 |

## 工具

| 文件 | 用途 |
| --- | --- |
| [tools/parse_proto.py](tools/parse_proto.py) | 解析 `.proto` 源码 |
| [tools/gen_doc.py](tools/gen_doc.py) | 生成上面的接口参考文档 |

## 中文技术文档（`.feishu_import/`，29 个 md + 2 张图）

官方文档汉化版，含 `networking-zh.md`、`access-control-zh.md`、`futurework-zh.md`，以及 `docA/B/C.md` 与 `c01`–`c24` 分章。

## 网页存档（`doc-fetch-resources/`）

3 个已抓取的 HTML 页面存档。

---

**恢复说明**：若需恢复原 `any-sync-ecosystem` 目录本身（例如为了找回仓库目录内的本地改动），可用 Time Machine 本地快照 `2026-10-17-140754`（删除前 31 分钟）。
