#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据 /tmp/proto_parse_result.json 生成《any-sync 协议 Protobuf 接口参考》Markdown 文档。"""
import json, os

ROOT = "/Users/ruizhihe/Documents/使用pixcall管理/资源库文件夹/使用百度网盘同步/whynownote/any-sync-ecosystem"
results = json.load(open("/tmp/proto_parse_result.json", encoding="utf-8"))

# 服务职责映射（按 服务名 -> (职责, 调用方→被调方)）
SVC_ROLE = {
    "Coordinator": ("协调器：空间注册/路由、网络配置下发、空间列表与配置查询", "客户端 ↔ coordinator"),
    "SpaceSync": ("空间同步核心：对象变更同步、空间存储操作、对象拉取/订阅（客户端↔sync node 主协议）", "客户端 ↔ sync node"),
    "PubSub": ("空间事件发布订阅：推送空间内对象变更事件", "客户端 ↔ sync node"),
    "ClientSpace": ("客户端空间辅助：space 级轻量远程调用（会话/存储信息获取）", "客户端 ↔ sync node"),
    "Consensus": ("ACL 共识校验：成员/权限变更记录的校验与批准（sync node 间由 RAFT 承载）", "sync node ↔ consensus node"),
    "NodeSync": ("sync node 之间的空间数据同步（节点间复制、对账）", "sync node ↔ sync node"),
    "File": ("文件同步 v1：CID 寻址的文件块上传/下载/校验（客户端↔filenode）", "客户端 ↔ filenode"),
    "FileV2": ("文件同步 v2：文件组/文件快照粒度的同步接口（客户端↔filenode）", "客户端 ↔ filenode"),
    "FileP2P": ("P2P 文件传输：客户端之间直接传输文件块（不经 filenode）", "客户端 ↔ 客户端"),
    "IdentityRepo": ("身份仓库：identity 元数据的注册、查询、删除", "客户端 ↔ identity node"),
    "Anyns": ("名字服务：.any 名称的可用性查询、注册、解析、续期、转移", "客户端 ↔ name service"),
    "AnynsAccountAbstraction": ("名字服务账户抽象：链上交易/账户相关的名称操作", "客户端 ↔ name service"),
    "AnyPaymentProcessing": ("支付处理 v1：套餐/订阅/支付意图、余额查询", "客户端 ↔ payment service"),
    "AnyPaymentProcessingV2": ("支付处理 v2：会话支付、订阅管理、发票、权益", "客户端 ↔ payment service"),
    "NodeApi": ("节点调试/管理 API：仅用于调试运维，非业务协议", "运维工具 ↔ sync node"),
    "Test": ("协议测试服务：仅用于框架自测（endtoendtest / streampool）", "测试"),
}

def rel(p):
    return os.path.relpath(p, ROOT)

def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()

def type_cell(f):
    t = f["type"]
    if f["repeated"]:
        return f"repeated {t}"
    return t

# ---------- 组装 ----------
parts = []

parts.append("""# any-sync 协议 Protobuf 接口参考

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
""")

# ---------- 一、协议总览 ----------
parts.append("""
## 一、协议总览

### 1.1 服务全景

| 包 | 服务 | RPC 数 | 职责 | 调用关系 |
|---|---|---|---|---|""")
for r in sorted(results, key=lambda x: (x["pkg"] or "zzz", x["services"][0]["name"] if x["services"] else "")):
    for s in r["services"]:
        role, caller = SVC_ROLE.get(s["name"], ("", ""))
        parts.append(f"| `{r['pkg'] or '（无 package）'}` | `{s['name']}` | {len(s['rpcs'])} | {role} | {caller} |")
parts.append("")

# 1.2 文件清单
parts.append("### 1.2 文件清单\n\n| 相对路径 | package | 服务 | RPC | 消息 | 枚举 |\n|---|---|---|---|---|---|")
for r in sorted(results, key=lambda x: rel(x["path"])):
    svc = "、".join(s["name"] for s in r["services"]) or "—"
    n_rpc = sum(len(s["rpcs"]) for s in r["services"])
    parts.append(f"| `{rel(r['path'])}` | `{r['pkg'] or '—'}` | {svc} | {n_rpc} | {len(r['messages'])} | {len(r['enums'])} |")
parts.append("")

# ---------- 二、RPC 方法详表 ----------
parts.append("""
## 二、RPC 方法详表

> 流式列：`R`=请求流式，`S`=响应流式，`RS`=双向流式，空=普通一元调用。
""")
for r in sorted(results, key=lambda x: rel(x["path"])):
    if not r["services"]:
        continue
    for s in r["services"]:
        role, _ = SVC_ROLE.get(s["name"], ("", ""))
        parts.append(f"\n### {s['name']} · `{r['pkg'] or '（无 package）'}`\n\n**文件**：`{rel(r['path'])}`　　**职责**：{role}\n")
        if s["comment"]:
            parts.append(f"> {esc(s['comment'])}\n")
        parts.append("| 方法 | 流式 | 请求 | 响应 | 说明 |\n|---|---|---|---|---|")
        for m in s["rpcs"]:
            stream = ("R" if m["stream_req"] else "") + ("S" if m["stream_resp"] else "")
            parts.append(f"| `{m['name']}` | {stream or '—'} | `{m['req']}` | `{m['resp']}` | {esc(m['comment'])} |")
        parts.append("")

# ---------- 三、消息结构 ----------
parts.append("""
## 三、消息结构

> 按文件分组；嵌套消息用 `Parent.Child` 点路径表示。`oneof` 行无字段编号。
""")
for r in sorted(results, key=lambda x: rel(x["path"])):
    parts.append(f"\n### {rel(r['path'])}\n")
    for msg in sorted(r["messages"], key=lambda x: ".".join(x["path"])):
        p = ".".join(msg["path"])
        parts.append(f"#### `{p}`\n")
        if msg["comment"]:
            parts.append(f"> {esc(msg['comment'])}\n")
        parts.append("| # | 类型 | 字段 | 说明 |\n|---|---|---|---|")
        for f in msg["fields"]:
            if f["num"] is None:
                parts.append(f"| — | {f['name']} | | {esc(f['comment'])} |")
            else:
                parts.append(f"| {f['num']} | `{type_cell(f)}` | `{f['name']}` | {esc(f['comment'])} |")
        parts.append("")

# ---------- 四、枚举 ----------
parts.append("""
## 四、枚举

> 按文件分组；嵌套枚举用点路径表示。
""")
for r in sorted(results, key=lambda x: rel(x["path"])):
    if not r["enums"]:
        continue
    parts.append(f"\n### {rel(r['path'])}\n")
    for en in sorted(r["enums"], key=lambda x: ".".join(x["path"])):
        parts.append(f"#### `{'.'.join(en['path'])}`\n")
        if en["comment"]:
            parts.append(f"> {esc(en['comment'])}\n")
        parts.append("| 值 | 编号 |\n|---|---|")
        for v in en["values"]:
            parts.append(f"| `{v['name']}` | {v['num']} |")
        parts.append("")

# ---------- 五、附录 ----------
parts.append("""
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
""")

doc = "\n".join(parts)
outdir = os.path.join(ROOT, "docs")
os.makedirs(outdir, exist_ok=True)
out = os.path.join(outdir, "any-sync-protobuf-接口参考.md")
with open(out, "w", encoding="utf-8") as f:
    f.write(doc)

print(f"written: {out}")
print(f"lines: {doc.count(chr(10))}")
print(f"bytes: {os.path.getsize(out)}")
