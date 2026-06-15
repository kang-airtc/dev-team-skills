---
name: docker-basics
description: Docker 与 docker compose 日常操作命令速查（启停、日志、进容器、镜像清理、状态诊断）
---

# Docker Basics - 命令速查

整理 Docker 与 docker compose 日常操作里最高频的命令，配每条命令一句使用场景。Agent 在被问到「怎么看日志」「怎么进容器」「怎么清理镜像」时按关键词从 cheatsheet 摘取相关条目，而不必每次现查文档。

## 触发场景

- 临时排查容器状态（启停、日志、进入容器）
- 镜像与磁盘清理
- 想快速定位某条 docker 命令的写法

## 目录结构

```
docker-basics/
├── SKILL.md
└── cheatsheet.md
```

## 依赖

- 本机已安装 Docker 20.10+（含 `docker compose` 子命令）

## 使用方法

本 Skill 不含可执行脚本。Agent 直接读取 `cheatsheet.md`，按用户问题里的关键词（如 “日志”、“进容器”、“清理”）匹配分组，返回相关条目并附一句场景说明。

```bash
cat .opencode/skills/docker-basics/cheatsheet.md
```

## 速查表分组

| 分组 | 关键词 | 典型命令 |
|------|--------|----------|
| 生命周期 | 启动/停止/重启/销毁 | `docker compose up -d` / `stop` / `restart` / `down` |
| 日志查看 | 日志/排错/启动失败 | `docker compose logs -f --tail=100 backend` |
| 进入容器 | 进容器/调试/exec | `docker compose exec backend bash` |
| 镜像管理 | 镜像/拉取/列出 | `docker images` / `docker rmi` / `docker pull` |
| 资源清理 | 清理/磁盘/瘦身 | `docker system prune -f` / `docker volume prune` |
| 状态诊断 | 状态/资源/占用 | `docker compose ps` / `docker stats` |

## 边界

- 只覆盖单机 Docker 与 docker-compose 场景；Kubernetes、swarm 不在范围内
- 仅提供命令与一句场景说明，不替代 Docker 官方文档对参数的完整解释
- 关键词命中是粗粒度匹配；遇到歧义请直接打开 `cheatsheet.md` 浏览相关分组

## 与其他 Skill 的关系

```
docker-basics ──▶ docker-compose-setup ──▶ deploy-check
   命令速查        生成 compose 配置        发布前检查
```
