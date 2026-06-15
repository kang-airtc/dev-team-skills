# 日志根因分析（INC-2026-001）

> 来源 Skill：`incident-log`  
> 窗口：2026-04-25 14:20 - 14:30  
> 输入：`docker logs company-site-backend` + `docker logs company-site-postgres`

## 异常聚类

| 聚类标签 | 模板 | 次数 |
|---|---|---|
| C1 | `[ERROR] 1301 DATABASE_CONNECTION_ERROR connection refused` | 47 |
| C2 | `[ERROR] Bad Gateway 502 upstream timeout` | 12 |
| C3 | `[WARN] retry backoff 1s/2s/4s/...` | 89 |

## 时间序列

```
14:23:00  postgres: container stopped (人工)
14:23:02  backend: C1 第 1 次
14:23:02  backend: C3 retry 开始
14:23:15  backend: C2 502 第 1 次（连接耗尽影响前端）
14:25:00  backend: 重试间隔达上限 30s
14:28:00  postgres: container started
14:28:03  backend: connection pool restored
14:28:04  backend: C1 / C2 / C3 全部停止
```

## 根因候选

| 候选 | 证据 | 评分 |
|---|---|---|
| ① 数据库容器宕机 | postgres 容器 14:23 stop / 14:28 start | 高 |
| ② 网络中断 | 同 host 内其它容器互通正常 | 低 |
| ③ 应用 Bug | backend 重启数据库恢复后立即恢复 | 低 |

## 选择

候选 ①，与 `incident-container` 诊断一致。

## 旁观察

- backend 在数据库不可用期间持续 retry，没有熔断或降级，进一步拖累 frontend 体验
- 这是除直接根因之外的"二级根因"，应作为改进项
