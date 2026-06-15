---
name: dev-db
description: 从 model-spec.md 生成 SQLAlchemy 2.x Mapped 语法的 ORM 模型（含正确的可空类型、server_default、onupdate）
tools: []
---

# dev-db

## 用途

根据 `model-spec.md` 字段说明，生成继承 `Base` 的 SQLAlchemy 2.x ORM 类文件，规避三类典型坑：
- 可空字段 `Mapped` 类型与 `nullable` 矛盾
- `created_at` 用 Python 层 `default` 而非数据库层 `server_default`
- `updated_at` 漏写 `onupdate`

## 输入

- `intent.md`：自然语言描述意图
- `model-spec.md`：表名、字段（名/类型/约束/说明）、附注

## 产出

```
[output-dir]/
└── [table]_model.py
```

## 使用方式

```bash
python3 .opencode/skills/dev-db/scripts/generate.py \
  --input path/to/model-spec.md \
  --output-dir path/to/output
```
