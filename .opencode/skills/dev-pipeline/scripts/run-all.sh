#!/usr/bin/env bash
# dev-pipeline/run-all.sh
# 整合 10 个 dev-* Skill：文档线（可并行）+ 代码线（串行）
set -uo pipefail

MODULE="${1:-news}"
INPUTS_DIR="${2:-./inputs}"
OUTPUT_DIR="${3:-${MODULE}-output}"
SKILLS_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

mkdir -p \
  "$OUTPUT_DIR/docs" \
  "$OUTPUT_DIR/server" \
  "$OUTPUT_DIR/client"

echo "=== Dev Pipeline 启动 ==="
echo "模块名称  : $MODULE"
echo "输入目录  : $INPUTS_DIR"
echo "输出目录  : $OUTPUT_DIR"
echo

run_or_skip() {
  local step="$1"
  local name="$2"
  local check="$3"
  shift 3

  if [[ -n "$check" && ! -e "$check" ]]; then
    echo "[$step] ⏭  跳过 $name（未找到 $check）"
    echo
    return 0
  fi

  echo "[$step] ▶  $name"
  if "$@" > "/tmp/dev-pipeline-${step//\//-}.log" 2>&1; then
    echo "[$step] ✅ 完成"
  else
    echo "[$step] ⚠️  失败（继续后续步骤），日志见 /tmp/dev-pipeline-${step//\//-}.log"
  fi
  echo
}

# ── 文档线（可并行） ──────────────────────────────────────────────
run_or_skip "1/10" "生成架构图 (dev-arch)" "$INPUTS_DIR/arch-spec.md" \
  python3 "$SKILLS_DIR/dev-arch/scripts/generate.py" \
    --input "$INPUTS_DIR/arch-spec.md" \
    --output "$OUTPUT_DIR/docs/arch.drawio"

run_or_skip "2/10" "生成时序图 (dev-sequence)" "$INPUTS_DIR/sequence-spec.md" \
  python3 "$SKILLS_DIR/dev-sequence/scripts/generate.py" \
    --input "$INPUTS_DIR/sequence-spec.md" \
    --output "$OUTPUT_DIR/docs/sequence.drawio"

run_or_skip "3/10" "生成技术方案 (dev-techspec)" "" \
  python3 "$SKILLS_DIR/dev-techspec/scripts/generate.py" \
    --title "$MODULE" \
    --author "$(whoami)" \
    --output "$OUTPUT_DIR/docs/tech-spec.md"

run_or_skip "4/10" "生成接口文档 (dev-apidoc)" "$INPUTS_DIR/openapi-snippet.json" \
  python3 "$SKILLS_DIR/dev-apidoc/scripts/generate.py" \
    --input "$INPUTS_DIR/openapi-snippet.json" \
    --output "$OUTPUT_DIR/docs/api-spec.docx"

# ── 代码线（必须串行，上游产物是下游输入） ──────────────────────────
run_or_skip "5/10" "生成 ORM 模型 (dev-db)" "$INPUTS_DIR/model-spec.md" \
  python3 "$SKILLS_DIR/dev-db/scripts/generate.py" \
    --input "$INPUTS_DIR/model-spec.md" \
    --output-dir "$OUTPUT_DIR/server/models"

run_or_skip "6/10" "生成迁移文件 (dev-migrate)" "$INPUTS_DIR/migration-spec.md" \
  python3 "$SKILLS_DIR/dev-migrate/scripts/generate.py" \
    --input "$INPUTS_DIR/migration-spec.md" \
    --output-dir "$OUTPUT_DIR/server"

run_or_skip "7/10" "生成 DAO (dev-backend-dao)" "$INPUTS_DIR/dao-spec.md" \
  python3 "$SKILLS_DIR/dev-backend-dao/scripts/generate.py" \
    --input "$INPUTS_DIR/dao-spec.md" \
    --output-dir "$OUTPUT_DIR/server/dao"

run_or_skip "8/10" "生成后端路由 (dev-backend)" "$INPUTS_DIR/api-spec.md" \
  python3 "$SKILLS_DIR/dev-backend/scripts/generate.py" \
    --input "$INPUTS_DIR/api-spec.md" \
    --output-dir "$OUTPUT_DIR"

run_or_skip "9/10" "生成前端页面 (dev-frontend)" "$INPUTS_DIR/page-spec.md" \
  python3 "$SKILLS_DIR/dev-frontend/scripts/generate.py" \
    --input "$INPUTS_DIR/page-spec.md" \
    --output "$OUTPUT_DIR/client/${MODULE}_page.tsx"

run_or_skip "10/10" "生成前端表单 (dev-frontend-form)" "$INPUTS_DIR/form-spec.md" \
  python3 "$SKILLS_DIR/dev-frontend-form/scripts/generate.py" \
    --input "$INPUTS_DIR/form-spec.md" \
    --output-dir "$OUTPUT_DIR/client"

echo "=== Pipeline 完成 ==="
echo "产出文件："
find "$OUTPUT_DIR" -type f | sort | sed 's/^/  /'
