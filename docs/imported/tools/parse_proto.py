#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析 any-sync-ecosystem 中的 .proto 文件，生成结构化 RPC/消息 Markdown 文档（递归解析嵌套消息）。"""
import re, glob, os, json

ROOT = "/Users/ruizhihe/Documents/使用pixcall管理/资源库文件夹/使用百度网盘同步/whynownote/any-sync-ecosystem"

FILES = []
for d in ["any-sync", "any-sync-node", "any-sync-filenode"]:
    FILES += sorted(glob.glob(f"{ROOT}/{d}/**/*.proto", recursive=True))
FILES += sorted(glob.glob(f"{ROOT}/any-block/format/v1/proto/*.proto"))

def parse_block(lines, i, path, out_messages, out_enums, cmt):
    """从开括号后的一行开始解析，遇到匹配的 } 结束。返回 (fields, next_i)。"""
    fields = []
    while i < len(lines):
        l = lines[i].strip()
        if l.startswith("//"):
            cmt.append(l[2:].strip()); i += 1; continue
        if l == "}":
            return fields, i + 1
        m = re.match(r'message\s+(\w+)\s*\{', l)
        if m:
            c = " ".join(cmt); cmt.clear()
            if "}" in l:  # 单行空消息 message Foo {}
                out_messages.append({"path": path + [m.group(1)], "fields": [], "comment": c})
                i += 1
                continue
            sub, i = parse_block(lines, i + 1, path + [m.group(1)], out_messages, out_enums, cmt)
            out_messages.append({"path": path + [m.group(1)], "fields": sub, "comment": c})
            continue
        m = re.match(r'enum\s+(\w+)\s*\{', l)
        if m:
            c = " ".join(cmt); cmt.clear()
            values = []
            i += 1
            while i < len(lines):
                ll = lines[i].strip()
                if ll == "}":
                    i += 1; break
                if ll.startswith("//"):
                    i += 1; continue
                em = re.match(r'(\w+)\s*=\s*(\d+)\s*;', ll)
                if em:
                    values.append({"name": em.group(1), "num": int(em.group(2))})
                i += 1
            out_enums.append({"path": path + [m.group(1)], "values": values, "comment": c})
            continue
        # 字段：map / repeated / optional / 普通
        fm = re.match(r'(?:(repeated)\s+)?(map\s*<\s*([^,>]+)\s*,\s*([^>]+)\s*>|optional\s+([\w.]+)|([\w.<>\[\]]+))\s+(\w+)\s*=\s*(\d+)\s*;', l)
        if fm:
            if fm.group(3):
                ftype = f"map<{fm.group(3).strip()}, {fm.group(4).strip()}>"
            elif fm.group(5):
                ftype = f"optional {fm.group(5)}"
            else:
                ftype = fm.group(6)
            fields.append({
                "num": int(fm.group(8)), "name": fm.group(7), "type": ftype,
                "repeated": bool(fm.group(2)), "comment": " ".join(cmt)
            })
            cmt.clear(); i += 1; continue
        if l.startswith("oneof ") and l.endswith("{"):
            fields.append({"num": None, "name": f"(oneof) {l.split()[1]}", "type": "", "repeated": False,
                           "comment": " ".join(cmt)})
            cmt.clear(); i += 1
            # 跳过 oneof 内部字段（它们没有编号）
            while i < len(lines) and lines[i].strip() != "}":
                i += 1
            i += 1
            continue
        if l.startswith("reserved") or l.startswith("option ") or l.startswith("extensions"):
            i += 1; continue
        i += 1
    return fields, i

def parse_proto(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    pkg = None; imports = []
    services = []; messages = []; enums = []
    cmt = []
    i = 0
    while i < len(lines):
        l = lines[i].strip()
        if l.startswith("//"):
            cmt.append(l[2:].strip()); i += 1; continue
        m = re.match(r'package\s+([\w.]+)\s*;', l)
        if m:
            pkg = m.group(1); i += 1; continue
        m = re.match(r'import\s+["\'<]([^"\'>]+)["\'>]\s*;', l)
        if m:
            imports.append(m.group(1)); i += 1; continue
        m = re.match(r'service\s+(\w+)\s*\{', l)
        if m:
            c = " ".join(cmt); cmt.clear()
            svc = {"name": m.group(1), "rpcs": [], "comment": c}
            i += 1
            while i < len(lines):
                ll = lines[i].strip()
                if ll.startswith("//"):
                    cmt.append(ll[2:].strip()); i += 1; continue
                if ll == "}":
                    i += 1; break
                rm = re.match(r'rpc\s+(\w+)\s*\(\s*(stream\s+)?([\w.]+)\s*\)\s*returns\s*\(\s*(stream\s+)?([\w.]+)\s*\)', ll)
                if rm:
                    svc["rpcs"].append({
                        "name": rm.group(1), "stream_req": bool(rm.group(2)), "req": rm.group(3),
                        "stream_resp": bool(rm.group(4)), "resp": rm.group(5), "comment": " ".join(cmt)
                    })
                    cmt.clear()
                i += 1
            services.append(svc)
            continue
        m = re.match(r'message\s+(\w+)\s*\{', l)
        if m:
            c = " ".join(cmt); cmt.clear()
            if "}" in l:  # 单行空消息 message Foo {}
                messages.append({"path": [m.group(1)], "fields": [], "comment": c})
                i += 1
                continue
            fields, i = parse_block(lines, i + 1, [m.group(1)], messages, enums, cmt)
            messages.append({"path": [m.group(1)], "fields": fields, "comment": c})
            continue
        m = re.match(r'enum\s+(\w+)\s*\{', l)
        if m:
            c = " ".join(cmt); cmt.clear()
            values = []
            i += 1
            while i < len(lines):
                ll = lines[i].strip()
                if ll == "}":
                    i += 1; break
                if ll.startswith("//"):
                    i += 1; continue
                em = re.match(r'(\w+)\s*=\s*(\d+)\s*;', ll)
                if em:
                    values.append({"name": em.group(1), "num": int(em.group(2))})
                i += 1
            enums.append({"path": [m.group(1)], "values": values, "comment": c})
            continue
        i += 1
    return {"path": path, "pkg": pkg, "imports": imports,
            "services": services, "messages": messages, "enums": enums}

results = []
for p in FILES:
    try:
        results.append(parse_proto(p))
    except Exception as e:
        print("PARSE FAIL", p, repr(e))

with open("/tmp/proto_parse_result.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)

svc_total = sum(len(r["services"]) for r in results)
rpc_total = sum(len(s["rpcs"]) for r in results for s in r["services"])
msg_total = sum(len(r["messages"]) for r in results)
enum_total = sum(len(r["enums"]) for r in results)
print(f"files={len(results)} services={svc_total} rpcs={rpc_total} messages={msg_total} enums={enum_total}")
for r in results:
    rel = os.path.relpath(r["path"], ROOT)
    print(f"  {rel}: pkg={r['pkg']} svc={len(r['services'])} rpc={sum(len(s['rpcs']) for s in r['services'])} msg={len(r['messages'])} enum={len(r['enums'])}")
