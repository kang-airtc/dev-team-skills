# 容器故障诊断报告

**容器**: release-demo-backend-1
**诊断时间**: 2026-05-04 08:36

---

## 容器状态

- **状态**: running
- **退出码**: 0

## 资源限制

- **内存限制**: 无限制

## 环境变量

```
DATABASE_URL=postgresql://demo:demo_dev@localhost:5433/demo
SECRET_KEY=dev-secret-change-me
NEXT_PUBLIC_API_URL=http://localhost:8000
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=C.UTF-8
GPG_KEY=A035C8C19219BA821ECEA86B64E628F8D684696D
PYTHON_VERSION=3.11.15
PYTHON_SHA256=272179ddd9a2e41a0fc8e42e33dfbdca0b3711aa5abf372d3f2d51543d09b625```

## 最近日志

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [1]
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 根因分析

⚠️ 退出码: 0

**建议**: 查看完整日志排查问题

