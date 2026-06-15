# 第 8 章示例：测试阶段 Skill（自包含小例子）

本目录为书稿第 8 章配套：**不要求**检出第 12 章 **company-site** 全仓库；输入在 **inputs/**（含各 **intent-*.md**，正文与书稿**自然语言意图示例**一致），典型生成物在 **outputs/** 目录下 **chapter08-*.py** / **chapter08-*.md**，仓库已附一份示例产物，可按下文命令本地重跑覆盖。

路径均相对于 **dev-team-skills** 仓库根目录。

## 布局

| 路径 | 说明 |
|------|------|
| inputs/auth_utils.py | test-unit 演示源码 |
| inputs/openapi.json | test-api 用片段（登录 + 评论 CRUD） |
| inputs/mock-coverage.xml | test-coverage 演示 cobertura |
| inputs/mock-pytest-results.xml | test-report 演示 JUnit |
| inputs/intent-test-*.md | 与各 Skill 对应的自然语言意图 |
| outputs/chapter08-*.py / chapter08-*.md | 5 个 Skill 跑出来的示例产物 |
| _shared-git/init-regression-demo.sh | 重建迷你 Git 并生成回归清单 |
| _shared-git/regression-demo/ | 演示仓库（init 后含 .git） |

## 一键复现（仓库根目录）

将 `/path/to/dev-team-skills` 换为本机路径。

```bash
cd /path/to/dev-team-skills
SKILLS=.opencode/skills
BASE=examples/chapter-08
mkdir -p $BASE/outputs

python3 $SKILLS/test-unit/scripts/generate.py \
  -i $BASE/inputs/auth_utils.py \
  -o $BASE/outputs/chapter08-unit-tests.py

python3 $SKILLS/test-api/scripts/generate.py \
  -i $BASE/inputs/openapi.json \
  -o $BASE/outputs/chapter08-api-tests.py

python3 $SKILLS/test-coverage/scripts/analyze.py \
  -i $BASE/inputs/mock-coverage.xml \
  -o $BASE/outputs/chapter08-coverage-report.md

python3 $SKILLS/test-report/scripts/generate.py \
  -i $BASE/inputs/mock-pytest-results.xml \
  -o $BASE/outputs/chapter08-test-report.md

bash $BASE/_shared-git/init-regression-demo.sh
```

生成 **coverage.xml** 的常见方式：在业务项目根执行 **pytest**，并指定 **--cov** 与 **--cov-report=xml**（见项目文档）。

## test-pipeline

第 8 章书稿 **8.7 节**为占位说明；分步掌握上述命令后，可在自有项目中使用 **test-pipeline/scripts/run-all.sh**（需在 Git 工作目录下以启用回归步骤，参数见该脚本）。

## 与第 6、7 章的关系

OpenAPI 与认证、评论路径可与**公司站点**及 **News** 子模块叙事对照；本章命令与路径**仅以本目录为准**，便于单独复现。
