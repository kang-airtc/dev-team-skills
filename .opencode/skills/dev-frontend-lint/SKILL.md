---
name: dev-frontend-lint
description: 检查前端代码是否遵守团队规范——组件命名、错误码消费（1000/2000 段）、API 调用统一封装、样式规范等
---

# Dev Frontend Lint - 前端规范检查

读取前端工程目录，对比 `references/frontend-standard.md` 的规范要求，输出违规清单和修复建议。

## 触发场景

- PR 提交前自检，避免被打回
- 接手老前端工程，先扫一遍规范一致性
- 团队规范升级后，批量检查存量代码

## 目录结构

```
dev-frontend-lint/
├── SKILL.md
├── scripts/
│   └── lint.py
└── references/
    └── frontend-standard.md     # 前端规范（含错误码消费约定）
```

## 依赖

仅使用 Python 标准库。

## 使用方法

```bash
python3 .opencode/skills/dev-frontend-lint/scripts/lint.py \
  --path ./blog/frontend/src \
  --output ./reports/frontend-lint.md
```

参数：
- `--path, -p`：要扫描的前端源码目录（默认 `./src`）
- `--output, -o`：输出报告路径，默认 stdout

## 检查项

按 `references/frontend-standard.md` 的规范，检查包括但不限于：

- **组件命名**：PascalCase（如 `UserCard.tsx`），文件名与默认导出一致
- **API 调用统一封装**：禁止裸 `fetch` / `axios`，必须经 `src/lib/api.ts` 统一封装
- **错误码消费**：API 返回的 `code` 字段必须按 1000-2999 段映射到提示语（详见规范）
- **样式规范**：禁止行内 style，统一用 Tailwind 或 CSS Module
- **import 顺序**：第三方包 → 项目模块 → 相对路径
- **TypeScript any**：限制使用，必须时加 `// @ts-expect-error 原因` 注释

## 输出格式

```markdown
# 前端规范检查报告

**扫描目录**：./blog/frontend/src
**违规总数**：12 处

## P1 严重违规

- `pages/login.tsx:42` 直接调用 `fetch('/api/login')`，未经统一封装
- ...

## P2 一般违规

- `components/Card.tsx:1` 文件名 `Card.tsx` 与默认导出 `BlogCard` 不一致
- ...

## P3 风格建议

- ...
```

## 边界

- 只检查代码文件，不分析依赖版本（依赖检查见 `dev-deps-audit`）
- 仅做静态规则匹配，不做语义级别的代码审查
- 规范文档可以改，改完检查结果会立即变化
