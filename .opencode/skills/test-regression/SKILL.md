---
name: test-regression
description: 基于git diff分析变更影响范围，推荐需要回归测试的用例和模块
---

# Test Regression - 回归测试范围分析

读取 `git diff` 的变更文件列表，分析影响范围，推荐需要回归测试的模块和测试用例。

## 触发场景

- 代码变更后，不确定需要跑哪些测试
- 评估变更影响范围
- 生成回归测试清单
- 避免全量测试浪费时间

## 目录结构

```
test-regression/
├── SKILL.md
├── scripts/
│   └── analyze.sh
└── assets/
    └── impact-map.md
```

## 依赖

- `git`
- `grep`
- 仅使用 Shell

## 使用方法

```bash
# 分析当前分支相对 main 的变更
bash .opencode/skills/test-regression/scripts/analyze.sh --base main

# 指定输出文件
bash .opencode/skills/test-regression/scripts/analyze.sh --base main --output regression-checklist.md
```

参数：
- `--base, -b`：基础分支，默认 `main`
- `--output, -o`：输出路径，默认 `regression-checklist.md`

## 分析规则

| 变更文件 | 推荐测试 |
|---------|---------|
| `src/api/*.py` | 接口测试、集成测试 |
| `src/models/*.py` | 单元测试、数据库测试 |
| `src/utils/*.py` | 单元测试、工具函数测试 |
| `frontend/components/*.jsx` | 组件测试、E2E测试 |
| `database/migrations/*.sql` | 数据迁移测试、回归测试 |
| `config/*.yaml` | 配置加载测试、环境测试 |

## 输出格式

```markdown
# 回归测试范围分析

**变更分支**: feature/login → main
**变更文件数**: 8
**分析时间**: 2024-01-15

## 变更概览

| 文件 | 类型 | 影响等级 |
|------|------|---------|
| src/api/auth.py | API层 | 🔴 高 |
| src/models/user.py | 数据层 | 🟡 中 |
| src/utils/jwt.py | 工具层 | 🟡 中 |
| frontend/pages/login.jsx | 前端页面 | 🟡 中 |
| config/auth.yaml | 配置 | 🟢 低 |

## 推荐回归测试

### 🔴 高优先级（必须测试）

- [ ] 登录接口测试（正常/异常流程）
- [ ] Token生成与验证测试
- [ ] 权限控制测试

### 🟡 中优先级（建议测试）

- [ ] 用户模型单元测试
- [ ] JWT工具函数测试
- [ ] 登录页面E2E测试

### 🟢 低优先级（可选测试）

- [ ] 配置加载测试

## 影响分析

**直接影响的模块**:
- 认证模块（auth）
- 用户管理模块（user）

**间接影响的模块**:
- 所有需要鉴权的接口
- 前端路由守卫

## 建议

1. 优先执行高优先级测试
2. 如涉及数据库变更，需执行迁移测试
3. 建议在 staging 环境做完整回归
```

## 边界

- 基于文件路径推断，**无法分析代码依赖关系**
- 复杂的间接影响需要人工判断
- 只推荐测试方向，不生成具体测试代码

## 与其他 Skill 的关系

```
test-regression ──▶ test-pipeline
  回归分析         整合流水线
```
