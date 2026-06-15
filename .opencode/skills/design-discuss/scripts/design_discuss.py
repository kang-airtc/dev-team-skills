#!/usr/bin/env python3
"""
设计决策讨论工具
模拟多角色讨论，输出结构化决策记录
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent

ROLES = {
    "product-manager": {
        "name": "Product Manager",
        "focus": "业务与用户",
        "concerns": ["用户体验", "业务目标", "转化路径", "竞品对标"]
    },
    "ui-designer": {
        "name": "UI Designer",
        "focus": "视觉与交互",
        "concerns": ["视觉层次", "空间利用", "设计一致性", "品牌表达"]
    },
    "frontend-dev": {
        "name": "Frontend Dev",
        "focus": "实现与维护",
        "concerns": ["实现成本", "组件复用", "状态管理", "性能影响"]
    },
    "backend-dev": {
        "name": "Backend Dev",
        "focus": "数据与接口",
        "concerns": ["接口影响", "数据流", "权限控制", "服务端性能"]
    }
}

# 预设的讨论场景模板
SCENARIOS = {
    "弹窗 vs 独立页面": {
        "options": ["弹窗", "独立页面"],
        "role_opinions": {
            "product-manager": {
                "弹窗": {"pros": ["用户不离开当前页面", "登录后无缝继续"], "cons": ["移动端体验差", "不利于SEO"], "verdict": "不推荐"},
                "独立页面": {"pros": ["移动端体验好", "可以做SEO", "品牌展示空间大"], "cons": ["用户可能流失"], "verdict": "推荐"}
            },
            "ui-designer": {
                "弹窗": {"pros": ["可以复用弹窗组件"], "cons": ["空间拥挤", "难以展示品牌元素"], "verdict": "不推荐"},
                "独立页面": {"pros": ["设计空间大", "符合用户认知"], "cons": [], "verdict": "推荐"}
            },
            "frontend-dev": {
                "弹窗": {"pros": ["无需新路由", "状态管理简单"], "cons": ["z-index管理复杂"], "verdict": "推荐"},
                "独立页面": {"pros": [], "cons": ["需要新路由", "登录后返回逻辑复杂"], "verdict": "不推荐"}
            }
        }
    }
}


def interactive_mode():
    """交互式讨论模式"""
    print("=" * 60)
    print("设计决策讨论")
    print("=" * 60)
    print()
    
    topic = input("讨论主题: ").strip()
    if not topic:
        print("[错误] 主题不能为空")
        sys.exit(1)
    
    options_input = input("选项（逗号分隔）: ").strip()
    options = [o.strip() for o in options_input.split(",")]
    
    if len(options) < 2:
        print("[错误] 至少需要2个选项")
        sys.exit(1)
    
    print("\n可用角色:")
    for key, role in ROLES.items():
        print(f"  {key}: {role['name']} ({role['focus']})")
    
    roles_input = input("\n参与角色（逗号分隔，默认全部）: ").strip()
    if roles_input:
        roles = [r.strip() for r in roles_input.split(",")]
    else:
        roles = list(ROLES.keys())
    
    return topic, options, roles


def generate_discussion(topic, options, roles):
    """生成讨论记录"""
    lines = [
        f"# 设计决策记录：{topic}",
        "",
        f"**决策时间**: {datetime.now().strftime('%Y-%m-%d')}",
        f"**参与角色**: {', '.join(ROLES[r]['name'] for r in roles if r in ROLES)}",
        "",
        "## 议题",
        "",
        f"{topic}"
    ]
    
    # 尝试匹配预设场景
    scenario = None
    for key, data in SCENARIOS.items():
        if key in topic or all(opt in topic for opt in data["options"]):
            scenario = data
            break
    
    lines.extend(["", "## 选项分析", ""])
    
    for option in options:
        lines.extend([
            f"### 选项：{option}",
            ""
        ])
        
        for role_key in roles:
            if role_key not in ROLES:
                continue
            
            role = ROLES[role_key]
            
            # 使用预设观点或生成通用观点
            if scenario and role_key in scenario.get("role_opinions", {}):
                opinion = scenario["role_opinions"][role_key].get(option, {})
                pros = opinion.get("pros", [])
                cons = opinion.get("cons", [])
                verdict = opinion.get("verdict", "待评估")
            else:
                pros = [f"符合{role['focus']}要求"]
                cons = [f"可能存在{role['focus']}风险"]
                verdict = "待讨论"
            
            lines.append(f"**{role['name']}**")
            
            for pro in pros:
                lines.append(f"- 👍 优点：{pro}")
            
            for con in cons:
                lines.append(f"- 👎 缺点：{con}")
            
            lines.append(f"- **倾向**: {verdict}")
            lines.append("")
    
    # 决策结果
    lines.extend([
        "## 决策结果",
        "",
        "**采用方案**: （请填写最终决策）",
        "",
        "**决策理由**:",
        "1. （理由1）",
        "2. （理由2）",
        "3. （理由3）",
        "",
        "**异议记录**:",
        "- （记录不同意见）",
        "",
        "## 后续行动",
        "",
        "- [ ] （行动项1）",
        "- [ ] （行动项2）",
        "- [ ] （行动项3）",
        "",
        "## 备注",
        "",
        "（此处记录其他相关信息）",
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='设计决策讨论工具')
    parser.add_argument('--topic', '-t', help='讨论主题')
    parser.add_argument('--options', '-o', help='选项列表，逗号分隔')
    parser.add_argument('--roles', '-r', help='参与角色，逗号分隔')
    parser.add_argument('--output', default='decision.md', help='输出路径')
    args = parser.parse_args()
    
    # 确定输入方式
    if args.topic and args.options:
        topic = args.topic
        options = [o.strip() for o in args.options.split(",")]
        roles = [r.strip() for r in args.roles.split(",")] if args.roles else list(ROLES.keys())
    else:
        topic, options, roles = interactive_mode()
    
    print(f"\n[信息] 正在生成决策讨论记录...")
    print(f"[信息] 主题: {topic}")
    print(f"[信息] 选项: {', '.join(options)}")
    print(f"[信息] 角色: {', '.join(ROLES[r]['name'] for r in roles if r in ROLES)}")
    
    # 生成记录
    discussion = generate_discussion(topic, options, roles)
    
    # 保存
    output_path = Path(args.output)
    output_path.write_text(discussion, encoding='utf-8')
    
    print(f"[成功] 决策记录已生成: {output_path.absolute()}")
    print("\n💡 提示：")
    print("  - 此记录为模板，需要人工补充最终决策")
    print("  - 建议召集团队会议确认决策结果")
    print("  - 保留异议记录，便于后续追溯")


if __name__ == "__main__":
    main()
