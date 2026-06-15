---
name: dev-backend-lint
description: 检查后端代码（Python / FastAPI）是否遵守团队规范——统一 {code,msg,data} 响应格式、1000-2999 错误码段、ORM 查询规范等
---

# Dev Backend Lint - 后端规范检查

读取后端工程目录，对比 `references/backend-standard.md` 的规范要求，重点检查 API 响应格式和错误码使用。

## 触发场景

- PR 提交前自检
- 接手老后端工程，先扫一遍规范偏离
- 团队规范升级后批量检查存量代码

## 目录结构

```
dev-backend-lint/
├── SKILL.md
├── scripts/
│   └── lint.py
└── references/
    ├── backend-standard.md       # 后端规范（含响应格式、错误码段）
    └── error-codes.md            # 错误码字典
```

## 依赖

仅使用 Python 标准库。

## 使用方法

```bash
python3 .opencode/skills/dev-backend-lint/scripts/lint.py \
  --path ./blog/backend/app \
  --output ./reports/backend-lint.md
```

参数：
- `--path, -p`：要扫描的后端源码目录
- `--output, -o`：输出报告路径，默认 stdout

## 检查项

参考 `references/backend-standard.md`，重点项包括：

- **响应格式**：所有 HTTP 接口必须返回 `{code, msg, data}` 三字段结构（详见规范）
- **错误码合规**：错误码必须落在 1000-2999 段，且在 `error-codes.md` 字典里有定义
  - 1000-1999：通用错误（参数错误、鉴权失败、限流等）
  - 2000-2999：业务错误（业务规则不通过、状态冲突等）
- **异常处理**：禁止裸 `raise Exception`，必须用业务异常类映射到错误码
- **日志规范**：关键路径必须打 `logger.info`，错误必须打 `logger.error` 含上下文
- **ORM 规范**：禁止在循环里执行 SQL，必须用批量查询或 join

## 输出格式

```markdown
# 后端规范检查报告

**扫描目录**：./blog/backend/app
**违规总数**：8 处

## P1 严重违规

- `routers/posts.py:78` 返回 `{"data": ...}` 缺少 code/msg 字段
- `routers/comments.py:45` 抛出 `raise Exception("...")`，未使用业务异常类
- ...

## P2 一般违规

- `services/auth.py:120` 错误码 9999 未在 error-codes.md 字典中定义
- ...
```

## 边界

- 仅做静态规则匹配，不验证业务逻辑正确性
- 错误码字典 `error-codes.md` 是单一事实源，新增错误码必须先注册
- 不替代代码审查，是审查的前置过滤器
