#!/usr/bin/env python3
"""
记录 design-pencil 产物摘要，写入 Markdown 报告
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='记录设计稿产物摘要')
    parser.add_argument('--file', '-f', required=True, help='.pen 文件路径')
    parser.add_argument('--pages', '-p', default='', help='包含的页面名称（逗号分隔）')
    parser.add_argument('--notes', '-n', default='', help='备注')
    parser.add_argument('--output', '-o', default='', help='报告输出路径（默认同目录下同名 .md）')
    args = parser.parse_args()

    pen_path = Path(args.file)
    if not pen_path.exists():
        print(f"[错误] .pen 文件不存在: {pen_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else pen_path.with_suffix('.md')

    pages = [p.strip() for p in args.pages.split(',') if p.strip()]
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    lines = [
        f"# 设计稿产物：{pen_path.stem}",
        "",
        f"**生成时间**: {now}  **文件**: `{pen_path}`",
        "",
        "## 页面清单",
        "",
    ]

    if pages:
        for i, page in enumerate(pages, 1):
            lines.append(f"{i}. {page}")
    else:
        lines.append("（未指定页面，请手动补充）")

    lines.extend([
        "",
        "## 备注",
        "",
        args.notes if args.notes else "（无）",
        "",
        "## 后续步骤",
        "",
        "- [ ] 用 `design-review` 进行多角色评审",
        "- [ ] 用 `design-ui-check` 检查数值合规",
        "",
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"[成功] 产物报告已写入: {output_path}")


if __name__ == '__main__':
    main()
