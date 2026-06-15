# 第 11 章示例：故障排查

本目录为书稿第 11 章配套说明；可执行脚本在 **.opencode/skills/incident-***。演示容器使用第 9 章 **examples/chapter-09/release-demo/** 启动后的实例。

**路径**相对于 **dev-team-skills** 仓库根目录。

**inputs/intent-incident-*.md** 与书稿各小节**自然语言意图示例**一致；**output/** 下报告由读者本地生成，请先 **mkdir -p examples/chapter-11/output**（或自定目录）。

## 前置条件

- **release-demo** 已启动，**docker ps** 能看到 **backend** 容器（示例名 **release-demo-backend-1**，以本机为准）。

## 分步命令

```bash
mkdir -p examples/chapter-11/output

bash .opencode/skills/incident-container/scripts/diagnose.sh \
  --container release-demo-backend-1 \
  --output examples/chapter-11/output/1-container-diagnosis.md

python3 .opencode/skills/incident-log/scripts/analyze.py \
  --container release-demo-backend-1 \
  --since 1h \
  --output examples/chapter-11/output/2-log-analysis.md

python3 .opencode/skills/incident-report/scripts/generate.py \
  --title "release-demo backend 异常演练" \
  --severity P2 \
  --duration 15 \
  --output examples/chapter-11/output/3-postmortem.md
```

## 一键排查：incident-pipeline

```bash
bash .opencode/skills/incident-pipeline/scripts/run-all.sh \
  --container release-demo-backend-1 \
  --output examples/chapter-11/output/incident-pipeline-run
```

## 与书稿用语对照

| 书稿旧称 | 配套仓库 `.opencode/skills/` |
|----------|------------------------------|
| container-diagnose | incident-container |
| log-rca | incident-log |
| fix-advisor | （无独立脚本；诊断报告中含修复建议，团队可自建 playbook 模板） |
| incident-report | incident-report |
| troubleshoot-master | incident-pipeline |
