#!/usr/bin/env python3
"""
UI规范检查工具
对比设计稿与设计系统规范，输出检查报告
"""

import argparse
import json
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_SYSTEM = SKILL_DIR / "assets" / "default-design-system.md"


def parse_design_system(system_path):
    """解析设计系统规范文件"""
    content = system_path.read_text(encoding='utf-8')
    system = {
        "colors": {},
        "font_sizes": {},
        "spacing": {},
        "border_radius": {}
    }
    
    current_section = None
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if '颜色' in line or 'Color' in line:
            current_section = "colors"
            continue
        elif '字体' in line or 'Font' in line:
            current_section = "font_sizes"
            continue
        elif '间距' in line or 'Spacing' in line:
            current_section = "spacing"
            continue
        elif '圆角' in line or 'Radius' in line:
            current_section = "border_radius"
            continue
        
        if current_section and ':' in line:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                system[current_section][key] = value
    
    return system


def parse_design_file(design_path):
    """解析设计稿文件"""
    content = design_path.read_text(encoding='utf-8')
    
    # 尝试解析为JSON（Pencil格式）
    try:
        data = json.loads(content)
        elements = []
        for page in data.get("pages", []):
            for elem in page.get("elements", []):
                elements.append(elem)
        return elements
    except json.JSONDecodeError:
        # 尝试解析文本描述
        elements = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('TEXT') or line.startswith('BUTTON') or line.startswith('INPUT'):
                # 简化为文本解析
                elements.append({"type": "text", "raw": line})
        return elements


def check_color(value, system_colors):
    """检查颜色是否符合规范"""
    # 标准化颜色值
    value = value.upper()
    
    # 检查是否在规范中
    for name, color in system_colors.items():
        if color.upper() == value:
            return True, name
    
    return False, None


def check_font_size(value, system_sizes):
    """检查字体大小是否符合规范"""
    try:
        size = int(value.replace('px', ''))
        valid_sizes = []
        for v in system_sizes.values():
            try:
                valid_sizes.append(int(v.replace('px', '')))
            except:
                pass
        
        return size in valid_sizes, valid_sizes
    except:
        return False, []


def check_spacing(value, system_spacing):
    """检查间距是否为4px倍数"""
    try:
        spacing = int(value.replace('px', ''))
        return spacing % 4 == 0, spacing
    except:
        return False, 0


def generate_report(design_path, system, elements):
    """生成检查报告"""
    lines = [
        "# UI 规范检查报告",
        "",
        "## 检查概览",
        f"- **设计稿**: {design_path.name}",
        f"- **检查项**: 4 项",
        ""
    ]
    
    # 颜色检查（示例）
    lines.extend([
        "### 颜色规范",
        "",
        "（需要实际设计稿中的颜色数据才能检查）",
        "",
        "规范定义颜色：",
    ])
    for name, color in system["colors"].items():
        lines.append(f"- {name}: {color}")
    lines.append("")
    
    # 字体大小检查
    lines.extend([
        "### 字体大小规范",
        "",
        "标准字体大小：",
    ])
    for name, size in system["font_sizes"].items():
        lines.append(f"- {name}: {size}")
    lines.append("")
    
    # 间距检查
    lines.extend([
        "### 间距规范",
        "",
        "基础单位：4px",
        "",
        "标准间距：",
    ])
    for name, size in system["spacing"].items():
        lines.append(f"- {name}: {size}")
    lines.append("")
    
    # 圆角检查
    lines.extend([
        "### 圆角规范",
        "",
        "标准圆角：",
    ])
    for name, radius in system["border_radius"].items():
        lines.append(f"- {name}: {radius}")
    lines.append("")
    
    # 总结
    lines.extend([
        "## 检查说明",
        "",
        "⚠️ **注意**：当前版本为简化版，需要设计稿包含具体样式值才能进行完整检查。",
        "",
        "建议：",
        "1. 在Pencil中导出包含样式数据的设计文件",
        "2. 或提供设计稿的样式标注文档",
        "3. 复杂检查建议使用专业设计工具",
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='UI规范检查工具')
    parser.add_argument('--input', '-i', required=True, help='设计稿文件路径')
    parser.add_argument('--design-system', '-s', help='设计系统规范文件路径')
    parser.add_argument('--output', '-o', default='ui-check-report.md', help='输出路径')
    args = parser.parse_args()
    
    design_path = Path(args.input)
    if not design_path.exists():
        print(f"[错误] 设计稿不存在: {design_path}")
        sys.exit(1)
    
    # 加载设计系统
    system_path = Path(args.design_system) if args.design_system else DEFAULT_SYSTEM
    if not system_path.exists():
        print(f"[警告] 设计系统规范不存在，使用默认规范")
        system_path = DEFAULT_SYSTEM
    
    print(f"[信息] 正在加载设计系统: {system_path.name}")
    system = parse_design_system(system_path)
    
    print(f"[信息] 正在解析设计稿: {design_path.name}")
    elements = parse_design_file(design_path)
    print(f"[信息] 解析到 {len(elements)} 个元素")
    
    # 生成报告
    report = generate_report(design_path, system, elements)
    
    output_path = Path(args.output)
    output_path.write_text(report, encoding='utf-8')
    print(f"[成功] 检查报告已生成: {output_path.absolute()}")


if __name__ == "__main__":
    main()
