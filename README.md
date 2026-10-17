# any-sync-learn

> 从源码构建自有 any-sync 去中心化同步网络的学习与研究项目。
> 未来计划开发自己的去中心化知识、资源以及数字资产管理工具做准备；

当前版本：0.0.0（唯一真源为 package.json，随「准备发布新版」流程同步）

## 项目介绍

本项目用于学习与研究如何从源码构建一套自有的 any-sync 网络，目标是把 Anytype 官方去中心化同步栈的编译、组网、配置与运行流程摸清并复现出来。项目以学习研究为导向，产出可复现的构建步骤、配置说明与验证方法，而非直接用于生产部署。

适用场景：

- 在本地或私有环境拉起一套最小可用的 any-sync 网络，理解各节点职责与依赖关系。
- 跟踪官方仓库（any-sync、any-sync-node、any-sync-coordinator、any-sync-consensusnode、any-sync-filenode、any-sync-tools 等）的源码结构、构建方式与版本兼容性。
- 记录构建与组网过程中遇到的坑、选型对比与验证结论，形成可追溯的学习档案。

## 功能特性

- 从源码构建 any-sync 各节点组件，并记录可复现的构建步骤。
- 搭建最小可用网络拓扑（协调节点 + 共识节点 + 同步节点），跑通客户端接入与数据同步。
- 记录各组件依赖的外部服务（MongoDB 副本集、Redis-stack + Bloom、S3 兼容存储、EVM 链环境）与配置要点。
- 沉淀学习笔记、构建脚本与验证清单，供后续复现与扩展。

## 环境依赖

<!-- 运行时、依赖库、外部服务 -->

- 源码：Anytype 官方 any-sync 系列仓库（待随研究进展逐项确认版本与提交点）
- 构建工具链：Go 1.22+（协调/共识/同步节点）、Node.js（部分工具与脚本）
- 数据服务：MongoDB 副本集；文件节点另需 Redis（含 Bloom 模块）与 S3 兼容对象存储
- 容器与编排：Docker / Docker Compose（用于快速拉起依赖服务）

## 安装

```bash
# 待补充：各节点源码的克隆与构建步骤，随研究进展写入
```

## 使用方法

```bash
# 待补充：最小网络的启动、配置与连通性验证步骤
```

## 作者

- hoxiudimdim（GitHub: [@raysico](https://github.com/raysico)）

## 贡献者

- 欢迎提交 Issue 与 Pull Request。
- 贡献者名单：hoxiudimdim

## 许可证

本项目采用 MIT 许可证，版权归 hoxiudimdim 所有，版权年份 2026。全文见 [LICENSE.md](LICENSE.md)。
