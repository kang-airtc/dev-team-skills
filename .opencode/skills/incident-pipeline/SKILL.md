---
name: incident-pipeline
description: 整合故障排查阶段所有 Skill，提供一键式故障诊断流水线——容器诊断、日志分析、复盘报告
---

# Incident Pipeline - 故障排查助手

整合 incident-container、incident-log、incident-report，提供一键式故障诊断和复盘流程。

## 触发场景

- 故障发生后快速诊断
- 一站式故障排查
- 生成完整故障报告
- 团队协作排查

## 目录结构

```
incident-pipeline/
├── SKILL.md
└── scripts/
    └── run-all.sh
```

## 依赖

- Docker
- 同级 `incident-*` Skill

## 使用方法

### 方式一：一键故障诊断

```bash
# 诊断指定容器
./scripts/run-all.sh --container blog-backend

# 输出：
# incident-output/
# ├── 1-container-diagnosis.md   # 容器诊断
# ├── 2-log-analysis.md          # 日志分析
# └── 3-postmortem.md            # 复盘报告模板
```


## 流水线步骤

```
1. incident-container  容器诊断
2. incident-log        日志根因分析
3. incident-report     生成复盘报告
```

## 完整工作流

```
故障发生
    │
    ▼
┌─────────────────┐
│ incident-container│ ──> 容器诊断报告
│ (容器诊断)        │      状态、资源、日志
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ incident-log     │ ──> 日志分析报告
│ (日志分析)       │      时间线、根因推断
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ incident-report  │ ──> 复盘报告
│ (故障复盘)       │      时间线、改进措施
└─────────────────┘
    │
    ▼
团队复盘、执行改进
```

## 与其他 Skill 的关系

```
incident-container ──┬──▶ incident-pipeline
incident-log ────────┤     （故障排查编排）
incident-report ─────┘
```
