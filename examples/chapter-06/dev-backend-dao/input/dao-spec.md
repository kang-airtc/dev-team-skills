# DAO 描述：NewsDAO

## 模型
News（server/models/news_model.py）

## 需要的方法

| 方法 | 说明 |
|------|------|
| list_ | 分页列表，支持 published_only 过滤，按 published_at desc 排序 |
| get_by_id | 按 ID 查单条，返回 Optional[News] |
| get_by_slug | 按 slug 查单条，返回 Optional[News] |
| create | 新建记录，commit 并 refresh |
| update | 按 ID 更新字段，commit 并 refresh |
| delete | 按 ID 删除，返回 bool |

## 技术约束

- 使用 SQLAlchemy 2.x async（select + await session.execute）
- 注入 AsyncSession = Depends(get_db_session)
- list_ 需要同时返回列表和总数（Tuple[List[News], int]）
