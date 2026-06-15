# 后端代码规范

## 1. 接口响应格式

所有 HTTP 接口必须返回统一的三字段结构：

```json
{
  "code": 0,
  "msg": "ok",
  "data": { ... }
}
```

字段说明：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | int | 是 | 业务状态码。`0` 表示成功，非 0 表示失败 |
| `msg` | string | 是 | 状态描述。成功时通常为 `"ok"`，失败时是给用户看的简短说明 |
| `data` | object/array/null | 是 | 业务数据。失败时可为 `null` 或包含错误上下文 |

**为什么不直接用 HTTP 状态码？**
HTTP 状态码（200/400/500）粒度太粗，不足以表达业务级错误。前端需要知道"这次失败是因为用户名重复（2001）还是因为账号被禁用（2002）"，HTTP 状态码做不到。

**HTTP 状态码仍然要用**：
- 系统级错误（连接失败、服务挂掉）：返回 5xx
- 业务级错误（参数不对、规则不过）：返回 200，靠 `code` 字段区分

## 2. 错误码段约定

错误码分两段：

| 段位 | 用途 | 示例 |
|------|------|------|
| `0` | 成功 | `code: 0` |
| `1000-1999` | 通用错误 | 参数错误、鉴权失败、限流、签名错误 |
| `2000-2999` | 业务错误 | 业务规则未通过、状态冲突、资源不存在 |
| `3000-3999`（预留） | 第三方依赖错误 | 上游 API 调用失败 |

**所有错误码必须在 `error-codes.md` 字典中注册**——禁止在代码里硬写未注册的码。

## 3. 异常处理

禁止裸抛 `Exception`，必须用业务异常类：

```python
# ❌ 错误
raise Exception("用户名已存在")

# ✅ 正确
from app.exceptions import BizError
raise BizError(code=2001, msg="用户名已存在")
```

`BizError` 由统一的异常处理器拦截，转换为标准响应。

## 4. 日志规范

关键路径必须有日志：

- `logger.info(...)`：业务流程关键节点
- `logger.warning(...)`：可恢复的异常情况
- `logger.error(...)`：不可恢复的错误，必须包含上下文（用户 ID、请求 ID 等）

```python
# ✅ 好的日志
logger.error(
    "支付回调验签失败",
    extra={"order_id": order_id, "sign": sign_received}
)

# ❌ 差的日志
logger.error("失败了")
```

## 5. ORM 规范

- 禁止在循环里执行 SQL（N+1 查询）：

```python
# ❌ 错误
for post in posts:
    author = db.query(User).filter_by(id=post.author_id).first()

# ✅ 正确
authors = db.query(User).filter(User.id.in_([p.author_id for p in posts])).all()
```

- 复杂查询用 `join` 或 `selectinload`，不要用应用层拼接

## 6. 命名规范

- 路由文件：`routers/<resource>.py`（如 `posts.py`、`comments.py`）
- 服务文件：`services/<resource>_service.py`
- 数据模型：`models/<resource>.py`，类名 PascalCase（`Post`、`Comment`）
- 函数：snake_case（`get_post_by_id`），不用驼峰
