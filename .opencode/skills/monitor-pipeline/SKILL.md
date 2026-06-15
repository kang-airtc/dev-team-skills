---
name: monitor-pipeline
description: 整合监控阶段所有 Skill，提供一键式系统巡检流水线——容器、日志、备份、健康报告
---

# Monitor Pipeline - 监控巡检助手

整合 monitor-containers、monitor-logs、monitor-backup、monitor-health，提供一键式系统巡检。

## 触发场景

- 定期系统巡检
- 发布前环境检查
- 生成运维报告
- 故障排查前快速摸底

## 目录结构

```
monitor-pipeline/
├── SKILL.md
└── scripts/
    └── run-all.sh
```

## 依赖

- Docker
- 同级 `monitor-*` Skill

## 使用方法

### 方式一：一键巡检

```bash
bash .opencode/skills/monitor-pipeline/scripts/run-all.sh \
  --output examples/chapter-10/output/pipeline-run \
  --db-container release-demo-db-1 \
  --db-name demo \
  --db-user demo \
  --name-filter release-demo

# 输出：
# pipeline-run/
# ├── 0-summary.md           # 一页纸总览（含健康分、状态表、关键提示、IM 推送片段）
# ├── 1-container-status.md  # 容器状态（Health、RestartCount、CPU/Mem）
# ├── 2-log-analysis.md      # 日志关键字统计
# ├── 3-backup-report.md     # 备份结果（备份文件在 backups/ 下）
# ├── 4-health-report.md     # 5 维加权健康报告
# └── backups/
#     └── demo_YYYYmmdd_HHMMSS.sql
```

参数：
- `--output, -o`：产物目录
- `--db-container`：PostgreSQL 容器名（缺省时跳过备份步骤）
- `--db-name` / `--db-user`：数据库名 / 用户
- `--name-filter`：容器名前缀过滤（多 docker 项目共存时建议使用）
- `--since`：日志时间窗，默认 `1h`

任一子步骤失败不会中断后续步骤；最终在 `0-summary.md` 中标注每步状态（✅ / ❌ / 跳过）。


## 流水线步骤

```
1. monitor-containers  容器状态检查
2. monitor-logs        日志巡检
3. monitor-backup      数据库备份（可选）
4. monitor-health      综合健康报告
```

## 完整工作流

```
定期巡检 / 故障排查前
    │
    ▼
┌─────────────────┐
│ monitor-containers│ ──> 容器状态报告
│ (容器检查)        │      发现异常容器
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ monitor-logs     │ ──> 日志分析报告
│ (日志巡检)       │      发现 ERROR/FATAL
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ monitor-backup   │ ──> 备份报告（可选）
│ (数据库备份)     │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ monitor-health   │ ──> 综合健康报告
│ (健康评估)       │      总体评分和建议
└─────────────────┘
```
