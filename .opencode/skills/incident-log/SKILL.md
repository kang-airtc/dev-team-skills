---
name: incident-log
description: 分析容器日志中的错误模式，按时间线聚合异常，识别根因
---

# Incident Log - 日志根因分析

聚合多个容器的日志，按时间线分析错误模式，识别故障根因和传播路径。

## 触发场景

- 故障发生后分析日志
- 定位错误根因
- 分析故障传播路径
- 发现日志中的异常模式

## 目录结构

```
incident-log/
├── SKILL.md
├── scripts/
│   └── analyze.py
└── assets/
    └── log-patterns.md
```

## 依赖

- Python 标准库
- Docker

## 使用方法

```bash
# 分析最近 1 小时的日志
python3 .opencode/skills/incident-log/scripts/analyze.py --since 1h

# 分析指定容器
python3 .opencode/skills/incident-log/scripts/analyze.py \
  --container blog-backend \
  --since 30m
```

参数：
- `--since`：时间范围（如 10m, 1h, 24h）
- `--container, -c`：指定容器
- `--output, -o`：输出路径

## 分析维度

| 维度 | 说明 |
|------|------|
| **时间线** | 按时间顺序展示错误 |
| **错误聚类** | 相同错误合并统计 |
| **传播路径** | 错误如何在服务间传播 |
| **根因推断** | 基于时间线推断最先出错的服务 |

## 输出格式

```markdown
# 日志根因分析报告

**分析时间**: 2024-01-15 16:00
**时间范围**: 最近 1 小时

## 错误时间线

| 时间 | 容器 | 级别 | 错误 |
|------|------|------|------|
| 15:23 | blog-db | ERROR | 连接数超限 |
| 15:24 | blog-backend | ERROR | 数据库连接失败 |
| 15:25 | blog-frontend | ERROR | API 请求超时 |

## 根因推断

🔴 **根因**: blog-db 连接数超限

**传播路径**:
blog-db (连接超限) → blog-backend (连接失败) → blog-frontend (请求超时)

## 建议

1. 增加 blog-db 最大连接数
2. 检查 blog-backend 连接池配置
3. 添加连接超时重试机制
```

## 边界

- 基于关键字匹配，**不理解业务语义**
- 只能分析已有的日志
- 复杂分布式故障需要人工判断

## 与其他 Skill 的关系

```
incident-log ──▶ incident-pipeline
  日志分析        故障排查流水线
```
