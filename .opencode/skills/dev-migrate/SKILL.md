---
name: dev-migrate
description: 从 migration-spec.md 生成 Alembic 升降级迁移脚本（downgrade 与 upgrade 严格镜像，先删索引再删表）
tools: []
---

# dev-migrate

## 用途

根据 `migration-spec.md` 变更说明，生成 Alembic 版本迁移文件，确保：
- `upgrade()` 和 `downgrade()` 完整成对
- `downgrade` 操作顺序与 `upgrade` 严格相反（先删最后建的）
- 索引在 downgrade 中先于表被删除

## 输入

- `intent.md`：自然语言描述意图
- `migration-spec.md`：变更内容（字段列表、索引）、要求

## 产出

```
[output-dir]/alembic/versions/
└── YYYYMMDDHHMMSS_add_[table]_table.py
```

## 使用方式

```bash
python3 .opencode/skills/dev-migrate/scripts/generate.py \
  --input path/to/migration-spec.md \
  --output-dir path/to/output
```
