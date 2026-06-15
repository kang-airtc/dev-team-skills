---
name: test-unit
description: 读取Python源代码文件，自动生成pytest风格的单元测试用例
---

# Test Unit - 单元测试生成

读取Python源代码，提取函数签名和文档字符串，自动生成pytest风格的单元测试代码。

## 触发场景

- 写完函数后，不想手动写测试用例
- 快速为模块建立基础测试覆盖
- 需要遵循统一测试格式
- 重构前想补全测试

## 目录结构

```
test-unit/
├── SKILL.md
├── scripts/
│   └── generate.py
└── assets/
    └── test-template.md
```

## 依赖

- Python 标准库（`ast`、`inspect`）

## 使用方法

```bash
# 为单个文件生成测试
python3 .opencode/skills/test-unit/scripts/generate.py \
  --input src/auth.py \
  --output tests/test_auth.py

# 为整个目录生成测试
python3 .opencode/skills/test-unit/scripts/generate.py \
  --input src/ \
  --output tests/
```

参数：
- `--input, -i`：源代码文件或目录
- `--output, -o`：输出测试文件路径

## 生成规则

| 函数特征 | 生成的测试 |
|---------|-----------|
| 返回布尔值 | `assert func() is True/False` |
| 返回数值 | 正常值、边界值、异常值 |
| 有参数 | 参数组合：正常、空值、非法值 |
| 抛出异常 | `with pytest.raises(Exception)` |
| 有类型注解 | 基于类型生成测试数据 |

## 输出示例

输入 `auth.py`：
```python
def login(username: str, password: str) -> dict:
    """用户登录"""
    pass

def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pass
```

输出 `test_auth.py`：
```python
import pytest
from auth import login, validate_email

class TestLogin:
    def test_login_success(self):
        result = login("admin", "123456")
        assert result is not None
        assert "token" in result

    def test_login_empty_username(self):
        with pytest.raises(ValueError):
            login("", "123456")

    def test_login_empty_password(self):
        with pytest.raises(ValueError):
            login("admin", "")

class TestValidateEmail:
    def test_valid_email(self):
        assert validate_email("test@example.com") is True

    def test_invalid_email_no_at(self):
        assert validate_email("testexample.com") is False

    def test_invalid_email_empty(self):
        assert validate_email("") is False
```

## 边界

- 只生成**骨架测试**，具体断言值需要人工补充
- 基于类型注解和文档字符串推断，**不理解业务逻辑**
- 复杂依赖（数据库、API调用）需要手动mock
- 不支持异步函数测试生成

## 与其他 Skill 的关系

```
test-unit ──▶ test-pipeline
  生成测试      整合流水线
```
