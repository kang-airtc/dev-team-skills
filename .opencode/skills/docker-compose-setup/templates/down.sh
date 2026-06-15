#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose down 2>/dev/null || docker-compose down
echo "已停止。如需删除数据卷请加 -v 参数。"
