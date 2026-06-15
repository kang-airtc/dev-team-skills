---
name: req-prd
description: 基于澄清后的需求，自动生成 PRD（产品需求文档）标准结构
---

# PRD Draft - PRD 草稿生成

读取需求澄清文档，基于标准模板自动生成产品需求文档的骨架和内容填充。

## 触发场景

- 需求澄清完成后，需要正式文档化
- 快速启动新项目，需要 PRD 骨架
- 统一团队 PRD 格式，减少重复劳动

## 目录结构

```
req-prd/
├── SKILL.md
├── scripts/
│   └── generate-prd.py
└── assets/
    └── prd-template.md
```

## 依赖

仅使用 Python 标准库，无需额外依赖。

## 使用方法

```bash
# 基于需求澄清文档生成 PRD
python3 .opencode/skills/req-prd/scripts/generate-prd.py \
  --input "clarified-requirement.md" \
  --output "PRD-v1.md"

# 使用自定义模板
python3 .opencode/skills/req-prd/scripts/generate-prd.py \
  --input "clarified.md" \
  --template "my-template.md" \
  --output "PRD.md"
```

参数：
- `--input, -i`：必填，需求澄清文档路径
- `--output, -o`：可选，输出 PRD 路径，默认 `PRD.md`
- `--template, -t`：可选，自定义模板路径

## PRD 标准结构

生成的 PRD 包含以下章节：

| 章节 | 内容 | 来源 |
|------|------|------|
| 1. 背景与目标 | 为什么要做这个功能 | 需求澄清的 Why |
| 2. 需求范围 | 包含什么、不做什么 | 需求澄清的 What + 推断 |
| 3. 用户故事 | 标准格式用户故事 | 需求澄清的 Who + What |
| 4. 功能详述 | 具体逻辑和规则 | 需求澄清的 What + How |
| 5. 非功能需求 | 性能、安全、兼容 | 需求澄清的 How |
| 6. 验收标准 | 完成定义和测试标准 | 需求澄清的 How |
| 7. 风险与依赖 | 潜在风险和外部依赖 | 推断 + 待补充 |
| 8. 附录 | 参考文档、术语表 | 原始需求记录 |

## 输出格式

```markdown
# {产品名} 产品需求文档

**版本**: v1.0
**日期**: {today}
**状态**: 草稿

## 1. 背景与目标
...

## 2. 需求范围
### 2.1 包含范围
...
### 2.2 排除范围
...

## 3. 用户故事
...

## 4. 功能详述
...

## 5. 非功能需求
...

## 6. 验收标准
...

## 7. 风险与依赖
...

## 8. 附录
...
```

## 边界

- 本 Skill 生成的是**草稿**，需要产品经理人工审核和补充
- 自动填充的内容来自需求澄清文档，如果输入质量低，输出质量也低
- 复杂的业务逻辑和交互细节需要人工补充
- 用户故事采用标准格式：`作为 [角色]，我希望 [功能]，以便于 [价值]`

## 与其他 Skill 的关系

```
req-clarify ──▶ req-prd ──▶ req-decompose
  clarify.md ──▶ PRD.md ──▶ backlog.md
```
