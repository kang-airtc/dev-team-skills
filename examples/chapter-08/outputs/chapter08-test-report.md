# 测试执行报告

**报告时间**: 2026-05-02 14:17
**测试文件数**: 1

## 执行概况

| 指标 | 数值 |
|------|------|
| **总用例数** | 18 |
| **通过** | 15 ✅ |
| **失败** | 2 ❌ |
| **跳过** | 1 ⏭️ |
| **错误** | 0 |
| **通过率** | 83.33% |
| **总耗时** | 12.5s |

## 失败用例详情

### tests.test_api_auth.TestLogin::test_login_wrong_password

- **状态**: ❌ failed
- **耗时**: 0.22s

- **错误信息**:
  AssertionError: 200 != 401
  


### tests.test_api_comments.TestUpdateComment::test_update_comment_not_found

- **状态**: ❌ failed
- **耗时**: 0.13s

- **错误信息**:
  AssertionError: comment found unexpectedly


## 慢测试（Top 5）

| 用例 | 耗时 | 状态 |
|------|------|------|
| tests.test_dao_user.TestUserDao::test_create_and_query_user | 9.82s | ✅ |
| tests.test_api_auth.TestLogin::test_login_success | 0.23s | ✅ |
| tests.test_api_auth.TestLogin::test_login_wrong_password | 0.22s | ❌ |
| tests.test_api_comments.TestCreateComment::test_create_comment_authorized | 0.20s | ✅ |
| tests.test_api_comments.TestUpdateComment::test_update_comment_owner | 0.19s | ✅ |

⚠️ 测试通过率良好，建议修复失败用例。