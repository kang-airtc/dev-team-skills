# 后端代码审查报告

**审查文件**：`server/web/api/comments/views.py`
**对照规范**：`references/backend-standard.md`
**违规总数**：8 处（P1×4 / P2×2 / P3×2）

---

## 🔴 P1 必须修复（4 处）

### 1. 响应格式未使用 `ApiResponse`，直接返回裸字典
**位置**：第 13、26、38、44 行

```python
# ❌ 违规
return {"code": 0, "data": items}
return {"code": 0, "msg": "ok", "data": {"id": obj.id}}
return {"code": 0, "msg": "删除成功", "data": None}
return {"code": 0, "data": {"count": len(items)}}
```

规范 §3：所有接口必须通过 `ApiResponse.success()` 返回，禁止裸字典。

```python
# ✅ 修复
from server.web.api.response import ApiResponse

return ApiResponse.success(data=[CommentResponse.model_validate(i) for i in items])
return ApiResponse.success(data=CommentResponse.model_validate(obj), msg="评论成功")
return ApiResponse.success(data={"id": comment_id}, msg="删除成功")
return ApiResponse.success(data={"count": count})
```

---

### 2. 业务错误用了 `raise HTTPException`
**位置**：第 22、35 行

```python
# ❌ 违规
raise HTTPException(status_code=400, detail="评论内容不能为空")
raise HTTPException(status_code=404, detail="评论不存在")
```

规范 §3：`HTTPException` 只用于系统级错误，业务错误必须 `return ApiResponse.error(...)`，且错误码需在 `error-codes.md` 中注册。

```python
# ✅ 修复
from server.web.api.error_codes import ErrorCode

return ApiResponse.error(code=ErrorCode.PARAM_MISSING, msg="评论内容不能为空")
return ApiResponse.error(code=ErrorCode.COMMENT_NOT_FOUND, msg="评论不存在")
```

---

### 3. `get_comment_count` 全量拉取数据再 `len()` 计算数量
**位置**：第 42–44 行

```python
# ❌ 违规
items = await dao.list_by_news(news_id)
return {"code": 0, "data": {"count": len(items)}}
```

规范 §7：分页/统计查询禁止全量拉取再切片，必须在数据库层用 `COUNT`。

```python
# ✅ 修复：在 DAO 里加 count 方法
# comment_dao.py
async def count_by_news(self, news_id: int) -> int:
    stmt = select(func.count(Comment.id)).where(Comment.news_id == news_id)
    return (await self.session.execute(stmt)).scalar_one()

# views.py
count = await dao.count_by_news(news_id)
return ApiResponse.success(data={"count": count})
```

---

### 4. 使用 `print()` 代替 logger
**位置**：第 37 行

```python
# ❌ 违规
print(f"评论 {comment_id} 已删除")
```

规范 §6：禁止 `print()` 调试，必须使用 `logger`，且需包含上下文信息。

```python
# ✅ 修复
import logging
logger = logging.getLogger(__name__)

logger.info("评论删除成功", extra={"comment_id": comment_id, "news_id": news_id})
```

---

## 🟡 P2 建议修复（2 处）

### 5. 路由处理函数命名用了驼峰
**位置**：第 29 行

```python
# ❌ 违规
async def deleteComment(news_id: int, ...):

# ✅ 修复
async def delete_comment(news_id: int, ...):
```

---

### 6. 响应模型未在路由装饰器中声明 `response_model`
**位置**：第 10、17、29、41 行

```python
# ❌ 违规
@router.get("/{news_id}/comments")
@router.post("/{news_id}/comments")

# ✅ 修复
@router.get("/{news_id}/comments", response_model=ApiResponse[CommentListResponse])
@router.post("/{news_id}/comments", response_model=ApiResponse[CommentResponse], status_code=201)
```

---

## 🟢 P3 小改进（2 处）

### 7. 参数校验逻辑放在 view 层，应移入 Pydantic Schema
**位置**：第 21–22 行

```python
# ❌ 当前写法（校验逻辑散落在 view）
if not payload.content or len(payload.content.strip()) == 0:
    raise HTTPException(status_code=400, detail="评论内容不能为空")

# ✅ 修复（移到 schema.py）
class CommentCreate(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("评论内容不能为空")
        return v.strip()
```

---

### 8. 缺少模块文档字符串
**位置**：第 1 行

```python
# ❌ 违规（文件顶部没有 docstring）
from fastapi import APIRouter, ...

# ✅ 修复
"""评论 API 路由。"""
from fastapi import APIRouter, ...
```

---

## 汇总

| 级别 | 数量 | 主要问题 |
|------|------|----------|
| 🔴 P1 必须修复 | 4 | 裸字典响应、HTTPException 处理业务错误、全量拉取计数、print 调试 |
| 🟡 P2 建议修复 | 2 | 函数名驼峰、缺 response_model |
| 🟢 P3 小改进 | 2 | 校验逻辑位置、缺 docstring |

**结论**：P1 全部修复后方可提交。
