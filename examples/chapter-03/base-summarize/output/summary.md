已扫描目录：examples/company-site/backend/

  README.md
  requirements.txt
  alembic.ini
  server/
    __main__.py
    auth.py
    settings.py
    dao/          （category_dao / comment_dao / news_dao / product_dao / user_dao）
    models/       （category / comment / news / product / user 五类模型）
    migrations/   （Alembic 迁移脚本）
    web/api/      （categories / comments / news / products / uploads / users 六组路由）
    utils/jwt.py
  scripts/seed_demo.py

---

## 摘要

**用途**：电商平台后端服务，提供商品、资讯、用户和评论的管理接口，配套权限认证体系

**核心要点**：
- 使用 FastAPI + SQLAlchemy 2.x 作为框架和 ORM，Alembic 管理数据库迁移
- 主要资源分五类：商品（product）、资讯（news）、分类（category）、用户（user）、评论（comment）
- 鉴权基于 JWT，分普通用户和管理员两个角色
- DAO 层与路由层分离，各资源均有独立 router 文件

**关键依赖**：
- FastAPI：HTTP 框架
- SQLAlchemy：ORM
- PyJWT：token 签发
- Alembic：数据库迁移
- PostgreSQL（外部）：主数据库

**潜在问题**：
- 评论接口没有看到频率限制
- category 删除时未见级联处理逻辑
- 测试目录暂时为空，缺少接口级测试
