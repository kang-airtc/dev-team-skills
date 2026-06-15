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
