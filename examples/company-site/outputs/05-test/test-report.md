# 测试报告

> 来源 Skill：`test-report`  
> 输入：`backend/junit.xml`  
> 运行环境：CI runner（python 3.11 + PG 15）

## 总览

| 指标 | 数值 |
|---|---|
| 总用例数 | 87 |
| 通过 | 87 |
| 失败 | 0 |
| 跳过 | 0 |
| 用时 | 12.4s |

## 按模块

| 模块 | 用例 | 通过 |
|---|---|---|
| `test_api_uploads.py` | 6 | 6 |
| `test_api_products.py` | 14 | 14 |
| `test_api_news.py` | 11 | 11 |
| `test_api_comments.py` | 8 | 8 |
| `test_auth.py` | 9 | 9 |
| `test_product_dao.py` | 12 | 12 |
| `test_news_dao.py` | 10 | 10 |
| `test_comment_dao.py` | 8 | 8 |
| `test_settings.py` | 4 | 4 |
| 其他 | 5 | 5 |

## 慢用例 Top 5

| 用例 | 用时 |
|---|---|
| `test_upload_too_large` | 1.2s |
| `test_create_product_with_gallery` | 0.8s |
| `test_list_products_with_filter` | 0.6s |
| `test_refresh_rotate_invalidates_old_token` | 0.5s |
| `test_seed_demo_idempotent` | 0.4s |

## 结论

全部通过，覆盖率达标，可进入发布阶段。
