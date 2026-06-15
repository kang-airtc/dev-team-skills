---
name: deploy-release
description: 生成版本发布说明文档，包含版本号、变更摘要、升级指南和回滚方案
---

# Deploy Release - 发布说明生成

基于 CHANGELOG 和项目配置，生成完整的版本发布说明文档（Release Notes），包含升级指南和回滚方案。

## 触发场景

- 版本发布时需要发布说明
- 需要升级指南和回滚方案
- 对外发布版本时需要正式文档
- 团队协作时统一发布标准

## 目录结构

```
deploy-release/
├── SKILL.md
├── scripts/
│   └── generate.py
└── assets/
    └── release-template.md
```

## 依赖

- Python 标准库

## 使用方法

```bash
# 基于 CHANGELOG 生成发布说明
python3 .opencode/skills/deploy-release/scripts/generate.py \
  --version v1.2.0 \
  --changelog CHANGELOG.md

# 指定输出
python3 .opencode/skills/deploy-release/scripts/generate.py \
  --version v1.2.0 \
  --output release-v1.2.0.md
```

参数：
- `--version, -v`：版本号（必填）
- `--changelog`：CHANGELOG 文件路径
- `--previous-version`：回滚目标版本号；不传时优先从 CHANGELOG 中匹配，再从 `git tag` 列表推断，都失败时输出 `<previous-version>` 占位符
- `--output, -o`：输出路径

## 输出格式

```markdown
# Release Notes - v1.2.0

**发布日期**: 2024-01-15
**版本类型**: 功能版本

## 变更摘要

### 新增功能
- 添加用户登录功能
- 支持手机号注册

### 问题修复
- 修复登录态过期问题
- 修复移动端样式错位

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

- **数据库**: 有 Schema 变更，需执行迁移
- **API**: 向下兼容
- **前端**: 需清除浏览器缓存
```

## 边界

- 基于 CHANGELOG 生成，需要先有 CHANGELOG
- 回滚方案为通用模板，需根据实际情况调整
- 不自动执行发布操作

## 与其他 Skill 的关系

```
deploy-changelog ──▶ deploy-release ──▶ deploy-pipeline
  变更日志          发布说明          发布流水线
```
