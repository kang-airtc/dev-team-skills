# 健康日报（2026-05-10）

> 来源 Skill：`monitor-health`  
> 汇总：容器状态 + 日志巡检 + 数据库备份

## 总体：🟢 正常

## 容器层

| 容器 | 状态 | 内存峰值 | CPU 峰值 |
|---|---|---|---|
| frontend | 🟢 healthy | 178 MiB | 14% |
| backend | 🟢 healthy | 212 MiB | 22% |
| postgres | 🟢 healthy | 124 MiB | 8% |

## 日志层

| 级别 | 计数 | 备注 |
|---|---|---|
| ERROR | 0 | — |
| WARN | 14 | 12 条为 "client disconnected"（前端切页正常），2 条为慢查询提示 |
| INFO | 8.4 万 | 正常业务流量 |

## 备份

- 凌晨 02:00 自动 `pg_dump` 成功
- 文件：`backups/server-20260510.sql.gz`（3.2 MB）
- 保留窗口：7 天，最早 `server-20260504.sql.gz`

## 慢查询 Top 3

| SQL 模板 | 平均耗时 | 次数 |
|---|---|---|
| `SELECT * FROM comments WHERE target_type=? AND target_id=? ORDER BY id DESC` | 86ms | 213 |
| `SELECT * FROM products WHERE is_published=true ORDER BY created_at DESC LIMIT 20` | 41ms | 145 |
| `SELECT COUNT(*) FROM news WHERE published_at <= now()` | 22ms | 86 |

## 建议

- 评论复合索引已生效，但模板查询仍较慢，下个 Sprint 评估增加 `id desc` 覆盖索引
- 慢查询占总流量 < 0.3%，无需告警
