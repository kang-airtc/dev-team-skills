#!/usr/bin/env bash
# dev-pipeline/run-step.sh
# 单步执行：跑某一个 dev-* skill
# 用法：./run-step.sh <step_name> [项目名] [输入目录]
#   step_name: arch | sequence | techspec | frontend-lint |
#              backend-lint | spec-diff | deps-audit | apidoc
set -uo pipefail

STEP="${1:-}"
PROJECT_NAME="${2:-dev-output}"
INPUTS_DIR="${3:-./inputs}"
OUTPUT_DIR="$PROJECT_NAME"
SKILLS_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

FRONTEND_DIR="${FRONTEND_DIR:-./blog/frontend}"
BACKEND_DIR="${BACKEND_DIR:-./blog/backend}"

mkdir -p "$OUTPUT_DIR"

case "$STEP" in
  arch)
    python3 "$SKILLS_DIR/dev-arch/scripts/generate.py" \
      --input "$INPUTS_DIR/arch-spec.md" \
      --output "$OUTPUT_DIR/1-arch.drawio"
    ;;
  sequence)
    python3 "$SKILLS_DIR/dev-sequence/scripts/generate.py" \
      --input "$INPUTS_DIR/sequence-spec.md" \
      --output "$OUTPUT_DIR/2-sequence.drawio"
    ;;
  techspec)
    python3 "$SKILLS_DIR/dev-techspec/scripts/generate.py" \
      --title "$PROJECT_NAME" \
      --author "$(whoami)" \
      --output "$OUTPUT_DIR/3-tech-spec.md"
    ;;
  frontend-lint)
    python3 "$SKILLS_DIR/dev-frontend-lint/scripts/lint.py" \
      --path "$FRONTEND_DIR" \
      --output "$OUTPUT_DIR/4-frontend-lint.md"
    ;;
  backend-lint)
    python3 "$SKILLS_DIR/dev-backend-lint/scripts/lint.py" \
      --path "$BACKEND_DIR" \
      --output "$OUTPUT_DIR/5-backend-lint.md"
    ;;
  spec-diff)
    python3 "$SKILLS_DIR/dev-spec-diff/scripts/diff.py" \
      --code "$BACKEND_DIR" \
      --output "$OUTPUT_DIR/6-spec-diff.md"
    ;;
  deps-audit)
    "$SKILLS_DIR/dev-deps-audit/scripts/audit.sh" \
      "$FRONTEND_DIR" "$BACKEND_DIR" "$OUTPUT_DIR/7-deps-audit.md"
    ;;
  apidoc)
    python3 "$SKILLS_DIR/dev-apidoc/scripts/generate.py" \
      --input "$INPUTS_DIR/openapi.json" \
      --output "$OUTPUT_DIR/8-api-spec.docx"
    ;;
  '')
    echo "用法：$0 <step_name> [项目名] [输入目录]" >&2
    echo "step_name: arch | sequence | techspec | frontend-lint | backend-lint | spec-diff | deps-audit | apidoc" >&2
    exit 1
    ;;
  *)
    echo "错误：未知步骤 '$STEP'" >&2
    exit 1
    ;;
esac
