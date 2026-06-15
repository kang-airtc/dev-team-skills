# INC-2026-001：PostgreSQL 中断导致后台 API 短时不可用

## 1. 概要
- 影响：后台 API 完全不可用，公开站 /products 列表与详情 5xx
- 时长：5 分钟（14:23 - 14:28）
- 等级：P1（业务受损但 < 30 分钟）
- 责任服务：company-site-postgres

## 2. 时间线
| 时间 | 事件 | 来源 |
|------|------|------|
| 14:23:00 | PG 容器停止 | 人工演练（docker stop） |
| 14:23:02 | backend 开始报 1301 | monitor-logs |
| 14:23:15 | 前端 /products 502 | monitor-logs |
| 14:25:00 | 自动重连机制持续重试 | backend 日志 |
| 14:28:00 | PG 容器恢复 | 人工演练（docker start） |
| 14:28:03 | backend 错误停止 | monitor-logs |

## 3. 根因
- 直接原因：PostgreSQL 容器被停
- 深层原因：教学演练，无生产意义；但暴露出 backend 缺乏熔断与降级机制——
  数据库不可用时仍持续重试，导致前台请求挂起 5 秒后才返回 502，体验差

## 4. 改进项（行动项）
| 优先级 | 行动项 | 负责人 | 截止 |
|--------|--------|--------|------|
| P1 | backend 加 PG 连接熔断（连续失败 3 次直接 fail-fast） | @backend | 2026-05-03 |
| P2 | 前端 /products 加骨架屏与"暂时不可用"占位 | @frontend | 2026-05-10 |
| P3 | 给 monitor-logs 加 P1 告警自动触发 incident-pipeline 的钩子 | @ops | 2026-05-15 |

## 5. 同类事件预防
- 关联到 deploy-check Skill：发布前确保 postgres 资源限制与 health check 已配置
- 关联到 monitor-backup Skill：演练期间最近一次备份是 14:00，未受影响

## 6. 关联产物

- `incident-container.md`：容器层诊断
- `incident-log-rca.md`：日志层根因分析
- `outputs/07-monitor/log-inspect.md`：触发本次复盘的告警来源

## 7. 复盘参与人

- backend-dev / frontend-dev / ops / PM 共 4 人，复盘会议 30 分钟

## 8. 状态

- 行动项 P1 已于 2026-04-30 落地（commit a2c4...）
- 行动项 P2 已于 2026-05-08 落地
- 行动项 P3 已于 2026-05-12 落地
- 本事件归档
