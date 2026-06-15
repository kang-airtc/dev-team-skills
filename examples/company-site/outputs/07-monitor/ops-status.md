# monitor-pipeline 编排状态

> 来源 Skill：`monitor-pipeline`  
> 当前周期：2026-05-10

## 节奏

| 频率 | 子任务 | 最近运行 | 结果 |
|---|---|---|---|
| 每小时 | `monitor-containers` | 14:00 | ✅ |
| 每小时 | `monitor-logs --since 1h` | 14:00 | ✅ |
| 每天 02:00 | `monitor-backup` | 02:00 | ✅ |
| 每天 08:00 | `monitor-health` | 08:00 | ✅ |
| 每周一 09:00 | `monitor-pipeline --report weekly` | 上周一 | ✅ |

## 上次中断恢复

最近 30 天发生过 1 次自动恢复：

- 2026-04-25 14:23 数据库窗口故障 5 分钟，`monitor-logs` 捕获后自动触发 `incident-pipeline`，产物落 `outputs/08-incident/`
- 见 `incident-report-001.md`

## 编排健康度

- 子任务连续运行 30 天无失败
- 子任务执行时长稳定（5s ~ 12s）
- 日志输出未发现编排器自身异常
