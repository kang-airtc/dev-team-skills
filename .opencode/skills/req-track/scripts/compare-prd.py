#!/usr/bin/env python3
"""
PRD 差异对比工具
对比两个 PRD 版本，生成可视化差异报告
"""

import argparse
import difflib
import re
import sys
from pathlib import Path


def read_prd(prd_path: Path) -> list:
    """读取 PRD 文件，返回行列表"""
    content = prd_path.read_text(encoding='utf-8')
    return content.splitlines()


def compare_versions(old_lines: list, new_lines: list, old_name: str, new_name: str) -> str:
    """生成差异报告"""
    differ = difflib.Differ()
    diff = list(differ.compare(old_lines, new_lines))
    
    # 分类变更
    additions = []
    deletions = []
    modifications = []
    
    i = 0
    while i < len(diff):
        line = diff[i]
        
        if line.startswith('+ ') and not line.startswith('+++'):
            # 新增
            content = line[2:]
            if content.strip():
                additions.append(content)
        elif line.startswith('- ') and not line.startswith('---'):
            # 删除
            content = line[2:]
            if content.strip():
                deletions.append(content)
        elif line.startswith('? '):
            # 修改标记，跳过
            pass
        
        i += 1
    
    # 生成报告
    report_lines = [
        "# PRD 差异对比报告",
        "",
        f"**对比版本**: {old_name} → {new_name}",
        f"**生成时间**: 自动生成",
        "",
        "---",
        "",
        "## 变更统计",
        "",
        f"- **新增内容**: {len(additions)} 行",
        f"- **删除内容**: {len(deletions)} 行",
        f"- **修改内容**: {len(modifications)} 处",
        "",
        "---",
        "",
    ]
    
    # 新增内容
    if additions:
        report_lines.extend([
            "## 新增内容",
            "",
            "```diff",
            "+ 新增",
            "```",
            ""
        ])
        for line in additions[:50]:  # 最多显示50行
            report_lines.append(f"- {line}")
        if len(additions) > 50:
            report_lines.append(f"\n... 还有 {len(additions) - 50} 行新增内容 ...")
        report_lines.append("")
    
    # 删除内容
    if deletions:
        report_lines.extend([
            "## 删除内容",
            "",
            "```diff",
            "- 删除",
            "```",
            ""
        ])
        for line in deletions[:50]:
            report_lines.append(f"- ~~{line}~~")
        if len(deletions) > 50:
            report_lines.append(f"\n... 还有 {len(deletions) - 50} 行删除内容 ...")
        report_lines.append("")
    
    # 完整 diff（可折叠）
    report_lines.extend([
        "## 完整差异",
        "",
        "```diff",
    ])
    
    for line in diff:
        report_lines.append(line)
    
    report_lines.extend([
        "```",
        "",
        "---",
        "",
        "## 影响范围分析",
        "",
        "（请人工评估以下影响）",
        "",
        "- [ ] 需要重新估算工时",
        "- [ ] 影响已开始的开发任务",
        "- [ ] 需要更新测试用例",
        "- [ ] 需要同步给相关团队",
        ""
    ])
    
    return "\n".join(report_lines)


def extract_version_info(prd_path: Path) -> dict:
    """提取 PRD 版本信息"""
    content = prd_path.read_text(encoding='utf-8')
    info = {
        "version": "未知",
        "date": "未知"
    }
    
    version_match = re.search(r'\*\*版本\*\*[:：]\s*(.+)', content)
    if version_match:
        info["version"] = version_match.group(1).strip()
    
    date_match = re.search(r'\*\*日期\*\*[:：]\s*(.+)', content)
    if date_match:
        info["date"] = date_match.group(1).strip()
    
    return info


def main():
    parser = argparse.ArgumentParser(description='PRD 差异对比工具')
    parser.add_argument('--old', required=True, help='旧版本 PRD 路径')
    parser.add_argument('--new', required=True, help='新版本 PRD 路径')
    parser.add_argument('--output', '-o', default='diff-report.md', help='输出路径')
    args = parser.parse_args()
    
    old_path = Path(args.old)
    new_path = Path(args.new)
    
    if not old_path.exists():
        print(f"[错误] 旧版本文件不存在: {old_path}")
        sys.exit(1)
    
    if not new_path.exists():
        print(f"[错误] 新版本文件不存在: {new_path}")
        sys.exit(1)
    
    # 读取文件
    print("[信息] 正在读取 PRD 文件...")
    old_lines = read_prd(old_path)
    new_lines = read_prd(new_path)
    
    # 提取版本信息
    old_info = extract_version_info(old_path)
    new_info = extract_version_info(new_path)
    
    old_name = f"{old_path.name} ({old_info['version']})"
    new_name = f"{new_path.name} ({new_info['version']})"
    
    # 生成差异报告
    print("[信息] 正在生成差异报告...")
    report = compare_versions(old_lines, new_lines, old_name, new_name)
    
    # 保存
    output_path = Path(args.output)
    output_path.write_text(report, encoding='utf-8')
    
    print(f"[成功] 差异报告已生成: {output_path.absolute()}")
    print(f"\n对比结果:")
    print(f"  旧版本: {old_name}")
    print(f"  新版本: {new_name}")


if __name__ == "__main__":
    main()
