#!/usr/bin/env python3
"""
设计评审工具 - 多角色视角评审
读取设计稿，按不同角色视角输出评审报告
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CHECKLIST_PATH = SKILL_DIR / "assets" / "review-checklist.md"
AGENTS_PATH = Path("AGENTS.md")
AGENT_DIR = Path("agent")

DEFAULT_ROLES = ["ui-designer", "frontend-dev", "product-manager", "backend-dev"]

ROLE_DEFINITIONS = {
    "ui-designer": {
        "name": "UI Designer",
        "focus": "视觉层面",
        "sections": ["视觉层次", "色彩规范", "字体与排版", "间距与布局"]
    },
    "frontend-dev": {
        "name": "Frontend Dev",
        "focus": "实现层面",
        "sections": ["实现可行性", "性能考虑", "状态管理"]
    },
    "product-manager": {
        "name": "Product Manager",
        "focus": "业务层面",
        "sections": ["信息架构", "文案", "业务目标"]
    },
    "backend-dev": {
        "name": "Backend Dev",
        "focus": "数据层面",
        "sections": ["接口可行性", "权限与安全"]
    }
}


def load_checklist():
    """加载检查清单"""
    if not CHECKLIST_PATH.exists():
        return {}
    
    content = CHECKLIST_PATH.read_text(encoding='utf-8')
    checklist = {}
    current_section = None
    current_role = None
    
    for line in content.splitlines():
        line = line.strip()
        
        # 识别角色标题
        if line.startswith('## ') and '检查项' in line:
            role_match = re.match(r'##\s+(.+?)\s+检查项', line)
            if role_match:
                role_name = role_match.group(1)
                # 映射角色名到key
                for key, role in ROLE_DEFINITIONS.items():
                    if role['name'] == role_name:
                        current_role = key
                        checklist[current_role] = []
                        break
        
        # 识别检查项
        elif line.startswith('- [ ]') and current_role:
            item = line.replace('- [ ]', '').strip()
            checklist[current_role].append(item)
    
    return checklist


def generate_mock_review(role_key, design_name):
    """生成模拟评审意见（实际项目中应基于真实设计分析）"""
    role = ROLE_DEFINITIONS[role_key]
    opinions = []
    
    # 根据角色生成示例意见
    if role_key == "ui-designer":
        opinions = [
            {
                "priority": "P1",
                "location": "登录按钮",
                "issue": "按钮对比度不足",
                "detail": "当前背景色对比度低于 WCAG AA 标准",
                "suggestion": "加深主色或调整文字颜色"
            },
            {
                "priority": "P2",
                "location": "输入框",
                "issue": "缺少焦点状态设计",
                "detail": "聚焦时无视觉反馈",
                "suggestion": "添加边框颜色变化"
            }
        ]
    elif role_key == "frontend-dev":
        opinions = [
            {
                "priority": "P1",
                "location": "密码输入框",
                "issue": "密码可见切换需要额外状态管理",
                "detail": "需要维护 showPassword 状态",
                "suggestion": "建议复用现有 Input 组件的密码模式"
            },
            {
                "priority": "P3",
                "location": "整体",
                "issue": "表单验证逻辑较复杂",
                "detail": "邮箱格式、密码强度需要多规则验证",
                "suggestion": "使用统一的表单验证库"
            }
        ]
    elif role_key == "product-manager":
        opinions = [
            {
                "priority": "P2",
                "location": "页面顶部",
                "issue": "缺少返回/关闭按钮",
                "detail": "用户可能误进入登录页，需要退出路径",
                "suggestion": "添加返回首页按钮"
            }
        ]
    elif role_key == "backend-dev":
        opinions = [
            {
                "priority": "P2",
                "location": "登录接口",
                "issue": "需要支持多端登录状态管理",
                "detail": "PC端和移动端登录状态需要同步",
                "suggestion": "使用统一的 session/token 策略"
            }
        ]
    
    return opinions


def generate_report(design_name, roles, checklist):
    """生成评审报告"""
    lines = [
        f"# 设计评审报告：{design_name}",
        "",
        f"**评审时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**评审角色**: {', '.join(ROLE_DEFINITIONS[r]['name'] for r in roles)}",
        "",
        "---",
        ""
    ]
    
    all_opinions = {}
    
    # 各角色评审
    for role_key in roles:
        role = ROLE_DEFINITIONS[role_key]
        opinions = generate_mock_review(role_key, design_name)
        all_opinions[role_key] = opinions
        
        lines.extend([
            f"## {role['name']} 评审意见",
            "",
            f"**关注领域**: {role['focus']}",
            ""
        ])
        
        if opinions:
            for i, op in enumerate(opinions, 1):
                lines.extend([
                    f"### [{op['priority']}] {op['issue']}",
                    "",
                    f"- **位置**: {op['location']}",
                    f"- **问题**: {op['detail']}",
                    f"- **建议**: {op['suggestion']}",
                    ""
                ])
        else:
            lines.append("（该角色暂无评审意见）")
            lines.append("")
    
    # 汇总优先级
    lines.extend([
        "---",
        "",
        "## 汇总优先级",
        ""
    ])
    
    priorities = {"P1": [], "P2": [], "P3": []}
    for role_key, opinions in all_opinions.items():
        role_name = ROLE_DEFINITIONS[role_key]['name']
        for op in opinions:
            priorities[op['priority']].append(f"{op['issue']}（{role_name}）")
    
    for prio, items in priorities.items():
        lines.extend([
            f"### {prio}（{'必须修改' if prio == 'P1' else '建议修改' if prio == 'P2' else '可选优化'}）",
            ""
        ])
        if items:
            for item in items:
                lines.append(f"- [ ] {item}")
        else:
            lines.append("（无）")
        lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='设计评审工具')
    parser.add_argument('--input', '-i', help='设计稿截图路径')
    parser.add_argument('--pencil', '-p', help='Pencil设计文件路径')
    parser.add_argument('--roles', '-r', help='评审角色，逗号分隔')
    parser.add_argument('--output', '-o', default='review-report.md', help='输出路径')
    parser.add_argument('--design-name', '-n', default='设计稿', help='设计名称')
    args = parser.parse_args()
    
    if not args.input and not args.pencil:
        print("[错误] 请提供 --input 或 --pencil 参数")
        sys.exit(1)
    
    # 解析角色
    roles = DEFAULT_ROLES
    if args.roles:
        roles = [r.strip() for r in args.roles.split(',')]
    
    # 加载检查清单
    checklist = load_checklist()
    
    print(f"[信息] 开始评审: {args.design_name}")
    print(f"[信息] 评审角色: {', '.join(ROLE_DEFINITIONS[r]['name'] for r in roles)}")
    
    # 生成报告
    report = generate_report(args.design_name, roles, checklist)
    
    # 保存
    output_path = Path(args.output)
    output_path.write_text(report, encoding='utf-8')
    
    print(f"[成功] 评审报告已生成: {output_path.absolute()}")
    print(f"\n📊 统计:")
    for role_key in roles:
        opinions = generate_mock_review(role_key, args.design_name)
        print(f"  - {ROLE_DEFINITIONS[role_key]['name']}: {len(opinions)} 条意见")


if __name__ == "__main__":
    main()
