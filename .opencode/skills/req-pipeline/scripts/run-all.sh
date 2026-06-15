#!/bin/bash
# 需求管理流水线 - 一键执行完整流程

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 参数检查
if [ $# -lt 2 ]; then
    echo "用法: $0 <项目名称> <原始需求文件>"
    echo "示例: $0 user-auth-system raw-requirement.txt"
    exit 1
fi

PROJECT_NAME="$1"
INPUT_FILE="$2"
OUTPUT_DIR="./projects/$PROJECT_NAME"

echo "🚀 启动需求管理流程: $PROJECT_NAME"
echo "====================================="

# 创建项目目录
mkdir -p "$OUTPUT_DIR"
cp "$INPUT_FILE" "$OUTPUT_DIR/0-raw-requirement.txt"

echo "📁 项目目录: $OUTPUT_DIR"
echo ""

# Step 1: 需求澄清
echo "📋 Step 1/6: 需求澄清..."
python3 "$SKILLS_DIR/req-clarify/scripts/clarify.py" \
    --input "$OUTPUT_DIR/0-raw-requirement.txt" \
    --output "$OUTPUT_DIR/1-clarified.md"
echo ""

# Step 2: 生成 PRD
echo "📝 Step 2/6: 生成 PRD..."
python3 "$SKILLS_DIR/req-prd/scripts/generate-prd.py" \
    --input "$OUTPUT_DIR/1-clarified.md" \
    --output "$OUTPUT_DIR/2-PRD.md" \
    --product "$PROJECT_NAME"
echo ""

# Step 3: 需求拆解
echo "🔨 Step 3/6: 需求拆解..."
python3 "$SKILLS_DIR/req-decompose/scripts/decompose.py" \
    --input "$OUTPUT_DIR/2-PRD.md" \
    --output "$OUTPUT_DIR/3-backlog.md"
echo ""

# Step 4: 初始化变更追踪
echo "📊 Step 4/6: 初始化变更追踪..."
python3 "$SKILLS_DIR/req-track/scripts/track-change.py" \
    --init \
    --output "$OUTPUT_DIR/4-CHANGELOG.md" \
    --project "$PROJECT_NAME"
echo ""

# Step 5: 生成故事地图
echo "🗺️  Step 5/6: 生成故事地图..."
python3 "$SKILLS_DIR/req-storymap/scripts/generate-story-map.py" \
    --input "$OUTPUT_DIR/3-backlog.md" \
    --output "$OUTPUT_DIR/5-story-map.md"
echo ""

# Step 6: 生成流程图
echo "📈 Step 6/6: 生成流程图..."
python3 "$SKILLS_DIR/req-flowchart/scripts/generate-flowchart.py" \
    --input "$OUTPUT_DIR/2-PRD.md" \
    --output "$OUTPUT_DIR/6-flowchart.md" \
    --title "$PROJECT_NAME 核心流程"
echo ""

# 完成
echo "====================================="
echo "✅ 完成！所有产物已保存到 $OUTPUT_DIR/"
echo "====================================="
echo ""
echo "产物清单:"
echo "  0-raw-requirement.txt  - 原始需求"
echo "  1-clarified.md         - 需求澄清"
echo "  2-PRD.md               - PRD 草稿"
echo "  3-backlog.md           - 需求拆解"
echo "  4-CHANGELOG.md         - 变更追踪"
echo "  5-story-map.md         - 故事地图"
echo "  6-flowchart.md         - 流程图"
echo ""
echo "下一步建议:"
echo "  1. 检查 2-PRD.md 并人工补充细节"
echo "  2. 检查 3-backlog.md 并调整估算"
echo "  3. 根据评审意见使用变更追踪 Skill 记录变更"
