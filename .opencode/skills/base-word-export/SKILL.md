---
name: base-word-export
description: 把 Markdown 文件导出为 Word 文档（.docx），支持标题、段落、列表、代码块四种基本元素
---

# Word Export - Markdown 转 Word

把一份 Markdown 文档转成 Word 文档，便于分享给非技术同事，或作为正式交付物归档。

## 触发场景

- 写完一份技术文档，要发给产品/运营/法务等不熟悉 Markdown 的同事
- 周报、月报需要 Word 格式归档
- 给客户的交付文档需要正式排版

## 目录结构

```
base-word-export/
├── SKILL.md
└── scripts/
    └── word_export.py
```

## 依赖

需要 `python-docx`，已在工程根 `requirements.txt` 中。在工程根执行：

```bash
source venv/bin/activate
python -c "import docx" && echo OK
```

## 使用方法

```bash
python3 .opencode/skills/base-word-export/scripts/word_export.py <md文件> [-o <输出路径>]
```

参数：
- `<md文件>`：必填，要转换的 Markdown 文件
- `-o, --output`：可选，输出 .docx 路径，默认与输入同目录、同文件名

## 支持的 Markdown 元素

| Markdown | Word 渲染 |
|----------|-----------|
| `# / ## / ### / ####` | 一到四级标题 |
| 普通段落 | 默认字体段落 |
| `- 项` 或 `* 项` | 项目符号列表 |
| 三个反引号围栏 | 等宽字体段落（Courier New） |

## 边界

- **不支持**：表格、图片、行内格式（`**加粗**` / `*斜体*` / `` `代码` ``）
- **不输出**：页眉、页脚、目录
- 这是一个教学版本，演示 Python 类 Skill 的写法。生产场景里建议使用功能更全的 word-generator（出版社规范）
