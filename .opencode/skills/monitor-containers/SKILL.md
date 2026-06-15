---
name: monitor-containers
description: 监控 Docker 容器状态，检测异常容器（Exited/Restarting/Unhealthy），输出巡检报告
---

# Monitor Containers - 容器状态监控

检查 Docker 容器运行状态，识别异常容器（Exited、Restarting、Unhealthy），统计资源使用情况。

## 触发场景

- 定期检查容器健康状态
- 发现异常退出的容器
- 监控容器资源使用
- 巡检时生成状态报告

## 目录结构

```
monitor-containers/
├── SKILL.md
├── scripts/
│   └── check.sh
└── assets/
    └── container-rules.conf
```

## 依赖

- `docker`
- 仅使用 Shell

## 使用方法

```bash
# 检查当前所有运行中容器
bash .opencode/skills/monitor-containers/scripts/check.sh

# 仅检查 release-demo 栈，输出到指定文件
bash .opencode/skills/monitor-containers/scripts/check.sh \
  --filter release-demo \
  --output container-status.md

# 包含已退出容器（默认仅展示运行中）
bash .opencode/skills/monitor-containers/scripts/check.sh --all
```

参数：
- `--output, -o`：输出报告路径
- `--filter, -f`：按容器名前缀过滤（多 docker 项目共存时建议使用）
- `--all, -a`：包含已退出容器（默认仅展示运行中）

报告字段：容器名、镜像、状态、Health（来自 `docker inspect`）、RestartCount、CPU%、Mem%（来自 `docker stats --no-stream`）。

## 检查项

| 状态 | 说明 | 处理建议 |
|------|------|---------|
| **Exited** | 容器已退出 | 检查日志，重启容器 |
| **Restarting** | 反复重启 | 检查健康检查配置 |
| **Unhealthy** | 健康检查失败 | 检查应用状态和依赖 |
| **Dead** | 僵尸容器 | 强制删除并重建 |

## 输出格式

```markdown
# 容器状态巡检报告

**巡检时间**: 2024-01-15 14:30

## 运行状态

| 容器名 | 服务 | 状态 | 运行时间 | 重启次数 | CPU | 内存 |
|--------|------|------|---------|---------|-----|------|
| blog-frontend | Next.js | ✅ running | 3d | 0 | 2% | 128MB |
| blog-backend | FastAPI | ✅ running | 3d | 0 | 5% | 256MB |
| blog-db | PostgreSQL | ✅ running | 3d | 0 | 1% | 512MB |

## 异常容器

⚠️ 未发现异常容器

## 资源统计

- **总容器数**: 3
- **运行中**: 3
- **已退出**: 0
- **CPU 总占用**: 8%
- **内存 总占用**: 896MB
```

## 边界

- 需要 Docker 环境
- 只检查本地容器
- 不自动修复异常

## 与其他 Skill 的关系

```
monitor-containers ──▶ monitor-pipeline
  容器监控            巡检流水线
```
