# Docker / docker compose 命令速查

> 本表覆盖单机 Docker 与 docker-compose 的高频操作；所有命令默认在 `docker-compose.yml` 所在目录执行。

## 1. 生命周期（启停服务）

关键词：启动、停止、重启、销毁、up、down

| 命令 | 场景 |
|------|------|
| `docker compose up -d` | 后台启动全部服务（首次或代码无改动时） |
| `docker compose up -d --build` | 后台启动并强制重新构建镜像 |
| `docker compose stop` | 停止容器但保留状态，可用 `start` 再启 |
| `docker compose restart backend` | 仅重启某个服务（常用于改完配置） |
| `docker compose down` | 停止并删除容器、网络（**保留数据卷**） |
| `docker compose down -v` | 同上，**额外删数据卷**（清空 db 数据时用） |

## 2. 日志查看（排查启动失败、追踪运行错误）

关键词：日志、log、排错、启动失败

| 命令 | 场景 |
|------|------|
| `docker compose logs` | 一次性打印全部服务最近的日志 |
| `docker compose logs -f` | 持续跟随全部服务日志（Ctrl+C 退出） |
| `docker compose logs -f --tail=100 backend` | 只跟随 backend 服务最近 100 行（最常用） |
| `docker compose logs --since 10m backend` | 只看最近 10 分钟的 backend 日志 |
| `docker logs <container_id>` | 直接按容器 ID 看（compose 之外的容器） |

## 3. 进入容器（临时调试、查文件、跑命令）

关键词：进容器、exec、shell、bash、调试

| 命令 | 场景 |
|------|------|
| `docker compose exec backend bash` | 进入 backend 容器交互 shell（Debian/Ubuntu 镜像） |
| `docker compose exec backend sh` | 同上，alpine 等无 bash 镜像用 sh |
| `docker compose exec backend python` | 直接进 Python REPL |
| `docker compose exec db psql -U demo -d demo` | 进 PostgreSQL 客户端 |
| `docker compose run --rm backend pytest` | 临时跑一次性命令（用完就清） |

## 4. 镜像管理（列出、删除、拉取）

关键词：镜像、image、pull、rmi

| 命令 | 场景 |
|------|------|
| `docker images` | 列出本机所有镜像 |
| `docker images \| grep backend` | 按关键字筛选镜像 |
| `docker rmi <image_id>` | 删除指定镜像（容器引用时需先删容器） |
| `docker image prune -f` | 删除所有 dangling（无 tag 引用）镜像 |
| `docker pull postgres:15-alpine` | 显式拉取镜像（CI 预热缓存常用） |
| `docker tag local:dev registry/foo:v1.2.0` | 给镜像打远程仓库 tag |
| `docker push registry/foo:v1.2.0` | 推送镜像到镜像仓库 |

## 5. 资源清理（释放磁盘）

关键词：清理、磁盘、瘦身、prune

| 命令 | 场景 |
|------|------|
| `docker system df` | 查看 Docker 占用的磁盘空间分项 |
| `docker system prune -f` | 一键清理停止的容器 + 无引用镜像 + 无引用网络 |
| `docker system prune -a -f` | 同上，**还会删未被任何容器引用的镜像**（更狠） |
| `docker volume prune -f` | 清理无引用的数据卷（**警惕：误删会丢数据**） |
| `docker builder prune -f` | 清理 buildx/buildkit 构建缓存 |

> 注意：`-a -f` 与 `volume prune` 在共享开发机上慎用，可能误删别人的镜像或卷。

## 6. 状态诊断（看谁在跑、占多少资源）

关键词：状态、ps、stats、资源、占用

| 命令 | 场景 |
|------|------|
| `docker compose ps` | 列出本 compose 工程所有容器及状态 |
| `docker ps` | 列出本机所有运行中的容器 |
| `docker ps -a` | 同上，连已停止的也列出 |
| `docker stats` | 实时查看所有容器 CPU / 内存 / 网络 / IO |
| `docker stats --no-stream backend` | 只看 backend 单次快照 |
| `docker compose top` | 看每个容器内的进程列表 |
| `docker inspect <container>` | 看容器完整配置（IP、挂载、环境变量等 JSON） |

## 7. 网络与端口（少用但偶尔需要）

关键词：网络、network、端口、port

| 命令 | 场景 |
|------|------|
| `docker network ls` | 列出 Docker 网络 |
| `docker port <container>` | 查看容器端口映射 |
| `docker compose port backend 8000` | 查看 compose 服务的端口映射 |

---

**小贴士：**

- `docker compose`（中间空格）是 V2 内置子命令；旧版独立可执行的 `docker-compose`（中划线）仍然可用，命令参数基本一致。
- 容器名带前缀（默认是工程目录名）。`docker compose exec backend bash` 自动按服务名匹配，比直接 `docker exec <container_name> bash` 友好。
- 排查启动失败的标准三连：`docker compose ps` → `docker compose logs --tail=200 <服务>` → `docker compose exec <服务> sh`。
