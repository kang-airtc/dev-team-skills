# 第 9 章示例：发布阶段（自包含 release-demo）

本目录为书稿第 9 章配套：**不要求**检出 **company-site** 全仓。**release-demo/** 为最小 **PostgreSQL + FastAPI + nginx 静态前端** 三服务 compose（前端静态占位，对应正文「前端容器」角色）。

**路径**均相对于 **dev-team-skills** 仓库根目录。

**inputs/intent-*.md** 与各 Skill 小节中**自然语言意图示例**一致；**chapter09-*.md** 与 **output/pipeline-*/** 下典型报告由命令**本地生成**，不随仓库提供 Golden。

## 初始化（含 .git 与 tag v1.1.0）

```bash
bash examples/chapter-09/init-release-demo.sh
```

迷你仓库的 .git 可加入本仓库 .gitignore；若删除后需复现，请重新执行上述脚本。

## 分步命令

在仓库根目录（完整参数与顺序如下；书正文以对话说明为主）：

```bash
cd examples/chapter-09/release-demo

bash ../../../.opencode/skills/deploy-check/scripts/check.sh \
  --output ../chapter09-check-report.md

bash ../../../.opencode/skills/deploy-changelog/scripts/generate.sh \
  --version v1.2.0 \
  --output ../chapter09-CHANGELOG.md

cd ..
python3 ../../.opencode/skills/deploy-release/scripts/generate.py \
  --version v1.2.0 \
  --changelog chapter09-CHANGELOG.md \
  --output chapter09-release-notes.md
```

## deploy-pipeline 一键

```bash
cd examples/chapter-09/release-demo
bash ../../../.opencode/skills/deploy-pipeline/scripts/run-all.sh \
  --version v1.2.0 \
  --output ../output/pipeline-v1.2.0
```

期望得到 **output/pipeline-v1.2.0/** 下 **0-summary.md**、**1-check-report.md**、**2-CHANGELOG.md**、**3-release-notes.md**（本地生成）。

## 与书稿 Skill 名称

| 书稿用语 | 配套 .opencode/skills/ |
|----------|------------------------|
| deploy-check | deploy-check |
| deploy-changelog | deploy-changelog |
| deploy-release | deploy-release |
| deploy-pipeline | deploy-pipeline |

**docker-compose-setup**、**docker-basics** 以正文模板与 **docker-basics** 速查为主；若未附带可执行 **generate.py**，以 **init-release-demo.sh** 产物与正文 Dockerfile 片段对照即可。
