---
name: base-dir-view
description: 列出指定目录的树形结构，附带每个文件的大小和修改时间，自动跳过 node_modules、.git、venv 等噪声目录
---

# Dir View - 目录浏览

打印目录的树形结构，附带文件大小和修改时间，让 Agent（或读者本人）快速建立对项目布局的认知。

## 触发场景

- 第一次进入一个项目目录，想看清楚都有什么文件
- 排查"哪个目录占空间"、"哪些文件最近改过"
- 配合 `base-summarize`、代码审查类 Skill 给出后续操作建议

## 目录结构

```
base-dir-view/
├── SKILL.md
└── scripts/
    └── view.sh
```

## 使用方法

```bash
.opencode/skills/base-dir-view/scripts/view.sh <目录路径> [最大深度]
```

参数：
- `<目录路径>`：必填，要查看的目录
- `[最大深度]`：可选，默认 3

## 输出格式

层级缩进 + 文件大小（人类可读）+ 修改日期：

```
my-project/  (12K, 2026-04-25)
  README.md  (2.3K, 2026-04-25)
  src/  (8.4K, 2026-04-24)
    main.py  (3.1K, 2026-04-24)
    utils.py  (5.3K, 2026-04-23)
  tests/  (1.2K, 2026-04-22)
    test_main.py  (1.2K, 2026-04-22)
```

## 边界

- 自动跳过 `node_modules/`、`.git/`、`venv/`、`__pycache__/`、`.next/`、`dist/`、`build/`
- 不递归符号链接，避免循环
- 跨平台兼容 macOS 和 Linux 的 `date` / `stat` 差异
