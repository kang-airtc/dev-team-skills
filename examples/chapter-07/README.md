# 第 7 章示例：代码质量（`review-*`）

本目录配合书稿第 7 章，场景为公司站点 **News** 相关前后端与 PR 小例子。**路径相对于 dev-team-skills 仓库根目录。**

## 约定

- 各子目录 **input/** 内除结构化输入外另有 **intent.md**，正文与书稿对应小节**自然语言意图示例**一致。
- **output/** 为本地生成目录，典型 Markdown 报告不随仓库提供；完整命令见本节下方「一键复现」。
- **review-pr**、**review-conflict** 依赖 **_shared-git/news-pr-demo**；若无 **.git**，先执行 **_shared-git/init-news-pr-demo.sh**。

## 书中 Skill 名与脚本目录

| 书中 Skill | 脚本目录 |
|------------|-----------|
| review-lint-frontend | dev-frontend-lint |
| review-lint-backend | dev-backend-lint |
| review-diff | dev-spec-diff |
| review-deps | dev-deps-audit |
| review-code | review-code |
| review-pr | review-pr |
| review-conflict | review-conflict |
| review-consistency | 无单一脚本 |
| review-git | 无单一脚本 |

## 一键复现（仓库根目录）

```bash
SKILLS=.opencode/skills
BASE=examples/chapter-07

python3 $SKILLS/dev-frontend-lint/scripts/lint.py \
  -p $BASE/review-lint-frontend/input \
  -o $BASE/review-lint-frontend/output/lint-frontend.md

python3 $SKILLS/dev-backend-lint/scripts/lint.py \
  -p $BASE/review-lint-backend/input \
  -o $BASE/review-lint-backend/output/lint-backend.md

python3 $SKILLS/dev-spec-diff/scripts/diff.py \
  -c $BASE/review-diff/input/code \
  -s $SKILLS/dev-backend-lint/references/backend-standard.md \
  -o $BASE/review-diff/output/spec-diff.md

bash $SKILLS/dev-deps-audit/scripts/audit.sh \
  $BASE/review-deps/input/frontend \
  $BASE/review-deps/input/backend \
  $BASE/review-deps/output/deps-audit.md

bash $SKILLS/review-code/scripts/review.sh \
  --diff $BASE/review-code/input/news-change.diff \
  --output $BASE/review-code/output/code-review.md
```

**review-pr**（需在 **news-pr-demo** 内、分支 **feat/news-module**）：

```bash
cd examples/chapter-07/_shared-git/news-pr-demo
git checkout feat/news-module
bash ../../../../.opencode/skills/review-pr/scripts/generate-pr.sh \
  --base main \
  --output ../../review-pr/output/pr-description.md
```

**review-conflict**：

```bash
cd examples/chapter-07/_shared-git/news-pr-demo
bash ../../../../.opencode/skills/review-conflict/scripts/conflict.sh \
  --source feat/news-module \
  --target main \
  --output ../../review-conflict/output/conflict-check.md
```

**review-consistency**、**review-git** 无固定脚本，按各 **input/** 与书稿表格自行生成 **output/** 报告即可。
