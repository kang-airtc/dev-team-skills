---
name: req-clarify
description: 通过结构化提问，将模糊的用户需求转化为清晰、可执行的需求描述
---

# Requirement Clarify - 需求澄清

使用五维澄清法（Who/What/Why/When/How），通过交互式提问帮助用户梳理和明确需求。

## 触发场景

- 收到业务部门的一句话需求，需要转化为可执行的需求描述
- 开发者在接到"帮我做个功能"这类模糊任务时
- 需求评审会上发现需求描述不清，需要现场澄清

## 目录结构

```
req-clarify/
├── SKILL.md
├── scripts/
│   └── clarify.py
└── assets/
    └── question-bank.md
```

## 依赖

仅使用 Python 标准库，无需额外依赖。

## 使用方法

```bash
# 交互式运行（推荐）
python3 .opencode/skills/req-clarify/scripts/clarify.py

# 从文件读取原始需求，输出到指定文件
python3 .opencode/skills/req-clarify/scripts/clarify.py \
  --input "raw-requirement.txt" \
  --output "clarified.md"

# 从命令行参数传入需求描述
python3 .opencode/skills/req-clarify/scripts/clarify.py \
  --requirement "我们需要一个用户注册功能"
```

参数：
- `--input, -i`：可选，原始需求文件路径
- `--output, -o`：可选，输出文件路径，默认 `clarified-requirement.md`
- `--requirement, -r`：可选，直接传入需求描述字符串

## 五维澄清法

| 维度 | 问题 | 输出 |
|------|------|------|
| **Who** | 用户是谁？为谁做？ | 用户画像 |
| **What** | 具体要做什么功能？ | 功能清单 |
| **Why** | 解决什么痛点？带来什么价值？ | 业务目标 |
| **When** | 在什么场景下使用？使用频率？ | 使用场景 |
| **How** | 怎么算完成了？验收标准是什么？ | 验收条件 |

## 输出格式

生成结构化的 `clarified-requirement.md`：

```markdown
# 已澄清的需求：{需求标题}

## 1. 基本信息
- **需求提出者**：{who}
- **目标用户**：{who}

## 2. 功能维度（What）
{功能清单}

## 3. 价值维度（Why）
{业务目标和痛点}

## 4. 场景维度（When）
{使用场景和频率}

## 5. 验收维度（How）
{验收标准和完成定义}

## 6. 原始需求记录
{保留原始描述，便于追溯}
```

## 边界

- 本 Skill 只做**需求澄清**，不生成 PRD、不拆解任务
- 如果用户回答"不知道"，会记录为"待确认"，不会阻止流程
- 问题库可自定义：修改 `assets/question-bank.md`
- 输出文件会被覆盖，建议及时重命名保存
