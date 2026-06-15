#!/usr/bin/env bash
# incident-container: 容器故障诊断

set -uo pipefail

CONTAINER=""
LAST_MODE=false
OUTPUT_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --container|-c)
            CONTAINER="$2"
            shift 2
            ;;
        --last)
            LAST_MODE=true
            shift
            ;;
        --output|-o)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 确定诊断的容器
if [[ "$LAST_MODE" == true ]]; then
    CONTAINER=$(docker ps -a --filter "status=exited" --format "{{.Names}}" | head -1)
    if [[ -z "$CONTAINER" ]]; then
        echo "未找到已退出的容器"
        exit 0
    fi
    echo "🔍 诊断最近退出的容器: $CONTAINER"
elif [[ -z "$CONTAINER" ]]; then
    echo "请指定容器名或使用 --last"
    exit 1
else
    echo "🔍 诊断容器: $CONTAINER"
fi

# 检查容器是否存在
if ! docker ps -a --format "{{.Names}}" | grep -q "^${CONTAINER}$"; then
    echo "错误: 容器 $CONTAINER 不存在"
    exit 1
fi

REPORT="# 容器故障诊断报告\n\n"
REPORT+="**容器**: $CONTAINER\n"
REPORT+="**诊断时间**: $(date '+%Y-%m-%d %H:%M')\n"
REPORT+="\n---\n\n"

# 容器状态
STATUS=$(docker inspect --format "{{.State.Status}}" "$CONTAINER")
EXIT_CODE=$(docker inspect --format "{{.State.ExitCode}}" "$CONTAINER")
ERROR_MSG=$(docker inspect --format "{{.State.Error}}" "$CONTAINER")

REPORT+="## 容器状态\n\n"
REPORT+="- **状态**: $STATUS\n"
REPORT+="- **退出码**: $EXIT_CODE\n"
if [[ -n "$ERROR_MSG" ]]; then
    REPORT+="- **错误信息**: $ERROR_MSG\n"
fi
REPORT+="\n"

# 资源限制
REPORT+="## 资源限制\n\n"
MEMORY_LIMIT=$(docker inspect --format "{{.HostConfig.Memory}}" "$CONTAINER")
if [[ "$MEMORY_LIMIT" == "0" ]]; then
    REPORT+="- **内存限制**: 无限制\n"
else
    REPORT+="- **内存限制**: ${MEMORY_LIMIT} bytes\n"
fi
REPORT+="\n"

# 环境变量
REPORT+="## 环境变量\n\n"
ENV_VARS=$(docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}' "$CONTAINER" | head -10)
if [[ -n "$ENV_VARS" ]]; then
    REPORT+="\`\`\`\n${ENV_VARS}\n\`\`\`\n"
else
    REPORT+="未设置环境变量\n"
fi
REPORT+="\n"

# 日志
REPORT+="## 最近日志\n\n"
LOGS=$(docker logs --tail 50 "$CONTAINER" 2>&1 || true)
if [[ -n "$LOGS" ]]; then
    REPORT+="\`\`\`\n${LOGS}\n\`\`\`\n"
else
    REPORT+="无日志\n"
fi
REPORT+="\n"

# 根因分析和建议
REPORT+="## 根因分析\n\n"

if [[ "$EXIT_CODE" == "1" ]]; then
    if echo "$LOGS" | grep -qi "database\|connection\|refused"; then
        REPORT+="❌ 数据库连接失败\n\n"
        REPORT+="**可能原因**:\n"
        REPORT+="- 数据库容器未启动\n"
        REPORT+="- 网络配置错误\n"
        REPORT+="- 连接字符串错误\n"
    elif echo "$LOGS" | grep -qi "port\|address already in use"; then
        REPORT+="❌ 端口冲突\n\n"
        REPORT+="**可能原因**:\n"
        REPORT+="- 端口被其他进程占用\n"
        REPORT+="- docker-compose 端口映射冲突\n"
    else
        REPORT+="❌ 应用启动失败（退出码 1）\n\n"
        REPORT+="**建议**:\n"
        REPORT+="- 查看完整日志：docker logs $CONTAINER\n"
        REPORT+="- 检查环境变量配置\n"
    fi
elif [[ "$EXIT_CODE" == "137" ]]; then
    REPORT+="❌ 容器被强制终止（OOM 或手动 kill）\n\n"
    REPORT+="**建议**:\n"
    REPORT+="- 检查内存限制是否过低\n"
    REPORT+="- 查看系统日志：dmesg | grep -i kill\n"
else
    REPORT+="⚠️ 退出码: $EXIT_CODE\n\n"
    REPORT+="**建议**: 查看完整日志排查问题\n"
fi

REPORT+="\n"

# 输出
if [[ -n "$OUTPUT_FILE" ]]; then
    printf "%b" "$REPORT" > "$OUTPUT_FILE"
    echo "✅ 诊断报告已保存: $OUTPUT_FILE"
else
    printf "%b" "$REPORT"
fi
