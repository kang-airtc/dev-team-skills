# base-word-export 输出示例

**输入**：input/sample.md

## 命令行输出

```
$ source venv/bin/activate
$ python3 .opencode/skills/base-word-export/scripts/word_export.py /tmp/sample.md
已生成：/tmp/sample.docx
```

## 生成的 .docx 内容（对应书稿图 3-1）

用 Word 打开 `sample.docx`，可以看到由 `input/sample.md` 转换出的四类元素：

| Markdown 源 | Word 呈现 |
|-------------|-----------|
| `# 测试文档` | 一级标题：测试文档 |
| `这是一段普通文字。` | 正文段落 |
| `## 子标题` | 二级标题：子标题 |
| `- 第一项` / `- 第二项` | 项目符号列表 |

> .docx 为二进制产物，不随仓库提供。按 input/intent.md 中的「等价命令行」即可在本地重新生成。
