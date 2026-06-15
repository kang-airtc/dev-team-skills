---
name: dev-backend-dao
description: 从 dao-spec.md 生成 SQLAlchemy 2.x async DAO（list_ 含子查询计数、create/update 含 refresh）
tools: []
---

# dev-backend-dao

## 用途

根据 `dao-spec.md` 生成 SQLAlchemy 2.x async 风格的 DAO 类文件，避免以下三类典型错误：
- `await` 漏写（拿到 coroutine 而非结果）
- `count` 未复用 WHERE 条件（全表计数与分页数据不匹配）
- `create` 后未 `refresh`（`id` 等自增字段为 None）

## 输入

- `intent.md`：自然语言描述意图
- `dao-spec.md`：模型名、方法清单（list_/get_by_id/get_by_slug/create/update/delete）、技术约束

## 产出

```
[output-dir]/
└── [module]_dao.py
```

## 使用方式

```bash
python3 .opencode/skills/dev-backend-dao/scripts/generate.py \
  --input path/to/dao-spec.md \
  --output-dir path/to/output
```
