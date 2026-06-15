# 发布前检查报告

## ❌ 阻断项（必须修）
- `backend/Dockerfile`：缺 `HEALTHCHECK`，编排层无法判断容器存活

## ⚠️ 警告项（建议修）
- `docker-compose.yml`：未声明 `mem_limit` 与 `cpus`，单容器爆掉会拖垮宿主机
- `docker-compose.yml`：postgres 镜像 tag 为 `15`（推荐 `15.6` 等具体小版本，防止滚动升级）

## ✅ 通过项
- `.env.example` 已提供
- 端口 3000/8000/5432 在 compose 里都有显式映射
- 所有服务声明了 `restart: unless-stopped`
- frontend 镜像构建已启用多阶段，体积 < 200 MB
- backend 容器以非 root 用户运行

## 修复建议

`backend/Dockerfile` 末尾追加：

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -fsS http://localhost:8000/api/health || exit 1
```

`docker-compose.yml` 给 backend / frontend 加：

```yaml
mem_limit: 512m
cpus: 1.0
```
