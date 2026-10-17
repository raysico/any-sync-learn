#!/bin/bash
# 独立本地 any-sync 网络（全源码二进制）公共环境变量
# 用法：source scripts/localnet-env.sh
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export LOCALNET_ROOT="$ROOT/playground/local-net"
export GO_BIN="$ROOT/src"

# 各组件二进制路径
export BIN_COORDINATOR="$GO_BIN/any-sync-coordinator/bin/any-sync-coordinator"
export BIN_CONFAPPLY="$GO_BIN/any-sync-coordinator/bin/any-sync-confapply"
export BIN_CONSENSUS="$GO_BIN/any-sync-consensusnode/bin/any-sync-consensusnode"
export BIN_FILENODE="$GO_BIN/any-sync-filenode/bin/any-sync-filenode"
export BIN_NODE="$GO_BIN/any-sync-node/bin/any-sync-node"
export BIN_NETCHECK="$GO_BIN/any-sync-tools/bin/any-sync-netcheck"
