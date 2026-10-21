#!/bin/bash
cd "$(dirname "$0")"
repos="any-sync any-sync-coordinator any-sync-node any-sync-filenode any-sync-consensusnode any-ns-node any-sync-tools any-sync-dockercompose ansible-anysync puppet-anysync any-block anytype-heart"
for r in $repos; do
  if [ -d "$r" ]; then echo "SKIP $r (已存在)"; continue; fi
  echo ">>> 下载 $r ..."
  curl -sL --max-time 180 -o tmp.tar.gz "https://api.github.com/repos/anyproto/$r/tarball/main"
  if [ -s tmp.tar.gz ] && file tmp.tar.gz | grep -q gzip; then
    mkdir -p "$r"
    tar -xzf tmp.tar.gz -C "$r" --strip-components=1
    cnt=$(find "$r" -type f | wc -l | tr -d ' ')
    sz=$(du -sh "$r" | cut -f1)
    echo "    OK $r: $cnt 文件, $sz"
  else
    echo "    FAIL $r"
  fi
  rm -f tmp.tar.gz
done
echo "===== 全部完成 ====="
ls -d */ 2>/dev/null
