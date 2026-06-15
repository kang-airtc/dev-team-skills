# 容器异常诊断（INC-2026-001）

> 来源 Skill：`incident-container`  
> 采集窗口：2026-04-25 14:20 - 14:30

## docker inspect 关键字段

```
{
  "Name": "/company-site-postgres",
  "State": {
    "Status": "exited",
    "Running": false,
    "Paused": false,
    "Restarting": false,
    "OOMKilled": false,
    "Dead": false,
    "Pid": 0,
    "ExitCode": 137,
    "Error": "",
    "StartedAt": "2026-04-25T01:00:00.000Z",
    "FinishedAt": "2026-04-25T06:23:00.000Z"
  }
}
```

## 诊断

- `ExitCode: 137` 通常对应 SIGKILL，结合演练剧本可以确定是人工 `docker stop` 触发
- `OOMKilled: false` 排除内存超限
- `RestartPolicy: unless-stopped` 在演练期未触发，因为 `docker stop` 是用户主动操作

## 同时段其它容器

| 容器 | 状态 |
|---|---|
| frontend | 一直 healthy，但 fetch `/api` 失败 |
| backend | 持续 retry，CPU 飙到 35%（重连风暴） |

## 结论

故障是数据库容器停机，影响范围：backend 完全不可用，frontend 渲染失败。
