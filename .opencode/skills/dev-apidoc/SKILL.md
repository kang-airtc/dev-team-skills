---
name: dev-apidoc
description: 从 FastAPI / OpenAPI 规范生成 Word 格式接口文档（.docx），用于交付给非技术同事或归档
---

# Dev API Doc - 接口文档生成

读取 OpenAPI JSON（FastAPI 自动暴露的 `/openapi.json`），生成结构化的 Word 接口文档。

## 触发场景

- 客户/合作方需要接口文档，但他们不会看 Swagger
- 项目交付时归档需要 Word 格式
- 内部对接时给非技术同事（产品/运营）一份接口说明

## 目录结构

```
dev-apidoc/
├── SKILL.md
├── scripts/
│   └── generate.py
└── references/
    └── doc-template.md         # Word 文档模板说明
```

## 依赖

`python-docx`，已在工程根 `requirements.txt` 中。

## 使用方法

```bash
# 从本地 FastAPI 服务读取
python3 .opencode/skills/dev-apidoc/scripts/generate.py \
  --url http://localhost:8000/openapi.json \
  --output ./docs/api-spec.docx

# 从已有 OpenAPI JSON 文件读取
python3 .opencode/skills/dev-apidoc/scripts/generate.py \
  --input ./openapi.json \
  --output ./docs/api-spec.docx
```

参数：
- `--url, -u`：FastAPI 服务的 OpenAPI 端点（与 `--input` 二选一）
- `--input, -i`：本地 OpenAPI JSON 文件路径
- `--output, -o`：输出 Word 路径

## Word 文档结构

按章节组织：

1. **接口总览**：所有接口的清单（方法、路径、摘要）
2. **接口分组**：按 OpenAPI 的 `tags` 分组，每组一个一级章节
3. **每个接口**：
   - HTTP 方法 + 路径
   - 摘要 + 详细描述
   - 路径参数 / 查询参数 / 请求体（含字段类型、是否必填、说明）
   - 响应：按统一 `{code, msg, data}` 格式呈现，列出可能的错误码（来自 `dev-backend-lint/references/error-codes.md`）

## 边界

- 仅支持 OpenAPI 3.0+ 格式
- 不导出请求示例（curl / postman）——这部分仍建议用 Swagger UI
- 不输出页眉页脚，需要的话用 Word 自己加
