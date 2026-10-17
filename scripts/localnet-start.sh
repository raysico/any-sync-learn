#!/bin/bash
# 启动独立本地 any-sync 网络（全源码二进制）
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
source "$ROOT/scripts/localnet-env.sh"
mkdir -p "$LOCALNET_ROOT"/logs "$LOCALNET_ROOT"/data/coordinator "$LOCALNET_ROOT"/data/consensusnode "$LOCALNET_ROOT"/data/filenode "$LOCALNET_ROOT"/data/node-1 "$LOCALNET_ROOT"/data/node-2 "$LOCALNET_ROOT"/data/node-3

start() { # name cmd...
  local name=$1; shift
  local pidfile="/tmp/anysync-$name.pid"
  if [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then
    echo "  $name 已在运行（pid $(cat "$pidfile")）"; return
  fi
  nohup "$@" > "$LOCALNET_ROOT/logs/$name.log" 2>&1 &
  echo $! > "$pidfile"
  echo "  $name 启动（pid $(cat "$pidfile")）"
}

echo "== 启动本地网络（源码二进制）=="
start coordinator  "$BIN_COORDINATOR"  -c "$LOCALNET_ROOT/etc/any-sync-coordinator/config.yml"
sleep 3
start consensus    "$BIN_CONSENSUS"    -c "$LOCALNET_ROOT/etc/any-sync-consensusnode/config.yml"
start filenode     "$BIN_FILENODE"     -c "$LOCALNET_ROOT/etc/any-sync-filenode/config.yml"
for i in 1 2 3; do
  start "node-$i"  "$BIN_NODE"         -c "$LOCALNET_ROOT/etc/any-sync-node-$i.yml"
done
sleep 8
echo ""
echo "== 监听端口 =="
lsof -nP -iTCP:2001 -iTCP:2002 -iTCP:2003 -iTCP:2004 -iTCP:2005 -iTCP:2006 -sTCP:LISTEN 2>/dev/null | awk 'NR>1 {print "  " $2, $9}' | sort -k2
echo ""
echo "== netcheck =="
"$BIN_NETCHECK" -c "$LOCALNET_ROOT/etc/any-sync-coordinator/network.yml" 2>&1 | grep -E 'netcheck' | tail -1
