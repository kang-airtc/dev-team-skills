我在 feat/ch08-demo 分支上完成了评论模块的迭代，修改了 4 个文件：

- server/app/api/comments/views.py（API 层，新增评论接口的输入校验和错误处理）
- server/app/dao/comment_dao.py（DAO 层，新增 count_by_news 查询方法）
- frontend/src/app/page.tsx（首页集成评论计数显示）
- frontend/src/components/CommentCard.tsx（评论卡片组件重构）

请帮我完成合并前的完整测试链路：
1. 先分析这次变更需要回归哪些测试
2. 为新的业务逻辑生成单元测试骨架
3. 为新的接口生成接口测试骨架
4. 跑完 pytest 后分析覆盖率缺口
5. 生成最终测试报告贴到 PR 上
