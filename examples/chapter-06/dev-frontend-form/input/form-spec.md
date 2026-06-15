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
| summary | textarea | 否 | |
| cover_image | text（URL） | 否 | |
| content | textarea | 是 | 不能为空 |
| is_published | checkbox | 否 | 默认 false |

## 提交逻辑
- 新增：调用 createNews service，成功后跳转 /dashboard/news
- 编辑：调用 updateNews service，成功后跳转 /dashboard/news
- 失败：页面顶部展示错误提示（红色 alert）
- 提交中：按钮 disabled + 显示"保存中..."
