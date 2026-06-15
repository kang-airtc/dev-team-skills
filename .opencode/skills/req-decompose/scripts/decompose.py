#!/usr/bin/env python3
"""
需求拆解工具
将 PRD 拆解为 Epic → Story → Task 三层结构
"""

import argparse
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_TEMPLATE = SKILL_DIR / "assets" / "story-template.md"


def parse_prd(prd_path: Path) -> list:
    """解析 PRD，提取功能模块作为 Epic"""
    content = prd_path.read_text(encoding='utf-8')
    
    epics = []
    
    # 尝试从"功能详述"章节提取
    feature_section = extract_section(content, "功能详述")
    if feature_section:
        # 按标题分割功能点
        features = split_by_headings(feature_section)
        for i, feature in enumerate(features, 1):
            epic = create_epic_from_feature(i, feature)
            epics.append(epic)
    
    # 如果没有提取到，尝试从"用户故事"章节提取
    if not epics:
        story_section = extract_section(content, "用户故事")
        if story_section:
            stories = parse_user_stories(story_section)
            epic = {
                "id": 1,
                "title": "核心功能",
                "priority": "P0",
                "estimate": sum(s.get("estimate", 0) for s in stories),
                "stories": stories
            }
            epics.append(epic)
    
    # 如果还是没提取到，创建一个默认 Epic
    if not epics:
        epic = {
            "id": 1,
            "title": "主要功能",
            "priority": "P0",
            "estimate": 0,
            "stories": [{
                "id": "1.1",
                "title": "核心功能实现",
                "role": "用户",
                "want": "使用系统功能",
                "so_that": "完成业务目标",
                "priority": "P0",
                "estimate": 5,
                "acceptance": ["功能可用", "无明显Bug"],
                "tasks": []
            }]
        }
        epics.append(epic)
    
    return epics


def extract_section(content: str, section_name: str) -> str:
    """提取指定章节的内容"""
    pattern = rf'## \d*\.?\s*{re.escape(section_name)}.*?(?=\n## [^#]|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(0)
    return ""


def split_by_headings(section: str) -> list:
    """按四级标题（####）分割章节，提取具体功能项"""
    parts = re.split(r'\n####\s+', section)
    return [p.strip() for p in parts if p.strip() and not p.strip().startswith("#")]


def create_epic_from_feature(index: int, feature_text: str) -> dict:
    """从功能描述创建 Epic"""
    lines = feature_text.splitlines()
    title = lines[0].strip() if lines else f"功能 {index}"
    
    # 清理标题中的 Markdown 标记
    title = re.sub(r'^#{1,4}\s*', '', title)
    
    epic = {
        "id": index,
        "title": title,
        "priority": "P0" if index == 1 else "P1",
        "estimate": 0,
        "stories": []
    }
    
    # 从功能描述中提取用户故事
    story = create_story_from_text(f"{index}.1", title, feature_text)
    epic["stories"].append(story)
    epic["estimate"] = story["estimate"]
    
    return epic


def create_story_from_text(story_id: str, title: str, text: str) -> dict:
    """从文本创建用户故事"""
    # 尝试提取角色
    role = "用户"
    role_match = re.search(r'作为\s*(.+?)[，,]', text)
    if role_match:
        role = role_match.group(1).strip()
    
    # 尝试提取功能描述
    want = f"使用{title}"
    want_match = re.search(r'我希望\s*(.+?)[，,]', text)
    if want_match:
        want = want_match.group(1).strip()
    
    # 尝试提取价值
    so_that = "完成目标"
    so_that_match = re.search(r'以便于\s*(.+?)[，,。]', text)
    if so_that_match:
        so_that = so_that_match.group(1).strip()
    
    # 估算（基于内容复杂度）
    estimate = calculate_estimate(text)
    
    # 提取验收标准
    acceptance = extract_acceptance(text)
    
    # 生成任务
    tasks = generate_tasks(story_id, title)
    
    return {
        "id": story_id,
        "title": title,
        "role": role,
        "want": want,
        "so_that": so_that,
        "priority": "P0",
        "estimate": estimate,
        "acceptance": acceptance,
        "tasks": tasks
    }


def calculate_estimate(text: str) -> int:
    """基于文本复杂度计算 story points"""
    lines = len([l for l in text.splitlines() if l.strip()])
    if lines < 3:
        return 3
    elif lines < 8:
        return 5
    elif lines < 15:
        return 8
    else:
        return 13


def extract_acceptance(text: str) -> list:
    """提取验收标准"""
    acceptance = []
    
    # 查找列表项
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("-") or line.startswith("*"):
            item = line[1:].strip()
            if any(kw in item for kw in ["必须", "应该", "需要", "验证", "确认", "检查"]):
                acceptance.append(item)
    
    if not acceptance:
        acceptance = ["功能可用", "无明显Bug", "符合需求描述"]
    
    return acceptance[:5]  # 最多5条


def generate_tasks(story_id: str, story_title: str) -> list:
    """为用户故事生成默认任务"""
    tasks = []
    
    # 前端任务
    tasks.append({
        "id": f"{story_id}.1",
        "title": f"前端：{story_title}页面",
        "type": "前端",
        "estimate": "4h",
        "assignee": "（待分配）"
    })
    
    # 后端任务
    tasks.append({
        "id": f"{story_id}.2",
        "title": f"后端：{story_title}接口",
        "type": "后端",
        "estimate": "6h",
        "assignee": "（待分配）"
    })
    
    # 测试任务
    tasks.append({
        "id": f"{story_id}.3",
        "title": f"测试：{story_title}验收",
        "type": "测试",
        "estimate": "2h",
        "assignee": "（待分配）"
    })
    
    return tasks


def generate_backlog(epics: list, estimate_type: str = "story-points") -> str:
    """生成 Backlog Markdown"""
    lines = [
        "# 需求拆解 - Backlog",
        "",
        f"**生成时间**: 自动生成",
        f"**估算方式**: {estimate_type}",
        "",
        "---",
        ""
    ]
    
    for epic in epics:
        lines.extend([
            f"## Epic {epic['id']}: {epic['title']}",
            "",
            f"- **优先级**: {epic['priority']}",
            f"- **估算**: {epic['estimate']} story points",
            ""
        ])
        
        for story in epic["stories"]:
            lines.extend([
                f"### Story {story['id']}: {story['title']}",
                "",
                f"**作为** {story['role']}，",
                f"**我希望** {story['want']}，",
                f"**以便于** {story['so_that']}。",
                "",
                f"- **优先级**: {story['priority']}",
                f"- **估算**: {story['estimate']} story points",
                "",
                "**验收标准**："
            ])
            
            for acc in story["acceptance"]:
                lines.append(f"- [ ] {acc}")
            
            lines.append("")
            
            # 任务
            for task in story["tasks"]:
                lines.extend([
                    f"#### Task {task['id']}: {task['title']}",
                    "",
                    f"- **类型**: {task['type']}",
                    f"- **估算**: {task['estimate']}",
                    f"- **负责人**: {task['assignee']}",
                    ""
                ])
    
    return "\n".join(lines)


def parse_user_stories(section: str) -> list:
    """从用户故事章节解析故事列表"""
    stories = []
    
    # 查找故事标题
    story_blocks = re.split(r'###\s+', section)
    
    for i, block in enumerate(story_blocks[1:], 1):  # 跳过第一个空块
        story = create_story_from_text(f"1.{i}", f"故事 {i}", block)
        stories.append(story)
    
    return stories if stories else [create_story_from_text("1.1", "核心功能", section)]


def main():
    parser = argparse.ArgumentParser(description='需求拆解工具')
    parser.add_argument('--input', '-i', required=True, help='PRD 文档路径')
    parser.add_argument('--output', '-o', default='backlog.md', help='输出 Backlog 路径')
    parser.add_argument('--estimate', '-e', default='story-points', 
                       choices=['story-points', 'hours'], help='估算方式')
    args = parser.parse_args()
    
    # 读取 PRD
    prd_path = Path(args.input)
    if not prd_path.exists():
        print(f"[错误] 文件不存在: {prd_path}")
        sys.exit(1)
    
    # 解析 PRD
    print("[信息] 正在解析 PRD...")
    epics = parse_prd(prd_path)
    print(f"[信息] 识别到 {len(epics)} 个 Epic")
    
    # 生成 Backlog
    print("[信息] 正在生成 Backlog...")
    backlog = generate_backlog(epics, args.estimate)
    
    # 保存
    output_path = Path(args.output)
    output_path.write_text(backlog, encoding='utf-8')
    
    print(f"[成功] Backlog 已生成: {output_path.absolute()}")
    print(f"\n📊 统计:")
    print(f"  - Epic 数量: {len(epics)}")
    print(f"  - Story 数量: {sum(len(e['stories']) for e in epics)}")
    print(f"  - Task 数量: {sum(len(s['tasks']) for e in epics for s in e['stories'])}")
    print(f"\n⚠️  提示：估算值为预估值，实际开发前请团队评估")


if __name__ == "__main__":
    main()
