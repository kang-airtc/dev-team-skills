# company-site / backend

现代公司站点后端骨架。

## 技术栈

- FastAPI 0.100 + uvicorn
- SQLAlchemy 2.0（asyncio） + asyncpg + PostgreSQL 15
- Alembic 数据库迁移
- python-jose + passlib（bcrypt）
- Loguru 日志
- pydantic-settings 配置

## 目录

```
backend/
├── alembic.ini
├── requirements.txt
├── Dockerfile
├── .env.example
└── server/
    ├── __main__.py          # uvicorn 启动入口
    ├── settings.py
    ├── dependencies.py      # get_db_session
    ├── db_utils.py
    ├── logging.py           # loguru
    ├── auth.py              # 当前用户 / 超级管理员依赖
    ├── utils/jwt.py
    ├── models/              # User（骨架仅此一表）
    ├── dao/                 # UserDAO
    ├── migrations/          # Alembic
    └── web/
        ├── app.py           # FastAPI 工厂
        ├── app_events.py    # startup/shutdown
        └── api/
            ├── error_codes.py
            ├── response.py
            ├── router.py
            └── users/       # 注册 / 登录 / 刷新 / /me
```

## 启动

```bash
# 本机
pip install -r requirements.txt
cp .env.example .env
# 启动 PostgreSQL（或通过根目录 docker-compose.yml）
alembic revision --autogenerate -m "init"
alembic upgrade head
python -m server
```

- API 根：`http://localhost:8000/api`
- Swagger：`http://localhost:8000/api/docs`

## 业务路由待补


