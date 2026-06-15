#!/usr/bin/env bash
# monitor-pipeline: 一键巡检流水线
# 设计：子步骤失败不阻断整体；记录每步状态；最后写 0-summary.md。

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

OUTPUT_DIR="./monitor-output"
DB_CONTAINER=""
DB_NAME=""
DB_USER=""
NAME_FILTER=""
SINCE="1h"

while [[ $# -gt 0 ]]; do
    case $1 in
        --output|-o)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --db-container)
            DB_CONTAINER="$2"
            shift 2
            ;;
        --db-name)
            DB_NAME="$2"
            shift 2
            ;;
        --db-user)
            DB_USER="$2"
            shift 2
            ;;
        --name-filter)
            NAME_FILTER="$2"
            shift 2
            ;;
        --since)
            SINCE="$2"
            shift 2
            ;;
        --help|-h)
            echo "用法: run-all.sh [选项]"
            echo "  --output, -o      产物目录（默认 ./monitor-output）"
            echo "  --db-container    PostgreSQL 容器名（缺省时跳过备份）"
            echo "  --db-name         数据库名"
            echo "  --db-user         数据库用户"
            echo "  --name-filter     容器名前缀过滤（默认无）"
            echo "  --since           日志时间窗（默认 1h）"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

echo "🔍 启动系统巡检流水线"
echo "====================================="

mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/backups"

START_TS=$(date +%s)

# 状态变量
STEP_CONTAINERS="✅"
STEP_LOGS="✅"
STEP_BACKUP="-"
STEP_HEALTH="✅"

CONTAINER_FILTER_ARGS=()
[[ -n "$NAME_FILTER" ]] && CONTAINER_FILTER_ARGS=(--filter "$NAME_FILTER")

# Step 1: 容器状态
echo "📦 Step 1/4: 容器状态检查..."
if ! bash "$SKILLS_DIR/monitor-containers/scripts/check.sh" \
        "${CONTAINER_FILTER_ARGS[@]}" \
        --output "$OUTPUT_DIR/1-container-status.md"; then
    STEP_CONTAINERS="❌"
fi
echo ""

# Step 2: 日志巡检
echo "📋 Step 2/4: 日志巡检..."
if ! bash "$SKILLS_DIR/monitor-logs/scripts/analyze.sh" \
        --since "$SINCE" \
        --output "$OUTPUT_DIR/2-log-analysis.md"; then
    STEP_LOGS="❌"
fi
echo ""

# Step 3: 数据库备份（可选）
echo "💾 Step 3/4: 数据库备份..."
if [[ -n "$DB_CONTAINER" ]] && docker ps --format "{{.Names}}" | grep -q "^${DB_CONTAINER}$"; then
    if bash "$SKILLS_DIR/monitor-backup/scripts/backup.sh" \
            --container "$DB_CONTAINER" \
            --database "$DB_NAME" \
            --user "$DB_USER" \
            --output "$OUTPUT_DIR/backups" \
            --report-path "$OUTPUT_DIR/3-backup-report.md"; then
        STEP_BACKUP="✅"
    else
        STEP_BACKUP="❌"
    fi
    # 清理 backups/ 下的重复报告，pipeline 模式下使用顶层 3-backup-report.md
    rm -f "$OUTPUT_DIR/backups/backup-report.md"
else
    echo "⚠️ 跳过备份：未提供 --db-container 或容器未运行"
    STEP_BACKUP="跳过"
    cat > "$OUTPUT_DIR/3-backup-report.md" <<EOF
# 数据库备份报告

**状态**: ⚠️ 已跳过

未提供 \`--db-container\` 或目标容器未运行，本次未执行备份。
EOF
fi
echo ""

# Step 4: 健康报告
echo "🏥 Step 4/4: 生成健康报告..."
HEALTH_ARGS=(--output "$OUTPUT_DIR/4-health-report.md" --since "$SINCE" --backup-dir "$OUTPUT_DIR/backups")
[[ -n "$NAME_FILTER" ]] && HEALTH_ARGS+=(--name-filter "$NAME_FILTER")
if ! python3 "$SKILLS_DIR/monitor-health/scripts/report.py" "${HEALTH_ARGS[@]}"; then
    STEP_HEALTH="❌"
fi
echo ""

END_TS=$(date +%s)
DURATION=$((END_TS - START_TS))
DURATION_MIN=$((DURATION / 60))
DURATION_SEC=$((DURATION % 60))

# 解析健康分（从 4-health-report.md 抽 "X / 100"）
HEALTH_SCORE="-"
HEALTH_ICON="🟡"
HEALTH_LABEL="-"
if [[ -f "$OUTPUT_DIR/4-health-report.md" ]]; then
    LINE=$(grep -E "^## 综合健康分" "$OUTPUT_DIR/4-health-report.md" | head -1 || true)
    if [[ -n "$LINE" ]]; then
        HEALTH_ICON=$(echo "$LINE" | grep -oE "🟢|🟡|🔴" | head -1 || echo "🟡")
        HEALTH_SCORE=$(echo "$LINE" | grep -oE "[0-9]+ / 100" | head -1 || echo "-")
        HEALTH_LABEL=$(echo "$LINE" | grep -oE "（[^）]+）" | head -1 | tr -d '（）' || echo "-")
    fi
fi

# 提取异常关键提示（从子报告里抽 "⚠️" 行）
KEY_FINDINGS=""
for f in "$OUTPUT_DIR/1-container-status.md" "$OUTPUT_DIR/2-log-analysis.md" "$OUTPUT_DIR/4-health-report.md"; do
    [[ -f "$f" ]] || continue
    while IFS= read -r line; do
        # 只取以 - 开头并含 ⚠️ 或 ❌ 的列表项
        if [[ "$line" =~ ^-.*(⚠️|❌) ]]; then
            KEY_FINDINGS+="$line"$'\n'
        fi
    done < "$f"
done

# 写 0-summary.md
SUMMARY="# 巡检综合报告"$'\n\n'
SUMMARY+="**时间**: $(date '+%Y-%m-%d %H:%M:%S')"$'\n'
SUMMARY+="**总耗时**: ${DURATION_MIN} 分 ${DURATION_SEC} 秒"$'\n\n'
SUMMARY+="---"$'\n\n'
SUMMARY+="## 综合状态: ${HEALTH_ICON} 健康分 ${HEALTH_SCORE}（${HEALTH_LABEL}）"$'\n\n'
SUMMARY+="| 检查 | 状态 | 子报告 |"$'\n'
SUMMARY+="|---|---|---|"$'\n'
SUMMARY+="| 容器状态 | ${STEP_CONTAINERS} | [→](1-container-status.md) |"$'\n'
SUMMARY+="| 日志（${SINCE}） | ${STEP_LOGS} | [→](2-log-analysis.md) |"$'\n'
SUMMARY+="| 数据库备份 | ${STEP_BACKUP} | [→](3-backup-report.md) |"$'\n'
SUMMARY+="| 综合健康 | ${STEP_HEALTH} | [→](4-health-report.md) |"$'\n'
SUMMARY+=$'\n---\n\n'

if [[ -n "$KEY_FINDINGS" ]]; then
    SUMMARY+="## 关键提示"$'\n\n'
    SUMMARY+="$KEY_FINDINGS"
    SUMMARY+=$'\n'
else
    SUMMARY+="## 关键提示"$'\n\n'
    SUMMARY+="- 本次巡检未发现异常项"$'\n\n'
fi

SUMMARY+="---"$'\n\n'
SUMMARY+="## 推送到 IM"$'\n\n'
SUMMARY+='建议把汇总精简成一行推 IM：'$'\n\n'
SUMMARY+='```'$'\n'
SUMMARY+="[巡检] $(date '+%Y-%m-%d %H:%M') 健康分 ${HEALTH_SCORE}"$'\n'
if [[ -n "$KEY_FINDINGS" ]]; then
    SUMMARY+="⚠️ 存在异常项，详见完整报告"$'\n'
else
    SUMMARY+="✅ 无异常"$'\n'
fi
SUMMARY+='```'$'\n\n'

SUMMARY+="如系统持续异常，参考下一章 incident-* Skill 做深度排查。"$'\n'

printf '%s' "$SUMMARY" > "$OUTPUT_DIR/0-summary.md"

echo "====================================="
echo "✅ 巡检完成（耗时 ${DURATION}s）"
echo "====================================="
echo ""
echo "产物: $OUTPUT_DIR/"
ls -1 "$OUTPUT_DIR" | sed 's/^/  /'
