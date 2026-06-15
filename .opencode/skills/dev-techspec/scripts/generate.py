#!/usr/bin/env python3
"""dev-techspec: 按统一模板生成技术方案文档骨架"""

import argparse
import sys
from datetime import date
from pathlib import Path


# 模板路径（相对本脚本所在目录）
TEMPLATE_PATH = Path(__file__).parent.parent / 'references' / 'tech-spec-template.md'


def render(title: str, author: str) -> str:
    """读取模板，替换占位符，返回渲染后的 Markdown。

    用 replace 而非 str.format()——模板里可能出现 {code,msg,data}
    这样的字面文字，不应当成占位符处理。
    """
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f'模板文件不存在：{TEMPLATE_PATH}')

    template = TEMPLATE_PATH.read_text(encoding='utf-8')
    return (
        template
        .replace('{title}', title)
        .replace('{author}', author)
        .replace('{date}', date.today().isoformat())
    )


def main():
    parser = argparse.ArgumentParser(description='生成技术方案文档骨架')
    parser.add_argument('--title', '-t', required=True, help='方案标题')
    parser.add_argument('--author', '-a', required=True, help='作者')
    parser.add_argument('--output', '-o', required=True, help='输出 Markdown 路径')
    args = parser.parse_args()

    try:
        content = render(args.title, args.author)
    except FileNotFoundError as e:
        print(f'错误：{e}', file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding='utf-8')

    print(f'已生成：{out_path}')


if __name__ == '__main__':
    main()
