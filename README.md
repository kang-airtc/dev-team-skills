# 《Agent Skill 开发与实践：构建可复用的 AI 自动化技能体系》随书源码

本仓库是《Agent Skill 开发与实践：构建可复用的 AI 自动化技能体系》一书的随书源码，包含书中各章节的 opencode Agent Skill 示例与配套工程，可作为一个面向开发团队的完整技能集合直接运行。

## Skill 目录一览

全部 Skill 位于 `.opencode/skills/` 目录下，按章节阶段以前缀命名。

### 第 03 章 · 基础三形态（`base-`）

| Skill | 说明 |
|-------|------|
| base-summarize | 读取一个文件或目录，输出结构化的内容摘要——包含用途、核心要点、关键依赖、潜在问题四个维度 |
| base-dir-view | 列出指定目录的树形结构，附带每个文件的大小和修改时间，自动跳过 node_modules、.git、venv 等噪声目录 |
| base-word-export | 把 Markdown 文件导出为 Word 文档（.docx），支持标题、段落、列表、代码块四种基本元素 |

### 第 04 章 · 需求管理（`req-`）

| Skill | 说明 |
|-------|------|
| req-clarify | 通过结构化提问，将模糊的用户需求转化为清晰、可执行的需求描述 |
| req-prd | 基于澄清后的需求，自动生成 PRD（产品需求文档）标准结构 |
| req-decompose | 将 PRD 中的大需求拆解为可执行的用户故事和任务 |
| req-storymap | 将用户故事组织成二维地图，展示用户旅程和功能全景 |
| req-flowchart | 将需求中的业务流程转化为 Mermaid 流程图 |
| req-track | 版本化管理需求变更，记录变更历史，评估影响范围 |
| req-pipeline | 整合需求阶段的所有 Skill，提供一键式需求管理流水线 |

### 第 05 章 · 设计协作（`design-`）

| Skill | 说明 |
|-------|------|
| design-review | 读取设计稿截图，按多角色（UI、前端、产品、后端）视角进行设计评审，输出带优先级的评审报告 |
| design-sprint | 提供 5 天设计冲刺的完整流程模板，按天推进设计任务并跟踪产出物 |
| design-pencil | 通过 Pencil MCP 连接 Pencil.dev，用自然语言描述界面需求，在画布上生成低保真设计稿（.pen 文件） |
| design-ui-check | 检查设计稿是否符合设计系统规范，包括颜色、字体、间距、圆角等 |
| design-discuss | 针对设计方案的多选项决策，模拟多角色讨论并输出结构化决策记录 |

### 第 06 章 · 开发实现（`dev-`）

| Skill | 说明 |
|-------|------|
| dev-techspec | 按统一模板生成技术方案文档（Markdown），覆盖背景、目标、方案对比、详细设计、风险、里程碑等标准章节 |
| dev-arch | 根据文字描述或项目结构，生成软件架构图（draw.io 格式 .drawio 文件） |
| dev-sequence | 根据消息流描述生成时序图（draw.io 格式 .drawio 文件），用于接口调用、登录、支付链路等场景 |
| dev-apidoc | 从 FastAPI / OpenAPI 规范生成 Word 格式接口文档（.docx），用于交付或归档 |
| dev-db | 从 model-spec.md 生成 SQLAlchemy 2.x Mapped 语法的 ORM 模型 |
| dev-migrate | 从 migration-spec.md 生成 Alembic 升降级迁移脚本（downgrade 与 upgrade 严格镜像） |
| dev-backend | 从 api-spec.md 生成 FastAPI schema + views 骨架（Pydantic v2、ApiResponse 包装、JWT 鉴权注入） |
| dev-backend-dao | 从 dao-spec.md 生成 SQLAlchemy 2.x async DAO（list_ 含子查询计数、create/update 含 refresh） |
| dev-frontend | 根据 page-spec.md 生成 Next.js App Router 页面骨架（.tsx），含数据加载、骨架屏、空态与列表渲染三段式结构 |
| dev-frontend-form | 根据 form-spec.md 生成 Next.js App Router 后台 CRUD 表单骨架，含四种状态（正常/提交中/成功/失败）处理 |
| dev-backend-lint | 检查后端代码是否遵守团队规范——统一 {code,msg,data} 响应格式、错误码段、ORM 查询规范等 |
| dev-frontend-lint | 检查前端代码是否遵守团队规范——组件命名、错误码消费、API 调用统一封装、样式规范等 |
| dev-spec-diff | 对比当前代码与团队规范文档，输出偏差清单（违反、未使用、需补充） |
| dev-deps-audit | 审计 Next.js 前端 + FastAPI 后端依赖，列出已知 CVE 漏洞（npm audit / pip-audit） |
| dev-pipeline | 整合开发阶段 10 个 Skill，按文档线（可并行）+ 代码线（串行）编排，一键产出完整模块代码与文档 |

### 第 07 章 · 代码质量与协作（`review-` / Git）

| Skill | 说明 |
|-------|------|
| review-frontend | 检查前端新增代码是否符合团队规范——命名、TypeScript、API 封装、错误码消费、TailwindCSS、import 顺序等 |
| review-backend | 检查后端新增代码是否符合团队规范——响应格式、错误码、命名、异常处理、日志、ORM 查询、Pydantic Schema 等 |
| git-helper | Git 日常助手——提交代码、生成提交信息、管理分支、检查提交规范、起草 PR 描述 |

### 第 08 章 · 测试保障（`test-`）

| Skill | 说明 |
|-------|------|
| test-unit | 读取 Python 源代码文件，自动生成 pytest 风格的单元测试用例 |
| test-api | 读取 OpenAPI 或接口定义，自动生成 pytest+requests 风格的接口测试代码 |
| test-coverage | 解析 coverage.xml 或 lcov.info 测试覆盖率报告，生成结构化的覆盖率分析报告 |
| test-regression | 基于 git diff 分析变更影响范围，推荐需要回归测试的用例和模块 |
| test-report | 解析 pytest JUnit XML 或 JSON 测试结果，生成结构化的测试报告文档 |
| test-pipeline | 整合测试阶段所有 Skill，提供一键式测试生成与分析流水线 |

### 第 09 章 · 发布上线（`deploy-` / Docker）

| Skill | 说明 |
|-------|------|
| deploy-check | 发布前检查 Docker 镜像、docker-compose 配置、环境变量、端口冲突和健康检查 |
| deploy-changelog | 基于 git log 和 conventional commit 规范，自动生成版本变更日志 CHANGELOG.md |
| deploy-release | 生成版本发布说明文档，包含版本号、变更摘要、升级指南和回滚方案 |
| deploy-pipeline | 整合发布阶段所有 Skill，提供一键式应用发布流水线——检查、生成 CHANGELOG、发布说明 |
| docker-basics | Docker 与 docker compose 日常操作命令速查（启停、日志、进容器、镜像清理、状态诊断） |
| docker-compose-setup | 根据 project-spec.yaml 渲染前后端 Dockerfile、docker-compose.yml 与启停脚本，搭出三服务最小可运行容器化骨架 |

### 第 10 章 · 运维监控（`monitor-`）

| Skill | 说明 |
|-------|------|
| monitor-containers | 监控 Docker 容器状态，检测异常容器（Exited/Restarting/Unhealthy），输出巡检报告 |
| monitor-logs | 分析 Docker 容器日志，检测 ERROR/FATAL 关键字，统计日志量，输出日志巡检报告 |
| monitor-backup | 执行 PostgreSQL 数据库备份，生成带时间戳的备份文件，输出备份报告 |
| monitor-health | 综合容器状态、日志、资源使用情况，生成系统健康报告 |
| monitor-pipeline | 整合监控阶段所有 Skill，提供一键式系统巡检流水线——容器、日志、备份、健康报告 |

### 第 11 章 · 故障排查（`incident-`）

| Skill | 说明 |
|-------|------|
| incident-container | 诊断 Docker 容器异常（资源、网络、挂载），输出诊断报告和修复建议 |
| incident-log | 分析容器日志中的错误模式，按时间线聚合异常，识别根因 |
| incident-report | 生成故障复盘报告，包含时间线、根因、改进措施模板 |
| incident-pipeline | 整合故障排查阶段所有 Skill，提供一键式故障诊断流水线——容器诊断、日志分析、复盘报告 |

### 第三方 Skill

| Skill | 说明 |
|-------|------|
| ui-ux-pro-max | UI/UX 设计智能库（外部 Skill），内置可检索的设计风格、配色、字体与组件数据库 |

## 快速开始

```bash
# 1. 安装依赖环境
python3 setup.py

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 在工程根目录启动 OpenCode，按对话调用任意 Skill
opencode
```

## 许可证

MIT，详见 [LICENSE](LICENSE)。
