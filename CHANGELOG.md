# CHANGELOG

## 0.1.1 — 2026-10-22

**里程碑**：Milestones0.1.0（补丁版本，不新增里程碑）

### 新增

- **本地开发栈脚本**：`scripts/devstack-start.sh` 一条命令拉起基础设施 → 本地网络 → 本地 Web 组件；`scripts/devstack-stop.sh` 只停 devstack 启动的 Web 进程（pid 记录在 `/tmp`）。
- **Mongo shell 包装**：`scripts/localnet-mongo.sh` 从 `.env` 读 `MONGO_1_PORT`（本栈为 27001），避免 mongosh 默认连 27017 报 `ECONNREFUSED`；支持交互式，也支持 `--eval` 直接查 coordinator 库。
- **界面截图归档**：`resources/any-sync/userdomain-web/` 收录三栏界面与历史面板截图。
- 协作文档：`AGENTS.md` 增加「疑问 / 咨询只给答案，不改代码」条款。

### 变更

- `TECH.md` 补充密钥体系 S1–S9、空间分类与密钥来源、实时同步通道、设备密钥隔离、本地网络重启排障；§12.2 新增「Mongo 在 27001」的判定依据与空间记录查询。
- `scripts/fetch_all.sh` 移除 `any-sync-admin`（功能失效已弃用）；`TECH-ARCHI.md` 的版本基线同步标注弃用。

### 验证

- `bash -n scripts/*.sh` 全部通过。
- `scripts/localnet-mongo.sh coordinator --eval 'db.spaces.countDocuments({})'` 返回 11（2026-10-22 本地网络），`rs.status()` 为 `rs0` PRIMARY。
- 端口口径三处一致：compose `.env`、coordinator `mongo.connect`、包装脚本均为 27001。

### 关联提交

- dev：`4acf5b0`、`7125633`、`17e120b`、`85bcb62`、`055243a`、`078fb29`、`fb35702`、`9ba6455`、`3b609ab`、`268f336`
- tag：`v0.1.1`（发布时打在 main 的合并提交上）

## 0.1.0 — 2026-10-18

**里程碑**：Milestones0.1.0

### 新增

- **userDomain Web 客户端**（本地工具，位于 `test/tools/userdomain-web`）
  - 用户域 = any-sync Space；库 / 信息对象 = 空间内独立对象树
  - 库注册表树（派生根）承载“用户域有哪些库”；库树承载字段定义与信息对象索引
  - 建库、写记录、删除库、删除记录均为网络变更，可被其他设备同步
  - 用助记词登录：清空本地残留 → 握手 → 按账户切换用户域 → 全量拉取
  - 「删除本地数据」「刷新本地」「从网络拉取」三个测试用操作
  - 三栏界面 + 底部 40px 版本页脚（版本取 package.json，提交号构建时注入）
  - 主 / 副本双实例：副本后台每 20 秒拉取，前端每 5 秒轮询列表
- **协议文档中文化**：`docs/protoinchinese/` 收录 38 个 .proto 中文注释版与索引
- **技术文档**：`TECH.md` 重写，覆盖对象模型、四条链路、错误码区间、排障速查；旧文档归档为 `TECH-ARCHI.md`

### 修复

- 节点反向流未被接受导致对象不落盘（`tree does not exist`）
- 追加变更时 objectId 误用变更 ID、缺少 SnapshotBaseId/ReadKeyId、内容双重加密
- 签名根树追加被拒（改用派生根）
- 新建用户域未真正创建空间，导致拉到上一个用户域的数据
- 助记词账户与用户域所有者不一致时静默写入
- 副本页面被浏览器缓存、数据不自动同步

### 关联提交

- dev：`956ade6` 及之前一系列提交
- tag：`Milestones0.1.0`
