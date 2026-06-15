## 本地开发（不用 Docker）

```bash
# 1. 启动 PostgreSQL（仅起 docker-compose 里的 postgres 服务）
docker compose up -d postgres

# 2. 后端
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python -m scripts.seed_demo      # 写入 admin 账号 + 演示数据
SERVER_RELOAD=true python -m server   # http://localhost:8000

# 3. 前端
cd ../frontend
npm install
npm run dev                           # http://localhost:3000
```

---

## Docker 方式启动

```bash
# postgres 已在跑，只构建并启动后端和前端
docker compose up --build backend frontend
```

启动后访问：

| 地址 | 说明 |
|------|------|
| http://localhost:3000 | 公开站 |
| http://localhost:3000/login | 后台登录（admin / admin123） |
| http://localhost:3000/dashboard | 后台控制台 |
| http://localhost:8000/api/docs | API 文档 |
