# 第 10 章示例：监控与巡检

本目录为书稿第 10 章说明：可执行脚本在 **.opencode/skills/monitor-***；运行对象与第 9 章相同，使用 **examples/chapter-09/release-demo/**（PostgreSQL + FastAPI + nginx 静态前端）。

**路径**相对于 **dev-team-skills** 仓库根目录。

**inputs/intent-monitor-*.md** 与书稿各小节**自然语言意图示例**一致；**output/** 下报告与备份由命令**本地生成**，请自建 **examples/chapter-10/output**（或自定目录）。

## 前置条件

1. 已安装 Docker，可使用 **docker compose** 或 **docker-compose**。
2. 已按 **examples/chapter-09/README.md** 初始化并启动 **release-demo**。
3. 用 **docker ps** 确认容器名；目录名为 **release-demo** 时常见 **release-demo-db-1**、**release-demo-backend-1**、**release-demo-frontend-1**。

## 分步命令

`--name-filter release-demo` 用于在多 docker 项目共存时只采样 release-demo 栈；
无此前缀时脚本会列出本机所有运行中的容器。

```bash
mkdir -p examples/chapter-10/output

bash .opencode/skills/monitor-containers/scripts/check.sh \
  --filter release-demo \
  --output examples/chapter-10/output/container-status.md

bash .opencode/skills/monitor-logs/scripts/analyze.sh \
  --since 1h \
  --output examples/chapter-10/output/log-analysis.md

bash .opencode/skills/monitor-backup/scripts/backup.sh \
  --container release-demo-db-1 \
  --database demo \
  --user demo \
  --output examples/chapter-10/output/backups

python3 .opencode/skills/monitor-health/scripts/report.py \
  --name-filter release-demo \
  --backup-dir examples/chapter-10/output/backups \
  --output examples/chapter-10/output/health-report.md
```

## 一键巡检：monitor-pipeline

```bash
bash .opencode/skills/monitor-pipeline/scripts/run-all.sh \
  --output examples/chapter-10/output/pipeline-run \
  --db-container release-demo-db-1 \
  --db-name demo \
  --db-user demo \
  --name-filter release-demo
```

## 与书稿用语对照

| 书稿旧称 | 配套 monitor-* |
|---------|----------------|
| container-monitor | monitor-containers |
| log-inspector | monitor-logs |
| db-backup | monitor-backup |
| health-report | monitor-health |
| ops-monitor | monitor-pipeline |

**metric-alert** 无独立 Skill，见第 10 章正文扩展说明。
