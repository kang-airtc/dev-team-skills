#!/usr/bin/env python3
"""
需求澄清工具 - 五维澄清法
通过结构化提问，将模糊需求转化为清晰描述
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_QUESTION_BANK = SKILL_DIR / "assets" / "question-bank.md"


def load_questions(bank_path: Path) -> list:
    """从问题库加载问题列表"""
    questions = []
    if not bank_path.exists():
        print(f"[警告] 问题库不存在: {bank_path}")
        return get_builtin_questions()
    
    content = bank_path.read_text(encoding='utf-8')
    for line in content.splitlines():
        line = line.strip()
        if line and line[0].isdigit() and '.' in line[:3]:
            # 提取问题文本（去掉序号）
            question = re.sub(r'^\d+\.\s*', '', line)
            questions.append(question)
    
    return questions if questions else get_builtin_questions()


def get_builtin_questions() -> list:
    """内置默认问题（当问题库不可用时）"""
    return [
        "这个需求的提出者是谁？",
        "最终使用这个功能的目标用户是谁？",
        "请用一句话描述这个功能要做什么？",
        "这个功能的核心操作步骤是什么？",
        "用户输入哪些数据？输出什么结果？",
        "用户现在遇到什么问题？这个需求解决什么痛点？",
        "如果不做这个功能，会有什么后果？",
        "用户在什么场景下会使用这个功能？",
        "这个功能的使用频率如何？",
        "怎么定义这个功能'做完了'？列出 3-5 个验收条件。"
    ]


def ask_questions(questions: list) -> dict:
    """交互式提问，收集答案"""
    print("=" * 60)
    print("需求澄清 - 结构化提问")
    print("=" * 60)
    print("\n请回答以下问题（直接回车表示跳过）：\n")
    
    answers = {}
    categories = {
        "who": [],
        "what": [],
        "why": [],
        "when": [],
        "how": []
    }
    
    # 根据问题内容自动分类
    category_keywords = {
        "who": ["谁", "用户", "提出者", "使用", "技术水平"],
        "what": ["功能", "做什么", "操作", "输入", "输出", "步骤", "竞品"],
        "why": ["为什么", "痛点", "价值", "后果", "优先级", "解决"],
        "when": ["场景", "频率", "时间", "什么时候", "截止日期"],
        "how": ["验收", "测试", "性能", "完成", "条件", "验证"]
    }
    
    for i, question in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] {question}")
        answer = input("> ").strip()
        answers[question] = answer if answer else "（待确认）"
        
        # 自动分类
        categorized = False
        for cat, keywords in category_keywords.items():
            if any(kw in question for kw in keywords):
                categories[cat].append((question, answers[question]))
                categorized = True
                break
        
        if not categorized:
            categories["what"].append((question, answers[question]))
    
    return categories


def generate_output(categories: dict, original_req: str = "", output_path: Path = None) -> str:
    """生成澄清后的需求文档"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    lines = [
        "# 已澄清的需求",
        "",
        f"**澄清时间**: {now}",
        "",
        "## 1. 用户维度（Who）",
        ""
    ]
    
    for q, a in categories["who"]:
        lines.append(f"- **{q}**\n  - {a}")
    
    lines.extend([
        "",
        "## 2. 功能维度（What）",
        ""
    ])
    
    for q, a in categories["what"]:
        lines.append(f"- **{q}**\n  - {a}")
    
    lines.extend([
        "",
        "## 3. 价值维度（Why）",
        ""
    ])
    
    for q, a in categories["why"]:
        lines.append(f"- **{q}**\n  - {a}")
    
    lines.extend([
        "",
        "## 4. 场景维度（When）",
        ""
    ])
    
    for q, a in categories["when"]:
        lines.append(f"- **{q}**\n  - {a}")
    
    lines.extend([
        "",
        "## 5. 验收维度（How）",
        ""
    ])
    
    for q, a in categories["how"]:
        lines.append(f"- **{q}**\n  - {a}")
    
    if original_req:
        lines.extend([
            "",
            "## 6. 原始需求记录",
            "",
            f"```\n{original_req}\n```"
        ])
    
    content = "\n".join(lines)
    
    if output_path:
        output_path.write_text(content, encoding='utf-8')
        print(f"\n[成功] 已保存到: {output_path}")
    
    return content


def main():
    parser = argparse.ArgumentParser(description='需求澄清工具')
    parser.add_argument('--input', '-i', help='原始需求文件路径')
    parser.add_argument('--output', '-o', default='clarified-requirement.md', help='输出文件路径')
    parser.add_argument('--requirement', '-r', help='直接传入需求描述')
    parser.add_argument('--question-bank', '-q', help='自定义问题库路径')
    args = parser.parse_args()
    
    # 读取原始需求
    original_req = ""
    if args.input:
        input_path = Path(args.input)
        if input_path.exists():
            original_req = input_path.read_text(encoding='utf-8')
        else:
            print(f"[错误] 文件不存在: {input_path}")
            sys.exit(1)
    elif args.requirement:
        original_req = args.requirement
    
    # 加载问题库
    bank_path = Path(args.question_bank) if args.question_bank else DEFAULT_QUESTION_BANK
    questions = load_questions(bank_path)
    
    # 交互式提问
    categories = ask_questions(questions)
    
    # 生成输出
    output_path = Path(args.output)
    content = generate_output(categories, original_req, output_path)
    
    print("\n" + "=" * 60)
    print("需求澄清完成！")
    print("=" * 60)
    print(f"\n输出文件: {output_path.absolute()}")
    print("\n下一步建议:")
    print("  1. 检查并补充标记为'（待确认）'的项目")
    print("  2. 将此文件作为输入，运行 PRD 草稿生成 Skill")


if __name__ == "__main__":
    main()
