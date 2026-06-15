#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose up -d --build 2>/dev/null || docker-compose up -d --build
echo "已启动。日志: docker compose logs -f"
