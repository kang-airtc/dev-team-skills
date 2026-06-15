# 08-incident · 故障排查产出物

| 文件 | 来源 Skill | 说明 |
|------|-----------|------|
| `incident-container.md` | `incident-container` | 容器异常诊断 |
| `incident-log-rca.md` | `incident-log` | 日志根因分析 |
| `incident-report-001.md` | `incident-report` | 复盘报告（时间线 + 根因 + 改进项） |

## 故障演练剧本

1. `docker stop company-site-postgres` 模拟数据库宕机 5 分钟
2. 后端日志开始飙 `1301 DATABASE_CONNECTION_ERROR`
3. 前端 `/products` 列表空、详情 500
4. 跑 `incident-pipeline` → 一份完整的复盘报告
