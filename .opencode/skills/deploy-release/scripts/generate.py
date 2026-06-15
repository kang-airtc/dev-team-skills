#!/usr/bin/env python3
"""
发布说明生成器
基于 CHANGELOG 生成版本发布说明
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def parse_changelog(changelog_path: Path) -> dict:
    """解析 CHANGELOG"""
    content = changelog_path.read_text(encoding='utf-8')
    
    sections = {
        "features": [],
        "fixes": [],
        "performance": [],
        "docs": [],
        "other": []
    }
    
    current_section = None
    for line in content.splitlines():
        line = line.strip()
        
        if line.startswith("### Features"):
            current_section = "features"
        elif line.startswith("### Bug Fixes"):
            current_section = "fixes"
        elif line.startswith("### Performance"):
            current_section = "performance"
        elif line.startswith("### Documentation"):
            current_section = "docs"
        elif line.startswith("###"):
            current_section = "other"
        elif line.startswith("-") and current_section:
            sections[current_section].append(line[1:].strip())
    
    return sections


def detect_previous_version(current: str, changelog_path: Path) -> str:
    """优先从 CHANGELOG 解析上一版本号；否则用 git tag 列表推断；都没有时返回占位符。"""
    if changelog_path.exists():
        versions = re.findall(r"^##\s*\[([^\]]+)\]", changelog_path.read_text(encoding="utf-8"), re.MULTILINE)
        for v in versions:
            if v != current:
                return v
    try:
        out = subprocess.check_output(
            ["git", "tag", "--sort=-v:refname"], stderr=subprocess.DEVNULL, text=True
        )
        for tag in out.splitlines():
            tag = tag.strip()
            if tag and tag != current:
                return tag
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return "<previous-version>"


def generate_release_notes(version: str, previous_version: str, changes: dict) -> str:
    """生成发布说明"""
    lines = [
        f"# Release Notes - {version}",
        "",
        f"**发布日期**: {datetime.now().strftime('%Y-%m-%d')}",
        "**版本类型**: 功能版本",
        "",
        "## 变更摘要",
        ""
    ]
    
    if changes["features"]:
        lines.append("### 新增功能")
        for item in changes["features"]:
            lines.append(f"- {item}")
        lines.append("")
    
    if changes["fixes"]:
        lines.append("### 问题修复")
        for item in changes["fixes"]:
            lines.append(f"- {item}")
        lines.append("")
    
    if changes["performance"]:
        lines.append("### 性能优化")
        for item in changes["performance"]:
            lines.append(f"- {item}")
        lines.append("")
    
    lines.extend([
        "## 升级指南",
        "",
        "1. 备份数据库",
        "2. 拉取最新代码：`git pull origin main`",
        "3. 更新依赖：`docker-compose build --no-cache`",
        "4. 执行数据库迁移：`docker-compose exec backend alembic upgrade head`",
        "5. 重启服务：`docker-compose up -d`",
        "",
        "## 回滚方案",
        "",
        "如升级后出现问题，按以下步骤回滚：",
        "",
        f"1. 停止服务：`docker-compose down`",
        f"2. 切换到上一个版本：`git checkout {previous_version}`",
        "3. 恢复数据库（如有迁移）：`docker-compose exec backend alembic downgrade -1`",
        "4. 重启服务：`docker-compose up -d`",
        "",
        "## 兼容性说明",
        "",
        "- **数据库**: 如有 Schema 变更，需执行迁移",
        "- **API**: 向下兼容",
        "- **前端**: 建议清除浏览器缓存",
        ""
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='发布说明生成器')
    parser.add_argument('--version', '-v', required=True, help='版本号')
    parser.add_argument('--changelog', default='CHANGELOG.md', help='CHANGELOG 文件')
    parser.add_argument('--previous-version', help='回滚目标版本号；不传时按 CHANGELOG/git tag 推断')
    parser.add_argument('--output', '-o', help='输出路径')
    args = parser.parse_args()

    changelog_path = Path(args.changelog)
    if not changelog_path.exists():
        print(f"[错误] CHANGELOG 不存在: {changelog_path}")
        sys.exit(1)

    print(f"[信息] 解析 CHANGELOG: {changelog_path}")
    changes = parse_changelog(changelog_path)

    total_changes = sum(len(v) for v in changes.values())
    print(f"[信息] 发现 {total_changes} 条变更记录")

    previous_version = args.previous_version or detect_previous_version(args.version, changelog_path)
    print(f"[信息] 回滚目标版本: {previous_version}")

    # 生成发布说明
    notes = generate_release_notes(args.version, previous_version, changes)
    
    output_path = Path(args.output) if args.output else Path(f"release-{args.version}.md")
    output_path.write_text(notes, encoding='utf-8')
    
    print(f"[成功] 发布说明已生成: {output_path}")


if __name__ == "__main__":
    main()
