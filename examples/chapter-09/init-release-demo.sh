#!/usr/bin/env bash
# 重建 release-demo：三服务最小 compose（db + FastAPI + nginx 静态前端）+ 带 tag 的 Git 历史
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
DEMO="$ROOT/release-demo"

rm -rf "$DEMO"
mkdir -p "$DEMO/backend" "$DEMO/frontend" "$DEMO/scripts"

cat > "$DEMO/README.md" << 'EOF'
# release-demo

第 9 章自包含小例：不依赖 corporate-site。前端为 nginx 静态页（占位），后端为最小 FastAPI，数据库为 PostgreSQL 15。

本地需已安装 Docker（支持 `docker compose` 或 `docker-compose`）。
EOF

cat > "$DEMO/.env" << 'EOF'
DATABASE_URL=postgresql://demo:demo_dev@localhost:5433/demo
SECRET_KEY=dev-secret-change-me
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF

cat > "$DEMO/.env.example" << 'EOF'
DATABASE_URL=postgresql://demo:demo_dev@localhost:5433/demo
SECRET_KEY=
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF

cat > "$DEMO/docker-compose.yml" << 'EOF'
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: demo
      POSTGRES_PASSWORD: demo_dev
      POSTGRES_DB: demo
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U demo"]
      interval: 5s
      timeout: 5s
      retries: 5
    ports:
      - "5433:5432"

  backend:
    build: ./backend
    depends_on:
      db:
        condition: service_healthy
    env_file: .env
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    depends_on:
      - backend
    env_file: .env
    ports:
      - "3000:80"

volumes:
  pg_data:
EOF

cat > "$DEMO/backend/Dockerfile" << 'EOF'
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn
COPY main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

printf '%s\n' 'from fastapi import FastAPI' 'app = FastAPI()' '@app.get("/health")' 'def health(): return {"ok": True}' > "$DEMO/backend/main.py"

cat > "$DEMO/frontend/Dockerfile" << 'EOF'
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
EOF

printf '%s\n' '<!DOCTYPE html><html><head><meta charset="utf-8"><title>ch09</title></head><body>chapter-09 demo</body></html>' > "$DEMO/frontend/index.html"

cat > "$DEMO/Dockerfile" << 'EOF'
# 可选根镜像：供 deploy-check 演示根目录构建；业务镜像在 backend/、frontend/ 下
FROM alpine:3.19
RUN echo "chapter-09 release-demo placeholder"
CMD ["true"]
EOF

cat > "$DEMO/scripts/up.sh" << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose up -d --build 2>/dev/null || docker-compose up -d --build
echo "已启动。日志: docker compose logs -f"
EOF

cat > "$DEMO/scripts/down.sh" << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose down 2>/dev/null || docker-compose down
EOF

cat > "$DEMO/scripts/rollback.sh" << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "rollback stub：请替换为实际回滚步骤"
EOF
chmod +x "$DEMO/scripts/up.sh" "$DEMO/scripts/down.sh" "$DEMO/scripts/rollback.sh"

cd "$DEMO"
git init -b main
git add .
git commit -m "chore: init release-demo compose"

git tag v1.1.0

echo "<!-- ch09 -->" >> frontend/index.html
git add frontend/index.html
git commit -m "feat(ui): tweak landing page for demo"

printf '%s\n' '# Changelog' '' '## v1.1.0' '- initial scaffold' > CHANGELOG.md
git add CHANGELOG.md
git commit -m "docs: add CHANGELOG seed"

git commit --allow-empty -m "fix(backend): stabilize health endpoint response"

echo "完成：$DEMO （已打 tag v1.1.0，后续提交可供 deploy-changelog 使用）"
