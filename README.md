# any-sync-learn

> 从源码构建自有 any-sync 去中心化同步网络，并在其上实现自研的 userDomain 客户端；
> 为后续的去中心化知识、资源以及数字资产管理工具做准备。

当前版本：0.1.0（里程碑 Milestones0.1.0；版本号唯一真源为 package.json，随「准备发布新版」流程同步）

## 项目介绍

本项目用于学习、研究与复现 Anytype 的 any-sync 去中心化同步栈，并在其之上实现一套**不依赖 anytype-heart** 的客户端。

产出分两部分：

- **网络侧**：从源码构建协调节点、共识节点、同步节点与文件节点，拉起一套本地可用的 any-sync 网络；
- **客户端侧**：自研 userDomain Web 客户端，用 any-sync 的 Space 承载「用户域 → 库 → 信息对象」，全部读写流程自己实现。

## 功能特性

### 网络

- 从源码构建 any-sync 各节点并记录可复现步骤；
- 本地网络拓扑：协调节点、共识节点、三个同步节点、文件节点，外加 MongoDB / Redis / MinIO；
- 客户端可向协调节点取网络配置、创建空间（SpaceSign + SpacePush）。

### userDomain 客户端

- **用户域 = Space**；库与信息对象都是空间内的独立对象树，记录通过载荷里的 `lib` 属性归属到库；
- **库注册表树**（派生根）记录用户域下有哪些库；**库树**记录字段定义与信息对象索引；
- **写入**：新建库、写记录都会推送到负责节点，并接受节点在同一连接上反向开流的回拉；
- **删除即更新**：删库写注册表 `del`，删记录写库树 `delInfo`，其他设备同步生效；
- **登录与自举**：用助记词登录 → 清空本地残留 → 握手 → 按账户切换到对应用户域 → 全量拉取；
- **双实例**：主实例与 OTHER 副本共用同一网络，副本后台定时拉取；
- **界面**：三栏布局（网络信息 / 操作与库面板 / 用户域历史），底部 40px 版本页脚。

### 文档

- `docs/protoinchinese/`：38 个 `.proto` 中文注释版与索引；
- `TECH.md`：对象模型、四条已跑通链路、错误码区间、排障速查；旧文档归档于 `TECH-ARCHI.md`。

## 环境依赖

- Go 1.26+（源码在 `src/`，已加入 `.gitignore`，需自行克隆）
- 网络依赖：MongoDB（副本集）、Redis（含 Bloom）、S3 兼容存储（MinIO）、Docker
- 前端：无构建步骤，纯静态页面由客户端进程内嵌服务

## 安装

```bash
# 1. 克隆各 any-sync 仓库到 src/（略，见 TECH-ARCHI.md 的版本基线）
# 2. 启动依赖服务
docker compose -f compose/local-net/docker-compose.yml up -d
# 3. 启动本地网络
npm run localnet:start
# 4. 构建客户端
cd test/tools/userdomain-web
COMMIT=$(git -C ../../.. rev-parse --short HEAD)
go build -ldflags "-X main.buildCommit=$COMMIT" -o bin/userdomain-web .
```

## 使用方法

```bash
# 主实例
./bin/userdomain-web -addr 127.0.0.1:8787
# OTHER 副本（共享同一份本地存档，后台每 20 秒拉取网络）
./bin/userdomain-web -addr 127.0.0.1:8788 -replica other
```

浏览器打开 <http://127.0.0.1:8787>：

1. 点「生成用户域」创建新的用户域（会真实在网络里建一个空间）；
2. 点右侧历史条目只填入助记词，再点「使用助记词登录」才会连接网络并拉取；
3. 在「新建库」处建库，在库卡片内写记录；
4. 「删除本地数据」清空本地，「从网络拉取」重新全量拉回。

## 项目结构

| 路径 | 说明 |
| --- | --- |
| `docs/protoinchinese/` | 38 个 .proto 中文注释版 |
| `docs/any-sync-学习计划.md` | 研习路线与资料索引 |
| `scripts/` | 本地网络启停脚本 |
| `TECH.md` / `TECH-ARCHI.md` | 现行技术文档 / 历史归档 |
| `test/tools/userdomain-web/` | userDomain 客户端（本地，不入库） |

## 作者

- hoxiudimdim（GitHub: [@raysico](https://github.com/raysico)）

## 贡献者

- 欢迎提交 Issue 与 Pull Request。
- 贡献者名单：hoxiudimdim

## 许可证

本项目采用 MIT 许可证，版权归 hoxiudimdim 所有，版权年份 2026。全文见 [LICENSE.md](LICENSE.md)。
