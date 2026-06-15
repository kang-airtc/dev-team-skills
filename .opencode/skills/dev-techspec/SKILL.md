---
name: dev-techspec
description: 按统一模板生成技术方案文档（Markdown），覆盖背景、目标、方案对比、详细设计、风险、里程碑等标准章节
---

# Dev TechSpec - 技术方案文档生成

按规范的技术方案模板，生成结构统一的 Markdown 文档，避免每次都从空白页起草。

## 触发场景

- 接到一个新功能/改造任务，要写技术方案给 Reviewer 看
- 跨团队协作时统一文档结构，方便他人快速找到关键信息
- 评审会前一晚才决定要写文档，需要快速产出骨架

## 目录结构

```
dev-techspec/
├── SKILL.md
├── scripts/
│   └── generate.py
└── references/
    └── tech-spec-template.md   # 文档模板
```

## 依赖

仅使用 Python 标准库。

## 使用方法

```bash
python3 .opencode/skills/dev-techspec/scripts/generate.py \
  --title "用户登录改造" \
  --author "张三" \
  --output ./docs/user-login-spec.md
```

参数：
- `--title, -t`：方案标题
- `--author, -a`：作者
- `--output, -o`：输出路径

## 文档结构

生成的 Markdown 包含以下固定章节，作者只需在每节下补内容：

1. 背景与目标
2. 现状分析
3. 方案对比（A 案 / B 案 / C 案，含取舍说明）
4. 详细设计（架构、数据流、接口、存储）
5. 兼容性与回滚
6. 风险与缓解
7. 里程碑与排期
8. 待决问题（Open Issues）

## 边界

- 只生成模板骨架，不自动填充内容
- 不集成到知识库，本地文件而已
- 模板可以改，路径在 `references/tech-spec-template.md`
