---
name: review-backend
description: 检查后端新增代码是否符合团队规范——响应格式、错误码、命名约定、异常处理、日志、ORM 查询、Pydantic Schema 等
---

# Review Backend - 后端代码审查

读取当前 Git 差异或指定的后端目录，对照 `references/backend-standard.md` 中的项目规范，逐条核查新增代码，输出分级违规清单和修复建议。

**只扫 diff 的加号行，不追究历史存量问题。**

---

## 触发场景

用自然语言说即可，例如：

- 帮我检查一下后端代码
- 我刚写完评论接口，review 一下
- 提交前帮我跑个后端审查
- 看看这个 views.py 有没有不规范的地方

---

## 目录结构

```
review-backend/
├── SKILL.md
└── references/
    ├── backend-standard.md     # 项目后端规范
    └── error-codes.md          # 错误码字典（新增错误码需先在此注册）
```

---

## 依赖

无外部依赖。读取 `git diff` 输出或目录文件，AI 直接分析。

---

## 使用方法

### 方式一：检查当前改动（推荐）

```
帮我 review 一下后端改动
```

Agent 自动执行 `git diff HEAD`，只分析新增的 `.py` 文件。

### 方式二：检查指定文件

```
review 一下 server/web/api/comments/views.py
帮我看看这个 DAO 写法对不对
```

### 方式三：命令行模式

```bash
git diff HEAD -- '*.py' | grep '^+'
```

---

## 检查项

按照 `references/backend-standard.md` 逐条核查，分以下八个维度：

### 1. 目录与文件组织

- 路由处理函数只在 `views.py` 里定义
- DAO 只负责数据库操作，不做业务判断
- `schema.py` 只放 Pydantic 模型，不导入 DAO / ORM

### 2. 命名规范

- 文件名、函数名：snake_case（`product_dao.py`、`get_product_by_id`）
- 类名：PascalCase（`Product`、`ProductDAO`、`ProductCreate`）
- ORM 模型类：单数业务名（`Product`，不是 `Products`）
- DAO 类：业务名 + `DAO`（`ProductDAO`）
- Pydantic 输入：业务名 + `Create` / `Update`
- Pydantic 响应：业务名 + `Response` / `ListResponse`
- 路由函数：动词 + 名词（`create_product`、`list_products`）

### 3. 接口响应格式

- 所有接口必须返回 `ApiResponse`，禁止裸字典 `{"data": ...}`
- 成功：`ApiResponse.success(data=...)`
- 失败：`ApiResponse.error(code=..., msg=...)`
- `raise HTTPException` 只用于系统级错误（401/403/500），不用于业务错误

### 4. 错误码规范

- 所有错误码必须在 `references/error-codes.md` 中已注册
- 禁止硬写未注册的数字（如 `code=9999`）
- 禁止裸抛 `Exception("xxx")`

### 5. 异常处理

- DAO 调用必须有异常处理，不让数据库异常裸抛到路由层
- 业务校验失败用 `return ApiResponse.error(...)`，不用 `raise`

### 6. 日志规范

- 禁止 `print()` 调试
- `logger.error` 必须包含上下文（资源 ID、用户 ID、请求参数等）
- 关键业务节点需要 `logger.info`

### 7. ORM / 数据库规范

- 禁止在循环里执行 SQL（N+1 查询）
- 分页查询必须同时查 `total`，不允许全量拉取再切片
- 复杂关联用 `selectinload` / `joinedload`

### 8. Pydantic Schema 规范

- 输入模型（`Create` / `Update`）和响应模型（`Response`）必须分开
- `Response` 模型必须有 `model_config = ConfigDict(from_attributes=True)`
- `Update` 模型所有字段设为 `Optional`
- Schema 里禁止做数据库操作

---

## 输出格式

```markdown
# 后端代码审查报告

**审查文件**：`server/web/api/comments/views.py`
**对照规范**：`references/backend-standard.md`
**违规总数**：N 处

## 🔴 P1 必须修复

- `views.py:23` 业务错误用了 `raise HTTPException(status_code=400)`，
  应改为 `return ApiResponse.error(code=ErrorCode.xxx, msg="...")`

## 🟡 P2 建议修复

- `views.py:45` `logger.error("失败了")` 缺少上下文，
  应加上 `extra={"comment_id": comment_id}`

## 🟢 P3 小改进

- `schema.py:12` `CommentUpdate` 的 `content` 字段不是 `Optional`，
  不支持部分更新
```

---

## 边界

- 只检查 `.py` 文件，不处理配置文件、migration 文件
- 只看 diff 加号行，不追究历史代码
- 不替代 ruff / pylint，linter 能查的不重复报
- 错误码字典在 `references/error-codes.md`，新增错误码需先注册再使用
