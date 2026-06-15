#!/usr/bin/env python3
"""
单元测试生成器
读取Python源代码，自动生成pytest风格的单元测试
"""

import argparse
import ast
import sys
from pathlib import Path


def parse_source(source_path: Path) -> list:
    """解析Python源文件，提取函数定义"""
    content = source_path.read_text(encoding='utf-8')
    tree = ast.parse(content)
    
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # 跳过私有函数和特殊方法
            if node.name.startswith('_'):
                continue
            
            func_info = {
                "name": node.name,
                "args": [],
                "returns": None,
                "docstring": ast.get_docstring(node) or ""
            }
            
            # 解析参数
            for arg in node.args.args:
                arg_info = {
                    "name": arg.arg,
                    "type": None
                }
                if arg.annotation and isinstance(arg.annotation, ast.Name):
                    arg_info["type"] = arg.annotation.id
                func_info["args"].append(arg_info)
            
            # 解析返回类型
            if node.returns and isinstance(node.returns, ast.Name):
                func_info["returns"] = node.returns.id
            
            functions.append(func_info)
    
    return functions


def generate_test_cases(func_info: dict) -> str:
    """为单个函数生成测试用例"""
    func_name = func_info["name"]
    args = func_info["args"]
    returns = func_info["returns"]
    
    lines = [f"class Test{func_name.title().replace('_', '')}:"]
    lines.append(f'    """测试 {func_info["docstring"] or func_name}"""')
    lines.append("")
    
    # 正常情况测试
    if args:
        arg_values = []
        for arg in args:
            arg_type = arg.get("type", "")
            if arg_type == "str":
                arg_values.append(f'"test_{arg["name"]}"')
            elif arg_type == "int":
                arg_values.append("1")
            elif arg_type == "bool":
                arg_values.append("True")
            else:
                arg_values.append(f'"{arg["name"]}"')
        
        arg_str = ", ".join(arg_values)
        lines.append(f"    def test_{func_name}_success(self):")
        lines.append(f"        result = {func_name}({arg_str})")
        
        if returns == "bool":
            lines.append(f"        assert result is True")
        elif returns == "dict":
            lines.append(f"        assert result is not None")
            lines.append(f"        assert isinstance(result, dict)")
        elif returns == "list":
            lines.append(f"        assert isinstance(result, list)")
        else:
            lines.append(f"        assert result is not None")
    else:
        lines.append(f"    def test_{func_name}(self):")
        lines.append(f"        result = {func_name}()")
        lines.append(f"        assert result is not None")
    
    lines.append("")
    
    # 边界情况测试（如果有参数）
    if args:
        # 空值测试
        empty_args = []
        for arg in args:
            arg_type = arg.get("type", "")
            if arg_type == "str":
                empty_args.append('""')
            elif arg_type == "int":
                empty_args.append("0")
            elif arg_type == "bool":
                empty_args.append("False")
            else:
                empty_args.append('""')
        
        empty_str = ", ".join(empty_args)
        lines.append(f"    def test_{func_name}_empty_values(self):")
        lines.append(f"        result = {func_name}({empty_str})")
        lines.append(f"        # TODO: 根据业务逻辑补充断言")
        lines.append("")
    
    # 异常测试（如果有参数）
    if args:
        lines.append(f"    def test_{func_name}_invalid_input(self):")
        lines.append(f"        with pytest.raises((ValueError, TypeError)):")
        
        invalid_args = []
        for arg in args:
            invalid_args.append("None")
        
        invalid_str = ", ".join(invalid_args)
        lines.append(f"            {func_name}({invalid_str})")
        lines.append("")
    
    return "\n".join(lines)


def generate_test_file(module_name: str, functions: list) -> str:
    """生成完整测试文件"""
    lines = [
        f"import pytest",
        f"from {module_name} import {', '.join(f['name'] for f in functions)}",
        "",
        f"# 由 test-unit Skill 自动生成",
        f"# 模块: {module_name}",
        f"# 函数数: {len(functions)}",
        "",
        "# TODO: 根据实际情况补充具体断言和测试数据",
        "",
    ]
    
    for func in functions:
        lines.append(generate_test_cases(func))
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='单元测试生成器')
    parser.add_argument('--input', '-i', required=True, help='源代码文件或目录')
    parser.add_argument('--output', '-o', help='输出测试文件路径')
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"[错误] 路径不存在: {input_path}")
        sys.exit(1)
    
    if input_path.is_file():
        # 处理单个文件
        print(f"[信息] 正在解析: {input_path}")
        functions = parse_source(input_path)
        
        if not functions:
            print("[警告] 未找到可测试的函数")
            sys.exit(0)
        
        module_name = input_path.stem
        test_content = generate_test_file(module_name, functions)
        
        # 确定输出路径
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.parent / f"test_{module_name}.py"
        
        output_path.write_text(test_content, encoding='utf-8')
        
        print(f"[成功] 测试文件已生成: {output_path}")
        print(f"   函数数: {len(functions)}")
        for func in functions:
            print(f"   - {func['name']}({', '.join(a['name'] for a in func['args'])})")
    
    else:
        # 处理目录
        print(f"[信息] 正在扫描目录: {input_path}")
        py_files = list(input_path.glob("*.py"))
        
        if not py_files:
            print("[警告] 未找到Python文件")
            sys.exit(0)
        
        output_dir = Path(args.output) if args.output else input_path / "tests"
        output_dir.mkdir(exist_ok=True)
        
        for py_file in py_files:
            functions = parse_source(py_file)
            if not functions:
                continue
            
            module_name = py_file.stem
            test_content = generate_test_file(module_name, functions)
            
            output_path = output_dir / f"test_{module_name}.py"
            output_path.write_text(test_content, encoding='utf-8')
            
            print(f"[成功] {py_file.name} -> {output_path.name}")
        
        print(f"\n共生成 {len(py_files)} 个测试文件到 {output_dir}/")


if __name__ == "__main__":
    main()
