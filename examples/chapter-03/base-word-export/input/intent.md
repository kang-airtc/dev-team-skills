# base-word-export 调用意图

对应书稿 3.4.7 节，三种调用方式：

## 显式调用

```
/base-word-export docs/design.md
```

## 自然语言调用（点名 Skill）

```
请使用 base-word-export 帮我把 docs/design.md 导出成 Word
```

## 隐式触发（和其他 Skill 串联）

```
读一下 docs/release-notes.md，整理一下措辞，然后导出成 Word 给 PM
```

> 串联场景下，Agent 会先用 Read 读文件 → 自己改一遍 → 调用 base-word-export 输出 .docx。

## 等价命令行（以本目录 sample.md 为例）

```bash
source venv/bin/activate
python3 .opencode/skills/base-word-export/scripts/word_export.py \
  examples/chapter-03/base-word-export/input/sample.md \
  -o examples/chapter-03/base-word-export/output/sample.docx
```
