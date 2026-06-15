#!/bin/bash
# deploy-pipeline: 一键发布流水线

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

VERSION=""
OUTPUT_DIR="./deploy-output"

while [[ $# -gt 0 ]]; do
    case $1 in
        --version|-v)
            VERSION="$2"
            shift 2
            ;;
        --output|-o)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

if [[ -z "$VERSION" ]]; then
    echo "用法: $0 --version v1.2.0"
    exit 1
fi

echo "🚀 启动发布流水线: $VERSION"
echo "====================================="

mkdir -p "$OUTPUT_DIR"

# Step 1: 发布前检查
echo "🔍 Step 1/3: 发布前检查..."
bash "$SKILLS_DIR/deploy-check/scripts/check.sh" \
    --output "$OUTPUT_DIR/1-check-report.md"
echo ""

# Step 2: 生成 CHANGELOG
echo "📝 Step 2/3: 生成 CHANGELOG..."
bash "$SKILLS_DIR/deploy-changelog/scripts/generate.sh" \
    --version "$VERSION" \
    --output "$OUTPUT_DIR/2-CHANGELOG.md"
echo ""

# Step 3: 生成发布说明
echo "📦 Step 3/3: 生成发布说明..."
python3 "$SKILLS_DIR/deploy-release/scripts/generate.py" \
    --version "$VERSION" \
    --changelog "$OUTPUT_DIR/2-CHANGELOG.md" \
    --output "$OUTPUT_DIR/3-release-notes.md"
echo ""

# 汇总
cat > "$OUTPUT_DIR/0-summary.md" << EOF
# 发布流水线汇总

**版本**: $VERSION
**时间**: $(date '+%Y-%m-%d %H:%M')

## 产出物

- **1-check-report.md**: 发布前检查报告
- **2-CHANGELOG.md**: 变更日志
- **3-release-notes.md**: 发布说明

## 下一步

1. 检查 1-check-report.md，修复问题
2. 审阅 2-CHANGELOG.md 确认变更记录
3. 基于 3-release-notes.md 执行发布
4. 手动打 tag: git tag $VERSION
5. 推送到远程: git push origin $VERSION

EOF

echo "====================================="
echo "✅ 发布流水线完成！"
echo "====================================="
echo ""
echo "产出物: $OUTPUT_DIR/"
