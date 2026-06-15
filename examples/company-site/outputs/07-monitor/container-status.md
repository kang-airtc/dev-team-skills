# 容器状态快照

> 来源 Skill：`monitor-containers`  
> 采集时间：2026-05-10 14:00:00 UTC+8  
> 命令：`docker ps --format` + `docker stats --no-stream`

## 容器列表

| 容器 | 镜像 | 状态 | 重启次数 | CPU | 内存 | 端口 |
|---|---|---|---|---|---|---|
| company-site-frontend | company-site/frontend:0.2.0 | Up 13h | 0 | 1.2% | 156 MiB / 512 MiB | 3000 |
| company-site-backend | company-site/backend:0.2.0 | Up 13h (healthy) | 0 | 3.8% | 184 MiB / 512 MiB | 8000 |
| company-site-postgres | postgres:15.6 | Up 13h (healthy) | 0 | 0.6% | 96 MiB / 256 MiB | 5432 |

## 卷使用

| 卷 | 挂载点 | 容量 | 使用率 |
|---|---|---|---|
| company-site_pgdata | /var/lib/postgresql/data | 1 GiB | 12% |
| 宿主机 ./uploads | /uploads | 5 GiB | 3% |

## 结论

全部容器运行正常，HEALTHCHECK 通过，资源消耗远低于上限。无需告警。
