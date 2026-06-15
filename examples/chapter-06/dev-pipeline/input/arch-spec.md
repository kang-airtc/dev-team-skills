# 架构描述：公司站点系统架构

## 组件

- browser: 用户浏览器
- frontend: Next.js 前端（公开站 + 后台管理，同一工程）
- api: FastAPI 后端
- db: PostgreSQL 15
- uploads: 静态文件存储（uploads/ 目录，挂载到 api 容器）

## 依赖关系

- browser -> frontend: HTTPS 访问
- frontend -> api: REST API 调用（JWT 鉴权）
- frontend -> uploads: 直接访问静态资源
- api -> db: SQLAlchemy 2 async 连接
- api -> uploads: 文件读写（本地挂载目录）

## 层次风格

layered（分层架构）
