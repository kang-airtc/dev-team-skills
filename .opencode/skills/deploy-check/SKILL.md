---
name: deploy-check
description: 发布前检查 Docker 镜像、docker-compose 配置、环境变量、端口冲突和健康检查
---

# Deploy Check - 发布前检查

在应用发布前，检查 Docker 镜像构建、docker-compose 配置、环境变量、端口冲突和健康检查，确保发布顺利。

## 触发场景

- 发布前做最后一轮检查
- CI/CD 流程中的前置检查
- 新环境部署前验证配置
- 排查发布失败原因

## 目录结构

```
deploy-check/
├── SKILL.md
├── scripts/
│   └── check.sh
└── assets/
    └── check-list.md
```

## 依赖

- `docker`
- `docker-compose`
- 仅使用 Shell

## 使用方法

```bash
# 检查当前项目
bash .opencode/skills/deploy-check/scripts/check.sh

# 指定 docker-compose 文件
bash .opencode/skills/deploy-check/scripts/check.sh --compose docker-compose.prod.yml

# 输出详细报告
bash .opencode/skills/deploy-check/scripts/check.sh --output deploy-check-report.md
```

参数：
- `--compose, -c`：docker-compose 文件路径，默认 `docker-compose.yml`
- `--output, -o`：输出报告路径

## 检查项

### Docker 镜像检查
- [ ] Dockerfile 是否存在
- [ ] 镜像能否成功构建
- [ ] 基础镜像版本是否指定（避免 latest）
- [ ] 镜像大小是否合理（< 500MB）

### docker-compose 配置检查
- [ ] 服务定义完整（frontend/backend/db）
- [ ] 端口映射无冲突
- [ ] 环境变量文件存在
- [ ] 数据卷挂载正确
- [ ] 网络配置正确
- [ ] 健康检查配置

### 环境变量检查
- [ ] `.env` 文件存在
- [ ] 必要变量已设置（DATABASE_URL、SECRET_KEY 等）
- [ ] 无硬编码敏感信息

### 端口冲突检查
- [ ] 3000（Next.js 默认）
- [ ] 8000（FastAPI 默认）
- [ ] 5432（PostgreSQL 默认）

## 输出格式

```markdown
# 发布前检查报告

**检查时间**: 2024-01-15
**项目**: blog-app

## 检查结果

### Docker 镜像 ✅
- [x] Dockerfile 存在
- [x] 镜像构建成功
- [x] 基础镜像版本已指定（node:18-alpine）
- [x] 镜像大小: 245MB ✅

### docker-compose ✅
- [x] 服务定义完整（3个服务）
- [x] 端口映射无冲突
- [x] 环境变量文件存在
- [x] 健康检查已配置

### 环境变量 ⚠️
- [x] `.env` 文件存在
- [ ] `DATABASE_URL` 未设置 ❌
- [x] 无硬编码敏感信息

## 结论

⚠️ 有 1 个问题需要修复后才能发布
```

## 边界

- 只检查配置和静态文件，不检查运行时状态
- 需要本地安装 Docker 才能构建镜像
- 端口冲突检查只检查常见端口

## 与其他 Skill 的关系

```
deploy-check ──▶ deploy-pipeline
  发布检查      发布流水线
```
