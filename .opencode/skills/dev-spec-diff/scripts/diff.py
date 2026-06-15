#!/usr/bin/env python3
"""dev-spec-diff: 规范-代码对照工具

按一份固定的"规则签名表"扫描代码，输出三类偏差：
  - 违规：禁止使用的模式在代码里出现
  - 已覆盖：必须使用的模式在代码里有应用
  - 未覆盖：必须使用的模式在代码里没找到（规范定义了但代码没用上）

规则签名表是手工维护的，对应 dev-backend-lint/references/backend-standard.md
里定义的核心规则。规范升级时同步更新这里即可。
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass


# 规则签名：(规则名, 在代码中查找的正则, 类型)
#   must_have    -> 必须出现，未出现 = 未覆盖
#   must_not_have -> 禁止出现，出现 = 违规
RULE_SIGNATURES = [
    ('响应使用 {code, msg, data} 三字段',
     re.compile(r'["\']code["\']\s*:'), 'must_have'),
    ('使用业务异常类 BizError',
     re.compile(r'\bBizError\b'), 'must_have'),
    ('禁止裸抛 Exception',
     re.compile(r'\braise\s+(Exception|RuntimeError)\s*\('), 'must_not_have'),
    ('使用 logger 记录日志',
     re.compile(r'\blogger\.(info|error|warning|debug)\b'), 'must_have'),
    ('禁止 print 输出',
     re.compile(r'^\s*print\s*\(', re.MULTILINE), 'must_not_have'),
    ('使用 selectinload/joinedload 优化 ORM 查询',
     re.compile(r'\b(selectinload|joinedload)\b'), 'must_have'),
]

SCAN_EXTS = {'.py'}
SKIP_DIRS = {'__pycache__', '.git', 'venv', '.venv', 'tests', 'test', 'migrations'}


@dataclass
class Hit:
    file: str
    line: int
    snippet: str


def walk_files(root: Path):
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix not in SCAN_EXTS:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def scan_rule(pattern: re.Pattern, root: Path) -> list:
    """扫描整个目录，返回所有命中的位置"""
    hits = []
    for path in walk_files(root):
        try:
            text = path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue
        for m in pattern.finditer(text):
            line_no = text.count('\n', 0, m.start()) + 1
            line_text = text.splitlines()[line_no - 1] if line_no <= len(text.splitlines()) else ''
            hits.append(Hit(
                file=str(path.relative_to(root)),
                line=line_no,
                snippet=line_text.strip()[:100],
            ))
    return hits


def render_report(results: dict, scanned: int, spec_path: str) -> str:
    """results: {rule_name: {'kind': str, 'hits': [Hit]}}"""
    lines = ['# 规范偏差报告', '']
    lines.append(f'**对照规范**：{spec_path}')
    lines.append(f'**扫描文件**：{scanned} 个 .py 文件')
    lines.append('')

    violations = [r for r, d in results.items() if d['kind'] == 'must_not_have' and d['hits']]
    covered = [r for r, d in results.items() if d['kind'] == 'must_have' and d['hits']]
    uncovered = [r for r, d in results.items() if d['kind'] == 'must_have' and not d['hits']]

    lines.append(f'**违规规则**：{len(violations)} 条')
    lines.append(f'**已覆盖规则**：{len(covered)} 条')
    lines.append(f'**未覆盖规则**：{len(uncovered)} 条')
    lines.append('')

    if violations:
        lines.append('## 1. 违规项（代码不符合规范）')
        lines.append('')
        for rule in violations:
            hits = results[rule]['hits']
            lines.append(f'### {rule}（{len(hits)} 处）')
            lines.append('')
            for h in hits[:5]:  # 最多展示 5 条
                lines.append(f'- `{h.file}:{h.line}`：`{h.snippet}`')
            if len(hits) > 5:
                lines.append(f'- ...（还有 {len(hits) - 5} 处省略）')
            lines.append('')

    if uncovered:
        lines.append('## 2. 未覆盖项（规范定义了但代码没用上）')
        lines.append('')
        for rule in uncovered:
            lines.append(f'- {rule}')
        lines.append('')
        lines.append('> 提示：未覆盖不一定是问题——可能这部分功能还没写到。但如果生产代码里完全没用到这些模式，说明规范没落地。')
        lines.append('')

    if covered:
        lines.append('## 3. 已覆盖项（规范在代码中有应用）')
        lines.append('')
        for rule in covered:
            count = len(results[rule]['hits'])
            lines.append(f'- {rule}（{count} 处应用）')
        lines.append('')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='规范-代码对照工具')
    parser.add_argument('--code', '-c', required=True, help='代码目录')
    parser.add_argument('--spec', '-s', help='规范文档路径（仅用于报告标注，实际规则在脚本内）')
    parser.add_argument('--output', '-o', help='输出报告路径（默认 stdout）')
    args = parser.parse_args()

    root = Path(args.code).resolve()
    if not root.exists():
        print(f'错误：代码目录不存在 {root}', file=sys.stderr)
        sys.exit(1)

    file_count = sum(1 for _ in walk_files(root))

    results = {}
    for rule_name, pattern, kind in RULE_SIGNATURES:
        hits = scan_rule(pattern, root)
        results[rule_name] = {'kind': kind, 'hits': hits}

    spec_label = args.spec or '(内置规则签名表)'
    report = render_report(results, file_count, spec_label)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding='utf-8')
        violations = sum(1 for d in results.values() if d['kind'] == 'must_not_have' and d['hits'])
        print(f'已生成报告：{out_path}（{violations} 条违规）')
    else:
        print(report)


if __name__ == '__main__':
    main()
