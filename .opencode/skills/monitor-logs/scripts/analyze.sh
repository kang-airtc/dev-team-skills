#!/usr/bin/env bash
# monitor-logs: 日志巡检

set -uo pipefail

CONTAINER=""
SINCE="1h"
OUTPUT_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --container|-c)
            CONTAINER="$2"
            shift 2
            ;;
        --since)
            SINCE="$2"
            shift 2
            ;;
        --output|-o)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --help|-h)
            echo "用法: analyze.sh [选项]"
            echo "  --container, -c   指定容器名（默认全部运行中）"
            echo "  --since           时间窗（默认 1h，可选 10m / 24h / 7d）"
            echo "  --output, -o      输出报告路径"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

echo "📋 日志巡检"
echo "====================================="

if ! command -v docker > /dev/null 2>&1; then
    echo "错误: Docker 未安装"
    exit 1
fi

if [[ -n "$CONTAINER" ]]; then
    CONTAINERS="$CONTAINER"
else
    CONTAINERS=$(docker ps --format "{{.Names}}")
fi

count_pattern() {
    # grep -c 在零匹配时返回退出码 1，需吞掉退出码并保证输出为单一数字
    local pattern="$1"
    local logs="$2"
    local n
    n=$(printf '%s\n' "$logs" | grep -ciE "$pattern" 2>/dev/null) || n=0
    echo "${n:-0}"
}

REPORT="# 日志巡检报告"$'\n\n'
REPORT+="**巡检时间**: $(date '+%Y-%m-%d %H:%M')"$'\n'
REPORT+="**时间范围**: 最近 $SINCE"$'\n'
REPORT+="**关键字**: ERROR / WARN / FATAL / Traceback / Exception"$'\n'
REPORT+=$'\n---\n\n'

REPORT+="## 容器关键字统计"$'\n\n'
REPORT+="| 容器 | 总行数 | ERROR | WARN | FATAL | Traceback |"$'\n'
REPORT+="|------|--------|-------|------|-------|-----------|"$'\n'

ERROR_DETAILS=""
TOTAL_ERRORS=0

while IFS= read -r container; do
    [[ -z "$container" ]] && continue

    LOGS=$(docker logs --since "$SINCE" "$container" 2>&1 || true)

    if [[ -z "$LOGS" ]]; then
        REPORT+="| $container | 0 | 0 | 0 | 0 | 0 |"$'\n'
        continue
    fi

    TOTAL=$(printf '%s\n' "$LOGS" | wc -l | tr -d ' ')
    ERRORS=$(count_pattern "error" "$LOGS")
    WARNS=$(count_pattern "warn" "$LOGS")
    FATALS=$(count_pattern "fatal" "$LOGS")
    TRACE=$(count_pattern "traceback|exception" "$LOGS")

    TOTAL_ERRORS=$((TOTAL_ERRORS + ERRORS + FATALS))

    ERR_DISPLAY="$ERRORS"
    [[ "$ERRORS" -gt 10 ]] && ERR_DISPLAY="**$ERRORS** ⚠️"
    TRACE_DISPLAY="$TRACE"
    [[ "$TRACE" -gt 0 ]] && TRACE_DISPLAY="**$TRACE** ⚠️"

    REPORT+="| $container | $TOTAL | $ERR_DISPLAY | $WARNS | $FATALS | $TRACE_DISPLAY |"$'\n'

    if [[ "$ERRORS" -gt 0 || "$FATALS" -gt 0 || "$TRACE" -gt 0 ]]; then
        SECTION="### $container 异常详情"$'\n\n'
        SECTION+="最近 5 条匹配（含 ERROR / FATAL / Traceback / Exception）："$'\n\n'
        SECTION+='```'$'\n'
        # 用 process substitution 避免 while 进入子 shell 导致变量丢失
        SAMPLES=$(printf '%s\n' "$LOGS" | grep -iE "error|fatal|traceback|exception" | tail -5 || true)
        SECTION+="$SAMPLES"$'\n'
        SECTION+='```'$'\n\n'
        ERROR_DETAILS+="$SECTION"
    fi
done <<< "$CONTAINERS"

REPORT+=$'\n'

if [[ -n "$ERROR_DETAILS" ]]; then
    REPORT+="## 异常详情"$'\n\n'
    REPORT+="$ERROR_DETAILS"
    REPORT+="## 建议"$'\n\n'
    REPORT+="- 检查错误频率与时间分布，关注外部依赖、数据库连接、认证模块"$'\n'
    REPORT+="- 高频同类错误（出现次数集中）应优先排查根因"$'\n'
else
    REPORT+="## ✅ 异常详情"$'\n\n'
    REPORT+="未检测到 ERROR / FATAL / Traceback / Exception 级别日志。"$'\n'
fi

if [[ -n "$OUTPUT_FILE" ]]; then
    printf '%s' "$REPORT" > "$OUTPUT_FILE"
    echo "✅ 报告已保存: $OUTPUT_FILE"
    echo "   累计错误数: $TOTAL_ERRORS"
else
    echo ""
    printf '%s' "$REPORT"
fi
