# 多角色设计评审纪要

> 来源 Skill：`design-review --roles ui-designer,frontend-dev,backend-dev,product-manager`  
> 评审对象：8 个接口草案（auth / uploads / products / news / comments / categories / users / dashboard-stats）  
> 评审日期：2026-04-19

## 总评

14 条讨论意见，按优先级：🔴 必须处理 5 条 / 🟡 建议处理 6 条 / 🟢 可选 3 条。全部在代码动工前落进设计文档。

## /api/auth —— 登录与刷新

### 讨论范畴

- 🔴 access token 过期时间团队建议 30 分钟（草案给的 7 天太长）
- 🟡 refresh 接口是否支持 rotate？

### 本次评审共识

- access 30 分钟 / refresh 7 天
- refresh 接口启用 rotate，旧 refresh token 立即失效——backend-dev 负责实现

## /api/uploads —— 文件上传

### 讨论范畴（设计阶段约定，供开发参考）
- 🔴 响应格式约定：团队建议统一用 `{code, msg, data}` 包装，当前草案未体现
- 🔴 错误码约定：业务错误走 `200 + code≠0`，HTTP 4xx/5xx 仅留给网关层
- 🟡 文件大小上限：建议在接口草案里写明，避免前后端各自假设

### 本次评审共识
- 统一走 `ApiResponse[dict]` 包装——前后端已对齐
- 业务错误用 `200 + code: 1xxx`——产品经理确认
- `maxBytes: 5242880`（5 MB）写进 OpenAPI 描述

## /api/products —— 产品 CRUD

### 讨论范畴

- 🔴 列表分页：草案返回数组，团队约定必须 `{items, total, page, page_size}`
- 🟡 推荐位字段 `is_featured`：是否需要独立接口？

### 本次评审共识

- 列表统一分页结构
- 推荐位复用 PATCH /products/{id}，不单独建接口

## /api/comments —— 多态评论

### 讨论范畴

- 🔴 多态查询性能：`(target_type, target_id)` 需要复合索引
- 🟡 评论默认顺序：按 `created_at desc` 还是 `id desc`？
- 🟢 是否支持楼中楼？

### 本次评审共识

- 复合索引必须有，迁移脚本中添加
- 默认按 `id desc`（性能更稳定）
- 楼中楼本期不做

## /api/dashboard/stats —— 后台统计

### 讨论范畴

- 🟡 是否需要按月维度？
- 🟢 是否要导出 CSV？

### 本次评审共识

- 本期仅返回累计数 + 最近 7 天数组
- CSV 导出本期不做

## 待整改清单（开发阶段引用）

| 编号 | 问题 | 负责人 | Story |
|---|---|---|---|
| R-001 | uploads 接口未走 ApiResponse 包装 | backend-dev | 1.2 |
| R-002 | products 列表未分页 | backend-dev | 1.1 |
| R-003 | comments 缺复合索引 | backend-dev | 3.1 |
| R-004 | auth refresh 缺 rotate | backend-dev | 4.1 |
| R-005 | 错误码缺统一目录 | backend-dev | 跨 Epic |
