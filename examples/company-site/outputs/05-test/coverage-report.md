# 覆盖率报告（pytest --cov）

## 总体：72.3%（达标线 70%）

## 按模块
| 模块 | 行覆盖 | 分支覆盖 | 备注 |
|------|--------|---------|------|
| server/dao | 89.4% | 81.2% | 优秀 |
| server/web/api/uploads | 78.5% | 70.0% | 达标 |
| server/web/api/products | 81.6% | 75.4% | 达标 |
| server/web/api/comments | 65.3% | 52.1% | ❌ 未达标 |
| server/auth.py | 70.1% | 60.0% | 达标 |

## 整改建议
- comments 模块缺 target_type 多态分支测试，至少补 4 条
- auth 模块的 refresh rotate 失效分支需补 1 条

## 采集命令

```bash
cd backend
pytest --cov=server --cov-report=xml:coverage.xml --cov-report=term
opencode run test-coverage \
    --input coverage.xml \
    --output ../outputs/05-test/coverage-report.md
```
