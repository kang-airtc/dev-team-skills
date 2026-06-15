---
name: dev-arch
description: 根据文字描述或项目结构，生成软件架构图（draw.io 格式 .drawio 文件），可在 draw.io Desktop 或 VS Code 插件中打开编辑
---

# Dev Arch - 架构图生成

读取项目目录或一段架构描述，生成 `.drawio` 格式的架构图，规避手画架构图反复调位置的麻烦。

## 触发场景

- 写技术方案文档需要附组件关系图
- 接手项目想快速画一张模块依赖图
- 评审会前需要把抽象架构变成可视化图

## 目录结构

```
dev-arch/
├── SKILL.md
├── scripts/
│   └── generate.py
└── references/
    └── arch-styles.md       # 三种预设样式说明
```

## 依赖

仅使用 Python 标准库——`.drawio` 是纯 XML 文本格式，不需要 draw.io 程序参与。

## 使用方法

```bash
python3 .opencode/skills/dev-arch/scripts/generate.py \
  --input arch-spec.md \
  --output arch.drawio \
  --style layered
```

参数：
- `--input, -i`：架构描述文件（Markdown 格式，包含组件清单和依赖关系）
- `--output, -o`：输出 `.drawio` 路径
- `--style, -s`：可选，预设样式 `layered` / `microservice` / `mvc`，默认 `layered`

## 输入格式

```markdown
# 系统架构

## 组件
- frontend: Next.js 前端
- backend: FastAPI 后端
- db: PostgreSQL 数据库

## 依赖
- frontend -> backend
- backend -> db
```

## 输出格式

draw.io XML 文件，用 draw.io Desktop 或 VS Code 的 Draw.io Integration 插件打开。组件用标准矩形，依赖用单向箭头，按选定样式自动配色和分层。

## 边界

- 只生成 `.drawio` 源文件，不导出 PNG（PNG 由 draw.io 自己导出）
- 不做精细布局优化，依赖 draw.io 自动布局
- 复杂架构（节点 > 20）建议人工拆分多张图后再分别生成
