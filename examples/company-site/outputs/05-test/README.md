# 05-test · 测试阶段产出物

| 文件 | 来源 Skill | 说明 |
|------|-----------|------|
| `coverage-report.md` | `test-coverage` | 覆盖率分析（按模块） |
| `regression-scope.md` | `test-regression` | 影响范围分析 |
| `test-report.md` | `test-report` | JUnit XML → 测试报告 |

> 测试代码（`test-unit` / `test-api` 产出）直接落到 `backend/tests/`：
>
> - `tests/test_product_dao.py`
> - `tests/test_api_products.py`
> - `tests/test_api_uploads.py`
