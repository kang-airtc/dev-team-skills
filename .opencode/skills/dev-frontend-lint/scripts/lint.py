#!/usr/bin/env python3
"""dev-frontend-lint: 前端代码规范检查（基于正则的轻量 lint）

只覆盖最高频的几条规则，不替代 ESLint。复杂的语法/类型检查交给专业工具。
"""

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass


# ---------- 规则定义 ----------
# 每条规则：(severity, name, 正则模式, 描述)
RULES = [
    ('P1', 'no-raw-fetch',
     re.compile(r'\bfetch\s*\('),
     '直接调用 fetch()，应通过 src/lib/api.ts 统一封装'),
    ('P1', 'no-raw-axios',
     re.compile(r'\baxios\.(get|post|put|delete|patch)\s*\('),
     '直接调用 axios，应通过 src/lib/api.ts 统一封装'),
    ('P1', 'no-inline-style',
     re.compile(r'style\s*=\s*\{\{'),
     '使用了行内 style，应改用 Tailwind 或 CSS Module'),
    ('P3', 'no-any',
     re.compile(r':\s*any\b(?!\s*//.*?@ts-expect-error)'),
     'TypeScript 使用了 any 类型，必要时请加 // @ts-expect-error 注释'),
]

# 扫描的扩展名
SCAN_EXTS = {'.ts', '.tsx', '.js', '.jsx'}

# 忽略的目录
SKIP_DIRS = {'node_modules', '.next', 'dist', 'build', '.git', '__pycache__'}

# Next.js App Router 约定文件名（小写）：这些文件名是框架约定，
# 导出名必然与文件名不同（如 page.tsx 导出 HomePage），不参与"文件名-导出一致"检查
NEXT_RESERVED_NAMES = {
    'page', 'layout', 'loading', 'error', 'not-found',
    'template', 'default', 'head', 'route', 'middleware',
}


@dataclass
class Violation:
    severity: str
    rule: str
    file: str
    line: int
    message: str
    snippet: str


def lint_file(path: Path, root: Path) -> list:
    """对单个文件跑所有规则，返回违规清单"""
    violations = []
    rel_path = str(path.relative_to(root))

    try:
        content = path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, OSError):
        return violations  # 跳过二进制或无法读取的文件

    for line_no, line in enumerate(content.splitlines(), start=1):
        # 跳过注释行
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('*'):
            continue
        for severity, rule_name, pattern, message in RULES:
            if pattern.search(line):
                violations.append(Violation(
                    severity=severity,
                    rule=rule_name,
                    file=rel_path,
                    line=line_no,
                    message=message,
                    snippet=line.strip()[:100],
                ))

    # 文件级检查：文件名与默认导出是否一致
    name_violation = check_filename_export(path, content, rel_path)
    if name_violation:
        violations.append(name_violation)

    return violations


def check_filename_export(path: Path, content: str, rel_path: str):
    """检查文件名是否与 export default 的标识符一致（仅针对 .tsx / .jsx 组件）。

    Next.js App Router 约定文件（page / layout / loading / error / ...）
    必然命名不一致，跳过。
    """
    if path.suffix not in {'.tsx', '.jsx'}:
        return None

    if path.stem.lower() in NEXT_RESERVED_NAMES:
        return None

    # 提取默认导出的标识符
    m = re.search(r'export\s+default\s+(?:function\s+|class\s+)?(\w+)', content)
    if not m:
        return None

    exported = m.group(1)
    expected = path.stem  # 不含扩展名的文件名
    if exported != expected:
        return Violation(
            severity='P2',
            rule='filename-export-mismatch',
            file=rel_path,
            line=1,
            message=f'默认导出 `{exported}` 与文件名 `{expected}` 不一致',
            snippet='',
        )
    return None


def walk_files(root: Path):
    """遍历目录，yield 需要扫描的文件路径"""
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix not in SCAN_EXTS:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def render_report(violations: list, scanned_count: int) -> str:
    """渲染 Markdown 报告"""
    lines = ['# 前端规范检查报告', '']
    lines.append(f'**扫描文件**：{scanned_count} 个')
    lines.append(f'**违规总数**：{len(violations)} 处')
    lines.append('')

    if not violations:
        lines.append('✅ 未发现违规项。')
        return '\n'.join(lines)

    # 按严重程度分组
    for severity in ('P1', 'P2', 'P3'):
        group = [v for v in violations if v.severity == severity]
        if not group:
            continue
        title_map = {'P1': '严重违规', 'P2': '一般违规', 'P3': '风格建议'}
        lines.append(f'## {severity} {title_map[severity]}')
        lines.append('')
        for v in group:
            line = f'- `{v.file}:{v.line}` [{v.rule}] {v.message}'
            if v.snippet:
                line += f'\n  > `{v.snippet}`'
            lines.append(line)
        lines.append('')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='前端代码规范检查')
    parser.add_argument('--path', '-p', default='./src', help='扫描目录（默认 ./src）')
    parser.add_argument('--output', '-o', help='输出报告路径（默认 stdout）')
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f'错误：目录不存在 {root}', file=sys.stderr)
        sys.exit(1)

    all_violations = []
    file_count = 0
    for path in walk_files(root):
        file_count += 1
        all_violations.extend(lint_file(path, root))

    report = render_report(all_violations, file_count)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding='utf-8')
        print(f'已生成报告：{out_path}（{len(all_violations)} 处违规）')
    else:
        print(report)


if __name__ == '__main__':
    main()
