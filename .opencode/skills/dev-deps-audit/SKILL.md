---
name: dev-deps-audit
description: 审计 Next.js 前端 + FastAPI 后端依赖，列出已知 CVE 漏洞——前端 npm audit、后端 pip-audit
---

# Dev Deps Audit - 依赖安全检查

封装 `npm audit`（Next.js）和 `pip-audit`（FastAPI），合并输出统一的 Markdown 报告。本 Skill 不追求通用性，只针对本书示例栈（Next.js + FastAPI）。

## 触发场景

- 发版前的安全自检
- 安全团队通报新 CVE，快速确认本项目是否受影响
- 季度依赖升级

## 目录结构

```
dev-deps-audit/
├── SKILL.md
└── scripts/
    └── audit.sh
```

## 依赖

- 前端：`npm` 已安装（系统装了 Node.js 就有）
- 后端：`pip-audit` 已安装（`pip install pip-audit`）

## 使用方法

```bash
# 默认扫描 ./blog/frontend 和 ./blog/backend
.opencode/skills/dev-deps-audit/scripts/audit.sh

# 自定义目录 + 输出报告到文件
.opencode/skills/dev-deps-audit/scripts/audit.sh \
  ./my-frontend ./my-backend ./reports/deps-audit.md
```

参数（位置参数）：
1. 前端目录（默认 `./blog/frontend`），需含 `package.json`
2. 后端目录（默认 `./blog/backend`），需含 `requirements.txt`
3. 输出报告路径（可选，默认输出到 stdout）

## 输出格式

合并的 Markdown 报告，含两节（前端 / 后端），每节包裹原工具的文本输出 + 一段修复建议。

## 边界

- 只针对 Next.js + FastAPI，其他栈不支持（保持简单——书里只用这两个）
- 仅做依赖级别 CVE 扫描，不做代码层面安全审计
- 工具未安装时跳过该侧并提示（不会让脚本失败）
- 不自动升级依赖，只输出建议
- 误报存在（某些 CVE 不影响本项目使用方式），最终判断由人做
