#!/usr/bin/env python3
"""
故障复盘报告生成器
生成结构化的 Postmortem 报告
"""

import argparse
import re
from pathlib import Path
from datetime import datetime


def generate_postmortem(title: str, severity: str, duration: int) -> str:
    """生成复盘报告"""
    incident_id = f"INC-{datetime.now().strftime('%Y%m%d')}-001"
    
    lines = [
        f"# 故障复盘报告：{title}",
        "",
        f"**故障编号**: {incident_id}",
        f"**严重级别**: {severity}",
        f"**持续时间**: {duration} 分钟",
        f"**报告时间**: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## 时间线",
        "",
        "| 时间 | 事件 |",
        "|------|------|",
        "| --:-- | （请填写故障发生时间） |",
        "| --:-- | （请填写发现时间） |",
        "| --:-- | （请填写诊断时间） |",
        "| --:-- | （请填写恢复时间） |",
        "",
        "## 根因分析",
        "",
        "**直接原因**:",
        "- （请填写直接原因）",
        "",
        "**深层原因**:",
        "1. （原因1）",
        "2. （原因2）",
        "3. （原因3）",
        "",
        "## 影响评估",
        "",
        "- **影响用户数**: （请填写）",
        "- **业务影响**: （请填写）",
        "- **数据影响**: （请填写）",
        "",
        "## 改进措施",
        "",
        "| 措施 | 负责人 | 截止时间 | 状态 |",
        "|------|--------|---------|------|",
        "| （措施1） | | | 待办 |",
        "| （措施2） | | | 待办 |",
        "| （措施3） | | | 待办 |",
        "",
        "## 经验教训",
        "",
        "1. （经验1）",
        "2. （经验2）",
        "3. （经验3）",
        ""
    ]
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='故障复盘报告生成器')
    parser.add_argument('--title', '-t', help='故障标题')
    parser.add_argument('--severity', default='P1', choices=['P0', 'P1', 'P2', 'P3'])
    parser.add_argument('--duration', type=int, default=0, help='持续时间（分钟）')
    parser.add_argument('--output', '-o', help='输出路径')
    args = parser.parse_args()
    
    # 交互式输入
    if not args.title:
        args.title = input("故障标题: ").strip()
    
    if args.duration == 0:
        try:
            args.duration = int(input("持续时间（分钟）: ").strip())
        except:
            args.duration = 0
    
    print(f"[信息] 生成复盘报告: {args.title}")
    
    report = generate_postmortem(args.title, args.severity, args.duration)
    
    if args.output:
        output_path = Path(args.output)
    else:
        safe_title = re.sub(r'[^\w\s-]', '', args.title).replace(' ', '-')
        output_path = Path(f"postmortem-{safe_title}.md")
    
    output_path.write_text(report, encoding='utf-8')
    
    print(f"[成功] 复盘报告已生成: {output_path}")
    print("\n⚠️  提示：报告中的占位符需要人工补充")


if __name__ == "__main__":
    main()
