---
name: test-report
description: 解析pytest JUnit XML或JSON格式的测试结果，生成结构化的测试报告文档
---

# Test Report - 测试报告生成

读取 pytest、Jest、JUnit 等工具生成的测试结果文件（XML 或 JSON 格式），汇总并生成 Markdown 格式的测试报告。

## 触发场景

- 测试运行后生成可读性强的报告
- 汇总多次测试的结果
- 生成测试周报/月报
- 归档测试记录

## 目录结构

```
test-report/
├── SKILL.md
├── scripts/
│   └── generate.py
└── assets/
    └── report-template.md
```

## 依赖

- Python 标准库（`xml.etree.ElementTree`、`json`）

## 使用方法

```bash
# 解析 pytest 的 JUnit XML 输出
python3 .opencode/skills/test-report/scripts/generate.py \
  --input pytest-results.xml \
  --output test-report.md

# 解析多个测试结果
python3 .opencode/skills/test-report/scripts/generate.py \
  --input results1.xml results2.xml \
  --output combined-report.md

# 从 JSON 格式生成（pytest-json 插件）
python3 .opencode/skills/test-report/scripts/generate.py \
  --input results.json \
  --format json \
  --output test-report.md
```

参数：
- `--input, -i`：测试结果文件（支持多个）
- `--format`：格式（`xml` | `json`），自动检测
- `--output, -o`：输出路径，默认 `test-report.md`

## 输入来源

**pytest 生成 JUnit XML**：
```bash
pytest --junitxml=pytest-results.xml
```

**pytest 生成 JSON**：
```bash
pytest --json-report --json-report-file=results.json
```

**Jest 生成 JUnit XML**：
```bash
jest --reporters=jest-junit
# 生成 junit.xml
```

## 输出格式

```markdown
# 测试执行报告

**报告时间**: 2024-01-15 14:30
**测试文件**: pytest-results.xml

## 执行概况

| 指标 | 数值 |
|------|------|
| **总用例数** | 156 |
| **通过** | 148 ✅ |
| **失败** | 5 ❌ |
| **跳过** | 3 ⏭️ |
| **错误** | 0 |
| **通过率** | 94.87% |
| **总耗时** | 45.2s |

## 失败用例详情

### test_auth.py::TestLogin::test_login_expired_token

- **状态**: ❌ 失败
- **耗时**: 0.45s
- **错误信息**:
  ```
  assert response.status_code == 401
  AssertionError: 200 != 401
  ```
- **建议**: 检查 Token 过期时间逻辑

### test_order.py::TestOrder::test_create_order_insufficient_balance

- **状态**: ❌ 失败
- **耗时**: 1.23s
- **错误信息**:
  ```
  InsufficientBalanceError not raised
  ```
- **建议**: 检查余额校验逻辑

## 慢测试（Top 5）

| 用例 | 耗时 | 状态 |
|------|------|------|
| test_payment.py::test_third_party_api | 12.5s | ✅ |
| test_report.py::test_large_data_export | 8.3s | ✅ |
| test_sync.py::test_data_sync | 6.1s | ✅ |

## 按模块统计

| 模块 | 用例数 | 通过 | 失败 | 通过率 |
|------|--------|------|------|--------|
| auth | 24 | 22 | 2 | 91.7% |
| order | 36 | 34 | 2 | 94.4% |
| payment | 18 | 18 | 0 | 100% |

## 趋势（对比上次）

| 指标 | 上次 | 本次 | 变化 |
|------|------|------|------|
| 通过率 | 96.2% | 94.87% | -1.33% ❌ |
| 失败数 | 2 | 5 | +3 ❌ |
| 新增用例 | - | 12 | +12 |
```

## 边界

- **不运行测试**，只解析已生成的结果文件
- 需要测试框架支持 JUnit XML 或 JSON 输出格式
- 复杂的错误堆栈可能截断显示
- 趋势对比需要历史报告文件

## 与其他 Skill 的关系

```
test-report ──▶ test-pipeline
  测试报告      整合流水线
```
