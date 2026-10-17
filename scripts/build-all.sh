#!/bin/bash
# 一键重建 any-sync 全部组件（学习计划第 2 期）
# 用法：bash build-all.sh [只构建指定仓库]
set -e
export PATH="$HOME/.local/go/bin:$PATH"
export GOPROXY="${GOPROXY:-https://goproxy.cn,direct}"
SRC="/Users/ruizhihe/Documents/使用pixcall管理/资源库文件夹/使用百度网盘同步/anythinks/dev/any-sync-learn/src"

REPOS="${*:-any-sync-tools any-sync-consensusnode any-sync-coordinator any-sync-node any-sync-filenode}"
TOTAL_START=$(date +%s)

for r in $REPOS; do
  echo ""
  echo "===== $r ====="
  cd "$SRC/$r" || { echo "  ❌ 目录不存在"; continue; }
  echo "  版本: $(git describe --tags --always 2>/dev/null)"
  start=$(date +%s)
  if make deps >/dev/null 2>&1 && make build >/tmp/build-$r.log 2>&1; then
    dur=$(( $(date +%s) - start ))
    echo "  ✅ 构建成功（${dur}s）"
    ls -la bin/ 2>/dev/null | grep -v "^total\|^d" | awk '{printf "     %-28s %s bytes\n", $NF, $5}'
  else
    echo "  ❌ 构建失败，日志末尾："
    tail -15 /tmp/build-$r.log | sed 's/^/     /'
  fi
done

echo ""
echo "===== 全部完成（总耗时 $(( $(date +%s) - TOTAL_START ))s）====="
