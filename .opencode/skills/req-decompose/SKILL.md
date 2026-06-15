---
name: req-decompose
description: 将 PRD 中的大需求拆解为可执行的用户故事和任务
---

# Requirement Decompose - 需求拆解

将 PRD 中的功能模块按 Epic → Story → Task 三层结构拆解，生成可执行的 Backlog。

## 触发场景

- PRD 完成后，需要进入开发排期
- 需要估算工时和分配任务
- Sprint 规划会议前，需要准备用户故事

## 目录结构

```
req-decompose/
├── SKILL.md
├── scripts/
│   └── decompose.py
└── assets/
    └── story-template.md
```

## 依赖

仅使用 Python 标准库，无需额外依赖。

## 使用方法

```bash
# 基于 PRD 生成 Backlog
python3 .opencode/skills/4.3-decompose/scripts/decompose.py \
  --input "PRD.md" \
  --output "backlog.md"

# 指定估算方式
python3 .opencode/skills/4.3-decompose/scripts/decompose.py \
  --input "PRD.md" \
  --estimate story-points \
  --output "backlog.md"
```

参数：
- `--input, -i`：必填，PRD 文档路径
- `--output, -o`：可选，输出路径，默认 `backlog.md`
- `--estimate, -e`：可选，估算方式（`story-points` / `hours`），默认 `story-points`

## 拆解结构

输出采用三层结构：

```
Epic（史诗）         ← 大模块，如"用户认证"
  └── Story（故事）   ← 可交付的功能单元，如"用户注册"
        └── Task（任务） ← 具体执行步骤，如"前端注册页面"
```

## 输出格式

```markdown
# 需求拆解 - Backlog

## Epic 1: {模块名}
- **优先级**: P0
- **估算**: 8 story points

### Story 1.1: {故事标题}
**作为** {角色}，
**我希望** {功能}，
**以便于** {价值}。

**验收标准**：
- [ ] 标准1
- [ ] 标准2

#### Task 1.1.1: {任务名称}
- **类型**: 前端/后端/测试/设计
- **估算**: 4h
- **负责人**: （待分配）
- **描述**: （任务详情）
```

## 边界

- 自动识别 PRD 中的功能模块作为 Epic
- 每个功能点生成标准格式的用户故事
- Task 需要人工补充具体执行细节
- 估算值为预估值，实际开发需团队评估
- 当前版本只支持一级 Epic 拆分

## 与其他 Skill 的关系

```
req-prd ──▶ req-decompose ──▶ req-storymap
  PRD.md ──▶ backlog.md ──▶ story-map.md
```
