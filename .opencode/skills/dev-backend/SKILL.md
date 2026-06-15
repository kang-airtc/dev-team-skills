---
name: dev-backend
description: 从 api-spec.md 生成 FastAPI schema + views 骨架（Pydantic v2、ApiResponse 包装、JWT 鉴权注入）
tools: []
---

# dev-backend

## 用途

根据 `api-spec.md` 接口规格说明，生成 FastAPI 路由目录下的三个文件：`__init__.py`、`schema.py`、`views.py`。

生成的代码统一：
- 使用 `ApiResponse[T]` 包装所有响应
- 鉴权接口注入 `current_user: User = Depends(get_current_user)`
- 未找到资源统一抛 `HTTPException(status_code=404)`
- DAO 通过 `Depends()` 自动注入

## 输入

- `intent.md`：自然语言描述意图
- `api-spec.md`：路由前缀、接口列表（方法/路径/鉴权/说明）、Schema 字段要求、技术约束

## 产出

```
server/web/api/[模块]/
├── __init__.py      ← 导出 router
├── schema.py        ← Pydantic v2 模型（Create/Update/Response/ListResponse）
└── views.py         ← 路由函数
```

## 使用方式

```bash
python3 .opencode/skills/dev-backend/scripts/generate.py \
  --input path/to/api-spec.md \
  --output-dir path/to/output
```
