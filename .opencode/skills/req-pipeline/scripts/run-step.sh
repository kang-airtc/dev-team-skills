#!/bin/bash
# 需求管理流水线 - 分步执行

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 参数解析
STEP=""
PROJECT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --step)
            STEP="$2"
            shift 2
            ;;
        --project)
            PROJECT="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

if [ -z "$STEP" ] || [ -z "$PROJECT" ]; then
    echo "用法: $0 --step <步骤> --project <项目名>"
    echo ""
    echo "可选步骤:"
    echo "  clarify     - 需求澄清"
    echo "  prd         - 生成 PRD"
    echo "  decompose   - 需求拆解"
    echo "  init-track  - 初始化变更追踪"
    echo "  story-map   - 生成故事地图"
    echo "  flowchart   - 生成流程图"
    echo ""
    echo "示例: $0 --step clarify --project user-auth-system"
    exit 1
fi

OUTPUT_DIR="./projects/$PROJECT"

if [ ! -d "$OUTPUT_DIR" ]; then
    echo "[错误] 项目不存在: $OUTPUT_DIR"
    echo "请先运行: ./run-all.sh \"$PROJECT\" \"raw-requirement.txt\""
    exit 1
fi

echo "🔄 执行步骤: $STEP (项目: $PROJECT)"
echo "====================================="

case $STEP in
    clarify)
        echo "📋 需求澄清..."
        python3 "$SKILLS_DIR/req-clarify/scripts/clarify.py" \
            --input "$OUTPUT_DIR/0-raw-requirement.txt" \
            --output "$OUTPUT_DIR/1-clarified.md"
        ;;
    
    prd)
        echo "📝 生成 PRD..."
        python3 "$SKILLS_DIR/req-prd/scripts/generate-prd.py" \
            --input "$OUTPUT_DIR/1-clarified.md" \
            --output "$OUTPUT_DIR/2-PRD.md" \
            --product "$PROJECT"
        ;;
    
    decompose)
        echo "🔨 需求拆解..."
        python3 "$SKILLS_DIR/req-decompose/scripts/decompose.py" \
            --input "$OUTPUT_DIR/2-PRD.md" \
            --output "$OUTPUT_DIR/3-backlog.md"
        ;;
    
    init-track)
        echo "📊 初始化变更追踪..."
        python3 "$SKILLS_DIR/req-track/scripts/track-change.py" \
            --init \
            --output "$OUTPUT_DIR/4-CHANGELOG.md" \
            --project "$PROJECT"
        ;;
    
    story-map)
        echo "🗺️  生成故事地图..."
        python3 "$SKILLS_DIR/req-storymap/scripts/generate-story-map.py" \
            --input "$OUTPUT_DIR/3-backlog.md" \
            --output "$OUTPUT_DIR/5-story-map.md"
        ;;
    
    flowchart)
        echo "📈 生成流程图..."
        python3 "$SKILLS_DIR/req-flowchart/scripts/generate-flowchart.py" \
            --input "$OUTPUT_DIR/2-PRD.md" \
            --output "$OUTPUT_DIR/6-flowchart.md" \
            --title "$PROJECT 核心流程"
        ;;
    
    *)
        echo "[错误] 未知步骤: $STEP"
        exit 1
        ;;
esac

echo ""
echo "✅ 步骤完成: $STEP"
