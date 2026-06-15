#!/usr/bin/env bash
# test-regression: 回归测试范围分析
# 基于 git diff 推荐需要回归测试的模块

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# 默认参数
BASE_BRANCH="main"
OUTPUT_FILE="regression-checklist.md"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --base|-b)
            BASE_BRANCH="$2"
            shift 2
            ;;
        --output|-o)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --help|-h)
            echo "用法: analyze.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --base, -b     基础分支 (默认: main)"
            echo "  --output, -o   输出文件 (默认: regression-checklist.md)"
            echo "  --help, -h     显示帮助"
            exit 0
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 检查 git 仓库
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "错误: 当前目录不是 git 仓库"
    exit 1
fi

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# 获取变更文件
CHANGED_FILES=$(git diff --name-only --diff-filter=ACM "$BASE_BRANCH...HEAD")

if [[ -z "$CHANGED_FILES" ]]; then
    echo "没有检测到代码变更"
    exit 0
fi

FILE_COUNT=$(echo "$CHANGED_FILES" | grep -c . || echo 0)

echo "🔍 分析变更影响范围"
echo "   分支: $CURRENT_BRANCH → $BASE_BRANCH"
echo "   变更文件: $FILE_COUNT"

# 初始化分类
HIGH_IMPACT=""
MEDIUM_IMPACT=""
LOW_IMPACT=""

# 分析每个文件
while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    
    # 判断影响等级和测试类型
    if echo "$file" | grep -qE "api/|controller/|handler/|route"; then
        HIGH_IMPACT+="| $file | API层 | 🔴 高 |\n"
    elif echo "$file" | grep -qE "model/|entity/|schema/|migration"; then
        MEDIUM_IMPACT+="| $file | 数据层 | 🟡 中 |\n"
    elif echo "$file" | grep -qE "service/|business/|logic"; then
        MEDIUM_IMPACT+="| $file | 业务层 | 🟡 中 |\n"
    elif echo "$file" | grep -qE "component/|page/|view"; then
        MEDIUM_IMPACT+="| $file | 前端 | 🟡 中 |\n"
    elif echo "$file" | grep -qE "util/|helper/|lib/"; then
        MEDIUM_IMPACT+="| $file | 工具层 | 🟡 中 |\n"
    elif echo "$file" | grep -qE "config/|setting"; then
        LOW_IMPACT+="| $file | 配置 | 🟢 低 |\n"
    elif echo "$file" | grep -qE "test/|spec"; then
        LOW_IMPACT+="| $file | 测试文件 | 🟢 低 |\n"
    else
        MEDIUM_IMPACT+="| $file | 其他 | 🟡 中 |\n"
    fi
done <<< "$CHANGED_FILES"

# 生成测试推荐
HIGH_TESTS=""
MEDIUM_TESTS=""
LOW_TESTS=""

# 根据变更文件推荐测试
if echo "$CHANGED_FILES" | grep -qE "api/|controller/|route"; then
    HIGH_TESTS+="- [ ] 接口测试（正常/异常流程）\n"
    HIGH_TESTS+="- [ ] 权限控制测试\n"
    HIGH_TESTS+="- [ ] 参数校验测试\n"
fi

if echo "$CHANGED_FILES" | grep -qE "auth|login|permission|token"; then
    HIGH_TESTS+="- [ ] 认证流程测试\n"
    HIGH_TESTS+="- [ ] Token生成与验证测试\n"
fi

if echo "$CHANGED_FILES" | grep -qE "model/|entity/|schema/"; then
    MEDIUM_TESTS+="- [ ] 数据模型单元测试\n"
    MEDIUM_TESTS+="- [ ] 数据库操作测试\n"
fi

if echo "$CHANGED_FILES" | grep -qE "service/|business/|logic"; then
    MEDIUM_TESTS+="- [ ] 业务逻辑单元测试\n"
    MEDIUM_TESTS+="- [ ] 边界条件测试\n"
fi

if echo "$CHANGED_FILES" | grep -qE "component/|page/|view"; then
    MEDIUM_TESTS+="- [ ] 前端组件测试\n"
    MEDIUM_TESTS+="- [ ] 页面交互测试\n"
fi

if echo "$CHANGED_FILES" | grep -qE "migration/|ddl|schema"; then
    HIGH_TESTS+="- [ ] 数据库迁移测试\n"
    HIGH_TESTS+="- [ ] 数据兼容性测试\n"
fi

if echo "$CHANGED_FILES" | grep -qE "config/|setting"; then
    LOW_TESTS+="- [ ] 配置加载测试\n"
    LOW_TESTS+="- [ ] 环境变量测试\n"
fi

# 默认测试项
if [[ -z "$HIGH_TESTS" ]]; then
    HIGH_TESTS="- [ ] 核心功能流程测试\n"
fi

if [[ -z "$MEDIUM_TESTS" ]]; then
    MEDIUM_TESTS="- [ ] 相关模块单元测试\n"
fi

if [[ -z "$LOW_TESTS" ]]; then
    LOW_TESTS="- [ ] 基础功能验证\n"
fi

# 生成报告
REPORT="# 回归测试范围分析\n\n"
REPORT+="**变更分支**: $CURRENT_BRANCH → $BASE_BRANCH\n"
REPORT+="**变更文件数**: $FILE_COUNT\n"
REPORT+="**分析时间**: $(date '+%Y-%m-%d')\n"
REPORT+="\n---\n\n"

# 变更概览
REPORT+="## 变更概览\n\n"
REPORT+="| 文件 | 类型 | 影响等级 |\n"
REPORT+="|------|------|---------|\n"
REPORT+="$HIGH_IMPACT"
REPORT+="$MEDIUM_IMPACT"
REPORT+="$LOW_IMPACT"
REPORT+="\n"

# 推荐测试
REPORT+="## 推荐回归测试\n\n"

if [[ -n "$HIGH_TESTS" ]]; then
    REPORT+="### 🔴 高优先级（必须测试）\n\n"
    REPORT+="$HIGH_TESTS"
    REPORT+="\n"
fi

if [[ -n "$MEDIUM_TESTS" ]]; then
    REPORT+="### 🟡 中优先级（建议测试）\n\n"
    REPORT+="$MEDIUM_TESTS"
    REPORT+="\n"
fi

if [[ -n "$LOW_TESTS" ]]; then
    REPORT+="### 🟢 低优先级（可选测试）\n\n"
    REPORT+="$LOW_TESTS"
    REPORT+="\n"
fi

# 影响分析
REPORT+="## 影响分析\n\n"
REPORT+="**直接影响的模块**:\n"
REPORT+="- 根据变更文件路径推断\n"
REPORT+="\n"
REPORT+="**建议**:\n"
REPORT+="1. 优先执行高优先级测试\n"
REPORT+="2. 如涉及数据库变更，需执行迁移测试\n"
REPORT+="3. 建议在 staging 环境做完整回归\n"

# 输出报告
printf '%b' "$REPORT" > "$OUTPUT_FILE"

echo "✅ 回归测试分析完成"
echo "   输出: $OUTPUT_FILE"
echo "   高优先级: $(echo "$HIGH_TESTS" | grep -c "\- \[" || echo 0)"
echo "   中优先级: $(echo "$MEDIUM_TESTS" | grep -c "\- \[" || echo 0)"
echo "   低优先级: $(echo "$LOW_TESTS" | grep -c "\- \[" || echo 0)"
