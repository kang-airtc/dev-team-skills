# 时序描述：新闻列表加载流程

## 角色

- user: 用户
- browser: 浏览器
- next: Next.js 前端
- api: FastAPI 后端
- db: PostgreSQL

## 消息流

- user -> browser: 访问 /news
- browser -> next: 请求页面
- next -> api: GET /api/news?limit=10&offset=0
- api -> db: SELECT * FROM news WHERE is_published=true ORDER BY published_at DESC LIMIT 10
- db -> api: 返回新闻列表
- api -> next: {code:0, data:{items:[...], total:N}}
- next -> browser: 渲染新闻卡片列表
- browser -> user: 展示新闻页面
