# 库（library）能力回归测试方案

> 对应工具：`test/tools/userdomain-web/`（不入库），测试方案入库。
> 方案来源：`20261017 18:52-01`（共享存储副本，只验收“持相同密钥看到相同数据”）。
> 前置：本地网络运行中；主客户端 8787（`-replica main`）、副本 8788（`-replica other`）。

## 一、实例区分

| # | 步骤 | 期望 |
|---|---|---|
| 1 | 打开 `http://127.0.0.1:8787/` | 右上角徽标「实例：MAIN（主）」，标题「用户域 · userDomain」 |
| 2 | 打开 `http://127.0.0.1:8788/` | 徽标「实例：OTHER（副本）」，标题带「OTHER 副本」，页面外框红色描边 |

## 二、建库与写记录

| # | 步骤 | 期望 |
|---|---|---|
| 1 | 主客户端生成用户域，抄下助记词 | 登录成功 |
| 2 | `POST /api/libraries` 带上助记词与库名 | 返回 spaceId，`responsibleNodes` 有 3 个地址 |
| 3 | `GET /api/libraries` | 列表中能看到该库 |
| 4 | `POST /api/libraries/entries?id=<spaceId>` 写一条 | 返回 changeId |
| 5 | 副本 `GET /api/libraries` | 能看到同一个库（共享存档） |

## 三、同步读取（当前版本口径）

| # | 步骤 | 期望 |
|---|---|---|
| 1 | 副本 `POST /api/libraries/sync?id=<spaceId>` | 返回 `library.entries`，其中至少包含由设置根解出的内容 |
| 2 | 检查响应里 `remote` / `merged` | `merged` ≥ 本地条数 |
| 3 | 已知限制 | 写入的记录（独立变更）当前不会出现在 `remote` 中——已定位为对象模型误用，见下一轮的独立对象根方案 |

## 四、命令行回归

```bash
B=http://127.0.0.1:8787
curl -s $B/api/replica | jq .            # main
curl -s http://127.0.0.1:8788/api/replica | jq .   # other / replica
curl -s $B/api/libraries | jq 'length'   # >= 1
curl -s -X POST $B/api/libraries -d '{"mnemonic":"<助记词>","name":"回归库"}' | jq '.spaceId, .responsibleNodes'
```

## 五、边界说明

- 本方案**不覆盖**共享/邀请（库级别的后续能力）。
- 副本与主客户端共用 `data/libraries.jsonl`，因此“多设备”是共享存储模拟，不是真实的设备授权加入。
- 读取链路的修复验收标准：副本 `/api/libraries/network` 返回的记录条数与主端写��条数一致，且内容一致。
