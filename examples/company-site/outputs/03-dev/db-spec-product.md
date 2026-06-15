# Product 数据模型规格

> 输入给 `dev-db`，生成 `server/models/product_model.py`

## 表名
`products`

## 字段

| 字段 | 类型 | 约束 | 备注 |
|---|---|---|---|
| id | int | PK, autoincrement | |
| name | str(150) | NOT NULL, index | 产品名 |
| slug | str(150) | UNIQUE, NOT NULL, index | URL 友好标识 |
| category_id | int | FK -> categories.id, ON DELETE SET NULL | 分类可独立删除 |
| price | numeric(12,2) | NOT NULL, server_default=0 | 单位元 |
| cover_url | str(255) | nullable | 封面相对 URL |
| gallery | text | nullable | JSON 字符串，图集 URL 列表 |
| specs | text | nullable | JSON 字符串，规格字典 |
| description | text | nullable | 产品描述 |
| is_published | bool | NOT NULL, server_default=false | 是否上架 |
| is_featured | bool | NOT NULL, server_default=false | 是否推荐 |
| created_at | datetime | NOT NULL, server_default=now() | |
| updated_at | datetime | NOT NULL, server_default=now(), onupdate=now() | |

## 索引

- `(category_id, is_published)` 列表筛选
- `is_featured` 推荐位查询

## 关系

- `category: Mapped[Category | None]`（多对一）
- `comments: Mapped[list[Comment]]`（一对多，target_type='product'，application-level）

## 兼容性

- `gallery` / `specs` 用 `Text` 存 JSON 字符串而不是 `JSONB`，保持 SQLite / PG 双向兼容（教学场景）
- 生产环境建议改 `JSONB` 并加 GIN 索引
