#!/usr/bin/env python3
# 把各仓库 .proto 翻译成中文注释版，输出到 docs/protoinchinese/
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "docs", "protoinchinese")

GLOSSARY = {
  "is used to": "用于", "is used for": "用于", "used for": "用于",
  "root change": "根变更", "tree change": "树变更", "raw tree change": "原始树变更",
  "tree head ids": "树的头节点 ID 列表", "acl head id": "ACL 头记录 ID",
  "snapshot base id": "快照基础 ID", "changes data": "变更数据", "read key id": "读密钥 ID",
  "read key": "读密钥", "identity": "身份", "is snapshot": "是否为快照", "data type": "数据类型",
  "space id": "空间 ID", "change type": "变更类型", "change payload": "变更载荷",
  "is derived": "是否为派生", "parent id": "父对象 ID", "repeated": "重复", "arbitrary": "任意",
  "timestamp": "时间戳", "signature": "签名", "payload": "载荷", "snapshot": "快照",
  "seed": "随机种子（使根变更唯一）", "space settings": "空间设置",
  "object delete": "对象删除", "space delete": "空间删除", "deleter peer id": "删除者 peer ID",
  "store header": "存储头", "storage name": "存储名", "header": "头部",
  "file proto version": "文件协议版本", "space header version": "空间头版本",
  "replication key": "复制键（一致性哈希路由）", "space header": "空间头", "space type": "空间类型",
  "space payload": "空间载荷", "space push": "空间推送", "space pull": "空间拉取",
  "head update": "头更新", "full sync request": "全量同步请求", "full sync response": "全量同步响应",
  "error response": "错误响应", "head sync": "头同步", "store diff": "存储差异", "store elements": "存储元素",
  "acl add record": "ACL 添加记录", "acl get records": "ACL 获取记录",
  "object sync": "对象同步", "object sync stream": "对象同步流",
  "object sync request stream": "对象同步请求流",
  "which": "其", "the": "", "of": "的", "to": "到", "in": "在", "for": "用于", "with": "带有",
  "from": "来自", "into": "写入", "on": "在", "that": "，", "this": "该", "these": "这些",
  "its": "其", "is": "是", "are": "是", "was": "曾是", "were": "曾是", "be": "被",
  "can": "可", "should": "应当", "must": "必须", "may": "可能", "will": "将", "if": "如果",
  "otherwise": "否则", "empty": "空", "optional": "可选", "deprecated": "已废弃", "required": "必需",
  "default": "默认", "only": "仅", "not": "不", "no": "无", "each": "每个", "all": "所有", "any": "任意",
  "first": "第一个", "last": "最后一个", "next": "下一个", "previous": "上一个", "same": "相同",
  "used": "使用", "store": "存储", "request": "请求", "response": "响应", "message": "消息",
  "field": "字段", "records": "记录", "record": "记录", "peer id": "peer ID", "node": "节点",
  "nodes": "节点", "space": "空间", "spaces": "空间", "user": "用户", "users": "用户",
  "account": "账户", "accounts": "账户", "file": "文件", "files": "文件", "key": "密钥",
  "keys": "密钥", "error": "错误", "errors": "错误", "public": "公开", "private": "私有",
  "current": "当前", "new": "新", "old": "旧", "size": "大小", "count": "数量", "list": "列表",
  "index": "索引", "tree": "树", "trees": "树", "object": "对象", "objects": "对象",
  "document": "文档", "document id": "文档 ID", "time": "时间", "type": "类型", "types": "类型",
  "code": "代码", "codes": "代码", "status": "状态", "limit": "限制", "limits": "限制",
  "offset": "偏移", "id": "ID", "ids": "ID", "true": "是", "false": "否", "zero value": "零值",
  "malformed": "格式错误", "oversized": "超大", "identity mismatch": "身份不匹配",
  "bad signature": "签名无效", "no permissions": "无权限", "in the space acl": "在空间的 ACL 中",
  "publish rate limit": "发布速率限制", "exceeded": "已超出",
  "wildcard placement": "通配符位置", "reserved chars": "保留字符", "non canonical form": "非规范形式",
  "note": "注意", "todo": "待办", "warning": "警告", "important": "重要",
  "e g": "例如", "i e": "即",
}

PHRASES = {
  "Acl record": "ACL 记录", "Acl root": "ACL 根", "Acl content value": "ACL 内容值",
  "Acl encrypted read key": "ACL 加密后的读密钥", "invite": "邀请", "revoke": "撤销",
  "permission change": "权限变更", "read key change": "读密钥变更", "account remove": "移除账户",
  "account request join": "账户申请加入", "account request accept": "账户申请通过",
  "account request decline": "账户申请拒绝", "account request remove": "账户申请移除",
  "account request cancel": "账户申请取消", "accounts add": "添加账户",
  "identity signature": "身份签名", "metadata pub key": "元数据公钥",
  "encrypted metadata priv key": "加密的元数据私钥", "encrypted owner metadata": "加密的所有者元数据",
  "invite join": "邀请加入", "invite change": "邀请变更",
}

SPECIALS = {
  "is a change of a tree": "是树的一次变更",
  "is a root of a tree": "是一棵树的根",
  "is an id of space where the document is placed": "文档所在空间的 ID",
  "is this change creation timestamp": "该变更的创建时间戳",
  "is a random bytes to make root change unique": "用于让根变更唯一的随机字节",
  "is a public key of the trees creator": "树创建者的公钥",
  "is a payload related to change type": "与变更类型相关的载荷",
  "tells if the tree is derived": "标识该树是否为派生树",
  "is the id of the parent object for bound derived objects": "绑定派生对象的父对象 ID",
  "are previous ids for this tree change": "本树变更的前置头 ID 列表",
  "is a cid of latest acl record at the time of this change": "本变更创建时最新 ACL 记录的 CID",
  "is a snapshot root of the tree where this change is added": "本变更所加入的树的快照（根）",
  "is an arbitrary payload to be read by the client": "供客户端读取的任意载荷",
  "is the id of the read key": "读密钥的 ID",
  "is a public key with which the raw payload of this change is signed": "用于签名本变更原始载荷的公钥",
  "indicates whether this change contains a snapshot of state": "表示本变更是否包含状态快照",
  "indicates some special parameters of data for the client": "为客户端提供的数据特殊参数",
}

def translate_comment(text):
    t = text.strip()
    if not t:
        return "//"
    if re.search(r"[\u4e00-\u9fff]", t):
        return "// " + t
    low = re.sub(r"[^a-z0-9 ]+", "", t.lower()).strip()
    low = re.sub(r"\s+", " ", low)
    if low in SPECIALS:
        return "// " + SPECIALS[low]
    out = t
    for k in sorted(PHRASES, key=len, reverse=True):
        out = re.sub(re.escape(k), PHRASES[k], out, flags=re.I)
    def repl(m):
        key = m.group(0).lower()
        return GLOSSARY.get(key, m.group(0))
    out = re.sub(r"[A-Za-z][A-Za-z\x27\-]*", repl, out)
    out = re.sub(r"\s+", " ", out).strip()
    out = out.replace(" ,", "，").replace(" .", "。")
    if not re.search(r"[\u4e00-\u9fff]", out):
        out = "【原文】" + t
    return "// " + out

def process_line(line, in_block):
    stripped = line.strip()
    if in_block:
        if stripped == "*/":
            return line, False
        m = re.match(r"^(\s*)\*(.*)$", line)
        if m:
            return m.group(1) + "* " + translate_comment(m.group(2).rstrip("/").strip())[3:] + "\n", True
        return line, True
    if stripped.startswith("/*"):
        return line, True
    m = re.match(r"^(.*?)(//\s*)(.*)$", line)
    if m and not stripped.startswith("//"):
        return m.group(1) + m.group(2) + translate_comment(m.group(3))[3:] + "\n", False
    if stripped.startswith("//"):
        return translate_comment(stripped[2:]) + "\n", False
    return line, False

def header(repo, rel, text):
    services = re.findall(r"^service\s+(\w+)", text, re.M)
    rpcs = re.findall(r"^\s*rpc\s+(\w+)", text, re.M)
    pkg = re.search(r"^package\s+([\w.]+)", text, re.M)
    return "\n".join([
      "// ============================================================",
      "// 源文件：src/" + rel,
      "// 所属仓库：" + repo,
      "// proto 包：" + (pkg.group(1) if pkg else "（无）"),
      "// 服务：" + (", ".join(services) if services else "（无 service，仅 message 定义）"),
      "// RPC 数量：" + str(len(rpcs)),
      "// 说明：由 scripts/translate-proto.py 生成；字段名、编号、类型保持原样，注释译为中文。",
      "// ============================================================",
      "", ""])

def main():
    targets = []
    for repo in sorted(os.listdir(SRC)):
        repo_dir = os.path.join(SRC, repo)
        if not os.path.isdir(repo_dir):
            continue
        for root, dirs, files in os.walk(repo_dir):
            if "/.git" in root or "/node_modules" in root:
                continue
            for f in files:
                if f.endswith(".proto"):
                    targets.append((repo, os.path.join(root, f)))
    print("found", len(targets), "proto files")
    os.makedirs(OUT, exist_ok=True)
    manifest = []
    hand_done = {
        "commonspace/object/tree/treechangeproto/protos/treechange.proto",
        "commonspace/object/acl/aclrecordproto/protos/aclrecord.proto",
        "commonspace/spacesyncproto/protos/spacesync.proto",
        "consensus/consensusproto/protos/consensus.proto",
        "identityrepo/identityrepoproto/protos/identityrepo.proto",
        "util/crypto/cryptoproto/protos/crypto.proto",
        "net/secureservice/handshake/handshakeproto/protos/handshake.proto",
        "commonspace/clientspaceproto/protos/clientspace.proto",
        "coordinator/coordinatorproto/protos/coordinator.proto",
        "commonspace/pubsub/pubsubproto/protos/pubsub.proto",
        "nodesync/nodesyncproto/protos/nodesync.proto",
        "debug/nodedebugrpc/nodedebugrpcproto/protos/nodedebugrpc.proto",
        "index/indexproto/protos/index.proto",
    }
    for repo, path in targets:
        rel = os.path.relpath(path, os.path.join(SRC, repo))
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if rel in hand_done:
            print("skip (hand translated):", rel)
            manifest.append((repo, rel))
            continue
        out_lines = [header(repo, rel, text)]
        in_block = False
        for line in text.splitlines(keepends=True):
            nl, in_block = process_line(line, in_block)
            out_lines.append(nl)
        dst = os.path.join(OUT, repo, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write("".join(out_lines))
        manifest.append((repo, rel))
    idx = ["# any-sync 生态 .proto 中文注释版", "",
           "> 由 `scripts/translate-proto.py` 从 `src/` 各仓库生成；字段名、编号、类型保持不变，注释译为中文。",
           "> 标注为【原文】的注释是词典未覆盖的句子，保留英文原文待人工复核。", "",
           "| 仓库 | 源路径 | 中文版 |", "| --- | --- | --- |"]
    for repo, rel in manifest:
        idx.append("| %s | `%s` | [%s](%s) |" % (repo, rel, rel, repo + "/" + rel))
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(idx) + "\n")
    print("wrote", len(manifest), "files")

if __name__ == "__main__":
    main()