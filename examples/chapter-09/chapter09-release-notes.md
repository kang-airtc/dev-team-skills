# Release Notes - v1.2.0

**发布日期**: 2026-04-27
**版本类型**: 功能版本

## 变更摘要

### 新增功能
- tweak landing page for demo

### 问题修复
- stabilize health endpoint response

## 升级指南

1. 备份数据库
2. 拉取最新代码：`git pull origin main`
3. 更新依赖：`docker-compose build --no-cache`
4. 执行数据库迁移：`docker-compose exec backend alembic upgrade head`
5. 重启服务：`docker-compose up -d`

## 回滚方案

如升级后出现问题，按以下步骤回滚：

1. 停止服务：`docker-compose down`
2. 切换到上一个版本：`git checkout v1.1.0`
3. 恢复数据库（如有迁移）：`docker-compose exec backend alembic downgrade -1`
4. 重启服务：`docker-compose up -d`

## 兼容性说明

- **数据库**: 如有 Schema 变更，需执行迁移
- **API**: 向下兼容
- **前端**: 建议清除浏览器缓存
