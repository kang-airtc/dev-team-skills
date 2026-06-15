# 迁移描述：新建 news 表

## 变更内容

新增 news 表，字段如下：

- id: Integer, 主键, autoincrement
- title: String(255), 非空, 索引 ix_news_title
- slug: String(255), 非空, 唯一, 索引 ix_news_slug
- summary: String(500), 可空
- cover_image: String(500), 可空
- content: Text, 非空
- author: String(100), 可空
- is_published: Boolean, 非空, 默认 true
- published_at: DateTime(timezone=True), 可空
- created_at: DateTime(timezone=True), server_default=now(), 非空
- updated_at: DateTime(timezone=True), server_default=now(), 非空

## 要求

- downgrade 必须完整，顺序与 upgrade 严格相反
- 索引在 downgrade 里先删索引再删表
