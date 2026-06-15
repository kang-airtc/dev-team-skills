---
name: test-coverage
description: 解析coverage.xml或lcov.info测试覆盖率报告，生成结构化的覆盖率分析报告
---

# Test Coverage - 覆盖率分析

读取项目运行测试后生成的覆盖率报告（coverage.xml 或 lcov.info），分析并生成可读性强的 Markdown 报告。

## 触发场景

- 运行测试后想看覆盖率汇总
- 找出覆盖率低的文件
- 生成测试覆盖率周报
- 对比多次测试的覆盖率变化

## 目录结构

```
test-coverage/
├── SKILL.md
├── scripts/
│   └── analyze.py
└── assets/
    └── coverage-report-template.md
```

## 依赖

- Python 标准库（`xml.etree.ElementTree`）

## 使用方法

```bash
# 分析 coverage.xml（pytest-cov 生成）
python3 .opencode/skills/test-coverage/scripts/analyze.py \
  --input coverage.xml \
  --output coverage-report.md

# 分析 lcov.info（JavaScript/Go 项目）
python3 .opencode/skills/test-coverage/scripts/analyze.py \
  --input lcov.info \
  --format lcov \
  --output coverage-report.md

# 对比两次覆盖率报告
python3 .opencode/skills/test-coverage/scripts/analyze.py \
  --input coverage.xml \
  --compare old-coverage.xml \
  --output coverage-diff.md
```

参数：
- `--input, -i`：覆盖率报告文件
- `--format`：报告格式（`xml` | `lcov`），自动检测
- `--compare`：对比的历史报告
- `--output, -o`：输出路径

## 输入来源

**pytest 项目**：
```bash
pytest --cov=src --cov-report=xml
# 生成 coverage.xml
```

**JavaScript 项目**：
```bash
nyc --reporter=lcov npm test
# 生成 lcov.info
```

**Go 项目**：
```bash
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html
```

## 输出格式

```markdown
# 测试覆盖率分析报告

**报告时间**: 2024-01-15
**分析文件**: coverage.xml

## 总体概况

| 指标 | 数值 | 状态 |
|------|------|------|
| **总行数** | 3,240 | - |
| **覆盖行数** | 2,850 | - |
| **覆盖率** | 87.96% | ✅ 达标 |
| **文件数** | 42 | - |

## 覆盖率分布

| 覆盖率区间 | 文件数 | 占比 |
|-----------|--------|------|
| 90-100% | 15 | 35.7% |
| 80-90% | 12 | 28.6% |
| 60-80% | 8 | 19.0% |
| 0-60% | 7 | 16.7% |

## 低覆盖率文件（需关注）

| 文件 | 覆盖率 | 未覆盖行数 | 建议 |
|------|--------|-----------|------|
| src/utils/email.py | 45% | 11 | 补充边界测试 |
| src/api/payment.py | 52% | 18 | 补充异常分支测试 |
| src/models/order.py | 58% | 9 | 补充状态转换测试 |

## 对比上次（2024-01-08）

| 指标 | 上次 | 本次 | 变化 |
|------|------|------|------|
| 覆盖率 | 85.2% | 87.96% | +2.76% ✅ |
| 覆盖行数 | 2,760 | 2,850 | +90 |

## 改进建议

1. 优先提升 email.py 和 payment.py 的覆盖率
2. 关注新增代码的测试覆盖
3. 建议设置 80% 的覆盖率门槛
```

## 边界

- **不运行测试**，只分析已生成的报告文件
- 不支持实时覆盖率监控
- 复杂分支覆盖需要人工分析
- 对比功能需要两次报告格式一致

## 与其他 Skill 的关系

```
test-coverage ──▶ test-pipeline
  覆盖率分析      整合流水线
```
