#!/usr/bin/env bash
# deploy-changelog: 基于 git log 生成 CHANGELOG

set -uo pipefail

VERSION=""
SINCE=""
OUTPUT_FILE="CHANGELOG.md"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --version|-v)
            VERSION="$2"
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
            echo "用法: generate.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --version, -v  版本号"
            echo "  --since        起始日期 (YYYY-MM-DD)"
            echo "  --output, -o   输出文件 (默认: CHANGELOG.md)"
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

# 获取上次 tag
LAST_TAG=$(git describe --tags --abbrev=0 2>&1 || echo "")

if [[ -z "$VERSION" ]]; then
    if [[ -n "$LAST_TAG" ]]; then
        # 自动推断版本号（简化版）
        VERSION="${LAST_TAG}-next"
    else
        VERSION="v0.1.0"
    fi
fi

# 获取 commit 范围
if [[ -n "$LAST_TAG" ]]; then
    COMMIT_RANGE="${LAST_TAG}..HEAD"
    echo "📋 生成 CHANGELOG: $LAST_TAG → HEAD"
else
    COMMIT_RANGE="HEAD"
    echo "📋 生成 CHANGELOG: 全部提交"
fi

# 生成 CHANGELOG（兼容 bash 3.2，不使用关联数组）
CHANGELOG="# Changelog\n\n"
CHANGELOG+="## [$VERSION] - $(date '+%Y-%m-%d')\n\n"

append_type_section() {
    local type="$1"
    local title="$2"
    local commits
    if [[ "$type" == "other" ]]; then
        commits=$(git log "$COMMIT_RANGE" --pretty=format:"%s" | grep -v -E "^(feat|fix|perf|refactor|docs|chore|test)(\(.+\))?:" || true)
    else
        commits=$(git log "$COMMIT_RANGE" --pretty=format:"%s" | grep -E "^${type}(\(.+\))?:" || true)
    fi
    if [[ -n "$commits" ]]; then
        CHANGELOG+="### $title\n\n"
        while IFS= read -r commit; do
            [[ -z "$commit" ]] && continue
            local message
            if [[ "$type" == "other" ]]; then
                message="$commit"
            else
                message=$(echo "$commit" | sed -E "s/^${type}(\(.+\))?:[[:space:]]*//")
            fi
            CHANGELOG+="- $message\n"
        done <<< "$commits"
        CHANGELOG+="\n"
    fi
}

append_type_section "feat" "Features"
append_type_section "fix" "Bug Fixes"
append_type_section "perf" "Performance"
append_type_section "refactor" "Refactoring"
append_type_section "docs" "Documentation"
append_type_section "chore" "Chores"
append_type_section "test" "Tests"
append_type_section "other" "Other"

# 输出（%b 将 \n 转为换行）
printf '%b' "$CHANGELOG" > "$OUTPUT_FILE"

echo "✅ CHANGELOG 已生成: $OUTPUT_FILE"
echo ""
echo "版本: $VERSION"

if [[ -n "$LAST_TAG" ]]; then
    COMMIT_COUNT=$(git log "$COMMIT_RANGE" --oneline | wc -l | tr -d ' ')
    echo "提交数: $COMMIT_COUNT"
fi
