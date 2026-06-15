---
name: incident-container
description: 诊断 Docker 容器异常（资源、网络、挂载），输出诊断报告和修复建议
---

# Incident Container - 容器故障诊断

当容器异常退出或行为异常时，通过 docker inspect 分析容器配置、资源限制、网络、挂载卷等，输出诊断报告和修复建议。

## 触发场景

- 容器反复重启
- 容器无法启动
- 容器性能异常
- 排查容器故障根因

## 目录结构

```
incident-container/
├── SKILL.md
├── scripts/
│   └── diagnose.sh
└── assets/
    └── container-troubleshooting.md
```

## 依赖

- `docker`

## 使用方法

```bash
# 诊断指定容器
bash .opencode/skills/incident-container/scripts/diagnose.sh --container blog-backend

# 诊断最近退出的容器
bash .opencode/skills/incident-container/scripts/diagnose.sh --last
```

参数：
- `--container, -c`：容器名
- `--last`：诊断最近退出的容器
- `--output, -o`：输出报告路径

## 诊断项

| 检查项 | 说明 |
|--------|------|
| **容器状态** | Exit Code、错误信息 |
| **资源限制** | CPU、内存限制是否过低 |
| **环境变量** | 必要变量是否缺失 |
| **网络配置** | 端口映射、网络模式 |
| **挂载卷** | 卷是否存在、权限是否正确 |
| **日志** | 最后 50 行日志 |

## 输出格式

```markdown
# 容器故障诊断报告

**容器**: blog-backend
**诊断时间**: 2024-01-15 15:30

## 容器状态

- **状态**: Exited (1)
- **退出码**: 1
- **退出时间**: 2024-01-15 15:25

## 错误日志

```
Error: DATABASE_URL is not set
    at connectToDatabase (/app/db.js:15)
```

## 根因分析

❌ 环境变量 `DATABASE_URL` 未设置

## 修复建议

1. 检查 `.env` 文件是否包含 `DATABASE_URL`
2. 确认 docker-compose.yml 中 env_file 配置正确
3. 重新启动容器：`docker-compose up -d`

## 预防措施

- 在 docker-compose 中添加健康检查
- 设置容器自动重启策略
```

## 边界

- 只能诊断已停止的容器
- 需要容器日志存在
- 不自动修复问题

## 与其他 Skill 的关系

```
incident-container ──▶ incident-pipeline
  容器诊断            故障排查流水线
```
