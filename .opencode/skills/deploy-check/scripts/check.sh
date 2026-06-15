#!/usr/bin/env bash
# deploy-check: 发布前检查脚本

set -uo pipefail

COMPOSE_FILE="docker-compose.yml"
OUTPUT_FILE=""
ISSUES=0
WARNINGS=0

echo "🔍 发布前检查"
echo "====================================="

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --compose|-c)
            COMPOSE_FILE="$2"
            shift 2
            ;;
        --output|-o)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --help|-h)
            echo "用法: check.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --compose, -c  docker-compose 文件 (默认: docker-compose.yml)"
            echo "  --output, -o   输出报告路径"
            echo "  --help, -h     显示帮助"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

REPORT="# 发布前检查报告\n\n"
REPORT+="**检查时间**: $(date '+%Y-%m-%d %H:%M')\n"
REPORT+="**项目**: $(basename "$(pwd)")\n"
REPORT+="\n---\n\n"

# 检查 docker-compose 文件是否存在
if [[ ! -f "$COMPOSE_FILE" ]]; then
    echo "❌ docker-compose 文件不存在: $COMPOSE_FILE"
    REPORT+="## ❌ 严重错误\n\n"
    REPORT+="docker-compose 文件不存在: $COMPOSE_FILE\n\n"
    printf '%b' "$REPORT" > "${OUTPUT_FILE:-deploy-check-report.md}"
    exit 1
fi

echo "📋 检查 docker-compose: $COMPOSE_FILE"

# 检查服务定义（优先 docker compose V2）
if docker compose version >/dev/null 2>&1; then
  SERVICES=$(docker compose -f "$COMPOSE_FILE" config --services 2>&1 || true)
else
  SERVICES=$(docker-compose -f "$COMPOSE_FILE" config --services 2>&1 || true)
fi
SERVICE_COUNT=$(echo "$SERVICES" | grep -c . || echo 0)

echo "   发现 $SERVICE_COUNT 个服务"
REPORT+="## 服务清单\n\n"
REPORT+="发现 $SERVICE_COUNT 个服务:\n\n"

while IFS= read -r service; do
    [[ -z "$service" ]] && continue
    REPORT+="- $service\n"
done <<< "$SERVICES"

REPORT+="\n"

# 检查端口冲突
REPORT+="## 端口检查\n\n"
PORTS=$(grep -E "^\s*-\s*[\"']?[0-9]+:" "$COMPOSE_FILE" | sed 's/.*-\s*//' | sed 's/"//g' | sed "s/'//g" || true)

if [[ -n "$PORTS" ]]; then
    REPORT+="映射的端口:\n\n"
    while IFS= read -r port; do
        HOST_PORT=$(echo "$port" | cut -d: -f1)
        if lsof -Pi :"$HOST_PORT" -sTCP:LISTEN -t > /dev/null 2>&1; then
            REPORT+="- ⚠️ $port (端口 $HOST_PORT 已被占用)\n"
            ((WARNINGS++))
        else
            REPORT+="- ✅ $port (可用)\n"
        fi
    done <<< "$PORTS"
else
    REPORT+="未配置端口映射\n"
fi

REPORT+="\n"

# 检查环境变量
REPORT+="## 环境变量检查\n\n"

if [[ -f ".env" ]]; then
    REPORT+="✅ .env 文件存在\n\n"
    
    # 检查关键变量
    REQUIRED_VARS=("DATABASE_URL" "SECRET_KEY" "NEXT_PUBLIC_API_URL")
    for var in "${REQUIRED_VARS[@]}"; do
        if grep -q "^${var}=" .env 2>/dev/null; then
            REPORT+="- ✅ $var 已设置\n"
        else
            REPORT+="- ⚠️ $var 未设置\n"
            ((WARNINGS++))
        fi
    done
else
    REPORT+="❌ .env 文件不存在\n"
    ((ISSUES++))
fi

REPORT+="\n"

# 检查 Dockerfile
REPORT+="## Docker 镜像检查\n\n"

if [[ -f "Dockerfile" ]]; then
    REPORT+="✅ Dockerfile 存在\n\n"
    
    # 检查是否使用 latest
    if grep -q "FROM.*:latest" Dockerfile; then
        REPORT+="⚠️ 使用了 latest 标签，建议指定具体版本\n"
        ((WARNINGS++))
    else
        REPORT+="✅ 基础镜像版本已指定\n"
    fi
    
    # 尝试构建镜像
    echo "🏗️  尝试构建镜像..."
    if docker build -t deploy-check-test . > /dev/null 2>&1; then
        REPORT+="✅ 镜像构建成功\n"
        
        # 检查镜像大小
        SIZE=$(docker images deploy-check-test --format "{{.Size}}")
        REPORT+="📦 镜像大小: $SIZE\n"
        
        # 清理测试镜像
        docker rmi deploy-check-test > /dev/null 2>&1
    else
        REPORT+="⚠️ 镜像构建失败（可能是 Docker 未启动或无网络；发布前请在本地确认 docker build 可通过）\n"
        ((WARNINGS++))
    fi
else
    REPORT+="⚠️ Dockerfile 不存在\n"
    ((WARNINGS++))
fi

REPORT+="\n"

# 健康检查配置
REPORT+="## 健康检查配置\n\n"
if grep -q "healthcheck" "$COMPOSE_FILE"; then
    REPORT+="✅ docker-compose 中配置了健康检查\n"
else
    REPORT+="⚠️ docker-compose 中未配置健康检查\n"
    REPORT+="建议添加 healthcheck 配置\n"
    ((WARNINGS++))
fi

REPORT+="\n"

# 总结
REPORT+="---\n\n"
REPORT+="## 检查总结\n\n"

if [[ $ISSUES -eq 0 && $WARNINGS -eq 0 ]]; then
    REPORT+="🎉 所有检查通过，可以安全发布！\n"
elif [[ $ISSUES -eq 0 ]]; then
    REPORT+="⚠️ 有 $WARNINGS 个警告，建议处理后再发布\n"
else
    REPORT+="❌ 有 $ISSUES 个严重问题，$WARNINGS 个警告，必须修复后才能发布\n"
fi

# 输出（%b 将 \n 转为换行）
if [[ -n "$OUTPUT_FILE" ]]; then
    printf '%b' "$REPORT" > "$OUTPUT_FILE"
    echo ""
    echo "✅ 检查报告已保存: $OUTPUT_FILE"
else
    echo ""
    printf '%b' "$REPORT"
fi

# 退出码
if [[ $ISSUES -gt 0 ]]; then
    exit 1
fi

exit 0
