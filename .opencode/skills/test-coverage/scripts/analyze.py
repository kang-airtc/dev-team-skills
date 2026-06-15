#!/usr/bin/env python3
"""
覆盖率分析工具
解析coverage.xml或lcov.info，生成分析报告
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET


def parse_coverage_xml(xml_path: Path) -> dict:
    """解析coverage.xml"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # 获取总体数据
    total = {
        "lines_valid": int(root.get("lines-valid", 0)),
        "lines_covered": int(root.get("lines-covered", 0)),
        "line_rate": float(root.get("line-rate", 0)),
        "files": []
    }
    
    # 解析每个文件
    for package in root.findall(".//package"):
        for cls in package.findall(".//class"):
            filename = cls.get("filename", "")
            line_rate = float(cls.get("line-rate", 0))
            lines_covered = int(cls.get("lines-covered", 0))
            lines_valid = int(cls.get("lines-valid", 0))
            
            total["files"].append({
                "filename": filename,
                "line_rate": line_rate,
                "lines_covered": lines_covered,
                "lines_valid": lines_valid,
                "lines_missed": lines_valid - lines_covered
            })
    
    return total


def parse_lcov(lcov_path: Path) -> dict:
    """解析lcov.info"""
    content = lcov_path.read_text(encoding='utf-8')
    
    total = {
        "lines_valid": 0,
        "lines_covered": 0,
        "line_rate": 0,
        "files": []
    }
    
    # 按文件分割
    current_file = None
    current_lines_valid = 0
    current_lines_covered = 0
    
    for line in content.splitlines():
        if line.startswith("SF:"):
            if current_file:
                total["files"].append({
                    "filename": current_file,
                    "line_rate": current_lines_covered / max(current_lines_valid, 1),
                    "lines_covered": current_lines_covered,
                    "lines_valid": current_lines_valid,
                    "lines_missed": current_lines_valid - current_lines_covered
                })
                total["lines_valid"] += current_lines_valid
                total["lines_covered"] += current_lines_covered
            
            current_file = line[3:]
            current_lines_valid = 0
            current_lines_covered = 0
        
        elif line.startswith("DA:"):
            # DA:行号,执行次数
            parts = line[3:].split(",")
            if len(parts) == 2:
                current_lines_valid += 1
                if int(parts[1]) > 0:
                    current_lines_covered += 1
    
    # 最后一个文件
    if current_file:
        total["files"].append({
            "filename": current_file,
            "line_rate": current_lines_covered / max(current_lines_valid, 1),
            "lines_covered": current_lines_covered,
            "lines_valid": current_lines_valid,
            "lines_missed": current_lines_valid - current_lines_covered
        })
        total["lines_valid"] += current_lines_valid
        total["lines_covered"] += current_lines_covered
    
    if total["lines_valid"] > 0:
        total["line_rate"] = total["lines_covered"] / total["lines_valid"]
    
    return total


def generate_report(data: dict, compare_data: dict = None) -> str:
    """生成覆盖率报告"""
    lines = [
        "# 测试覆盖率分析报告",
        "",
        f"**报告时间**: {datetime.now().strftime('%Y-%m-%d')}",
        f"**文件数**: {len(data['files'])}",
        ""
    ]
    
    # 总体概况
    coverage_pct = data['line_rate'] * 100
    status = "✅ 达标" if coverage_pct >= 80 else "⚠️ 需提升"
    
    lines.extend([
        "## 总体概况",
        "",
        "| 指标 | 数值 | 状态 |",
        "|------|------|------|",
        f"| **总行数** | {data['lines_valid']:,} | - |",
        f"| **覆盖行数** | {data['lines_covered']:,} | - |",
        f"| **覆盖率** | {coverage_pct:.2f}% | {status} |",
        f"| **文件数** | {len(data['files'])} | - |",
        ""
    ])
    
    # 对比
    if compare_data:
        old_coverage = compare_data['line_rate'] * 100
        diff = coverage_pct - old_coverage
        diff_icon = "✅" if diff > 0 else "❌" if diff < 0 else "➖"
        
        lines.extend([
            "## 对比上次",
            "",
            "| 指标 | 上次 | 本次 | 变化 |",
            "|------|------|------|------|",
            f"| 覆盖率 | {old_coverage:.2f}% | {coverage_pct:.2f}% | {diff:+.2f}% {diff_icon} |",
            f"| 覆盖行数 | {compare_data['lines_covered']:,} | {data['lines_covered']:,} | {data['lines_covered'] - compare_data['lines_covered']:+d} |",
            ""
        ])
    
    # 覆盖率分布
    ranges = {
        "90-100%": 0,
        "80-90%": 0,
        "60-80%": 0,
        "0-60%": 0
    }
    
    for f in data['files']:
        rate = f['line_rate'] * 100
        if rate >= 90:
            ranges["90-100%"] += 1
        elif rate >= 80:
            ranges["80-90%"] += 1
        elif rate >= 60:
            ranges["60-80%"] += 1
        else:
            ranges["0-60%"] += 1
    
    lines.extend([
        "## 覆盖率分布",
        "",
        "| 覆盖率区间 | 文件数 | 占比 |",
        "|-----------|--------|------|"
    ])
    
    total_files = len(data['files'])
    for range_name, count in ranges.items():
        pct = count / total_files * 100 if total_files > 0 else 0
        lines.append(f"| {range_name} | {count} | {pct:.1f}% |")
    
    lines.append("")
    
    # 低覆盖率文件
    low_coverage = [f for f in data['files'] if f['line_rate'] < 0.6]
    if low_coverage:
        lines.extend([
            "## 低覆盖率文件（需关注）",
            "",
            "| 文件 | 覆盖率 | 未覆盖行数 |",
            "|------|--------|-----------|"
        ])
        
        for f in sorted(low_coverage, key=lambda x: x['line_rate']):
            lines.append(f"| {f['filename']} | {f['line_rate']*100:.0f}% | {f['lines_missed']} |")
        
        lines.append("")
    
    # 建议
    lines.extend([
        "## 改进建议",
        "",
        "1. 优先提升低覆盖率文件的测试覆盖",
        "2. 新增代码应配套单元测试",
        "3. 建议设置覆盖率门槛（推荐 80%）",
        ""
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='覆盖率分析工具')
    parser.add_argument('--input', '-i', required=True, help='覆盖率报告文件')
    parser.add_argument('--format', choices=['xml', 'lcov'], help='报告格式')
    parser.add_argument('--compare', '-c', help='对比的历史报告')
    parser.add_argument('--output', '-o', default='coverage-report.md', help='输出路径')
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[错误] 文件不存在: {input_path}")
        sys.exit(1)
    
    # 检测格式
    report_format = args.format
    if not report_format:
        if input_path.suffix == '.xml':
            report_format = 'xml'
        elif 'lcov' in input_path.name:
            report_format = 'lcov'
    
    print(f"[信息] 解析格式: {report_format}")
    
    # 解析报告
    if report_format == 'lcov':
        data = parse_lcov(input_path)
    else:
        data = parse_coverage_xml(input_path)
    
    print(f"[信息] 文件数: {len(data['files'])}")
    print(f"[信息] 覆盖率: {data['line_rate']*100:.2f}%")
    
    # 对比数据
    compare_data = None
    if args.compare:
        compare_path = Path(args.compare)
        if compare_path.exists():
            if report_format == 'lcov':
                compare_data = parse_lcov(compare_path)
            else:
                compare_data = parse_coverage_xml(compare_path)
            print(f"[信息] 已加载对比报告: {compare_path}")
    
    # 生成报告
    report = generate_report(data, compare_data)
    
    output_path = Path(args.output)
    output_path.write_text(report, encoding='utf-8')
    
    print(f"[成功] 覆盖率报告已生成: {output_path}")


if __name__ == "__main__":
    main()
