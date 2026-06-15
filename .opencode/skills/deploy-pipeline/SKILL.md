---
name: deploy-pipeline
description: 整合发布阶段所有 Skill，提供一键式应用发布流水线——检查、生成CHANGELOG、发布说明
---

# Deploy Pipeline - 应用发布助手

整合 deploy-check、deploy-changelog、deploy-release，提供一键式应用发布流程。

## 触发场景

- 版本发布前一键执行全套检查
- 标准化发布流程
- 团队协作时统一发布标准
- 快速生成发布文档

## 目录结构

```
deploy-pipeline/
├── SKILL.md
└── scripts/
    └── run-all.sh
```

## 依赖

- 同级 `deploy-*` Skill

## 使用方法

### 方式一：一键完整发布流程

```bash
./scripts/run-all.sh --version v1.2.0

# 输出：
# deploy-output/
# ├── 1-check-report.md       # 发布前检查
# ├── 2-CHANGELOG.md          # 变更日志
# └── 3-release-notes.md      # 发布说明
```


## 流水线步骤

```
1. deploy-check     发布前检查
2. deploy-changelog 生成变更日志
3. deploy-release   生成发布说明
```

## 边界

- 不自动执行发布操作（如 docker push、git tag）
- 只生成文档和检查报告
- 需要人工确认后执行实际发布

## 完整工作流

```
准备发布
    │
    ▼
┌──────────────┐
│ deploy-check  │ ──> 检查报告
│ (发布前检查)   │      确保配置正确
└──────────────┘
    │
    ▼
┌──────────────┐
│ deploy-       │ ──> CHANGELOG.md
│ changelog     │      自动分类变更
└──────────────┘
    │
    ▼
┌──────────────┐
│ deploy-release│ ──> release-notes.md
│ (发布说明)    │      含升级指南和回滚方案
└──────────────┘
    │
    ▼
人工确认后执行实际发布
```
