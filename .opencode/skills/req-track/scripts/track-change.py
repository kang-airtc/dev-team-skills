#!/usr/bin/env python3
"""
需求变更记录工具
记录 PRD 变更历史，自动生成变更编号
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_TEMPLATE = SKILL_DIR / "assets" / "change-log-template.md"

CHANGE_TYPES = {
    "feature": "功能增强",
    "bugfix": "缺陷修复",
    "refactor": "重构优化",
    "remove": "功能移除"
}


def get_next_change_id(log_path: Path) -> str:
    """获取下一个变更编号"""
    if not log_path.exists():
        return "RC-001"
    
    content = log_path.read_text(encoding='utf-8')
    ids = re.findall(r'\[RC-(\d{3})\]', content)
    
    if ids:
        max_id = max(int(i) for i in ids)
        return f"RC-{max_id + 1:03d}"
    
    return "RC-001"


def format_change_entry(change_id: str, desc: str, reason: str, impact: str, 
                       change_type: str, date: str = None) -> str:
    """格式化单条变更记录"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    type_name = CHANGE_TYPES.get(change_type, change_type)
    
    entry = f"""## [{change_id}] {date} - {desc}

- **变更类型**: {type_name}
- **影响范围**: {impact}
- **变更内容**: {desc}
- **变更原因**: {reason}
- **影响分析**:
  - （待补充：哪些 Story/Task 受影响）
- **审批状态**: 待审批
- **预计工时影响**: （待评估）

---

"""
    return entry


def init_changelog(output_path: Path, project_name: str = "项目"):
    """初始化变更日志"""
    if not DEFAULT_TEMPLATE.exists():
        # 创建默认模板
        template_content = f"""# 需求变更日志

**项目**: {project_name}
**创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**维护说明**: 所有需求变更必须记录在此文件中，按时间倒序排列

---

## 变更统计

- **总变更数**: 0
- **功能增强**: 0
- **缺陷修复**: 0
- **重构优化**: 0
- **功能移除**: 0

---

## 变更记录

"""
    else:
        template = DEFAULT_TEMPLATE.read_text(encoding='utf-8')
        template_content = template.replace("{project_name}", project_name)
        template_content = template_content.replace("{create_time}", datetime.now().strftime("%Y-%m-%d %H:%M"))
        template_content = template_content.replace("{total_changes}", "0")
        template_content = template_content.replace("{feature_count}", "0")
        template_content = template_content.replace("{bugfix_count}", "0")
        template_content = template_content.replace("{refactor_count}", "0")
        template_content = template_content.replace("{remove_count}", "0")
    
    output_path.write_text(template_content, encoding='utf-8')
    print(f"[成功] 已创建变更日志: {output_path}")


def add_change(output_path: Path, desc: str, reason: str, impact: str, 
               change_type: str, prd_path: Path = None):
    """添加变更记录"""
    # 如果文件不存在，先初始化
    if not output_path.exists():
        print("[信息] 变更日志不存在，正在创建...")
        init_changelog(output_path)
    
    # 获取变更编号
    change_id = get_next_change_id(output_path)
    
    # 生成变更记录
    entry = format_change_entry(change_id, desc, reason, impact, change_type)
    
    # 追加到文件
    content = output_path.read_text(encoding='utf-8')
    
    # 找到"## 变更记录"的位置，在其后追加
    marker = "## 变更记录"
    if marker in content:
        idx = content.find(marker) + len(marker)
        new_content = content[:idx] + "\n\n" + entry + content[idx:]
    else:
        new_content = content + "\n" + entry
    
    output_path.write_text(new_content, encoding='utf-8')
    
    print(f"[成功] 已记录变更: {change_id}")
    print(f"  描述: {desc}")
    print(f"  类型: {CHANGE_TYPES.get(change_type, change_type)}")
    print(f"  影响: {impact}")
    
    return change_id


def interactive_mode(output_path: Path):
    """交互式记录变更"""
    print("=" * 60)
    print("需求变更记录")
    print("=" * 60)
    print()
    
    print("变更类型:")
    for key, name in CHANGE_TYPES.items():
        print(f"  {key}: {name}")
    print()
    
    change_type = input("请选择变更类型 (feature/bugfix/refactor/remove): ").strip()
    if change_type not in CHANGE_TYPES:
        print("[错误] 无效的变更类型")
        sys.exit(1)
    
    desc = input("变更描述: ").strip()
    if not desc:
        print("[错误] 变更描述不能为空")
        sys.exit(1)
    
    reason = input("变更原因: ").strip()
    impact = input("影响范围 (如 Epic-1, Story-2.1): ").strip()
    
    prd_input = input("关联 PRD 文件路径 (可选，直接回车跳过): ").strip()
    prd_path = Path(prd_input) if prd_input else None
    
    add_change(output_path, desc, reason, impact, change_type, prd_path)


def main():
    parser = argparse.ArgumentParser(description='需求变更记录工具')
    parser.add_argument('--init', action='store_true', help='初始化变更日志')
    parser.add_argument('--output', '-o', default='CHANGELOG.md', help='变更日志路径')
    parser.add_argument('--project', default='项目', help='项目名称')
    parser.add_argument('--prd', '-p', help='关联的 PRD 文件路径')
    parser.add_argument('--desc', '-d', help='变更描述')
    parser.add_argument('--reason', '-r', help='变更原因')
    parser.add_argument('--impact', '-i', help='影响范围')
    parser.add_argument('--type', '-t', choices=list(CHANGE_TYPES.keys()), help='变更类型')
    args = parser.parse_args()
    
    output_path = Path(args.output)
    
    if args.init:
        init_changelog(output_path, args.project)
        return
    
    # 如果有完整的参数，直接记录
    if args.desc and args.reason and args.impact and args.type:
        prd_path = Path(args.prd) if args.prd else None
        add_change(output_path, args.desc, args.reason, args.impact, args.type, prd_path)
    else:
        # 交互式模式
        interactive_mode(output_path)


if __name__ == "__main__":
    main()
