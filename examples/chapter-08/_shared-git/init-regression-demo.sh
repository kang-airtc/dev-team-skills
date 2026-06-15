#!/usr/bin/env bash
# 重建 regression-demo 迷你 Git 仓库（用于第 8 章 test-regression，无需 corporate-site）
set -euo pipefail
SHARED="$(cd "$(dirname "$0")" && pwd)"
DEMO="$SHARED/regression-demo"
CH08="$(cd "$SHARED/.." && pwd)"
SKILLS="$(cd "$SHARED/../../.." && pwd)/.opencode/skills"

rm -rf "$DEMO"
mkdir -p "$DEMO/server/app/api/comments" "$DEMO/server/app/dao" \
  "$DEMO/frontend/src/app" "$DEMO/frontend/src/components"
cd "$DEMO"

git init -b main
printf '%s\n' '# regression-demo' '迷你仓库：模拟评论相关 4 文件变更，供 test-regression 演示。' > README.md
printf '%s\n' 'def list_comments():' '    return []' > server/app/api/comments/views.py
printf '%s\n' 'export default function Page() { return null; }' > frontend/src/app/page.tsx
printf '%s\n' 'export function CommentCard() { return null; }' > frontend/src/components/CommentCard.tsx
printf '%s\n' 'class CommentDao:' '    pass' > server/app/dao/comment_dao.py

git add .
git commit -m "chore: init demo tree"

git checkout -b feat/ch08-demo
printf '%s\n' 'def list_comments():' '    return [{"id": 1}]' > server/app/api/comments/views.py
printf '%s\n' 'export default function Page() { return <main />; }' > frontend/src/app/page.tsx
cat > frontend/src/components/CommentCard.tsx << 'EOF'
export function CommentCard() { return null; }
// ch08
EOF
printf '%s\n' 'class CommentDao:' '    def find(self, i): return i' > server/app/dao/comment_dao.py

git add .
git commit -m "feat: comment module tweaks"

echo "生成回归清单…"
mkdir -p "$CH08/outputs"
bash "$SKILLS/test-regression/scripts/analyze.sh" \
  --base main \
  --output "$CH08/outputs/chapter08-regression-checklist.md"

echo "完成：$DEMO （当前分支 feat/ch08-demo，清单已写入 $CH08/outputs/chapter08-regression-checklist.md）"
