# INC-NOTIF-2026-001：通知邮件 500 根因报告

> 来源 Skill：`incident-log`
> 触发来源：第一篇新闻发布后 `notification` 容器返回 500
> 影响范围：管理员通知邮件未发出，公开站无影响
> 等级：P2（功能局部失效，可走人工兜底）
> 复盘负责人：@ops

## 1. 概要

- 发生时间：2026-04-26 10:42:18 - 10:42:31（持续 13 秒）
- 触发动作：admin 在 `/dashboard/news` 点击"发布"按钮
- 直接现象：`POST /api/news/{id}/publish` 返回 200，但 `notification` 容器同步抛 500，邮件未送达 `editor@company.com`

## 2. 时间线

| 时间 | 事件 | 来源 |
|------|------|------|
| 10:42:18 | admin 发布第一篇新闻 | nginx access log |
| 10:42:18 | backend 调用 notification 内部接口 | backend log |
| 10:42:18 | notification 容器读取 `os.getenv("NOTIFICATION_API_KEY")` 得到 `None` | notification log |
| 10:42:19 | notification 向邮件服务发起鉴权请求，被拒 `401` | notification log |
| 10:42:19 | notification 向 backend 返回 `500 EMAIL_AUTH_FAILED` | backend log |
| 10:42:31 | monitor-logs 聚类抓到 1 条 P1 错误，触发 incident-log | monitor-logs |

## 3. 根因分析

直接原因：`NOTIFICATION_API_KEY` 未在生产环境配置，`os.getenv()` 返回 `None`，邮件服务鉴权失败。

根本原因：`deploy-check` 的 `required_env_vars` 检查列表是手动维护的静态文件，未随功能迭代同步更新；本次 v0.2.0 引入的 notification 模块新增的环境变量没有加入清单。

触发路径：

```
新功能引入 NOTIFICATION_API_KEY
  → 开发环境手动配置本地 .env（未提交）
  → deploy-check 静态列表未更新
  → 生产环境部署时未被拦截
  → 第一次真实调用才暴露
```

## 4. 改进项（行动项）

| 优先级 | 行动项 | 负责人 | 截止 |
|--------|--------|--------|------|
| P1 | 把 `NOTIFICATION_API_KEY` 加入 `deploy-check` 必填环境变量清单 | @ops | 2026-04-27 |
| P1 | 让 `deploy-check` 改为自动扫描 `backend/server/settings.py` 与 `.env.example`，不再手动维护静态清单 | @backend | 2026-05-04 |
| P2 | notification 容器启动时若关键环境变量缺失，直接 fail-fast 不再起服务 | @backend | 2026-05-10 |
| P3 | 给 monitor-logs 加 `EMAIL_AUTH_FAILED` 关键字告警 | @ops | 2026-05-15 |

## 5. 同类事件预防

- 关联到 `deploy-check`：改为"扫描配置文件 → 自动生成清单"后，同类遗漏从根上消除
- 关联到 `release-demo` 演练：发布演练脚本里加上"故意删一个 env"的混沌测试

## 6. 关联产物

- `outputs/06-deploy/deploy-check.md`：未拦住本次缺漏的检查报告
- `outputs/07-monitor/log-inspect.md`：捕获本次 500 的日志聚类
- `incident-report-001.md`：完整版故障复盘（PostgreSQL 演练案例，与本通知独立）
