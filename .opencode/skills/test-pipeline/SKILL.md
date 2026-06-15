---
name: test-pipeline
description: 整合测试阶段所有Skill，提供一键式测试生成与分析流水线
---

# Test Pipeline - 测试助手流水线

整合 test-unit（单元测试生成）、test-api（接口测试生成）、test-coverage（覆盖率分析）、test-regression（回归分析）、test-report（报告生成），提供完整的测试协作流水线。

## 触发场景

- 功能开发完，一站式生成所有测试
- 测试运行后自动生成分析报告
- 需要完整的测试覆盖评估
- 团队协作时统一测试标准

## 目录结构

```
test-pipeline/
├── SKILL.md
└── scripts/
    ├── assistant.py
    └── run-all.sh
```

## 依赖

- Python 标准库
- 同级 `test-*` Skill

## 使用方法

### 方式一：一键完整流程

```bash
# 为当前项目生成测试和分析
./scripts/run-all.sh --source src/ --tests tests/

# 输出：
# test-output/
# ├── 1-unit-tests/           # 自动生成的单元测试
# ├── 2-api-tests/            # 自动生成的接口测试
# ├── 3-regression-checklist.md  # 回归测试清单
# └── 4-coverage-report.md    # 覆盖率报告（如提供coverage.xml）
```

### 方式二：分步执行

```bash
./scripts/run-all.sh --step unit --source src/auth.py
# 可选步骤：unit / api / regression / coverage / report
```

### 方式三：交互式助手

```bash
python3 scripts/assistant.py
```

## 流水线步骤

```
1. test-unit       为源代码生成单元测试
2. test-api        为接口生成接口测试（如提供openapi.yaml）
3. test-regression  分析变更范围，生成回归清单
4. test-coverage    分析覆盖率报告（如提供coverage.xml）
5. test-report      汇总测试结果生成报告
```


## 边界

- 一键流程会覆盖已有测试文件
- 生成的测试代码需要人工完善断言
- 覆盖率分析需要项目先运行测试生成报告
- 回归分析基于文件路径推断，不分析代码依赖

## 完整工作流

```
功能开发完成
    │
    ▼
┌──────────────┐
│ test-unit     │ ──> test_xxx.py（自动生成）
│ （单元测试）   │      需人工补充断言
└──────────────┘
    │
    ▼
┌──────────────┐
│ test-api      │ ──> test_api_xxx.py（自动生成）
│ （接口测试）   │      需配置BASE_URL
└──────────────┘
    │
    ▼
（运行测试后）
    │
    ▼
┌──────────────┐
│ test-regression│ ──> regression-checklist.md
│ （回归分析）   │      基于git diff推荐测试范围
└──────────────┘
    │
    ▼
┌──────────────┐
│ test-coverage │ ──> coverage-report.md
│ （覆盖率分析） │      解析coverage.xml
└──────────────┘
    │
    ▼
┌──────────────┐
│ test-report   │ ──> test-report.md
│ （测试报告）   │      汇总所有结果
└──────────────┘
```

## 与其他 Skill 的关系

```
test-unit ──┬──▶ test-pipeline
test-api ───┤     （整合编排）
test-regression┤
test-coverage─┤
test-report ──┘
```
