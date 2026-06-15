#!/usr/bin/env bash
# monitor-backup: PostgreSQL 数据库备份

set -uo pipefail

CONTAINER="blog-db"
DATABASE="blog"
DB_USER="postgres"
OUTPUT_DIR="./backups"
REPORT_PATH=""
MIN_SIZE=256

while [[ $# -gt 0 ]]; do
    case $1 in
        --container|-c)
            CONTAINER="$2"
            shift 2
            ;;
        --database|-d)
            DATABASE="$2"
            shift 2
            ;;
        --user|-u)
            DB_USER="$2"
            shift 2
            ;;
        --output|-o)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --report-path)
            REPORT_PATH="$2"
            shift 2
            ;;
        --min-size)
            MIN_SIZE="$2"
            shift 2
            ;;
        --help|-h)
            echo "用法: backup.sh [选项]"
            echo "  --container, -c   PostgreSQL 容器名"
            echo "  --database, -d    数据库名"
            echo "  --user, -u        数据库用户"
            echo "  --output, -o      备份目录（生成 *.sql 与 backup-report.md）"
            echo "  --report-path     额外把报告复制到该路径（供编排器汇总）"
            echo "  --min-size        最小可信字节数（默认 256，空 demo 库约 600B；生产可设 1048576）"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

echo "💾 数据库备份"
echo "====================================="
echo "容器: $CONTAINER"
echo "数据库: $DATABASE"
echo "用户: $DB_USER"

if ! docker ps --format "{{.Names}}" | grep -q "^${CONTAINER}$"; then
    echo "❌ 错误: 容器 $CONTAINER 未运行"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_FILE="${DATABASE}_${TIMESTAMP}.sql"
BACKUP_PATH="$OUTPUT_DIR/$BACKUP_FILE"

echo "备份文件: $BACKUP_PATH"

START_TS=$(date +%s)
if ! docker exec "$CONTAINER" pg_dump -U "$DB_USER" "$DATABASE" > "$BACKUP_PATH" 2> /tmp/.monitor-backup.err; then
    echo "❌ pg_dump 执行失败:"
    cat /tmp/.monitor-backup.err
    exit 1
fi
END_TS=$(date +%s)
DURATION=$((END_TS - START_TS))

# 三要素校验：退出码已通过；下面校验大小与内容
SIZE_BYTES=$(wc -c < "$BACKUP_PATH" | tr -d ' ')
SIZE_HUMAN=$(du -h "$BACKUP_PATH" | cut -f1)

VALID_SIZE=0
[[ "$SIZE_BYTES" -gt "$MIN_SIZE" ]] && VALID_SIZE=1

VALID_CONTENT=0
if grep -qE "PostgreSQL database dump|COPY |CREATE |INSERT " "$BACKUP_PATH" 2>/dev/null; then
    VALID_CONTENT=1
fi

REPORT="# 数据库备份报告"$'\n\n'
REPORT+="**备份时间**: $(date '+%Y-%m-%d %H:%M:%S')"$'\n'
REPORT+="**容器**: $CONTAINER"$'\n'
REPORT+="**数据库**: $DATABASE"$'\n'
REPORT+="**用户**: $DB_USER"$'\n\n'
REPORT+="---"$'\n\n'

if [[ $VALID_SIZE -eq 1 && $VALID_CONTENT -eq 1 ]]; then
    REPORT+="## 结果"$'\n\n'
    REPORT+="✅ 备份成功"$'\n\n'
    STATUS="success"
else
    REPORT+="## 结果"$'\n\n'
    REPORT+="❌ 备份失败（校验未通过）"$'\n\n'
    STATUS="failed"
fi

REPORT+="## 详情"$'\n\n'
REPORT+="- **备份文件**: $BACKUP_FILE"$'\n'
REPORT+="- **文件大小**: ${SIZE_HUMAN}（${SIZE_BYTES} 字节）"$'\n'
REPORT+="- **耗时**: ${DURATION} 秒"$'\n\n'

REPORT+="## 校验"$'\n\n'
REPORT+="- ✅ pg_dump 退出码 = 0"$'\n'
if [[ $VALID_SIZE -eq 1 ]]; then
    REPORT+="- ✅ 文件大小 > ${MIN_SIZE} 字节（${SIZE_HUMAN}）"$'\n'
else
    REPORT+="- ❌ 文件大小 ≤ ${MIN_SIZE} 字节（${SIZE_HUMAN}）"$'\n'
fi
if [[ $VALID_CONTENT -eq 1 ]]; then
    REPORT+="- ✅ 文件包含 SQL 头（COPY/CREATE/INSERT 关键字存在）"$'\n'
else
    REPORT+="- ❌ 文件未包含预期 SQL 头关键字"$'\n'
fi
REPORT+=$'\n'

# 历史对照（同目录最近 7 份同库备份）
HIST=$(ls -1t "$OUTPUT_DIR"/${DATABASE}_*.sql 2>/dev/null | head -7)
if [[ -n "$HIST" ]]; then
    REPORT+="## 历史对照"$'\n\n'
    REPORT+="同目录最近 7 份备份："$'\n\n'
    REPORT+="| 文件 | 大小 |"$'\n'
    REPORT+="|------|------|"$'\n'
    while IFS= read -r f; do
        [[ -z "$f" ]] && continue
        bn=$(basename "$f")
        sz=$(du -h "$f" | cut -f1)
        REPORT+="| $bn | $sz |"$'\n'
    done <<< "$HIST"
    REPORT+=$'\n'
fi

DEFAULT_REPORT="$OUTPUT_DIR/backup-report.md"
printf '%s' "$REPORT" > "$DEFAULT_REPORT"
echo "   报告: $DEFAULT_REPORT"

if [[ -n "$REPORT_PATH" ]]; then
    mkdir -p "$(dirname "$REPORT_PATH")"
    printf '%s' "$REPORT" > "$REPORT_PATH"
    echo "   报告（额外）: $REPORT_PATH"
fi

if [[ "$STATUS" == "success" ]]; then
    echo "✅ 备份成功（$SIZE_HUMAN, ${DURATION}s）"
    exit 0
else
    echo "❌ 备份校验未通过"
    exit 2
fi
