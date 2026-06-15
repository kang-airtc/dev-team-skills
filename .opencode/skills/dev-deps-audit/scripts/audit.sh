#!/usr/bin/env bash
# dev-deps-audit: 审计 Next.js + FastAPI 依赖安全
# 前端用 npm audit，后端用 pip-audit
set -uo pipefail

FRONTEND="${1:-./blog/frontend}"
BACKEND="${2:-./blog/backend}"
OUTPUT="${3:-}"

REPORT_FILE=$(mktemp)
trap 'rm -f "$REPORT_FILE"' EXIT

# 写报告头
{
  echo "# 依赖安全审计报告"
  echo
  echo "**审计时间**：$(date '+%Y-%m-%d %H:%M:%S')"
  echo
} > "$REPORT_FILE"

# ---------- 前端：Next.js / npm audit ----------
{
  echo "## 前端（Next.js）"
  echo
  if [[ ! -d "$FRONTEND" ]]; then
    echo "⚠️ 前端目录不存在：\`$FRONTEND\`"
    echo
  elif [[ ! -f "$FRONTEND/package.json" ]]; then
    echo "⚠️ \`$FRONTEND\` 下未找到 package.json，跳过"
    echo
  elif ! command -v npm >/dev/null 2>&1; then
    echo "⚠️ 未检测到 npm，请先安装 Node.js"
    echo
  else
    echo "**目录**：\`$FRONTEND\`"
    echo
    echo '```'
    (cd "$FRONTEND" && npm audit 2>&1) || true
    echo '```'
    echo
  fi
} >> "$REPORT_FILE"

# ---------- 后端：FastAPI / pip-audit ----------
{
  echo "## 后端（FastAPI）"
  echo
  if [[ ! -d "$BACKEND" ]]; then
    echo "⚠️ 后端目录不存在：\`$BACKEND\`"
    echo
  elif [[ ! -f "$BACKEND/requirements.txt" ]]; then
    echo "⚠️ \`$BACKEND\` 下未找到 requirements.txt，跳过"
    echo
  elif ! command -v pip-audit >/dev/null 2>&1; then
    echo "⚠️ 未检测到 pip-audit，请先安装：\`pip install pip-audit\`"
    echo
  else
    echo "**目录**：\`$BACKEND\`"
    echo
    echo '```'
    pip-audit -r "$BACKEND/requirements.txt" 2>&1 || true
    echo '```'
    echo
  fi
} >> "$REPORT_FILE"

# ---------- 提示 ----------
{
  echo "## 修复建议"
  echo
  echo "- **前端**：参考 \`npm audit fix\` 自动升级；高危漏洞需人工评估升级影响"
  echo "- **后端**：在 \`requirements.txt\` 中固定到安全版本；某些 CVE 实际不影响项目使用方式，可人工排除"
  echo "- 误报存在，最终发版决定由人做"
} >> "$REPORT_FILE"

# 输出
if [[ -n "$OUTPUT" ]]; then
  mkdir -p "$(dirname "$OUTPUT")"
  cp "$REPORT_FILE" "$OUTPUT"
  echo "已生成报告：$OUTPUT"
else
  cat "$REPORT_FILE"
fi
