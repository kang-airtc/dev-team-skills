# Word 文档模板说明

`dev-apidoc` 不使用外置 Word 模板文件，由脚本 `scripts/generate.py` 直接构建。文档结构固定如下：

## 文档结构

1. **标题**：API 名称 + 版本号（一级标题，居中）
2. **描述**：来自 OpenAPI `info.description`（普通段落）
3. **接口总览**：方法 / 路径 / 摘要 三列表格
4. **按 tag 分组**：每个 tag 一个一级标题，下面是该组的所有接口
5. **每个接口**：
   - 二级标题：`METHOD 路径`
   - 摘要、描述（来自 OpenAPI `summary` / `description`）
   - 参数表（如有）
   - 请求体（如有）
   - 响应表
6. **通用错误码**：固定一节，说明 `{code, msg, data}` 响应格式和 1000/2000 错误码段，引用到 `dev-backend-lint/references/error-codes.md`

## 输入约束

- 仅支持 OpenAPI 3.0+
- 接口的 `tags` 决定分组顺序，无 tags 的接口归入 `default` 组
- `$ref` 引用的 schema 仅显示名字，不展开字段（避免 Word 文档过长）

## 自定义建议

如需调整 Word 样式（字体、表格风格等），改 `scripts/generate.py` 里：
- 表格 style：`Light Grid` → 其他 Word 内置 style
- 标题层级：`level=0/1/2/3` 控制
- 段落字体：python-docx 提供 `font.name` / `font.size` 等接口
