# 回归范围分析

> 来源 Skill：`test-regression`  
> 输入：`git diff v0.1.0..HEAD`

## 变更模块

| 模块 | 变更类型 | 风险等级 |
|---|---|---|
| `server/web/api/uploads/` | 新增 | 中 |
| `server/web/api/comments/` | 新增 | 中 |
| `server/dao/product_dao.py` | 修改（新增分页） | 高 |
| `server/dao/news_dao.py` | 修改（新增分页） | 高 |
| `server/auth.py` | 修改（refresh rotate） | 高 |
| `frontend/components/admin/*` | 新增 4 个组件 | 中 |
| `frontend/lib/api.ts` | 修改（unwrapApi） | 全站 |

## 必跑用例

- `tests/test_api_uploads.py` 全部 6 条
- `tests/test_api_comments.py` 全部 8 条
- `tests/test_product_dao.py::test_list_with_pagination` 等 3 条
- `tests/test_auth.py::test_refresh_rotate_invalidates_old_token`

## 推荐手测

- 后台新建产品 → 上传 3 图 → 提交 → 公开站可见
- 公开站发评论 → 后台审核 → 公开站可见
- 长时间不操作（>30 分钟）→ 自动 refresh → 不应跳登录页

## 影响范围说明

- 列表分页字段调整：前端 admin 已全部跟进；公开站本期未消费列表分页，无回归点
- refresh rotate：前端只保存最新 refresh token，与 v0.1 行为兼容
