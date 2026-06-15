#!/usr/bin/env python3
"""
需求管理助手 - 主控脚本
提供交互式菜单和项目状态管理
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
PIPELINE_DIR = SKILL_DIR / "pipeline"
SKILLS_ROOT = SKILL_DIR.parent

PROJECTS_DIR = Path("./projects")

STEPS = {
    "1": ("新建需求项目（完整流程）", "run-all.sh"),
    "2": ("需求澄清", "req-clarify/scripts/clarify.py"),
    "3": ("生成 PRD", "req-prd/scripts/generate-prd.py"),
    "4": ("需求拆解", "req-decompose/scripts/decompose.py"),
    "5": ("记录变更", "req-track/scripts/track-change.py"),
    "6": ("生成故事地图", "req-storymap/scripts/generate-story-map.py"),
    "7": ("生成流程图", "req-flowchart/scripts/generate-flowchart.py"),
    "8": ("查看项目状态", None),
    "9": ("退出", None)
}


def show_menu():
    """显示主菜单"""
    print("=" * 50)
    print("    需求管理助手")
    print("=" * 50)
    print()
    
    for key, (name, _) in STEPS.items():
        print(f"{key}. {name}")
    
    print()


def get_project_list():
    """获取项目列表"""
    if not PROJECTS_DIR.exists():
        return []
    
    return [d.name for d in PROJECTS_DIR.iterdir() if d.is_dir()]


def select_project():
    """选择项目"""
    projects = get_project_list()
    
    if not projects:
        print("[错误] 没有找到项目，请先创建项目")
        return None
    
    print("可用项目:")
    for i, project in enumerate(projects, 1):
        print(f"  {i}. {project}")
    print()
    
    choice = input("请选择项目编号: ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(projects):
            return projects[idx]
    except ValueError:
        pass
    
    print("[错误] 无效选择")
    return None


def check_project_status(project_name):
    """检查项目状态"""
    project_dir = PROJECTS_DIR / project_name
    
    if not project_dir.exists():
        print(f"[错误] 项目不存在: {project_name}")
        return
    
    files = {
        "原始需求": "0-raw-requirement.txt",
        "需求澄清": "1-clarified.md",
        "PRD 草稿": "2-PRD.md",
        "需求拆解": "3-backlog.md",
        "变更追踪": "4-CHANGELOG.md",
        "故事地图": "5-story-map.md",
        "流程图": "6-flowchart.md"
    }
    
    print(f"\n项目: {project_name}")
    print("=" * 50)
    print()
    
    completed = 0
    for label, filename in files.items():
        filepath = project_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"✅ {label:12s}  ({size:6d} bytes)  {filename}")
            completed += 1
        else:
            print(f"⏳ {label:12s}  (待生成)      {filename}")
    
    print()
    print(f"完成度: {completed}/{len(files)} ({completed * 100 // len(files)}%)")
    
    if completed == len(files):
        print("🎉 所有文档已生成！")
    elif completed >= 4:
        print("💡 核心文档已完成，可以开始开发了")
    else:
        print("📝 请继续生成剩余文档")


def run_new_project():
    """创建新项目并执行完整流程"""
    project_name = input("项目名称: ").strip()
    if not project_name:
        print("[错误] 项目名称不能为空")
        return
    
    req_file = input("原始需求文件路径: ").strip()
    if not req_file or not Path(req_file).exists():
        print("[错误] 文件不存在")
        return
    
    # 执行 run-all.sh
    script = PIPELINE_DIR / "run-all.sh"
    os.system(f'bash "{script}" "{project_name}" "{req_file}"')


def run_step(step_key):
    """执行单个步骤"""
    step_name, script_path = STEPS[step_key]
    
    project_name = select_project()
    if not project_name:
        return
    
    project_dir = PROJECTS_DIR / project_name
    
    if step_key == "2":  # 需求澄清
        input_file = project_dir / "0-raw-requirement.txt"
        output_file = project_dir / "1-clarified.md"
        cmd = f'python3 "{SKILLS_ROOT}/{script_path}" --input "{input_file}" --output "{output_file}"'
    
    elif step_key == "3":  # PRD
        input_file = project_dir / "1-clarified.md"
        output_file = project_dir / "2-PRD.md"
        cmd = f'python3 "{SKILLS_ROOT}/{script_path}" --input "{input_file}" --output "{output_file}" --product "{project_name}"'
    
    elif step_key == "4":  # 拆解
        input_file = project_dir / "2-PRD.md"
        output_file = project_dir / "3-backlog.md"
        cmd = f'python3 "{SKILLS_ROOT}/{script_path}" --input "{input_file}" --output "{output_file}"'
    
    elif step_key == "5":  # 变更追踪
        output_file = project_dir / "4-CHANGELOG.md"
        cmd = f'python3 "{SKILLS_ROOT}/{script_path}" --output "{output_file}"'
    
    elif step_key == "6":  # 故事地图
        input_file = project_dir / "3-backlog.md"
        output_file = project_dir / "5-story-map.md"
        cmd = f'python3 "{SKILLS_ROOT}/{script_path}" --input "{input_file}" --output "{output_file}"'
    
    elif step_key == "7":  # 流程图
        input_file = project_dir / "2-PRD.md"
        output_file = project_dir / "6-flowchart.md"
        cmd = f'python3 "{SKILLS_ROOT}/{script_path}" --input "{input_file}" --output "{output_file}" --title "{project_name} 核心流程"'
    
    else:
        return
    
    print(f"\n🔄 执行: {step_name}")
    print("=" * 50)
    os.system(cmd)


def interactive_mode():
    """交互式模式"""
    while True:
        show_menu()
        choice = input("请选择: ").strip()
        
        if choice == "9":
            print("再见！")
            break
        
        elif choice == "1":
            run_new_project()
        
        elif choice == "8":
            project_name = select_project()
            if project_name:
                check_project_status(project_name)
        
        elif choice in STEPS:
            run_step(choice)
        
        else:
            print("[错误] 无效选择")
        
        print()
        input("按回车键继续...")
        print()


def main():
    parser = argparse.ArgumentParser(description='需求管理助手')
    parser.add_argument('--status', action='store_true', help='查看项目状态')
    parser.add_argument('--project', help='项目名称')
    args = parser.parse_args()
    
    if args.status and args.project:
        check_project_status(args.project)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
