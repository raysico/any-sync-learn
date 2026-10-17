#!/bin/bash
# 一键恢复本地 any-sync 集群（适配新路径）
# 用法：bash restart-network.sh
set -e
COMPOSE_DIR="/Users/ruizhihe/Documents/使用pixcall管理/资源库文件夹/使用百度网盘同步/anythinks/dev/any-sync-learn/compose/any-sync-dockercompose"
NETCHECK="any-sync-dockercompose-netcheck-1"
cd "$COMPOSE_DIR"

echo "== 1/4 检查 Docker daemon =="
if docker info >/dev/null 2>&1; then
  echo "   已在运行"
else
  echo "   启动 Docker Desktop..."
  open -a Docker 2>/dev/null || true
  for i in $(seq 1 40); do
    docker info >/dev/null 2>&1 && break
    sleep 3
  done
  docker info >/dev/null 2>&1 || { echo "   ❌ daemon 未就绪，请手动打开 Docker Desktop"; exit 1; }
fi

echo "== 2/4 拉起集群 =="
docker compose up -d

echo "== 3/4 等待 netcheck 通过 =="
for i in $(seq 1 40); do
  st=$(docker inspect --format '{{.State.Health.Status}}' "$NETCHECK" 2>/dev/null || echo none)
  [ "$st" = "healthy" ] && { echo "   ✅ netcheck healthy（约 $((i*3)) 秒）"; break; }
  sleep 3
done
st=$(docker inspect --format '{{.State.Health.Status}}' "$NETCHECK" 2>/dev/null || echo none)
[ "$st" != "healthy" ] && echo "   ⚠️ netcheck 尚未 healthy（当前=$st），请查看：docker compose logs netcheck"

echo "== 4/4 状态一览 =="
docker compose ps --format 'table {{.Service}}\t{{.Status}}'
echo ""
echo "客户端配置：$COMPOSE_DIR/etc/client.yml（本机）/ client-lan.yml（局域网）"
