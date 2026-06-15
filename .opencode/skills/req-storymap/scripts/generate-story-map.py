#!/usr/bin/env python3
"""
用户故事地图生成器
将 Backlog 转化为可视化的故事地图
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_TEMPLATE = SKILL_DIR / "assets" / "story-map-template.md"

DEFAULT_PHASES = ["了解", "注册", "登录", "使用", "管理", "退出"]


def parse_backlog(backlog_path: Path) -> list:
    """解析 Backlog，提取 Epic 和 Story"""
    content = backlog_path.read_text(encoding='utf-8')
    
    epics = []
    current_epic = None
    current_story = None
    
    for line in content.splitlines():
        line = line.strip()
        
        # 识别 Epic
        epic_match = re.match(r'## Epic\s+(\d+):\s*(.+)', line)
        if epic_match:
            if current_epic:
                epics.append(current_epic)
            current_epic = {
                "id": int(epic_match.group(1)),
                "title": epic_match.group(2).strip(),
                "priority": "P0",
                "stories": []
            }
            continue
        
        # 识别 Epic 优先级
        if current_epic and "优先级" in line:
            prio_match = re.search(r'P\d', line)
            if prio_match:
                current_epic["priority"] = prio_match.group(0)
            continue
        
        # 识别 Story
        story_match = re.match(r'### Story\s+([\d.]+):\s*(.+)', line)
        if story_match and current_epic:
            current_story = {
                "id": story_match.group(1),
                "title": story_match.group(2).strip(),
                "priority": "P1",
                "acceptance": []
            }
            current_epic["stories"].append(current_story)
            continue
        
        # 识别 Story 优先级
        if current_story and "优先级" in line:
            prio_match = re.search(r'P\d', line)
            if prio_match:
                current_story["priority"] = prio_match.group(0)
            continue
    
    if current_epic:
        epics.append(current_epic)
    
    return epics


def assign_to_releases(epics: list) -> dict:
    """按优先级分配 Story 到不同 Release"""
    releases = {
        "MVP": [],
        "Release 2": [],
        "Release 3": []
    }
    
    for epic in epics:
        for story in epic["stories"]:
            story_with_epic = {
                **story,
                "epic_title": epic["title"]
            }
            
            if story["priority"] == "P0":
                releases["MVP"].append(story_with_epic)
            elif story["priority"] == "P1":
                releases["Release 2"].append(story_with_epic)
            else:
                releases["Release 3"].append(story_with_epic)
    
    return releases


def generate_table_rows(epics: list, releases: dict) -> str:
    """生成 Markdown 表格行"""
    rows = []
    
    for epic in epics:
        epic_name = epic["title"]
        stories = epic["stories"]
        
        if not stories:
            continue
        
        # 第一行：Epic 名 + 第一个 Story
        first_story = stories[0]
        release_cells = []
        for release_name in ["MVP", "Release 2", "Release 3"]:
            if first_story in releases[release_name]:
                release_cells.append(f" {first_story['title']} ({first_story['priority']}) ")
            else:
                release_cells.append(" ")
        
        row = f"| **{epic_name}** | {first_story['title']} |{'|'.join(release_cells)}|"
        rows.append(row)
        
        # 后续 Story 行
        for story in stories[1:]:
            release_cells = []
            for release_name in ["MVP", "Release 2", "Release 3"]:
                if story in releases[release_name]:
                    release_cells.append(f" {story['title']} ({story['priority']}) ")
                else:
                    release_cells.append(" ")
            
            row = f"| | {story['title']} |{'|'.join(release_cells)}|"
            rows.append(row)
    
    return "\n".join(rows)


def generate_mermaid(epics: list, phases: list) -> str:
    """生成 Mermaid 用户旅程图"""
    sections = []
    
    # 将 Epic 映射到阶段
    for phase in phases:
        matching_epics = [e for e in epics if any(kw in e["title"] for kw in [phase])]
        if not matching_epics:
            continue
        
        section_lines = [f"    section {phase}"]
        
        for epic in matching_epics:
            for story in epic["stories"][:3]:  # 每个阶段最多3个故事
                # 简单评分：P0=5, P1=4, P2=3
                score = {"P0": 5, "P1": 4, "P2": 3, "P3": 2}.get(story["priority"], 3)
                section_lines.append(f"      {story['title']}: {score}: 用户")
        
        sections.append("\n".join(section_lines))
    
    return "\n".join(sections)


def generate_story_map(epics: list, phases: list, template_path: Path = None) -> str:
    """生成完整的用户故事地图"""
    releases = assign_to_releases(epics)
    
    # 表格行
    table_rows = generate_table_rows(epics, releases)
    
    # Mermaid
    mermaid_sections = generate_mermaid(epics, phases)
    
    # 使用模板或生成默认格式
    if template_path and template_path.exists():
        template = template_path.read_text(encoding='utf-8')
        content = template.replace("{{project_name}}", "项目")
        content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
        content = content.replace("{{release_1}}", "Release 1 (MVP)")
        content = content.replace("{{release_2}}", "Release 2")
        content = content.replace("{{release_3}}", "Release 3")
        content = content.replace("{{rows}}", table_rows)
        content = content.replace("{{journey_title}}", "用户旅程")
        content = content.replace("{{mermaid_sections}}", mermaid_sections)
        content = content.replace("{{release_1_desc}}", f"包含 {len(releases['MVP'])} 个核心功能")
        content = content.replace("{{release_2_desc}}", f"包含 {len(releases['Release 2'])} 个增强功能")
        content = content.replace("{{release_3_desc}}", f"包含 {len(releases['Release 3'])} 个扩展功能")
        content = content.replace("{{gaps}}", "（暂无）")
    else:
        # 默认格式
        content = f"""# 用户故事地图

**生成时间**: {datetime.now().strftime("%Y-%m-%d")}

---

## Markdown 表格版

| 活动 | 任务 | Release 1 (MVP) | Release 2 | Release 3 |
|------|------|-----------------|-----------|-----------|
{table_rows}

---

## Mermaid 用户旅程图

```mermaid
journey
    title 用户旅程
{mermaid_sections}
```

---

## 版本说明

### Release 1 (MVP)
- 核心功能: {len(releases['MVP'])} 个 Story
- 目标: 让用户能完成最基本的任务

### Release 2
- 增强功能: {len(releases['Release 2'])} 个 Story
- 目标: 提升用户体验和效率

### Release 3
- 扩展功能: {len(releases['Release 3'])} 个 Story
- 目标: 差异化竞争和高级用户
"""
    
    return content


def main():
    parser = argparse.ArgumentParser(description='用户故事地图生成器')
    parser.add_argument('--input', '-i', required=True, help='Backlog 文件路径')
    parser.add_argument('--output', '-o', default='story-map.md', help='输出路径')
    parser.add_argument('--phases', '-p', help='用户旅程阶段（逗号分隔）')
    parser.add_argument('--template', '-t', help='自定义模板路径')
    args = parser.parse_args()
    
    # 读取 Backlog
    backlog_path = Path(args.input)
    if not backlog_path.exists():
        print(f"[错误] 文件不存在: {backlog_path}")
        sys.exit(1)
    
    # 解析阶段
    phases = DEFAULT_PHASES
    if args.phases:
        phases = [p.strip() for p in args.phases.split(",")]
    
    # 解析 Backlog
    print("[信息] 正在解析 Backlog...")
    epics = parse_backlog(backlog_path)
    print(f"[信息] 识别到 {len(epics)} 个 Epic")
    
    # 生成故事地图
    print("[信息] 正在生成故事地图...")
    template_path = Path(args.template) if args.template else DEFAULT_TEMPLATE
    story_map = generate_story_map(epics, phases, template_path)
    
    # 保存
    output_path = Path(args.output)
    output_path.write_text(story_map, encoding='utf-8')
    
    print(f"[成功] 故事地图已生成: {output_path.absolute()}")
    print(f"\n📊 统计:")
    print(f"  - Epic: {len(epics)}")
    print(f"  - MVP: {len([s for e in epics for s in e['stories'] if s['priority'] == 'P0'])} 个 Story")
    print(f"  - Release 2: {len([s for e in epics for s in e['stories'] if s['priority'] == 'P1'])} 个 Story")
    print(f"\n💡 提示：在支持 Mermaid 的平台上查看可渲染的旅程图")


if __name__ == "__main__":
    main()
