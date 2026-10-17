#!/bin/bash
# 停止独立本地 any-sync 网络（源码二进制）
for name in coordinator consensus filenode node-1 node-2 node-3; do
  pidfile="/tmp/anysync-$name.pid"
  if [ -f "$pidfile" ]; then
    pid=$(cat "$pidfile")
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" && echo "  停止 $name（pid $pid）"
    else
      echo "  $name 未运行"
    fi
    rm -f "$pidfile"
  fi
done
echo "已停止（mongo/redis/minio 容器保持运行）"
