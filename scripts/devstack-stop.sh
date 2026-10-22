#!/bin/bash
# 停止 userdomain-web / any-sync-admin（本地网络用 localnet-stop.sh 停）
for f in /tmp/userdomain-web.pid /tmp/admin.pid; do
  [ -f "$f" ] && pid=$(cat "$f") && kill "$pid" 2>/dev/null && echo "停止 $(basename "$f" .pid)（$pid）"; rm -f "$f"
done