---
name: monitor-logs
description: 分析 Docker 容器日志，检测 ERROR/FATAL 关键字，统计日志量，输出日志巡检报告
---

# Monitor Logs - 日志巡检

分析 Docker 容器日志，检测 ERROR、FATAL、Exception 等关键字，统计日志量，识别异常模式。

## 触发场景

- 定期检查应用错误日志
- 发现异常错误模式
- 统计日志增长趋势
- 排查线上问题

## 目录结构

```
monitor-logs/
├── SKILL.md
├── scripts/
│   └── analyze.sh
└── assets/
    └── log-patterns.conf
```

## 依赖

- `docker`
- `grep` / `awk`

## 使用方法

```bash
# 分析所有容器日志
bash .opencode/skills/monitor-logs/scripts/analyze.sh

# 指定容器
bash .opencode/skills/monitor-logs/scripts/analyze.sh --container blog-backend

# 指定时间范围
bash .opencode/skills/monitor-logs/scripts/analyze.sh --since 10m
```

参数：
- `--container, -c`：指定容器名
- `--since`：时间范围（如 10m, 1h, 24h）
- `--output, -o`：输出报告路径

## 检查项

| 关键字 | 级别 | 说明 |
|--------|------|------|
| ERROR | 高 | 错误日志 |
| FATAL | 高 | 致命错误 |
| Exception | 高 | 异常堆栈 |
| WARN | 中 | 警告日志 |
| timeout | 中 | 超时错误 |

## 输出格式

```markdown
# 日志巡检报告

**巡检时间**: 2024-01-15 14:30
**时间范围**: 最近 1 小时

## 日志统计

| 容器 | 总日志量 | ERROR | WARN | 其他 |
|------|---------|-------|------|------|
| blog-frontend | 1,245 | 0 | 2 | 1,243 |
| blog-backend | 3,680 | 5 | 12 | 3,663 |
| blog-db | 890 | 0 | 0 | 890 |

## 错误详情

### blog-backend

| 时间 | 级别 | 内容 |
|------|------|------|
| 14:23 | ERROR | 数据库连接超时 |
| 14:15 | ERROR | 用户认证失败 |

## 建议

- blog-backend 有 5 个 ERROR，建议检查数据库连接池配置
```

## 边界

- 依赖 Docker 日志驱动
- 大量日志时分析可能较慢
- 不自动修复问题

## 与其他 Skill 的关系

```
monitor-logs ──▶ incident-log
  日志巡检       日志根因分析
```
