#!/usr/bin/env python3
"""dev-backend-lint: 后端代码规范检查（基于正则的轻量 lint）

重点：响应格式 {code,msg,data} 一致性、错误码必须在字典中注册。
其他复杂规则交给专业工具（如 ruff、pylint）。
"""

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass


# 错误码字典文件（相对本脚本所在目录）
CODES_FILE = Path(__file__).parent.parent / 'references' / 'error-codes.md'

# 行级规则
LINE_RULES = [
    ('P1', 'no-raw-exception',
     re.compile(r'\braise\s+(Exception|RuntimeError)\s*\('),
     '裸抛 Exception/RuntimeError，应使用业务异常类（如 BizError）'),
    ('P1', 'no-print',
     re.compile(r'^\s*print\s*\('),
     '使用了 print()，应改用 logger.info / logger.error'),
    ('P1', 'response-missing-code',
     re.compile(r'^\s*return\s+\{\s*[\'"]data[\'"]\s*:'),
     '响应缺少 code 字段，应为 {code, msg, data} 三字段结构'),
]

# 错误码使用模式：覆盖两种形态
#   - 函数参数：code=1234（如 BizError(code=1234, ...)）
#   - dict 字面量："code": 1234（如 {"code": 1234, "msg": ...}）
CODE_USAGE_PATTERNS = [
    re.compile(r'\bcode\s*=\s*(\d+)\b'),
    re.compile(r'["\']code["\']\s*:\s*(\d+)\b'),
]

SCAN_EXTS = {'.py'}
SKIP_DIRS = {'__pycache__', '.git', 'venv', '.venv', 'tests', 'test', 'migrations'}


@dataclass
class Violation:
    severity: str
    rule: str
    file: str
    line: int
    message: str
    snippet: str


def load_registered_codes() -> set:
    """从 error-codes.md 解析所有已注册的错误码"""
    if not CODES_FILE.exists():
        print(f'警告：错误码字典不存在 {CODES_FILE}', file=sys.stderr)
        return set()

    codes = {0}  # 0 永远代表成功，必然合规
    text = CODES_FILE.read_text(encoding='utf-8')
    # 表格行格式：| 1001 | msg | 说明 |
    for m in re.finditer(r'^\|\s*(\d+)\s*\|', text, re.MULTILINE):
        codes.add(int(m.group(1)))
    return codes


def lint_file(path: Path, root: Path, registered_codes: set) -> list:
    violations = []
    rel_path = str(path.relative_to(root))

    try:
        content = path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, OSError):
        return violations

    for line_no, line in enumerate(content.splitlines(), start=1):
        # 跳过注释行
        stripped = line.strip()
        if stripped.startswith('#'):
            continue

        # 行级规则
        for severity, rule_name, pattern, message in LINE_RULES:
            if pattern.search(line):
                violations.append(Violation(
                    severity=severity,
                    rule=rule_name,
                    file=rel_path,
                    line=line_no,
                    message=message,
                    snippet=line.strip()[:100],
                ))

        # 错误码合规检查（同一行去重，避免一行被多种 pattern 匹配重复报）
        seen_codes = set()
        for pattern in CODE_USAGE_PATTERNS:
            for m in pattern.finditer(line):
                code = int(m.group(1))
                if code in seen_codes:
                    continue
                seen_codes.add(code)
                # 跳过 HTTP 状态码（200-599）
                if 200 <= code < 600:
                    continue
                if code not in registered_codes:
                    violations.append(Violation(
                        severity='P1',
                        rule='unregistered-code',
                        file=rel_path,
                        line=line_no,
                        message=f'错误码 {code} 未在 error-codes.md 中注册',
                        snippet=stripped[:100],
                    ))
                elif not (code == 0 or 1000 <= code < 3000):
                    violations.append(Violation(
                        severity='P2',
                        rule='code-out-of-range',
                        file=rel_path,
                        line=line_no,
                        message=f'错误码 {code} 不在 1000-2999 段',
                        snippet=stripped[:100],
                    ))

    return violations


def walk_files(root: Path):
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix not in SCAN_EXTS:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def render_report(violations: list, scanned: int, code_count: int) -> str:
    lines = ['# 后端规范检查报告', '']
    lines.append(f'**扫描文件**：{scanned} 个 .py 文件')
    lines.append(f'**已注册错误码**：{code_count} 个')
    lines.append(f'**违规总数**：{len(violations)} 处')
    lines.append('')

    if not violations:
        lines.append('✅ 未发现违规项。')
        return '\n'.join(lines)

    title_map = {'P1': '严重违规', 'P2': '一般违规', 'P3': '风格建议'}
    for severity in ('P1', 'P2', 'P3'):
        group = [v for v in violations if v.severity == severity]
        if not group:
            continue
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
    parser = argparse.ArgumentParser(description='后端代码规范检查')
    parser.add_argument('--path', '-p', default='./app', help='扫描目录（默认 ./app）')
    parser.add_argument('--output', '-o', help='输出报告路径（默认 stdout）')
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f'错误：目录不存在 {root}', file=sys.stderr)
        sys.exit(1)

    registered = load_registered_codes()
    all_violations = []
    file_count = 0
    for path in walk_files(root):
        file_count += 1
        all_violations.extend(lint_file(path, root, registered))

    report = render_report(all_violations, file_count, len(registered))

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding='utf-8')
        print(f'已生成报告：{out_path}（{len(all_violations)} 处违规）')
    else:
        print(report)


if __name__ == '__main__':
    main()
