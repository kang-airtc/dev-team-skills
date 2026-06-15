---
name: test-api
description: 读取OpenAPI或接口定义，自动生成pytest+requests风格的接口测试代码
---

# Test API - 接口测试生成

读取OpenAPI YAML/JSON或Markdown格式的接口文档，自动生成基于pytest+requests的接口测试脚本。

## 触发场景

- 接口开发完，需要写接口测试
- 快速建立接口回归测试集
- 需要统一的接口测试格式
- 接口文档变更后同步更新测试

## 目录结构

```
test-api/
├── SKILL.md
├── scripts/
│   └── generate.py
└── assets/
    └── api-test-template.md
```

## 依赖

- Python 标准库（`json`、`yaml`）

## 使用方法

```bash
# 从 OpenAPI 文件生成
python3 .opencode/skills/test-api/scripts/generate.py \
  --input openapi.yaml \
  --output tests/test_api.py

# 从 Markdown 接口文档生成
python3 .opencode/skills/test-api/scripts/generate.py \
  --input api-doc.md \
  --format markdown \
  --output tests/test_api.py
```

参数：
- `--input, -i`：接口文档路径
- `--format`：文档格式（`openapi` | `markdown`），自动检测
- `--output, -o`：输出测试文件路径

## 生成规则

| 接口特征 | 生成的测试 |
|---------|-----------|
| GET 查询 | 正常查询、参数缺失、非法参数 |
| POST 创建 | 正常创建、必填字段缺失、字段格式错误 |
| PUT/PATCH 更新 | 正常更新、资源不存在、部分更新 |
| DELETE 删除 | 正常删除、重复删除、权限不足 |

## 输出示例

输入接口定义：
```yaml
POST /api/users:
  parameters:
    - name: username
      required: true
    - name: email
      required: true
  responses:
    201: 创建成功
    400: 参数错误
    409: 用户已存在
```

输出测试代码：
```python
import requests
import pytest

BASE_URL = "http://localhost:8000"

class TestUsersApi:
    def test_create_user_success(self):
        """测试正常创建用户"""
        payload = {
            "username": "testuser",
            "email": "test@example.com"
        }
        response = requests.post(f"{BASE_URL}/api/users", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data

    def test_create_user_missing_username(self):
        """测试缺少必填字段"""
        payload = {
            "email": "test@example.com"
        }
        response = requests.post(f"{BASE_URL}/api/users", json=payload)
        assert response.status_code == 400

    def test_create_user_duplicate(self):
        """测试重复创建"""
        payload = {
            "username": "existing_user",
            "email": "test@example.com"
        }
        response = requests.post(f"{BASE_URL}/api/users", json=payload)
        assert response.status_code == 409
```

## 边界

- 只生成**测试骨架**，具体URL、认证方式、数据准备需要人工配置
- 基于接口定义生成，**不理解业务逻辑**
- 复杂鉴权（OAuth、JWT）需要手动处理
- 文件上传、WebSocket等特殊接口不支持

## 与其他 Skill 的关系

```
test-api ──▶ test-pipeline
  接口测试      整合流水线
```
