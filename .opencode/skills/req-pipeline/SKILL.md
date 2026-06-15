---
name: req-pipeline
description: 整合需求阶段的所有 Skill，提供一键式需求管理流水线
---

# Requirement Pipeline - 需求管理流水线

整合需求澄清、PRD 生成、需求拆解、变更追踪、故事地图、流程图六个 Skill，提供完整的需求管理流水线。

## 触发场景

- 从零开始管理一个新需求
- 需要完整的需求生命周期管理
- 团队协作时统一需求处理流程
- 快速启动项目，一站式生成所有需求文档

## 目录结构

```
req-pipeline/
├── SKILL.md
├── scripts/
│   ├── assistant.py          # 主控脚本
│   ├── init.sh               # 初始化项目结构
│   ├── run-all.sh            # 一键执行完整流程
│   └── run-step.sh           # 执行单个步骤
└── references/
    └── pipeline.conf         # 流水线配置
```

## 依赖

- Python 标准库
- 依赖 req-clarify、req-prd、req-decompose、req-track、req-storymap、req-flowchart 六个 Skill（同级目录）

## 使用方法

### 方式一：一键完整流程

```bash
# 初始化并运行完整流程
./scripts/run-all.sh "user-auth-system" "raw-requirement.txt"

# 参数说明：
# $1: 项目名称（用于创建目录）
# $2: 原始需求文件路径
```

执行后会创建项目目录：

```
user-auth-system/
├── 0-raw-requirement.txt     # 原始需求
├── 1-clarified.md            # 需求澄清
├── 2-PRD.md                  # PRD 草稿
├── 3-backlog.md              # 需求拆解
├── 4-CHANGELOG.md            # 变更追踪（初始化）
├── 5-story-map.md            # 故事地图
└── 6-flowchart.md            # 流程图
```

### 方式二：分步执行

```bash
# 执行指定步骤
./scripts/run-step.sh --step clarify --project "user-auth-system"

# 可选步骤：clarify | prd | decompose | init-track | story-map | flowchart
```

### 方式三：交互式助手

```bash
python3 scripts/assistant.py
```

交互式菜单：

```
=====================================
    需求管理助手
=====================================

1. 新建需求项目（完整流程）
2. 需求澄清
3. 生成 PRD
4. 需求拆解
5. 记录变更
6. 生成故事地图
7. 生成流程图
8. 查看项目状态
9. 退出

请选择: _
```

## 流水线配置

`references/pipeline.conf`：

```ini
[paths]
skills_dir = ../../
output_base = ./projects

[steps]
clarify = 4.1-clarify/scripts/clarify.py
prd = 4.2-prd-draft/scripts/generate-prd.py
decompose = 4.3-decompose/scripts/decompose.py
track = 4.4-change-track/scripts/track-change.py
storymap = 4.5-story-map/scripts/generate-story-map.py
flowchart = 4.6-flowchart/scripts/generate-flowchart.py

[options]
auto_confirm = false
verbose = true
```

## 项目状态检查

```bash
python3 scripts/assistant.py --status --project "user-auth-system"
```

输出：

```
项目: user-auth-system
=====================================

✅ 1-clarified.md          (已完成)
✅ 2-PRD.md                (已完成)
✅ 3-backlog.md            (已完成)
⏳ 4-CHANGELOG.md          (待变更)
✅ 5-story-map.md          (已完成)
✅ 6-flowchart.md          (已完成)

完成度: 83% (5/6)
```

## 边界

- 一键流程会覆盖已有文件，请确保目录为空或使用新版本号
- 各步骤的输入输出文件路径固定，不建议修改
- 变更追踪初始化为空日志，需要手动记录变更
- 流程图生成基于 PRD 的功能详述，复杂流程建议手动补充 DSL

```
原始需求
    │
    ▼
┌──────────────┐
│ req-clarify  │ ──> 1-clarified.md
└──────────────┘
    │
    ▼
┌──────────────┐
│ req-prd      │ ──> 2-PRD.md
└──────────────┘
    │
    ▼
┌──────────────┐
│ req-decompose│ ──> 3-backlog.md
└──────────────┘
    │
    ├──> req-storymap ──> 5-story-map.md
    │
    ├──> req-flowchart ──> 6-flowchart.md
    │
    └──> req-track ──> 4-CHANGELOG.md (持续更新)
```
