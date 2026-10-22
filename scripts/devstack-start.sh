#!/bin/bash
# 本地开发栈：后台启动本地网络 + userdomain-web + any-sync-admin
# 说明：macOS 没有 setsid，子进程统一用 nohup 启动并记录 pid，避免父 shell 退出时被 SIGHUP 带走。
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== 1/3 基础设施 + 本地网络 =="
bash scripts/localnet-infra.sh >/dev/null
bash scripts/localnet-start.sh | tail -3

echo "== 2/3 userDomain Web（8787） =="
if lsof -nP -iTCP:8787 -sTCP:LISTEN >/dev/null 2>&1; then echo "   已在运行"; else
  ( cd test/tools/userdomain-web && nohup ./bin/userdomain-web -addr 0.0.0.0:8787 > /tmp/userdomain-web.log 2>&1 & echo $! > /tmp/userdomain-web.pid )
  sleep 2
fi

echo "== 3/3 any-sync-admin（8790） =="
if lsof -nP -iTCP:8790 -sTCP:LISTEN >/dev/null 2>&1; then echo "   已在运行"; else
  ( cd test/tools/any-sync-admin && nohup ./bin/any-sync-admin -addr 0.0.0.0:8790 > /tmp/admin.log 2>&1 & echo $! > /tmp/admin.pid )
  sleep 3
fi

echo ""
for p in 2004 8787 8790; do printf "端口 %-5s " $p; lsof -nP -iTCP:$p -sTCP:LISTEN >/dev/null 2>&1 && echo up || echo DOWN; done
echo "userDomain：http://127.0.0.1:8787/   admin：http://127.0.0.1:8790/"