# 后端代码规范

> 适用范围：FastAPI + SQLAlchemy（async）+ Pydantic v2 项目

---

## 1. 目录结构

```
server/
├── web/
│   └── api/
│       └── <resource>/        # 按资源分目录
│           ├── __init__.py
│           ├── views.py        # 路由处理函数
│           └── schema.py       # Pydantic 输入/输出模型
├── dao/
│   └── <resource>_dao.py      # 数据访问层（每个资源一个文件）
├── models/
│   └── <resource>_model.py    # SQLAlchemy ORM 模型
├── web/api/response.py        # 统一响应格式 ApiResponse
├── web/api/error_codes.py     # 错误码枚举
└── dependencies.py            # FastAPI 依赖注入
```

规则：
- 路由只在 `views.py` 里定义，不在 `__init__.py` 里写业务逻辑
- DAO 只负责数据库操作，不做业务判断
- `schema.py` 只放 Pydantic 模型，不导入 DAO / ORM

---

## 2. 命名规范

| 场景 | 规则 | 示例 |
|------|------|------|
| 文件名 | snake_case | `product_dao.py`、`news_model.py` |
| 函数名 | snake_case | `get_product_by_id`、`list_news` |
| 类名 | PascalCase | `Product`、`ProductCreate`、`ProductDAO` |
| ORM 模型类 | 单数业务名 | `Product`、`NewsArticle`、`User` |
| DAO 类 | 业务名 + `DAO` | `ProductDAO`、`NewsDAO` |
| Pydantic 输入模型 | 业务名 + `Create` / `Update` | `ProductCreate`、`ProductUpdate` |
| Pydantic 响应模型 | 业务名 + `Response` | `ProductResponse`、`ProductListResponse` |
| 路由处理函数 | 动词 + 名词 snake_case | `create_product`、`list_products`、`delete_product` |

---

## 3. 接口响应格式

所有接口必须返回统一三字段结构：

```json
{ "code": 0, "msg": "success", "data": { ... } }
```

- `code=0` 成功，非 `0` 失败
- 禁止直接 `return {"data": ...}` 裸字典，必须用 `ApiResponse.success()` 或 `ApiResponse.error()`
- 禁止用 `raise HTTPException` 返回业务错误，只用于系统级错误（404/401/403/500）

```python
# ✅ 正确
from server.web.api.response import ApiResponse
return ApiResponse.success(data=ProductResponse.model_validate(obj))

# ❌ 错误
return {"code": 0, "data": obj}
raise HTTPException(status_code=400, detail="slug 已存在")  # 业务错误不用 HTTPException
```

---

## 4. 错误码规范

| 段位 | 用途 | 示例 |
|------|------|------|
| `0` | 成功 | `code: 0` |
| `1000–1999` | 通用错误（参数/鉴权/限流） | 1001 参数缺失、1101 未登录 |
| `2000–2999` | 业务错误 | 2001 用户名已存在、2101 文章不存在 |

规则：
- **所有错误码必须在 `error_codes.py` 中注册**，禁止在代码里硬写未注册的数字
- 禁止裸抛 `Exception("xxx")`，必须用 `ApiResponse.error(code=xxxx, msg="...")`

```python
# ✅ 正确
from server.web.api.error_codes import ErrorCode
return ApiResponse.error(code=ErrorCode.USER_NOT_FOUND, msg="用户不存在")

# ❌ 错误
raise Exception("用户不存在")
return ApiResponse.error(code=9999, msg="错误")   # 9999 未注册
```

---

## 5. 异常处理

- 所有 DAO 调用必须有异常处理，不让数据库异常裸抛到路由层
- 业务校验失败：`return ApiResponse.error(...)`，不用 `raise`
- 真正的系统异常（数据库连接失败等）：记录日志后用 `raise HTTPException(status_code=500)`

```python
# ✅ 正确
async def create_product(payload: ProductCreate, dao: ProductDAO = Depends()):
    if await dao.get_by_slug(payload.slug):
        return ApiResponse.error(code=ErrorCode.SLUG_EXISTS, msg="slug 已存在")
    obj = await dao.create(**payload.model_dump())
    return ApiResponse.success(data=ProductResponse.model_validate(obj))
```

---

## 6. 日志规范

- `logger.info`：业务关键节点
- `logger.warning`：可恢复的异常
- `logger.error`：不可恢复错误，必须带上下文（用户 ID、资源 ID 等）
- **禁止** `print()` 调试，必须用 `logger`

```python
# ✅ 正确
logger.error("产品创建失败", extra={"slug": payload.slug, "error": str(e)})

# ❌ 错误
print("失败了", e)
logger.error("失败了")   # 没有上下文
```

---

## 7. ORM / 数据库规范

- **禁止在循环里执行 SQL**（N+1 查询）：

```python
# ❌ 错误（N+1）
for product in products:
    category = db.query(Category).filter_by(id=product.category_id).first()

# ✅ 正确
ids = [p.category_id for p in products]
categories = db.query(Category).filter(Category.id.in_(ids)).all()
```

- 复杂关联用 `selectinload` / `joinedload`，不做应用层拼接
- 分页查询必须同时查 `total`（`COUNT`），不允许全量拉取再切片

---

## 8. Pydantic Schema 规范

- 输入模型（`Create` / `Update`）和响应模型（`Response`）必须分开定义
- `Response` 模型必须加 `model_config = ConfigDict(from_attributes=True)` 以支持 ORM 对象转换
- `Update` 模型所有字段设为 `Optional`，允许部分更新
- 禁止在 Schema 里做数据库操作或调用 DAO

```python
# ✅ 正确
class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

class ProductUpdate(BaseModel):
    name: Optional[str] = None      # 所有字段 Optional
    price: Optional[Decimal] = None
```
