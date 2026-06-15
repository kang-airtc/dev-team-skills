---
name: deploy-changelog
description: 基于 git log 和 conventional commit 规范，自动生成版本变更日志 CHANGELOG.md
---

# Deploy Changelog - 变更日志生成

读取自上次 tag 以来的 git commit 记录，按 conventional commit 规范（feat/fix/refactor/docs 等）分类，生成结构化的 CHANGELOG.md。

## 触发场景

- 发版前需要写 CHANGELOG
- 自动生成版本发布说明
- 保持变更历史清晰可追溯
- 替代手工维护 CHANGELOG

## 目录结构

```
deploy-changelog/
├── SKILL.md
├── scripts/
│   └── generate.sh
└── assets/
    └── changelog-template.md
```

## 依赖

- `git`
- `grep` / `sed`
- 仅使用 Shell

## 使用方法

```bash
# 基于上次 tag 生成 CHANGELOG
bash .opencode/skills/deploy-changelog/scripts/generate.sh

# 指定版本号
bash .opencode/skills/deploy-changelog/scripts/generate.sh --version v1.2.0

# 指定日期范围
bash .opencode/skills/deploy-changelog/scripts/generate.sh --since 2024-01-01
```

参数：
- `--version, -v`：版本号，默认自动推断（最新 tag + 1）
- `--since`：起始日期
- `--output, -o`：输出路径，默认 `CHANGELOG.md`

## Commit 分类规则

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 添加用户登录` |
| `fix` | Bug 修复 | `fix: 修复登录态过期` |
| `refactor` | 重构 | `refactor: 优化数据库查询` |
| `perf` | 性能优化 | `perf: 减少首屏加载时间` |
| `docs` | 文档更新 | `docs: 更新 API 文档` |
| `chore` | 杂项 | `chore: 更新依赖版本` |

## 输出格式

```markdown
# Changelog

## [v1.2.0] - 2024-01-15

### Features
- 添加用户登录功能 (feat: login)
- 支持手机号注册 (feat: phone signup)

### Bug Fixes
- 修复登录态 7 天后过期问题 (fix: token expiry)
- 修复移动端样式错位 (fix: mobile layout)

### Performance
- 减少首屏加载时间 30% (perf: lazy loading)

## [v1.1.0] - 2024-01-08
...
```

## 边界

- 依赖团队的 commit message 规范
- 不解析 squash merge 的详细内容
- 只生成文本，不自动打 tag 或发 release

## 与其他 Skill 的关系

```
git commit ──▶ deploy-changelog ──▶ deploy-release
  提交记录      生成 CHANGELOG      生成发布说明
```
