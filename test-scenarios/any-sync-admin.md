# any-sync-admin 回归测试方案

> 对象：`test/tools/any-sync-admin`（方案 20261017 17:35-01 · 日志证据驱动）
> 前置：`bash scripts/localnet-infra.sh && bash scripts/localnet-start.sh`，userdomain-web 在 8787 运行

## 0. 启动

```bash
cd dev/any-sync-learn/test/tools/any-sync-admin
./bin/any-sync-admin -addr 0.0.0.0:8790
# 浏览器 http://127.0.0.1:8790/
```

## 1. 网络配置常驻

- [ ] 左栏显示 networkId / coordinator / 配置文件路径 / 配置 ID
- [ ] 左栏列出 6 个节点，标签为 node-1…node-3 / coordinator / file / consensus
- [ ] 改 `playground/local-net/nodes.yml` 的节点顺序后刷新，标签随之变化

## 2. 节点连接状态

- [ ] 6 个节点全绿，延迟 0–5ms
- [ ] `kill $(cat /tmp/anysync-node-2.pid)` 后 4 秒内 node-2 变红并显示 `connect: connection refused`
- [ ] 重启 node-2 后恢复绿色
- [ ] 链路矩阵只出现有 RPC 证据的边，且形如 `coordinator → node-1`

## 3. 已握手用户

- [ ] 右栏列出用户，含客户端与网络节点两类
- [ ] 「在线/离线」三个页签筛选正确
- [ ] 用 userdomain-web 生成用户域后，右栏在线数增加（有 RPC 时）

## 4. 远程日志来源（为远端部署预留）

```bash
mkdir -p /tmp/remote-logs && cp playground/local-net/logs/node-1.log /tmp/remote-logs/
(cd /tmp/remote-logs && python3 -m http.server 9100 --bind 127.0.0.1 &)
./bin/any-sync-admin -addr 0.0.0.0:8791 -network ../../../playground/local-net/nodes.yml \
  -logs "coordinator=http://127.0.0.1:9100/node-1.log,node-1=http://127.0.0.1:9100/node-1.log"
```

- [ ] 「日志来源」里对应条目显示 `remote`
- [ ] 远端不可达时该条目显示错误且其它来源不受影响

## 5. 只读性

- [ ] 运行期间 `playground/local-net/logs/` 文件大小只因节点自身写入而增长
- [ ] 无任何写网络的动作（不发 RPC、不改配置）
