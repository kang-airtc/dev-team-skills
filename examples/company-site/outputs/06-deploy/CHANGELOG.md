# CHANGELOG

## v0.2.0 - 2026-04-26

### Features
- feat(uploads): 新增单图与图集上传接口（PR-001）
- feat(comments): 新闻底部评论，支持后台审核（PR-003）
- feat(admin): 后台产品 CRUD 表单页（PR-002）

### Fixes
- fix(uploads): 文件大小上限校验（5MB）
- fix(auth): JWT 过期 refresh token 死循环

### Docs
- docs(arch): 补充 company-site 分层架构图
- docs(api): 接口文档导出 docx

### Chores
- chore(deploy): Dockerfile 增加 HEALTHCHECK
- chore(deps): 升级 next 13.5.4 → 13.5.6（修复 SSRF）
- chore(deps): 升级 python-jose 3.3.0 → 3.4.0

## v0.1.0 - 2026-03-30

### Features
- feat(core): 公开站首页 / 关于 / 产品 / 新闻 / 联系页面骨架
- feat(auth): JWT 鉴权
- feat(admin): 后台登录与导航

### Chores
- chore(infra): docker compose 一键启动
