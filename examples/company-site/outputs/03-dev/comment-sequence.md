# 评论提交时序

> 输入给 `dev-sequence`，渲染为 `comment-sequence.drawio`

## 参与者
- 访客（Visitor）
- 前端（Next.js）
- 后端（FastAPI）
- 数据库（PostgreSQL）
- 管理员（Admin）

## 时序

1. 访客 → 前端：在产品详情页底部填写评论表单
2. 前端 → 前端：本地校验（昵称非空、内容 ≤ 1000 字）
3. 前端 → 后端：POST /api/comments  {target_type, target_id, nickname, email, content}
4. 后端 → 后端：Pydantic 校验 + JWT 跳过（匿名允许）
5. 后端 → 数据库：INSERT comments (is_visible=false)
6. 数据库 → 后端：返回 row id
7. 后端 → 前端：ApiResponse.success({id, is_visible:false})
8. 前端 → 访客：提示"评论已提交，审核后显示"
9. 管理员 → 前端：登录后访问 /dashboard/comments
10. 前端 → 后端：GET /api/dashboard/comments?is_visible=false
11. 后端 → 数据库：SELECT comments WHERE is_visible=false ORDER BY id DESC
12. 数据库 → 后端：rows
13. 后端 → 前端：ApiResponse.success({items, total})
14. 管理员 → 前端：点击"显示"
15. 前端 → 后端：PATCH /api/dashboard/comments/{id}  {is_visible:true}
16. 后端 → 数据库：UPDATE comments SET is_visible=true WHERE id=?
17. 后端 → 前端：ApiResponse.success
18. 公开站访客后续刷新页面看到评论
