# 新闻模型（News）

## 表名
news

## 字段定义

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | int | 主键，自增 | |
| title | varchar(255) | 非空，带索引 | 新闻标题 |
| slug | varchar(255) | 非空，唯一，带索引 | URL 路径标识 |
| summary | varchar(500) | 可空 | 摘要 |
| cover_image | varchar(500) | 可空 | 封面图 URL |
| content | text | 非空 | 正文 |
| author | varchar(100) | 可空 | 作者 |
| is_published | bool | 非空，默认 true | 是否发布 |
| published_at | datetime(tz) | 可空 | 发布时间 |
| created_at | datetime(tz) | 自动填充 | |
| updated_at | datetime(tz) | 自动更新 | |

## 附注

- 使用 SQLAlchemy 2.x Mapped 注解语法
- 时间字段统一带时区（timezone=True）
- created_at 使用 server_default=func.now()，updated_at 还需 onupdate=func.now()
