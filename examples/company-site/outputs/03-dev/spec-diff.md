# OpenAPI 规范偏差对比

> 来源 Skill：`dev-spec-diff`  
> 输入：`openapi-v0.1.0.json` vs `openapi-v0.2.0.json`

## 总览

- 新增接口：5 条
- 删除接口：0 条
- 修改接口：3 条
- 破坏性变更：0 条

## 新增

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | /api/uploads | 单图上传 |
| POST | /api/comments | 提交评论 |
| GET | /api/dashboard/comments | 后台评论列表（含未审核） |
| PATCH | /api/dashboard/comments/{id} | 显示/隐藏评论 |
| DELETE | /api/dashboard/comments/{id} | 软删除评论 |

## 修改

| 方法 | 路径 | 变更 |
|---|---|---|
| GET | /api/products | 响应增加 `items / total / page / page_size` 分页字段（原为数组，向后兼容路径：在 v0.2 客户端先升级） |
| GET | /api/news | 同上 |
| POST | /api/auth/refresh | 启用 rotate，旧 refresh token 一次性失效 |

## 评估

- 列表分页结构调整为 `{items, total, page, page_size}`，仅前端 admin 调用，已同步升级；公开站本期未消费
- refresh rotate 对调用方透明，前端只需要继续保存最新 refresh token
- 无字段删除、无类型变更、无路径迁移 → 不计入破坏性变更
