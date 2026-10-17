# 用户域 Web 客户端 · 推荐回归测试方案

> 对应工具：`test/tools/userdomain-web/`（测试工具本身不入库，本方案入库）
> 适用版本：commit `db31858` 之后
> 前置：`bash scripts/localnet-infra.sh && bash scripts/localnet-start.sh`，然后 `cd test/tools/userdomain-web && ./bin/userdomain-web -addr 0.0.0.0:8787 -network ../../../playground/local-net/nodes.yml`

## 一、手工验收（浏览器）

| # | 步骤 | 期望结果 |
|---|---|---|
| 1 | 打开 `http://127.0.0.1:8787/` | 左栏显示 networkId / coordinator / 6 个节点；顶栏「网络配置已加载 · 6 个节点」 |
| 2 | 点「生成用户域」 | 右侧出现登录成功；中栏显示账户 ID、peerId、以太坊地址、四组密钥、助记词 |
| 3 | 抄下助记词 → 点「清空」→ 粘贴助记词 → 点「用助记词登录」 | 账户 ID 与第 2 步完全一致 |
| 4 | 点右侧历史列表里的旧记录 | 中栏切换成该记录，提示「已载入并登录」 |
| 5 | 点「导出全部」 | 浏览器下载 `userdomain-export-*.json`，内容是数组且含助记词 |
| 6 | 删除一条 → 点「导入」选刚导出的文件 | 「导入完成：新增 N 条」，记录被补回 |
| 7 | 改坏导出文件里某条的 `accountId` 后导入 | 入库记录的账户 ID 仍按助记词推导，不被篡改值影响 |
| 8 | 局域网访问 `http://<本机内网IP>:8787/` 重复第 2 步 | 同样登录成功；说明栏列出补全的局域网地址 |
| 9 | 改错一个助记词再登录 | 提示「助记词校验失败：请检查词数与拼写」 |
| 10 | `bash scripts/localnet-stop.sh` 后生成用户域 | 用户域已生成，登录失败并显示「无法建立连接」；恢复网络后重试成功 |

## 二、接口回归（命令行）

```bash
B=http://127.0.0.1:8787
curl -s $B/api/network | jq '.networkId, .coordinator, (.nodes|length)'          # 期望：6
curl -s -X POST $B/api/userdomain -d '{}' | jq '.login.ok'                      # 期望：true
curl -s $B/api/userdomains | jq 'length'                                         # 期望：>=1
curl -s -D- $B/api/userdomains/export -o /tmp/e.json | grep -i content-disposition
curl -s -X POST $B/api/userdomains/import --data-binary @/tmp/e.json | jq .     # {imported:N, skipped:0}
curl -s -X POST $B/api/userdomains/import --data-binary 'x' | jq .              # 期望：400 + error
curl -s -X POST $B/api/userdomains/delete?id=不存在的ID | jq .                     # 期望：{"deleted":...}
curl -s -X POST $B/api/login -d '{"mnemonic":"a b c d e f g h i j k l"}' | jq . # 期望：400
```

## 三、数据安全回归

| 检查 | 命令 | 期望 |
|---|---|---|
| 历史文件权限 | `ls -l test/tools/userdomain-web/data/userdomains.jsonl` | `-rw-------` |
| 数据目录权限 | `ls -ld test/tools/userdomain-web/data` | `drwx------` |
| 文件内容 | 抽查该文件 | 每条一行 JSON，含助记词（确认这是敏感文件） |

## 四、边界说明

- 助记词与私钥只在浏览器与本机之间流转，网络侧只收到签名；回归时不要在共享渠道粘贴真实助记词。
- 本方案只覆盖“登录 + 用户域 + 历史管理”，库（library）相关能力在下一轮补充测试方案。
