# Release v0.2.0

> 来源 Skill：`deploy-release`  
> 发布时间：2026-04-26

## 本版本带来什么

- 后台可以上传产品封面与图集，公开站详情页直接渲染
- 公开站新闻与产品支持评论，后台可"先审后显"
- 接口响应统一 `ApiResponse[T]` 包装，错误码集中目录
- 一处安全升级：python-jose、next 升级修复已知 CVE

## 升级步骤

1. 拉取代码

   ```bash
   git fetch --tags
   git checkout v0.2.0
   ```

2. 检查环境变量

   `.env.example` 无新增字段，复用旧 `.env` 即可。

3. 重建镜像

   ```bash
   docker compose build --no-cache
   ```

4. 跑数据库迁移（含 comments 表新增多态字段索引）

   ```bash
   docker compose up -d postgres
   docker compose run --rm backend alembic upgrade head
   ```

5. 重启全部服务

   ```bash
   docker compose up -d
   ```

6. 烟雾测试

   - 访问 http://localhost:3000 公开站首页正常
   - 访问 http://localhost:8000/api/health 返回 `{"code":0}`
   - admin 登录后台 → 新建产品 → 上传图集 → 提交成功

## 回滚方案

如发布后出现 P1 故障：

```bash
git checkout v0.1.0
docker compose build --no-cache
docker compose up -d
```

数据库回滚：

```bash
docker compose run --rm backend alembic downgrade <v0.1.0 base revision>
```

> 注意：v0.2.0 仅新增字段、未删除字段，downgrade 不会丢业务数据；但 v0.2.0 期间产生的评论与上传文件会在 downgrade 后无法在 v0.1.0 公开站显示。

## 质量证明

- 测试报告：`outputs/05-test/test-report.md`（87/87 通过）
- 覆盖率：`outputs/05-test/coverage-report.md`（72.3%）
- 发布前检查：`outputs/06-deploy/deploy-check.md`（已修复 HEALTHCHECK）
