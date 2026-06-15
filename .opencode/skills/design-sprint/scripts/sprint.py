#!/usr/bin/env python3
"""
设计冲刺计划生成器
生成5天设计冲刺的完整计划
"""

import argparse
import re
from pathlib import Path
from datetime import datetime


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_PATH = SKILL_DIR / "assets" / "sprint-template.md"


def generate_sprint_plan(topic, day=None):
    """生成冲刺计划"""
    if not TEMPLATE_PATH.exists():
        print("[错误] 模板文件不存在")
        return None
    
    template = TEMPLATE_PATH.read_text(encoding='utf-8')
    
    # 替换变量
    content = template.replace("{{topic}}", topic)
    content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
    content = content.replace("{{goal}}", f"在5天内完成{topic}的设计和验证")
    
    # 如果只输出特定天
    if day:
        day_markers = {
            1: "## Day 1: 理解（Understand）",
            2: "## Day 2: 发散（Sketch）",
            3: "## Day 3: 决策（Decide）",
            4: "## Day 4: 原型（Prototype）",
            5: "## Day 5: 验证（Validate）"
        }
        
        if day in day_markers:
            start_marker = day_markers[day]
            end_marker = day_markers.get(day + 1, "## 冲刺检查清单")
            
            # 提取指定天的内容
            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker)
            
            if start_idx != -1 and end_idx != -1:
                content = content[start_idx:end_idx].strip()
    
    return content


def main():
    parser = argparse.ArgumentParser(description='设计冲刺计划生成器')
    parser.add_argument('--topic', '-t', required=True, help='冲刺主题')
    parser.add_argument('--day', '-d', type=int, choices=range(1, 6), help='只输出指定天（1-5）')
    parser.add_argument('--output', '-o', default='sprint-plan.md', help='输出路径')
    args = parser.parse_args()
    
    print(f"[信息] 正在生成设计冲刺计划: {args.topic}")
    
    content = generate_sprint_plan(args.topic, args.day)
    
    if content:
        output_path = Path(args.output)
        output_path.write_text(content, encoding='utf-8')
        print(f"[成功] 计划已生成: {output_path.absolute()}")
        
        if args.day:
            print(f"\n📋 已输出 Day {args.day} 的任务安排")
        else:
            print(f"\n📋 完整5天冲刺计划已生成")
            print("\n提示：")
            print("  - 建议团队规模：5-7人")
            print("  - 需要真实用户参与Day 5测试")
            print("  - 每天准时开始和结束，保持节奏")


if __name__ == "__main__":
    main()
