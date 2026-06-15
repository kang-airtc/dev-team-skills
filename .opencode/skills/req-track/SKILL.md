---
name: req-track
description: 版本化管理需求变更，记录变更历史，评估影响范围
---

# Change Track - 需求变更追踪

记录需求从 PRD 诞生到最终交付过程中的所有变更，支持版本对比和影响分析。

## 触发场景

- 需求评审后发生变更
- 开发过程中业务方调整需求
- 需要追溯需求演化历史
- Sprint 中间插入新需求

## 目录结构

```
req-track/
├── SKILL.md
├── scripts/
│   ├── track-change.py
│   └── compare-prd.py
└── assets/
    └── change-log-template.md
```

## 依赖

仅使用 Python 标准库，无需额外依赖。

## 使用方法

### 记录变更

```bash
# 交互式记录变更
python3 .opencode/skills/4.4-change-track/scripts/track-change.py

# 命令行方式记录
python3 .opencode/skills/4.4-change-track/scripts/track-change.py \
  --prd "PRD.md" \
  --desc "增加手机号登录方式" \
  --reason "用户反馈邮箱注册门槛高" \
  --impact "Epic-1" \
  --type feature \
  --output "CHANGELOG.md"
```

### 对比 PRD 版本

```bash
# 对比两个 PRD 版本，生成差异报告
python3 .opencode/skills/4.4-change-track/scripts/compare-prd.py \
  --old "PRD-v1.md" \
  --new "PRD-v2.md" \
  --output "diff-report.md"
```

参数（track-change）：
- `--prd, -p`：PRD 文件路径（用于关联）
- `--desc, -d`：变更描述
- `--reason, -r`：变更原因
- `--impact, -i`：影响范围（Epic/Story 编号）
- `--type, -t`：变更类型（`feature` / `bugfix` / `refactor` / `remove`）
- `--output, -o`：变更日志路径，默认 `CHANGELOG.md`

参数（compare-prd）：
- `--old`：旧版本 PRD 路径
- `--new`：新版本 PRD 路径
- `--output, -o`：差异报告输出路径

## 变更类型

| 类型 | 标记 | 说明 |
|------|------|------|
| 功能增强 | `feature` | 新增功能或能力 |
| 缺陷修复 | `bugfix` | 修复问题 |
| 重构优化 | `refactor` | 代码/结构重构，功能不变 |
| 功能移除 | `remove` | 删除已有功能 |

## 输出格式

### 变更日志（CHANGELOG.md）

```markdown
# 需求变更日志

## [RC-003] 2024-01-15 - 增加手机号登录
- **变更类型**: 功能增强
- **影响范围**: Epic 1（用户认证）
- **变更内容**: 增加手机号登录方式
- **变更原因**: 用户反馈邮箱注册门槛高
- **影响分析**:
  - Story 1.1 需要修改
  - 新增 Story 1.3
- **审批状态**: 已批准
- **预计工时影响**: +4h

---

## [RC-002] 2024-01-10 - 调整密码规则
...
```

### 差异报告

包含：
- 新增段落（绿色标记）
- 删除段落（红色标记）
- 修改段落（黄色标记，附带修改前后对比）
- 影响范围统计

## 边界

- 变更编号自动生成（RC-001, RC-002...）
- 影响范围需人工确认，脚本提供建议
- 差异对比基于文本行，不识别语义变更
- 变更日志默认追加，不会覆盖历史记录

## 与其他 Skill 的关系

```
req-prd ──▶ req-track ──▶ req-pipeline
  PRD.md ──▶ CHANGELOG.md ──▶ 项目看板
```
