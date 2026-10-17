#!/bin/bash
# 启动本地网络依赖的基础设施：mongo-1 / redis / minio（仅这三个容器）
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/compose/any-sync-dockercompose"

if ! docker info >/dev/null 2>&1; then
  echo "== 启动 Docker Desktop =="
  open -a Docker
  for i in $(seq 1 60); do docker info >/dev/null 2>&1 && break; sleep 2; done
fi
docker info >/dev/null 2>&1 || { echo "ERROR: docker daemon 未就绪"; exit 1; }

docker compose up -d mongo-1 redis minio create-bucket
for s in mongo-1 redis minio; do
  name="any-sync-dockercompose-${s}-1"
  for i in $(seq 1 30); do
    st=$(docker inspect --format '{{.State.Health.Status}}' "$name" 2>/dev/null || echo none)
    [ "$st" = healthy ] && break; sleep 2
  done
  echo "  $s = $st"
done
echo "基础设施就绪：mongo 127.0.0.1:27001 / redis 127.0.0.1:6379 / minio 127.0.0.1:9000"
