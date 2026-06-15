#!/usr/bin/env python3
"""
测试报告生成器
解析 JUnit XML 或 JSON 格式的测试结果，生成 Markdown 报告
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET


def parse_junit_xml(xml_path: Path) -> dict:
    """解析 JUnit XML 格式"""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    if root.tag == "testsuites":
        suites = root.findall("testsuite")
        suite_node = suites[0] if suites else root
    else:
        suite_node = root

    result = {
        "testsuite": {
            "name": suite_node.get("name", "Unknown"),
            "tests": int(suite_node.get("tests", 0)),
            "failures": int(suite_node.get("failures", 0)),
            "errors": int(suite_node.get("errors", 0)),
            "skipped": int(suite_node.get("skipped", 0)),
            "time": float(suite_node.get("time", 0)),
        },
        "testcases": []
    }

    for testcase in root.findall(".//testcase"):
        case = {
            "name": testcase.get("name", ""),
            "classname": testcase.get("classname", ""),
            "time": float(testcase.get("time", 0)),
            "status": "passed"
        }
        
        # 检查失败
        failure = testcase.find("failure")
        if failure is not None:
            case["status"] = "failed"
            case["message"] = failure.get("message", "")
            case["details"] = failure.text or ""
        
        # 检查错误
        error = testcase.find("error")
        if error is not None:
            case["status"] = "error"
            case["message"] = error.get("message", "")
            case["details"] = error.text or ""
        
        # 检查跳过
        skipped = testcase.find("skipped")
        if skipped is not None:
            case["status"] = "skipped"
            case["message"] = skipped.get("message", "")
        
        result["testcases"].append(case)
    
    return result


def parse_json_results(json_path: Path) -> dict:
    """解析 JSON 格式"""
    content = json_path.read_text(encoding='utf-8')
    data = json.loads(content)
    
    result = {
        "testsuite": {
            "name": data.get("title", "Unknown"),
            "tests": len(data.get("tests", [])),
            "failures": 0,
            "errors": 0,
            "skipped": 0,
            "time": data.get("duration", 0),
        },
        "testcases": []
    }
    
    for test in data.get("tests", []):
        case = {
            "name": test.get("nodeid", test.get("name", "")),
            "classname": test.get("module", ""),
            "time": test.get("duration", 0),
            "status": test.get("outcome", "passed")
        }
        
        if case["status"] == "failed":
            result["testsuite"]["failures"] += 1
        elif case["status"] == "error":
            result["testsuite"]["errors"] += 1
        elif case["status"] == "skipped":
            result["testsuite"]["skipped"] += 1
        
        result["testcases"].append(case)
    
    return result


def generate_report(results: list) -> str:
    """生成测试报告"""
    # 汇总数据
    total_tests = sum(r["testsuite"]["tests"] for r in results)
    total_failures = sum(r["testsuite"]["failures"] for r in results)
    total_errors = sum(r["testsuite"]["errors"] for r in results)
    total_skipped = sum(r["testsuite"]["skipped"] for r in results)
    total_time = sum(r["testsuite"]["time"] for r in results)
    
    passed = total_tests - total_failures - total_errors - total_skipped
    pass_rate = passed / total_tests * 100 if total_tests > 0 else 0
    
    lines = [
        "# 测试执行报告",
        "",
        f"**报告时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**测试文件数**: {len(results)}",
        ""
    ]
    
    # 执行概况
    lines.extend([
        "## 执行概况",
        "",
        "| 指标 | 数值 |",
        "|------|------|",
        f"| **总用例数** | {total_tests} |",
        f"| **通过** | {passed} ✅ |",
        f"| **失败** | {total_failures} ❌ |",
        f"| **跳过** | {total_skipped} ⏭️ |",
        f"| **错误** | {total_errors} |",
        f"| **通过率** | {pass_rate:.2f}% |",
        f"| **总耗时** | {total_time:.1f}s |",
        ""
    ])
    
    # 收集所有失败的用例
    failed_cases = []
    all_cases = []
    
    for result in results:
        for case in result["testcases"]:
            all_cases.append(case)
            if case["status"] in ["failed", "error"]:
                failed_cases.append(case)
    
    # 失败用例详情
    if failed_cases:
        lines.extend([
            "## 失败用例详情",
            ""
        ])
        
        for case in failed_cases[:10]:  # 最多显示10个
            case_id = f"{case['classname']}::{case['name']}"
            lines.extend([
                f"### {case_id}",
                "",
                f"- **状态**: ❌ {case['status']}",
                f"- **耗时**: {case['time']:.2f}s",
                ""
            ])
            
            if "message" in case and case["message"]:
                lines.extend([
                    "- **错误信息**:",
                    "  ```",
                    f"  {case['message'][:200]}",
                    "  ```",
                    ""
                ])
            
            lines.append("")
        
        if len(failed_cases) > 10:
            lines.append(f"*还有 {len(failed_cases) - 10} 个失败用例未显示*\n")
    
    # 慢测试（Top 5）
    sorted_cases = sorted(all_cases, key=lambda x: x["time"], reverse=True)
    slow_cases = sorted_cases[:5]
    
    if slow_cases:
        lines.extend([
            "## 慢测试（Top 5）",
            "",
            "| 用例 | 耗时 | 状态 |",
            "|------|------|------|"
        ])
        
        for case in slow_cases:
            case_id = f"{case['classname']}::{case['name']}"
            status_icon = "✅" if case["status"] == "passed" else "❌"
            lines.append(f"| {case_id} | {case['time']:.2f}s | {status_icon} |")
        
        lines.append("")
    
    # 总结
    if pass_rate >= 95:
        lines.append("🎉 测试通过率优秀！\n")
    elif pass_rate >= 80:
        lines.append("⚠️ 测试通过率良好，建议修复失败用例。\n")
    else:
        lines.append("❌ 测试通过率偏低，请优先修复失败用例。\n")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='测试报告生成器')
    parser.add_argument('--input', '-i', required=True, nargs='+', help='测试结果文件（支持多个）')
    parser.add_argument('--format', choices=['xml', 'json'], help='文件格式')
    parser.add_argument('--output', '-o', default='test-report.md', help='输出路径')
    args = parser.parse_args()
    
    results = []
    
    for input_file in args.input:
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"[警告] 文件不存在: {input_path}")
            continue
        
        # 检测格式
        file_format = args.format
        if not file_format:
            if input_path.suffix == '.json':
                file_format = 'json'
            else:
                file_format = 'xml'
        
        print(f"[信息] 解析: {input_path.name} ({file_format})")
        
        if file_format == 'json':
            result = parse_json_results(input_path)
        else:
            result = parse_junit_xml(input_path)
        
        results.append(result)
        
        suite = result["testsuite"]
        print(f"   用例: {suite['tests']}, 失败: {suite['failures']}, 跳过: {suite['skipped']}")
    
    if not results:
        print("[错误] 没有成功解析的测试文件")
        sys.exit(1)
    
    # 生成报告
    report = generate_report(results)
    
    output_path = Path(args.output)
    output_path.write_text(report, encoding='utf-8')
    
    print(f"[成功] 测试报告已生成: {output_path}")


if __name__ == "__main__":
    main()
