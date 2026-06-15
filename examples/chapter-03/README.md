# 第 3 章示例：首个 Skill 开发（`base-*`）

本目录配合书稿第 3 章，演示三种形态 Skill 的输入意图与预期输出。**路径相对于 dev-team-skills 仓库根目录。**

## 约定

- 各子目录 **input/** 内含 **intent.md**，正文与书稿对应小节的**三种调用方式**一致；带脚本的 Skill 另附结构化输入。
- **output/** 为示例输出，内容取自书稿的「预期输出（示意）」，便于横向对照；二进制产物（如 .docx）不随仓库提供，按 intent.md 中的命令本地生成。

## 书中三个 Skill

| 书中 Skill | 形态 | 脚本目录 | 本目录示例 |
|------------|------|-----------|-----------|
| base-summarize | 纯 Markdown | 无脚本 | base-summarize/ |
| base-dir-view | 带 Shell 脚本 | scripts/view.sh | base-dir-view/ |
| base-word-export | 带 Python 脚本 | scripts/word_export.py | base-word-export/ |

## 一键复现（仓库根目录）

`base-summarize` 为纯 Markdown Skill，在 OpenCode 中按 input/intent.md 的意图调用即可，无脚本命令。

**base-dir-view**：

```bash
.opencode/skills/base-dir-view/scripts/view.sh ./examples/company-site 4
```

**base-word-export**：

```bash
source venv/bin/activate
python3 .opencode/skills/base-word-export/scripts/word_export.py \
  examples/chapter-03/base-word-export/input/sample.md \
  -o examples/chapter-03/base-word-export/output/sample.docx
```
