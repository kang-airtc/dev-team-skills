# company-site 架构

## 组件
- frontend: Next.js 13 前端（公开站 + 后台同工程）
- api: FastAPI 后端（REST 接口 + JWT）
- db: PostgreSQL 15
- uploads: 静态文件目录（挂载到 api 容器）

## 依赖
- frontend -> api: HTTPS REST
- api -> db: SQLAlchemy async
- api -> uploads: 文件读写
- frontend -> uploads: 静态资源直连

## 部署形态

- 三个容器：`company-site-frontend` / `company-site-backend` / `company-site-postgres`
- `uploads/` 通过 docker volume 挂载到宿主机 `./uploads`
- 公开站走 3000、API 走 8000、PostgreSQL 走 5432
- 所有服务在同一 docker network `company-site-net`

## 关键非功能性约束

- 单容器内存上限 512 MB（compose `mem_limit`）
- 上传单文件 ≤ 5 MB，MIME 白名单
- 数据库连接池上限 20，async
