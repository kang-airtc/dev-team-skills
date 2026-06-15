# 开发阶段汇总报告（dev-pipeline summary）

> 来源 Skill：`dev-pipeline`
> 运行命令：`opencode run dev-pipeline --project dev-team-skills/examples/company-site --output outputs/03-dev/`
> 生成时间：2026-04-25 16:08

本报告由 `dev-pipeline` 在跑完所有 `dev-*` 子 Skill 后聚合产出，作为开发阶段交给评审、测试、发布的"封口产物"。后续阶段只需读取本目录，不需要再去翻代码仓库。

## 1. 产物清单

| 类别 | 文件 | 来源 Skill | 用途 |
|------|------|------------|------|
| 架构图 | `arch.drawio` | dev-arch | 分层架构（前端/API/数据库）|
| 架构输入 | `arch-spec.md` | 人工 | dev-arch 的输入草稿 |
| 时序图 | `comment-sequence.md` | dev-sequence | 评论发布的多角色时序 |
| 技术方案 | `techspec-uploads.md` | dev-techspec | 上传模块的实现方案 |
| 数据模型输入 | `db-spec-product.md` | 人工 | dev-db 的字段描述 |
| OpenAPI | `openapi.json` | FastAPI 导出 | 6 模块 27 接口 |
| 接口文档 | `apidoc.docx` | dev-apidoc | Word 版接口文档（约 14 页）|
| 后端 lint | `backend-lint.md` | dev-lint | 反面教材的 P1/P2/P3 分级报告 |
| 前端 lint | `frontend-lint.md` | dev-lint | 前端组件规范扫描 |
| 规范偏差 | `spec-diff.md` | dev-specdiff | 实现 vs 设计草案的差异列表 |
| 依赖审计 | `deps-audit.md` | dev-deps | 第三方依赖的许可证与漏洞 |
| 汇总报告 | `dev-summary.md` | dev-pipeline | 本文件 |

合计 8 类、12 个文件，覆盖架构、数据模型、接口、代码质量与依赖五条线。

## 2. 关键指标

| 指标 | 数值 | 阈值 | 状态 |
|------|------|------|------|
| 接口数量 | 27 | — | — |
| 后端 P1 违规 | 3 | 0 | ❌ 需修复 |
| 后端 P2 违规 | 2 | ≤ 5 | ✅ |
| 前端 P1 违规 | 0 | 0 | ✅ |
| 规范偏差条目 | 4 | ≤ 5 | ✅ |
| 高危依赖（CVSS ≥ 7）| 0 | 0 | ✅ |
| OpenAPI 校验 | 通过 | — | ✅ |

## 3. 必修问题（交给评审阶段）

- `backend-lint.md` 中 3 条 P1：MIME 信任前端、无文件大小校验、未走 ApiResponse 包装
- 这些项会成为 `review-backend` 的预期发现，进入 PR-001 的"必修清单"

## 4. 流转关系

```
设计阶段（outputs/02-design/）
        │ design-review.md 中"上传接口约定"作为输入
        ▼
开发阶段（outputs/03-dev/）  ← 本目录
        │ apidoc.docx → 项目对接方
        │ backend-lint.md → 评审阶段（必修清单）
        │ openapi.json → 测试阶段（test-api 生成用例）
        ▼
评审阶段（outputs/04-review/）
```

## 5. 下一步

- 提交 `feature/uploads` 分支，触发评审阶段的 `review-backend` / `review-frontend`
- 把 `openapi.json` 同步给前端，让接口对接零猜测
- 把 `apidoc.docx` 归档到 wiki，作为对外交付物
