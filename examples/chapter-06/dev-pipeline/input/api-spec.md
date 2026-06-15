# 接口描述：新闻模块（News）

## 路由前缀
/api/news

## 接口列表

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| GET | / | 否 | 新闻列表，支持 limit/offset 分页 |
| GET | /slug/{slug} | 否 | 按 slug 查详情（公开站用） |
| GET | /{news_id} | 否 | 按 ID 查详情 |
| POST | / | 是 | 新建新闻 |
| PUT | /{news_id} | 是 | 编辑新闻 |
| DELETE | /{news_id} | 是 | 删除新闻 |

## Schema 要求

- NewsCreate：title(必填), slug(必填), content(必填), summary(可选), cover_image(可选), published_at(可选)
- NewsUpdate：所有字段可选（PATCH 语义）
- NewsResponse：全字段
- NewsListResponse：items: List[NewsResponse], total: int

## 技术约束

- 响应统一用 ApiResponse[T] 包装
- 鉴权接口注入 current_user: User = Depends(get_current_user)
- 未找到资源抛 HTTPException(status_code=404, detail="新闻不存在")
