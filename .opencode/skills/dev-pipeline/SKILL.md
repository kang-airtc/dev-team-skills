---
name: dev-pipeline
description: 整合开发阶段 10 个 Skill，按文档线（可并行）+ 代码线（串行）编排，一键产出完整模块代码与文档
---

# Dev Pipeline - 开发助手流水线

整合 dev-arch、dev-sequence、dev-techspec、dev-apidoc（文档线）以及 dev-db、dev-migrate、dev-backend-dao、dev-backend、dev-frontend、dev-frontend-form（代码线）10 个 Skill，一次生成一个完整功能模块的全套产物。

## 触发场景

- 新功能模块从需求确认后，要快速产出全套代码与文档
- 团队需要"标准化输出"——所有文件符合最新团队规范
- 减少样板代码的手动编写，让人专注业务逻辑

## 目录结构

```
dev-pipeline/
├── SKILL.md
├── scripts/
│   └── run-all.sh          # 一键完整流程
└── references/
    └── pipeline.conf       # 流水线配置（可选覆盖路径）
```

## 依赖

- Python 标准库 + `python-docx`
- 同目录下 10 个 dev-* Skill

## 使用方法

```bash
# 参数：模块名  输入目录  输出目录（可选，默认 <模块名>-output）
./scripts/run-all.sh news ./inputs/ ./news-output/
```

**输入目录需包含：**

| 文件名 | 用途 | 对应 Skill |
|--------|------|------------|
| `arch-spec.md` | 架构描述 | dev-arch |
| `sequence-spec.md` | 时序描述 | dev-sequence |
| `openapi-snippet.json` | 接口描述 | dev-apidoc |
| `model-spec.md` | 数据库模型字段 | dev-db |
| `migration-spec.md` | 迁移描述 | dev-migrate |
| `dao-spec.md` | 数据访问层描述 | dev-backend-dao |
| `api-spec.md` | 后端接口描述 | dev-backend |
| `page-spec.md` | 前端页面描述 | dev-frontend |
| `form-spec.md` | 前端表单描述 | dev-frontend-form |

（dev-techspec 只需要模块名，不需要输入文件）

**产出目录结构：**

```
news-output/
├── docs/
│   ├── arch.drawio
│   ├── sequence.drawio
│   ├── tech-spec.md
│   └── api-spec.docx
├── server/
│   ├── models/                # ORM 模型（dev-db）
│   ├── alembic/versions/      # 迁移文件（dev-migrate）
│   ├── dao/                   # DAO（dev-backend-dao）
│   └── web/api/news/          # 路由 + schema（dev-backend）
│       ├── __init__.py
│       ├── schema.py
│       └── views.py
└── client/
    ├── news_page.tsx          # 前端页面（dev-frontend）
    ├── NewsForm.tsx           # 表单组件（dev-frontend-form）
    ├── new/page.tsx           # 新建页
    └── [id]/edit/page.tsx     # 编辑页
```

## 内部依赖

```
文档线（可并行）：
  dev-arch ──┐
  dev-sequence ──┤
  dev-techspec ──┤── docs/
  dev-apidoc ──┘

代码线（必须串行）：
  dev-db
    ↓
  dev-migrate
    ↓
  dev-backend-dao
    ↓
  dev-backend
    ↓
  dev-frontend + dev-frontend-form
```

## 边界

- 缺少某个输入文件时，对应步骤自动跳过，不影响其他步骤
- 不修改已存在文件；在新模块目录下创建文件
- 生成产物是"60% 骨架"——业务规则、鉴权、缓存策略仍须人工补充
