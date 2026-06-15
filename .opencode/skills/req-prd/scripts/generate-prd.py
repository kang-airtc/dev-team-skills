#!/usr/bin/env python3
"""
PRD 草稿生成器
基于需求澄清文档和标准模板，自动生成 PRD
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_TEMPLATE = SKILL_DIR / "assets" / "prd-template.md"


def parse_clarified(input_path: Path) -> dict:
    """解析需求澄清文档，提取关键信息"""
    content = input_path.read_text(encoding='utf-8')
    data = {
        "background": "",
        "goals": "",
        "success_metrics": "",
        "in_scope": "",
        "out_scope": "",
        "primary_users": "",
        "user_stories": "",
        "feature_overview": "",
        "feature_details": "",
        "business_rules": "",
        "error_handling": "",
        "performance": "",
        "security": "",
        "compatibility": "",
        "usability": "",
        "acceptance_functional": "",
        "acceptance_non_functional": "",
        "risks": "",
        "dependencies": "",
        "glossary": "",
        "references": "",
        "changelog": ""
    }
    
    # 按章节解析
    sections = re.split(r'## \d+\.\s+', content)
    section_names = re.findall(r'## \d+\.\s+(.+)', content)
    
    for i, section_name in enumerate(section_names):
        if i + 1 < len(sections):
            section_content = sections[i + 1].strip()
            
            if "用户" in section_name or "Who" in section_name:
                data["primary_users"] = extract_answers(section_content)
                data["user_stories"] = generate_user_stories(section_content)
            
            elif "功能" in section_name or "What" in section_name:
                data["in_scope"] = extract_answers(section_content)
                data["feature_overview"] = extract_answers(section_content)
                data["feature_details"] = generate_feature_details(section_content)
            
            elif "价值" in section_name or "Why" in section_name:
                data["background"] = extract_answers(section_content)
                data["goals"] = extract_answers(section_content)
            
            elif "场景" in section_name or "When" in section_name:
                data["usability"] = extract_answers(section_content)
            
            elif "验收" in section_name or "How" in section_name:
                data["acceptance_functional"] = extract_answers(section_content)
                data["performance"] = extract_performance(section_content)
            
            elif "原始" in section_name:
                data["references"] = section_content
    
    # 推断排除范围
    if data["in_scope"]:
        data["out_scope"] = "（需人工补充：与本次需求无关的功能模块）"
    
    # 推断风险
    data["risks"] = """（需人工评估）
- 需求理解偏差风险
- 技术实现复杂度风险
- 时间进度风险"""
    
    return data


def extract_answers(content: str) -> str:
    """提取答案部分（去掉问题，保留回答）"""
    lines = []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("-") and "**" in line:
            # 提取问题和答案
            match = re.match(r'- \*\*(.+?)\*\*\s*\n?\s*- (.+)', line)
            if match:
                answer = match.group(2)
                if answer != "（待确认）":
                    lines.append(f"- {answer}")
            else:
                lines.append(line)
        elif line and not line.startswith("#"):
            lines.append(line)
    
    return "\n".join(lines) if lines else "（待补充）"


def generate_user_stories(who_content: str) -> str:
    """基于用户维度生成标准用户故事"""
    stories = []
    
    # 提取用户角色
    users = []
    for line in who_content.splitlines():
        if "用户" in line or "角色" in line:
            match = re.search(r'[:：]\s*(.+?)(?:\n|$)', line)
            if match:
                users.append(match.group(1).strip())
    
    if not users:
        users = ["用户"]
    
    for user in users[:3]:  # 最多3个用户故事
        story = f"""### 用户故事

**作为** {user}，
**我希望** [核心功能]，
**以便于** [实现价值]。

**验收标准**：
- [ ] 条件1
- [ ] 条件2
"""
        stories.append(story)
    
    return "\n\n".join(stories)


def generate_feature_details(what_content: str) -> str:
    """生成功能详情"""
    features = []
    
    for line in what_content.splitlines():
        if line.strip().startswith("-"):
            feature = line.strip()[1:].strip()
            if feature and feature != "（待确认）":
                features.append(f"#### {feature}\n\n（功能详情待补充）\n")
    
    return "\n".join(features) if features else "（功能详情待补充）"


def extract_performance(how_content: str) -> str:
    """提取性能相关内容"""
    performance_lines = []
    for line in how_content.splitlines():
        if any(kw in line for kw in ["性能", "响应", "并发", "速度", "时间"]):
            performance_lines.append(line)
    
    return "\n".join(performance_lines) if performance_lines else "（性能要求待补充）"


def fill_template(template_path: Path, data: dict, product_name: str = "产品") -> str:
    """填充模板"""
    template = template_path.read_text(encoding='utf-8')
    
    # 替换变量
    replacements = {
        "{{product_name}}": product_name,
        "{{version}}": "v1.0",
        "{{date}}": datetime.now().strftime("%Y-%m-%d"),
        "{{status}}": "草稿",
        "{{author}}": "（待填写）"
    }
    
    # 添加数据字段
    for key, value in data.items():
        replacements[f"{{{{ {key} }}}}"] = value
        replacements[f"{{{{{key}}}}}"] = value
    
    result = template
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)
    
    # 清理未替换的占位符
    result = re.sub(r'\{\{\s*\w+\s*\}\}', '（待补充）', result)
    
    return result


def main():
    parser = argparse.ArgumentParser(description='PRD 草稿生成器')
    parser.add_argument('--input', '-i', required=True, help='需求澄清文档路径')
    parser.add_argument('--output', '-o', default='PRD.md', help='输出 PRD 路径')
    parser.add_argument('--template', '-t', help='自定义模板路径')
    parser.add_argument('--product', '-p', default='产品', help='产品名称')
    args = parser.parse_args()
    
    # 读取输入
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[错误] 文件不存在: {input_path}")
        sys.exit(1)
    
    # 读取模板
    template_path = Path(args.template) if args.template else DEFAULT_TEMPLATE
    if not template_path.exists():
        print(f"[错误] 模板不存在: {template_path}")
        sys.exit(1)
    
    # 解析需求澄清文档
    print("[信息] 正在解析需求澄清文档...")
    data = parse_clarified(input_path)
    
    # 填充模板
    print("[信息] 正在生成 PRD 草稿...")
    prd_content = fill_template(template_path, data, args.product)
    
    # 保存输出
    output_path = Path(args.output)
    output_path.write_text(prd_content, encoding='utf-8')
    
    print(f"[成功] PRD 草稿已生成: {output_path.absolute()}")
    print("\n⚠️  提示：这是自动生成的草稿，请务必人工审核并补充以下内容：")
    print("  - 排除范围（Out of Scope）")
    print("  - 详细的业务规则")
    print("  - 具体的错误处理方案")
    print("  - 风险与依赖评估")


if __name__ == "__main__":
    main()
