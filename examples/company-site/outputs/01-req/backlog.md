# company-site Backlog v0.2.0

> 来源 Skill：`req-decompose`  
> 输入：`prd.md`  
> 拆解层级：Epic → Story → Task

## Epic 1：产品管理体系
- Story 1.1 产品 CRUD（5 个 Task：模型、DAO、API、表单页、列表页）
- Story 1.2 多图上传（3 个 Task：单图组件、图集组件、后端校验）
- Story 1.3 上架/下架（2 个 Task：状态字段、状态切换 API）

## Epic 2：新闻发布体系
- Story 2.1 新闻 CRUD（5 个 Task：模型、DAO、API、表单页、列表页）
- Story 2.2 定时发布（2 个 Task：published_at 字段、查询过滤）
- Story 2.3 公开站详情页（2 个 Task：SEO meta、面包屑）

## Epic 3：评论与审核
- Story 3.1 多态评论模型（3 个 Task：target_type 字段、复合索引、约束）
- Story 3.2 公开站发评（2 个 Task：表单组件、防刷限流）
- Story 3.3 后台审核（3 个 Task：列表筛选、批量隐藏、单条删除）

## Epic 4：鉴权与用户
- Story 4.1 JWT 登录（3 个 Task：access/refresh、刷新接口、登出黑名单）
- Story 4.2 角色权限（2 个 Task：admin/editor 区分、装饰器封装）

## Epic 5：工程化产物
- Story 5.1 需求阶段产物（6 个 Task：clarify / prd / backlog / storymap / flow / changes）
- Story 5.2 设计阶段产物（4 个 Task：sprint / ui-check / decision / review）
- Story 5.3 开发阶段产物（10 个 Task：架构图、时序图、技术方案、接口文档、lint 报告等）
- Story 5.4 评审 / 测试 / 发布 / 监控 / 排障产物（每阶段 3-5 个 Task）

## 优先级与排期

| Epic | 优先级 | 里程碑 |
|---|---|---|
| Epic 4 鉴权 | P0 | M1 |
| Epic 1 产品 | P0 | M2 |
| Epic 2 新闻 | P1 | M3 |
| Epic 3 评论 | P1 | M3 |
| Epic 5 工程化 | P0 | M1-M4（贯穿） |

## 验收口径

- 所有 Story 完成的标准：对应单元/接口测试通过、`review-backend`/`review-frontend` 报告无 P1
- 所有 Epic 完成的标准：公开站可演示对应用例 + 后台可对应 CRUD + `outputs/` 下产物齐全
