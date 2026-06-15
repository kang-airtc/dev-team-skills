---
name: monitor-health
description: 综合容器状态、日志、资源使用情况，生成系统健康报告
---

# Monitor Health - 系统健康报告

整合容器状态、日志错误、资源使用、数据库备份状态，生成综合的系统健康报告。

## 触发场景

- 定期系统健康巡检
- 生成运维周报
- 评估系统整体状态
- 发现潜在风险

## 目录结构

```
monitor-health/
├── SKILL.md
├── scripts/
│   └── report.py
└── assets/
    └── health-template.md
```

## 依赖

- Python 标准库
- Docker

## 使用方法

```bash
# 生成系统健康报告（仅 release-demo 栈，含备份维度）
python3 .opencode/skills/monitor-health/scripts/report.py \
  --name-filter release-demo \
  --backup-dir examples/chapter-10/output/backups \
  --output health-report.md

# 不传 --backup-dir 时，备份维度计 0 分
python3 .opencode/skills/monitor-health/scripts/report.py \
  --since 24h \
  --output health-report.md
```

参数：
- `--output, -o`：输出路径
- `--since`：日志时间窗，默认 `1h`
- `--name-filter`：按容器名前缀过滤（不传则覆盖所有运行中容器）
- `--backup-dir`：备份目录路径；用于检测最近一次备份；不传则备份维度计 0
- `--backup-min-size`：备份最小可信字节数，默认 `256`
- `--backup-max-age`：备份最大允许小时数，默认 `24`

评分（满分 100）：容器健康 30 + 重启次数 20 + 日志 ERROR 25 + 备份成功 15 + 资源压力 10。

## 输出格式

```markdown
# 系统健康报告

**报告时间**: 2024-01-15
**检查范围**: 最近 24 小时

## 总体评分: 85/100 🟡

| 维度 | 评分 | 状态 |
|------|------|------|
| 容器状态 | 95 | 🟢 优秀 |
| 日志健康 | 75 | 🟡 良好 |
| 资源使用 | 80 | 🟡 良好 |
| 备份状态 | 100 | 🟢 优秀 |

## 容器状态

✅ 所有容器运行正常（3/3）

## 日志健康

⚠️ blog-backend 有 5 个 ERROR
- 建议检查数据库连接池配置

## 资源使用

| 容器 | CPU | 内存 | 磁盘 |
|------|-----|------|------|
| blog-frontend | 2% | 128MB | - |
| blog-backend | 15% | 512MB | - |
| blog-db | 5% | 1GB | 85% |

⚠️ blog-db 磁盘使用率 85%，建议清理日志或扩容

## 备份状态

✅ 最近备份: 2024-01-15 02:00
✅ 备份大小: 15.2MB

## 建议

1. 关注 blog-backend 的数据库连接错误
2. 考虑 blog-db 磁盘扩容
3. 继续保持定期备份
```

## 边界

- 基于 Docker 状态，不监控宿主机
- 评分为简化算法，仅供参考
- 需要定期运行才能对比趋势

## 与其他 Skill 的关系

```
monitor-containers ──┐
monitor-logs ────────┼──▶ monitor-health
monitor-backup ──────┘
```
