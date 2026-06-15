---
name: dev-frontend
description: 根据页面描述（page-spec.md），生成符合项目约定的 Next.js App Router 页面骨架（.tsx），包含数据加载、骨架屏、空态与列表渲染三段式结构
---

# Dev Frontend - 前端页面骨架生成

读取 `page-spec.md` 描述，生成遵循项目规范的 Next.js App Router 页面骨架，避免手写时出现规范分叉。

## 触发场景

- 新建列表页或详情页，需要符合规范的骨架起点
- 接手项目，快速生成与现有页面风格一致的新页面
- 规范变更后，重新生成骨架对比旧页

## 目录结构

```
dev-frontend/
├── SKILL.md
└── scripts/
    └── generate.py    # page-spec.md → .tsx 页面骨架
```

## 依赖

仅使用 Python 标准库。

## 使用方法

```bash
python3 .opencode/skills/dev-frontend/scripts/generate.py \
  --input page-spec.md \
  --output dev-frontend/output/news_page.tsx
```

参数：
- `--input, -i`：页面描述文件（Markdown 格式）
- `--output, -o`：输出 .tsx 文件路径

## 输入格式

```markdown
# 页面描述：新闻列表页

## 路由
app/(public)/news/page.tsx

## 页面类型
列表页，客户端组件（含筛选交互）

## 数据来源
GET /api/news（调用 @/services/news 中的 listNews 函数）

## 展示内容
- 页面标题：公司新闻
- 新闻卡片列表（封面图、标题、发布时间、摘要）
- 空状态：暂无新闻

## UI 约束
- 使用 Tailwind CSS 布局
- 复用 @/components/Container 做页面容器
- 卡片点击跳转 /news/{slug}
- loading 状态：显示骨架屏占位
```

## 输出格式

符合以下约定的 `.tsx` 文件：

| 约定项 | 规则 |
|--------|------|
| 页面位置 | 公开页放 `app/(public)/`，后台页放 `app/(admin)/dashboard/` |
| 客户端组件 | 含 useState/useEffect/交互的页面加 `"use client"` |
| API 调用 | 通过 `@/services/[模块].ts` 封装，不直接写 fetch |
| 样式 | 使用 Tailwind CSS，不用行内 style |

骨架含三段式结构：数据加载（useEffect + service 调用）→ loading 骨架屏 → 列表渲染（空态 + 卡片）。

## 边界

- 生成客户端组件骨架（`"use client"`）；纯展示的 Server Component 需生成后手工改
- 不生成具体卡片样式细节，只留占位注释 `{/* TODO: 卡片内容 */}`
- 多字段录入表单由 dev-frontend-form 负责
