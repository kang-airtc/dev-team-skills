---
name: monitor-backup
description: 执行 PostgreSQL 数据库备份，生成带时间戳的备份文件，输出备份报告
---

# Monitor Backup - 数据库备份

执行 PostgreSQL 数据库备份（pg_dump），生成带时间戳的 SQL 文件，记录备份信息。

## 触发场景

- 定期数据库备份
- 发布前备份
- 数据迁移前备份
- 灾难恢复准备

## 目录结构

```
monitor-backup/
├── SKILL.md
├── scripts/
│   └── backup.sh
└── assets/
    └── backup-retention.md
```

## 依赖

- `docker`
- PostgreSQL 容器运行中

## 使用方法

```bash
# 备份 blog-db 容器的数据库
bash .opencode/skills/monitor-backup/scripts/backup.sh \
  --container blog-db \
  --database blog

# 指定备份目录
bash .opencode/skills/monitor-backup/scripts/backup.sh \
  --container blog-db \
  --database blog \
  --output /backups/
```

参数：
- `--container, -c`：PostgreSQL 容器名，默认 `blog-db`
- `--database, -d`：数据库名，默认 `blog`
- `--user, -u`：数据库角色（`pg_dump -U`），默认 `postgres`（`release-demo` 小例请用 `demo`）
- `--output, -o`：备份目录，默认 `./backups`
- `--report-path`：除默认 `${output}/backup-report.md` 外额外把报告复制到该路径（供 monitor-pipeline 汇总）
- `--min-size`：最小可信字节数，默认 `256`；空 demo 库约 600 字节，生产可设 `1048576`（1MB）

成功条件：pg_dump 退出码 = 0、文件大小 > min-size、文件包含 SQL 头关键字。任一失败即返回非零退出码。

## 输出

```
backups/
├── blog_20240115_143000.sql
└── backup-report.md
```

## 备份报告

```markdown
# 数据库备份报告

**备份时间**: 2024-01-15 14:30
**数据库**: blog
**容器**: blog-db
**备份文件**: blog_20240115_143000.sql
**文件大小**: 15.2MB
**状态**: ✅ 成功
```

## 边界

- 只支持 PostgreSQL（通过 docker exec pg_dump）
- 备份时数据库会短暂加锁
- 大表备份可能较慢
- 不自动清理旧备份

## 与其他 Skill 的关系

```
monitor-backup ──▶ monitor-pipeline
  数据库备份       巡检流水线
```
