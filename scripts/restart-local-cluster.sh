#!/bin/bash
# 重启后一键恢复本地 any-sync 集群
# 用法：bash restart-local-cluster.sh
set -e
cd "$(dirname "$0")"

echo "== 1/4 启动 Docker Desktop =="
if docker info >/dev/null 2>&1; then
  echo "   daemon 已在运行"
else
  open -a Docker 2>/dev/null || true
  echo "   已触发启动，等待 daemon..."
  for i in $(seq 1 40); do
    if docker info >/dev/null 2>&1; then echo "   daemon 就绪"; break; fi
    sleep 3
  done
  docker info >/dev/null 2>&1 || { echo "   ERROR: daemon 未就绪，请手动打开 Docker Desktop"; exit 1; }
fi

echo "== 2/4 拉起集群容器 =="
docker compose up -d

echo "== 3/4 等待 netcheck 通过 =="
for i in $(seq 1 40); do
  st=$(docker inspect --format '{{.State.Health.Status}}' any-sync-dockercompose-netcheck-1 2>/dev/null || echo none)
  if [ "$st" = "healthy" ]; then echo "   netcheck healthy（等待约 ${i}0 秒内）"; break; fi
  sleep 3
done
st=$(docker inspect --format '{{.State.Health.Status}}' any-sync-dockercompose-netcheck-1 2>/dev/null || echo none)
if [ "$st" != "healthy" ]; then
  echo "   WARN: netcheck 尚未 healthy，当前=$st（查看：docker compose logs netcheck）"
fi

echo "== 4/4 状态一览 =="
docker compose ps --format 'table {{.Service}}\t{{.Status}}' | grep -E "any-sync|netcheck|mongo|redis|minio"
echo ""
echo "恢复完成。局域网连接配置：etc/client.yml（含 192.168.3.180）"
