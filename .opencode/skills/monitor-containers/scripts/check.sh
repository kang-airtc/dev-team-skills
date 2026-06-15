#!/usr/bin/env bash
# monitor-containers: 容器状态监控

set -uo pipefail

OUTPUT_FILE=""
INCLUDE_ALL=0
NAME_FILTER=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --output|-o)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --all|-a)
            INCLUDE_ALL=1
            shift
            ;;
        --filter|-f)
            NAME_FILTER="$2"
            shift 2
            ;;
        --help|-h)
            echo "用法: check.sh [选项]"
            echo "  --output, -o   输出报告路径"
            echo "  --all, -a      包含已退出容器（默认仅展示运行中）"
            echo "  --filter, -f   按容器名前缀过滤（例如 release-demo）"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

echo "🔍 容器状态监控"
echo "====================================="

if ! command -v docker > /dev/null 2>&1; then
    echo "错误: Docker 未安装"
    exit 1
fi

PS_ARGS=()
[[ $INCLUDE_ALL -eq 1 ]] && PS_ARGS+=(-a)
[[ -n "$NAME_FILTER" ]] && PS_ARGS+=(--filter "name=$NAME_FILTER")

CONTAINERS=$(docker ps "${PS_ARGS[@]}" --format "{{.Names}}|{{.Image}}|{{.Status}}|{{.State}}" 2>&1 || true)

REPORT="# 容器状态巡检报告"$'\n\n'
REPORT+="**巡检时间**: $(date '+%Y-%m-%d %H:%M')"$'\n'
[[ -n "$NAME_FILTER" ]] && REPORT+="**过滤前缀**: $NAME_FILTER"$'\n'
REPORT+=$'\n---\n\n'

if [[ -z "$CONTAINERS" ]]; then
    REPORT+="未发现符合条件的容器。"$'\n'
    if [[ -n "$OUTPUT_FILE" ]]; then
        printf '%s' "$REPORT" > "$OUTPUT_FILE"
        echo "✅ 报告已保存: $OUTPUT_FILE"
    else
        printf '%s' "$REPORT"
    fi
    exit 0
fi

REPORT+="## 状态概览"$'\n\n'
REPORT+="| 容器 | 镜像 | 状态 | Health | 重启 | CPU | Mem |"$'\n'
REPORT+="|---|---|---|---|---|---|---|"$'\n'

ABNORMAL=""
WARNING_LINES=""
RUNNING_COUNT=0
TOTAL_COUNT=0
TOTAL_RESTARTS=0

while IFS='|' read -r name image status state; do
    [[ -z "$name" ]] && continue
    TOTAL_COUNT=$((TOTAL_COUNT + 1))

    HEALTH=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}-{{end}}' "$name" 2>/dev/null || echo "-")
    RESTART=$(docker inspect --format='{{.RestartCount}}' "$name" 2>/dev/null || echo "0")
    EXIT_CODE=$(docker inspect --format='{{.State.ExitCode}}' "$name" 2>/dev/null || echo "-")

    if [[ "$state" == "running" ]]; then
        RUNNING_COUNT=$((RUNNING_COUNT + 1))
        STATS=$(docker stats --no-stream --format "{{.CPUPerc}}|{{.MemPerc}}" "$name" 2>/dev/null || echo "-|-")
        CPU=${STATS%%|*}
        MEM=${STATS##*|}
        STATE_ICON="✅ running"
    else
        CPU="-"
        MEM="-"
        STATE_ICON="❌ $state"
    fi

    TOTAL_RESTARTS=$((TOTAL_RESTARTS + RESTART))

    RESTART_DISPLAY="$RESTART"
    [[ "$RESTART" -gt 0 ]] && RESTART_DISPLAY="**$RESTART** ⚠️"

    HEALTH_DISPLAY="$HEALTH"
    case "$HEALTH" in
        unhealthy) HEALTH_DISPLAY="**unhealthy** ⚠️" ;;
        healthy) HEALTH_DISPLAY="healthy" ;;
        starting) HEALTH_DISPLAY="starting" ;;
    esac

    ROW="| $name | $image | $STATE_ICON | $HEALTH_DISPLAY | $RESTART_DISPLAY | $CPU | $MEM |"$'\n'
    REPORT+="$ROW"

    if [[ "$state" != "running" ]]; then
        ABNORMAL+="- \`$name\` 状态 = $state（exit code = $EXIT_CODE）"$'\n'
    elif [[ "$HEALTH" == "unhealthy" ]]; then
        WARNING_LINES+="- \`$name\` healthcheck = unhealthy"$'\n'
    elif [[ "$RESTART" -gt 0 ]]; then
        WARNING_LINES+="- \`$name\` 重启次数 = $RESTART（请用 docker logs 查看原因）"$'\n'
    fi
done <<< "$CONTAINERS"

REPORT+=$'\n'

REPORT+="## 异常项"$'\n\n'
if [[ -n "$ABNORMAL" ]]; then
    REPORT+="$ABNORMAL"
elif [[ -n "$WARNING_LINES" ]]; then
    REPORT+="$WARNING_LINES"
else
    REPORT+="- 无异常容器"$'\n'
fi
REPORT+=$'\n'

REPORT+="## 通过项"$'\n\n'
[[ $RUNNING_COUNT -eq $TOTAL_COUNT ]] && REPORT+="- ✅ 所有容器都在运行"$'\n'
[[ $TOTAL_RESTARTS -eq 0 ]] && REPORT+="- ✅ 24h 内无容器重启"$'\n'
REPORT+=$'\n'

REPORT+="## 统计"$'\n\n'
REPORT+="- **总容器数**: $TOTAL_COUNT"$'\n'
REPORT+="- **运行中**: $RUNNING_COUNT"$'\n'
REPORT+="- **异常**: $((TOTAL_COUNT - RUNNING_COUNT))"$'\n'
REPORT+="- **累计重启**: $TOTAL_RESTARTS"$'\n'

if [[ -n "$OUTPUT_FILE" ]]; then
    printf '%s' "$REPORT" > "$OUTPUT_FILE"
    echo "✅ 报告已保存: $OUTPUT_FILE"
else
    echo ""
    printf '%s' "$REPORT"
fi
