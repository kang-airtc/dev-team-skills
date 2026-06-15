#!/usr/bin/env python3
"""
接口测试生成器
读取OpenAPI或接口文档，生成pytest+requests测试代码
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_openapi(doc_path: Path) -> list:
    """解析OpenAPI文档"""
    content = doc_path.read_text(encoding='utf-8')
    
    # 简化的OpenAPI解析（支持YAML和JSON）
    # 实际实现需要更完整的解析
    apis = []
    
    # 尝试解析JSON
    try:
        data = json.loads(content)
        paths = data.get("paths", {})
        for path, methods in paths.items():
            for method, spec in methods.items():
                if method in ["get", "post", "put", "patch", "delete"]:
                    api_info = {
                        "path": path,
                        "method": method.upper(),
                        "summary": spec.get("summary", ""),
                        "parameters": [],
                        "responses": list(spec.get("responses", {}).keys())
                    }
                    
                    # 解析参数
                    for param in spec.get("parameters", []):
                        api_info["parameters"].append({
                            "name": param.get("name", ""),
                            "required": param.get("required", False),
                            "type": param.get("schema", {}).get("type", "string")
                        })
                    
                    # 解析请求体
                    if "requestBody" in spec:
                        content = spec["requestBody"].get("content", {})
                        if "application/json" in content:
                            schema = content["application/json"].get("schema", {})
                            if "properties" in schema:
                                for prop_name, prop_spec in schema["properties"].items():
                                    api_info["parameters"].append({
                                        "name": prop_name,
                                        "required": prop_name in schema.get("required", []),
                                        "type": prop_spec.get("type", "string")
                                    })
                    
                    apis.append(api_info)
    except json.JSONDecodeError:
        # 简化的YAML/Markdown解析
        pass
    
    return apis


def parse_markdown(doc_path: Path) -> list:
    """解析Markdown格式的接口文档"""
    content = doc_path.read_text(encoding='utf-8')
    apis = []
    
    # 匹配常见的接口定义格式
    # 例如：POST /api/users 或 ### 创建用户 [POST /api/users]
    patterns = [
        r'(GET|POST|PUT|PATCH|DELETE)\s+(/[\w/-]+)',
        r'\[(GET|POST|PUT|PATCH|DELETE)\s+(/[\w/-]+)\]'
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            apis.append({
                "path": match.group(2),
                "method": match.group(1).upper(),
                "summary": "",
                "parameters": [],
                "responses": ["200"]
            })
    
    return apis


def generate_test_case(api: dict) -> str:
    """为单个接口生成测试用例"""
    method = api["method"]
    path = api["path"]
    path_var = path.replace("/", "_").replace("{", "").replace("}", "")
    
    lines = [f"    def test_{method.lower()}_{path_var}_success(self):"]
    lines.append(f'        """测试 {method} {path} 正常情况"""')
    lines.append(f"        ")
    
    # 生成请求参数
    if api["parameters"]:
        lines.append(f"        # 请求参数")
        lines.append(f"        payload = {{")
        for param in api["parameters"]:
            if param.get("required"):
                param_type = param.get("type", "string")
                if param_type == "string":
                    lines.append(f'            "{param["name"]}": "test_{param["name"]}",')
                elif param_type == "integer":
                    lines.append(f'            "{param["name"]}": 1,')
                elif param_type == "boolean":
                    lines.append(f'            "{param["name"]}": True,')
                else:
                    lines.append(f'            "{param["name"]}": "test",')
        lines.append(f"        }}")
        lines.append(f"        ")
    
    # 生成请求代码
    if method == "GET":
        if api["parameters"]:
            lines.append(f'        response = requests.get(f"{{BASE_URL}}{path}", params=payload)')
        else:
            lines.append(f'        response = requests.get(f"{{BASE_URL}}{path}")')
    elif method in ["POST", "PUT", "PATCH"]:
        lines.append(f'        response = requests.{method.lower()}(f"{{BASE_URL}}{path}", json=payload)')
    elif method == "DELETE":
        lines.append(f'        response = requests.delete(f"{{BASE_URL}}{path}")')
    
    lines.append(f"        ")
    
    # 生成断言
    lines.append(f"        # 状态码断言")
    if method == "POST":
        lines.append(f"        assert response.status_code == 201")
    elif method == "DELETE":
        lines.append(f"        assert response.status_code == 204")
    else:
        lines.append(f"        assert response.status_code == 200")
    
    lines.append(f"        ")
    lines.append(f"        # 响应体断言（根据实际接口调整）")
    lines.append(f"        data = response.json()")
    lines.append(f"        assert data is not None")
    
    lines.append(f"        ")
    
    # 生成异常情况测试
    if api["parameters"] and any(p.get("required") for p in api["parameters"]):
        lines.append(f"    def test_{method.lower()}_{path_var}_missing_required(self):")
        lines.append(f'        """测试 {method} {path} 缺少必填字段"""')
        lines.append(f"        ")
        lines.append(f"        payload = {{}}")
        lines.append(f"        ")
        if method in ["POST", "PUT", "PATCH"]:
            lines.append(f'        response = requests.{method.lower()}(f"{{BASE_URL}}{path}", json=payload)')
        else:
            lines.append(f'        response = requests.{method.lower()}(f"{{BASE_URL}}{path}")')
        lines.append(f"        ")
        lines.append(f"        assert response.status_code == 400")
        lines.append(f"        ")
    
    return "\n".join(lines)


def generate_test_file(apis: list) -> str:
    """生成完整测试文件"""
    lines = [
        "import requests",
        "import pytest",
        "",
        "# 由 test-api Skill 自动生成",
        "# 接口数: {}".format(len(apis)),
        "",
        "# TODO: 根据实际环境修改 BASE_URL",
        'BASE_URL = "http://localhost:8000"',
        "",
        "# TODO: 如需认证，在此添加 headers 或 cookies",
        "# HEADERS = {\"Authorization\": \"Bearer token\"}",
        "",
    ]
    
    # 按接口分组
    for api in apis:
        class_name = "Test" + api["path"].replace("/", "_").replace("{", "").replace("}", "").title()
        lines.append(f"class {class_name}:")
        lines.append(f'    """测试 {api["method"]} {api["path"]}"""')
        lines.append("")
        lines.append(generate_test_case(api))
        lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='接口测试生成器')
    parser.add_argument('--input', '-i', required=True, help='接口文档路径')
    parser.add_argument('--format', choices=['openapi', 'markdown'], help='文档格式')
    parser.add_argument('--output', '-o', default='tests/test_api.py', help='输出路径')
    args = parser.parse_args()
    
    doc_path = Path(args.input)
    if not doc_path.exists():
        print(f"[错误] 文件不存在: {doc_path}")
        sys.exit(1)
    
    # 检测格式
    doc_format = args.format
    if not doc_format:
        if doc_path.suffix in ['.yaml', '.yml', '.json']:
            doc_format = 'openapi'
        else:
            doc_format = 'markdown'
    
    print(f"[信息] 解析格式: {doc_format}")
    
    # 解析文档
    if doc_format == 'openapi':
        apis = parse_openapi(doc_path)
    else:
        apis = parse_markdown(doc_path)
    
    print(f"[信息] 发现 {len(apis)} 个接口")
    
    if not apis:
        print("[警告] 未找到接口定义")
        sys.exit(0)
    
    # 生成测试
    test_content = generate_test_file(apis)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(test_content, encoding='utf-8')
    
    print(f"[成功] 接口测试已生成: {output_path}")
    for api in apis:
        print(f"   - {api['method']} {api['path']}")


if __name__ == "__main__":
    main()
