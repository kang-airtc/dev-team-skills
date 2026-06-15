#!/usr/bin/env python3
"""
测试助手 - 主控脚本
提供交互式菜单
"""

import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
PIPELINE_DIR = SKILL_DIR / "pipeline"
SKILLS_ROOT = SKILL_DIR.parent

STEPS = {
    "1": ("一键生成全部测试", "run-all.sh"),
    "2": ("生成单元测试", "test-unit/scripts/generate.py"),
    "3": ("生成接口测试", "test-api/scripts/generate.py"),
    "4": ("回归测试分析", "test-regression/scripts/analyze.sh"),
    "5": ("覆盖率分析", "test-coverage/scripts/analyze.py"),
    "6": ("生成测试报告", "test-report/scripts/generate.py"),
    "7": ("退出", None)
}


def show_menu():
    """显示主菜单"""
    print("=" * 50)
    print("    测试助手")
    print("=" * 50)
    print()
    for key, (name, _) in STEPS.items():
        print(f"{key}. {name}")
    print()


def run_step(step_key):
    """执行单个步骤"""
    step_name, script_path = STEPS[step_key]
    
    if step_key == "1":
        # 完整流程
        script = PIPELINE_DIR / "run-all.sh"
        os.system(f'bash "{script}"')
    elif script_path:
        script = SKILLS_ROOT / script_path
        if script_path.endswith('.sh'):
            os.system(f'bash "{script}"')
        else:
            os.system(f'python3 "{script}"')
    
    print(f"\n✅ {step_name} 完成")


def interactive_mode():
    """交互式模式"""
    while True:
        show_menu()
        choice = input("请选择: ").strip()
        
        if choice == "7":
            print("再见！")
            break
        
        if choice in STEPS:
            run_step(choice)
        else:
            print("[错误] 无效选择")
        
        print()
        input("按回车键继续...")
        print()


def main():
    interactive_mode()


if __name__ == "__main__":
    main()
