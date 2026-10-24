#!/usr/bin/env bash
# Clone every source repo (shallow) into ./src, named owner_repo, ready for build.py.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p src
while read -r repo; do
  [ -n "$repo" ] || continue
  dir="src/$(echo "$repo" | tr '/' '_')"
  if [ -d "$dir" ]; then git -C "$dir" pull -q --depth 1; else git clone -q --depth 1 "https://github.com/$repo" "$dir"; fi
  echo "$repo"
done < sources.txt
