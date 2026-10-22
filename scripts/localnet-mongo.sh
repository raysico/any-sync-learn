#!/bin/bash
# 打开本地 any-sync 网络的 Mongo shell，自动使用 compose/.env 里的 MONGO_1_PORT。
#
# 为什么需要它：本栈的 mongod 监听 27001（不是默认 27017）。在容器里直接
# 跑 `mongosh` 会去连 127.0.0.1:27017，报 ECONNREFUSED——看起来像 Mongo 挂了，
# 实际 coordinator 一直连着 mongo-1:27001，业务完全正常。
#
# 用法：
#   scripts/localnet-mongo.sh                                  # 交互式 shell
#   scripts/localnet-mongo.sh coordinator                      # 直接进 coordinator 库
#   scripts/localnet-mongo.sh coordinator --eval 'db.spaces.countDocuments({})'
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_DIR="$ROOT/compose/any-sync-dockercompose"
cd "$COMPOSE_DIR"

if [ ! -f .env ]; then
  echo "ERROR: 缺少 $COMPOSE_DIR/.env（先按 README 准备本地网络）" >&2
  exit 1
fi

PORT="$(sed -n 's/^MONGO_1_PORT=//p' .env | head -1)"
PORT="${PORT:-27001}"

if [ "$#" -eq 0 ]; then
  exec docker compose exec mongo-1 mongosh --port "$PORT"
fi
exec docker compose exec -T mongo-1 mongosh --port "$PORT" "$@"
