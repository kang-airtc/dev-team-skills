---
name: dev-frontend-form
description: 根据表单描述（form-spec.md），生成 Next.js App Router 后台 CRUD 表单骨架，包含四种状态（正常/提交中/成功/失败）的完整处理
---

# Dev Frontend Form - 后台表单骨架生成

读取 `form-spec.md` 描述，生成可复用的表单组件和 new/edit 页面，确保每个表单都包含完整的四态处理。

## 触发场景

- 新建后台 CRUD 表单（新增 + 编辑页）
- 规范约束：所有表单必须处理正常/提交中/成功跳转/失败提示四种状态

## 目录结构

```
dev-frontend-form/
├── SKILL.md
└── scripts/
    └── generate.py    # form-spec.md → 表单组件 + new/edit 页面
```

## 依赖

仅使用 Python 标准库。

## 使用方法

```bash
python3 .opencode/skills/dev-frontend-form/scripts/generate.py \
  --input form-spec.md \
  --output-dir dev-frontend-form/output
```

参数：
- `--input, -i`：表单描述文件（Markdown 格式）
- `--output-dir, -o`：输出目录（按目录树生成三个文件）

## 输入格式

```markdown
# 表单描述：新闻管理后台表单

## 适用场景
新增 + 编辑新闻（复用同一个表单组件）

## 路由
- 新增：app/(admin)/dashboard/news/new/page.tsx
- 编辑：app/(admin)/dashboard/news/[id]/edit/page.tsx

## 字段

| 字段名 | 类型 | 必填 | 校验 |
|--------|------|------|------|
| title | text | 是 | 不能为空 |
| slug | text | 是 | 不能为空，只允许小写字母、数字、连字符 |
| content | textarea | 是 | 不能为空 |
| is_published | checkbox | 否 | 默认 false |

## 提交逻辑
- 新增：调用 createNews service，成功后跳转 /dashboard/news
- 编辑：调用 updateNews service，成功后跳转 /dashboard/news
- 失败：页面顶部展示错误提示（红色 alert）
- 提交中：按钮 disabled + 显示"保存中..."
```

## 输出格式

三个文件：
| 文件 | 说明 |
|------|------|
| `components/[Module]Form.tsx` | 可复用表单组件，新增和编辑均可用 |
| `app/(admin)/dashboard/[module]/new/page.tsx` | 新增页面 |
| `app/(admin)/dashboard/[module]/[id]/edit/page.tsx` | 编辑页面 |

表单统一约定：四态完整（正常/提交中/成功跳转/失败顶栏错误）。

## 边界

- 图片字段默认生成 URL 文本框，真实文件上传需手工替换
- 分步表单、联动字段需生成后手工扩展
- 不引入 react-hook-form 等表单库，使用原生 useState
