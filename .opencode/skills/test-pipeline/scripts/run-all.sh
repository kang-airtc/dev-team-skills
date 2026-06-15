#!/bin/bash
# test-pipeline: 一键测试流水线

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 默认参数
SOURCE_DIR="./src"
OUTPUT_DIR="./test-output"
API_DOC=""
COVERAGE_REPORT=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --source)
            SOURCE_DIR="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --api-doc)
            API_DOC="$2"
            shift 2
            ;;
        --coverage)
            COVERAGE_REPORT="$2"
            shift 2
            ;;
        --help|-h)
            echo "用法: run-all.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --source       源代码目录 (默认: ./src)"
            echo "  --output       输出目录 (默认: ./test-output)"
            echo "  --api-doc      接口文档路径 (可选)"
            echo "  --coverage     覆盖率报告路径 (可选)"
            echo "  --help, -h     显示帮助"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

echo "🧪 启动测试生成流水线"
echo "====================================="
echo "源代码: $SOURCE_DIR"
echo "输出: $OUTPUT_DIR"
echo ""

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# Step 1: 生成单元测试
echo "📝 Step 1/3: 生成单元测试..."
if [[ -d "$SOURCE_DIR" ]]; then
    UNIT_OUTPUT="$OUTPUT_DIR/1-unit-tests"
    mkdir -p "$UNIT_OUTPUT"
    
    python3 "$SKILLS_DIR/test-unit/scripts/generate.py" \
        --input "$SOURCE_DIR" \
        --output "$UNIT_OUTPUT"
    
    echo "✅ 单元测试已生成到 $UNIT_OUTPUT"
else
    echo "⚠️ 源代码目录不存在，跳过单元测试生成"
fi
echo ""

# Step 2: 生成接口测试
echo "🌐 Step 2/3: 生成接口测试..."
if [[ -n "$API_DOC" && -f "$API_DOC" ]]; then
    API_OUTPUT="$OUTPUT_DIR/2-api-tests"
    mkdir -p "$API_OUTPUT"
    
    python3 "$SKILLS_DIR/test-api/scripts/generate.py" \
        --input "$API_DOC" \
        --output "$API_OUTPUT/test_api.py"
    
    echo "✅ 接口测试已生成到 $API_OUTPUT"
else
    echo "⚠️ 未提供接口文档，跳过接口测试生成"
fi
echo ""

# Step 3: 回归测试分析
echo "🔍 Step 3/3: 回归测试分析..."
if git rev-parse --git-dir > /dev/null 2>&1; then
    bash "$SKILLS_DIR/test-regression/scripts/analyze.sh" \
        --base main \
        --output "$OUTPUT_DIR/3-regression-checklist.md"
    
    echo "✅ 回归测试清单已生成"
else
    echo "⚠️ 不是 git 仓库，跳过回归分析"
fi
echo ""

# Step 4: 覆盖率分析（如果提供了报告）
if [[ -n "$COVERAGE_REPORT" && -f "$COVERAGE_REPORT" ]]; then
    echo "📊 Step 4: 覆盖率分析..."
    python3 "$SKILLS_DIR/test-coverage/scripts/analyze.py" \
        --input "$COVERAGE_REPORT" \
        --output "$OUTPUT_DIR/4-coverage-report.md"
    
    echo "✅ 覆盖率报告已生成"
    echo ""
fi

# 生成汇总
cat > "$OUTPUT_DIR/0-summary.md" << EOF
# 测试生成汇总

**生成时间**: $(date '+%Y-%m-%d %H:%M')
**源代码**: $SOURCE_DIR

## 产出物

- **1-unit-tests/**: 自动生成的单元测试
- **2-api-tests/**: 自动生成的接口测试（如提供接口文档）
- **3-regression-checklist.md**: 回归测试清单
- **4-coverage-report.md**: 覆盖率报告（如提供）

## 下一步

1. 检查生成的单元测试，补充具体断言
2. 配置接口测试的 BASE_URL 和认证信息
3. 运行测试：pytest 1-unit-tests/
4. 根据回归清单执行回归测试
5. 查看覆盖率报告，补充未覆盖的代码

EOF

echo "====================================="
echo "✅ 流水线完成！"
echo "====================================="
echo ""
echo "产出物保存在: $OUTPUT_DIR/"
echo "汇总报告: $OUTPUT_DIR/0-summary.md"
