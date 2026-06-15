#!/usr/bin/env python3
"""dev-pipeline/assistant.py
交互式开发助手——给那些不喜欢敲长命令的人。
本质是 run-step.sh 的菜单封装。
"""

import os
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
RUN_ALL = SCRIPT_DIR / 'run-all.sh'
RUN_STEP = SCRIPT_DIR / 'run-step.sh'

STEPS = [
    ('arch',          '生成架构图（draw.io）'),
    ('sequence',      '生成时序图（draw.io）'),
    ('techspec',      '生成技术方案文档骨架'),
    ('frontend-lint', '前端规范检查'),
    ('backend-lint',  '后端规范检查'),
    ('spec-diff',     '规范偏差对比'),
    ('deps-audit',    '依赖安全审计（Next.js + FastAPI）'),
    ('apidoc',        '生成接口文档（Word）'),
]


def show_menu():
    print('\n' + '=' * 40)
    print('   Dev Pipeline 开发助手')
    print('=' * 40)
    print('  0. 一键完整流程（跑所有 8 步）')
    for idx, (name, desc) in enumerate(STEPS, start=1):
        print(f'  {idx}. {desc}')
    print('  q. 退出')
    print('-' * 40)


def prompt(text: str, default: str = '') -> str:
    suffix = f' [{default}]' if default else ''
    val = input(f'{text}{suffix}: ').strip()
    return val or default


def run_pipeline(project: str, inputs: str):
    subprocess.run(['bash', str(RUN_ALL), project, inputs])


def run_step(step: str, project: str, inputs: str):
    subprocess.run(['bash', str(RUN_STEP), step, project, inputs])


def main():
    project = prompt('项目名称', 'dev-output')
    inputs = prompt('输入目录', './inputs')

    while True:
        show_menu()
        choice = input('请选择: ').strip().lower()
        if choice == 'q':
            print('再见。')
            break
        if choice == '0':
            run_pipeline(project, inputs)
            continue
        try:
            idx = int(choice)
            if 1 <= idx <= len(STEPS):
                step_name, _ = STEPS[idx - 1]
                run_step(step_name, project, inputs)
                continue
        except ValueError:
            pass
        print('无效输入，请重选')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n已取消。')
        sys.exit(0)
