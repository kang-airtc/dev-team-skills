---
name: dev-spec-diff
description: 对比当前代码与团队规范文档，输出偏差清单（哪些规则违反、哪些规则代码里没用上、哪些需要补充）
---

# Dev Spec Diff - 规范偏差对比

把代码现状和 `references/` 里的规范文档放一起 diff，输出三类偏差：违规、未覆盖、可优化。

## 触发场景

- 团队规范升级后，要看存量代码偏离了多少
- 接手新项目后，先 diff 一下规范遵守度
- 季度技术债盘点

## 目录结构

```
dev-spec-diff/
├── SKILL.md
├── scripts/
│   └── diff.py
└── references/
    └── (空，规范文档来自 dev-frontend-lint / dev-backend-lint)
```

## 依赖

仅使用 Python 标准库。读取的规范文档来自同级 `dev-frontend-lint/references/` 或 `dev-backend-lint/references/`。

## 使用方法

```bash
python3 .opencode/skills/dev-spec-diff/scripts/diff.py \
  --code ./blog/backend/app \
  --spec ../dev-backend-lint/references/backend-standard.md \
  --output ./reports/spec-diff.md
```

参数：
- `--code, -c`：代码目录
- `--spec, -s`：规范文档路径
- `--output, -o`：输出报告路径

## 输出格式

```markdown
# 规范偏差报告

## 1. 违规项（代码不符合规范）
- routers/posts.py:78 响应缺少 code/msg 字段（违反规范第 1 节）

## 2. 未覆盖项（规范定义了但代码没用到）
- 规范第 5 节定义了 ORM 批量查询规范，代码里未发现使用（中性提示）

## 3. 可优化项（代码可以做得更好）
- services/auth.py 缺少 logger.info 关键节点日志
```

## 边界

- 只做静态对比，不分析运行时行为
- 规范文档需要语义清晰，模糊条款无法被准确 diff
- 输出仅供参考，最终判断由人决定
