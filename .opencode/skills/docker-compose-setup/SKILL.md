---
name: docker-compose-setup
description: 根据 project-spec.yaml 渲染前端、后端 Dockerfile、docker-compose.yml 与启停脚本，搭出三服务（frontend / backend / db）的最小可运行容器化骨架
---

# Docker Compose Setup - 容器化骨架生成

读取项目根目录下 `project-spec.yaml`，套模板渲染出前端 Dockerfile、后端 Dockerfile、`docker-compose.yml` 与 `scripts/up.sh`。把多阶段构建、健康检查、依赖顺序、非 root 用户切换等常见最佳实践固化在模板里，避免每个项目从零搭一遍踩同样的坑。

## 触发场景

- 新建项目，需要把代码包装为可 `docker compose up` 的形态
- 现有项目重构容器化配置，统一团队约定
- 想用一份 spec 一键生成可对照的容器化基线，再手工补充业务细节

## 目录结构

```
docker-compose-setup/
├── SKILL.md
├── scripts/
│   └── generate.py
└── templates/
    ├── Dockerfile.frontend.nextjs
    ├── Dockerfile.frontend.nginx-static
    ├── Dockerfile.backend.fastapi
    ├── docker-compose.yml
    └── up.sh
```

## 依赖

- Python 3.8+（标准库即可，无需第三方）
- 渲染产物运行时需本机已安装 Docker

## 使用方法

```bash
# 在含 project-spec.yaml 的目录下
python3 .opencode/skills/docker-compose-setup/scripts/generate.py \
  --spec project-spec.yaml \
  --output ./
```

参数：

- `--spec, -s`：project-spec.yaml 路径（默认 `project-spec.yaml`）
- `--output, -o`：渲染目标目录（默认当前目录）
- `--force, -f`：覆盖已存在的同名文件（默认 false，避免误盖手写改动）

## project-spec.yaml 字段

```yaml
project: release-demo
frontend:
  framework: nginx-static   # 可选：nextjs / nginx-static
  node_version: "18"        # 仅 nextjs 模板使用
  port: 3000
  container_port: 80        # nginx-static 默认 80；nextjs 默认 3000
backend:
  framework: fastapi
  python_version: "3.11"
  port: 8000
  module: main:app          # uvicorn 入口（容器内执行的字符串）
db:
  type: postgres
  version: "15-alpine"
  database: demo
  user: demo
  host_port: 5433           # 宿主机端口，避免和本机已有 PG 冲突
```

> 当前模板覆盖 nginx-static + FastAPI + PostgreSQL（与第 9 章 `release-demo` 一致），以及 Next.js + FastAPI + PostgreSQL 两种典型组合。其他框架可在 `templates/` 下追加同名前缀文件。

## 渲染产出

```
output/
├── Dockerfile                # 占位，供 deploy-check 试构建
├── docker-compose.yml
├── frontend/Dockerfile
├── backend/Dockerfile
├── scripts/up.sh
└── scripts/down.sh
```

模板用 `${var}` 风格的简单字符串替换，不引入 Jinja2，避免 Dockerfile / yaml 里的特殊字符产生歧义。

## 内置最佳实践

- 多阶段构建（Next.js 模板）：builder 阶段 `npm ci` 后 build，runner 阶段只复制 `.next/standalone` 与静态资源，体积可压到 200 MB 量级
- 非 root 用户：runner 阶段创建独立用户后 `USER` 切换，避免容器以 root 跑
- 健康检查：db 服务用 `pg_isready` 探活；backend 用 `condition: service_healthy` 等 db 真正就绪再启动，规避典型启动 race
- 数据卷：db 默认挂 `pg_data` 卷，`docker compose down` 不会丢数据；frontend / backend 不挂卷（无状态）
- 依赖锁定：Python 用 `pip install --no-cache-dir` 不留缓存；Node 用 `npm ci` 严格按 lock 文件安装

## 边界

- 仅覆盖单机 docker-compose 场景，不生成 Kubernetes / swarm 清单
- 模板只给 frontend / backend / db 三服务骨架；多 worker、Redis、消息队列需在生成后手工追加
- 数据库口令默认走 `${DB_PASSWORD:-demo_dev}` 走环境变量；生产部署须改为强口令并由 secrets 注入
- 仅支持 nginx-static 与 nextjs 两种前端模板；其他前端框架需扩展 `templates/`

## 与其他 Skill 的关系

```
docker-basics ──▶ docker-compose-setup ──▶ deploy-check ──▶ deploy-pipeline
   命令速查        生成容器化骨架            发布前检查        发布流水线
```
