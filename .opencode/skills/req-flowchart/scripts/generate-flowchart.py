#!/usr/bin/env python3
"""
需求流程图生成器
将业务流程描述转化为 Mermaid 流程图
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_TEMPLATE = SKILL_DIR / "assets" / "flowchart-template.md"

# DSL 关键字映射
NODE_TYPES = {
    "START": ("([{text}])", "start"),
    "END": ("([{text}])", "end"),
    "INPUT": ("[/{text}/]", "input"),
    "ACTION": ("[{text}]", "action"),
    "DECISION": ("{{{text}}}", "decision"),
    "PROCESS": ("[{text}]", "process")
}


def parse_dsl(dsl_path: Path) -> dict:
    """解析 DSL 流程描述文件"""
    content = dsl_path.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    nodes = {}
    edges = []
    node_counter = 0
    
    # 节点栈，用于处理嵌套
    stack = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # 检查是否是分支定义
        branch_match = re.match(r'(YES|NO)\s*->\s*(\w+):\s*(.+)', line)
        if branch_match:
            branch_type = branch_match.group(1)
            node_type = branch_match.group(2)
            text = branch_match.group(3).strip()
            
            node_id = chr(65 + node_counter)  # A, B, C...
            node_counter += 1
            
            if node_type in NODE_TYPES:
                shape, node_kind = NODE_TYPES[node_type]
                nodes[node_id] = shape.format(text=text)
            else:
                nodes[node_id] = f"[{text}]"
            
            # 关联到当前决策节点（不入栈，保持决策节点在栈顶供后续分支使用）
            if stack:
                parent_id = stack[-1]
                edges.append((parent_id, node_id, branch_type))
            continue
        
        # 检查是否是节点定义
        node_match = re.match(r'(\w+):\s*(.+)', line)
        if node_match:
            node_type = node_match.group(1)
            text = node_match.group(2).strip()
            
            node_id = chr(65 + node_counter)
            node_counter += 1
            
            if node_type in NODE_TYPES:
                shape, node_kind = NODE_TYPES[node_type]
                nodes[node_id] = shape.format(text=text)
                
                if node_kind == "decision":
                    stack.append(node_id)
                elif node_kind == "end" and stack:
                    stack.pop()
            else:
                nodes[node_id] = f"[{text}]"
            
            # 连接到前一个非分支节点
            if len(nodes) > 1 and not line.startswith(('YES', 'NO')):
                prev_id = chr(65 + node_counter - 2)
                if prev_id in nodes and prev_id != node_id:
                    edges.append((prev_id, node_id, None))
            
            continue
        
        # 箭头连接
        arrow_match = re.match(r'(\w+)\s*->\s*(\w+)', line)
        if arrow_match:
            from_node = arrow_match.group(1)
            to_node = arrow_match.group(2)
            edges.append((from_node, to_node, None))
    
    return {"nodes": nodes, "edges": edges}


def generate_mermaid(flow_data: dict, direction: str = "TD") -> str:
    """生成 Mermaid 流程图代码"""
    lines = [f"flowchart {direction}"]
    
    # 定义节点
    for node_id, node_def in flow_data["nodes"].items():
        lines.append(f"    {node_id}{node_def}")
    
    # 定义边
    for from_node, to_node, label in flow_data["edges"]:
        if label:
            lines.append(f"    {from_node} -->|{label}| {to_node}")
        else:
            lines.append(f"    {from_node} --> {to_node}")
    
    return "\n".join(lines)


def extract_flow_from_prd(prd_path: Path) -> str:
    """从 PRD 中提取流程描述"""
    content = prd_path.read_text(encoding='utf-8')
    
    # 查找功能详述章节
    flow_section = extract_section(content, "功能详述")
    if not flow_section:
        flow_section = extract_section(content, "流程")
    
    if not flow_section:
        print("[警告] 未在 PRD 中找到流程描述，将生成默认流程")
        return None
    
    # 简单提取步骤列表
    steps = []
    for line in flow_section.splitlines():
        line = line.strip()
        if line.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            step_text = re.sub(r'^\d+\.\s*', '', line)
            steps.append(step_text)
    
    if not steps:
        return None
    
    # 转换为简单 DSL
    dsl_lines = ["START: 开始"]
    for step in steps:
        dsl_lines.append(f"ACTION: {step}")
    dsl_lines.append("END: 结束")
    
    return "\n".join(dsl_lines)


def extract_section(content: str, section_name: str) -> str:
    """提取指定章节"""
    pattern = rf'## \d*\.?\s*{re.escape(section_name)}.*?(?=\n## [^#]|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(0)
    return ""


def generate_flowchart(flow_data: dict, title: str, source: str, template_path: Path = None) -> str:
    """生成完整的流程图文档"""
    mermaid_code = generate_mermaid(flow_data)
    
    if template_path and template_path.exists():
        template = template_path.read_text(encoding='utf-8')
        content = template.replace("{{title}}", title)
        content = content.replace("{{source}}", source)
        content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
        content = content.replace("{{mermaid_code}}", mermaid_code)
    else:
        content = f"""# 需求流程图：{title}

**来源**: {source}
**生成时间**: {datetime.now().strftime("%Y-%m-%d")}

---

## Mermaid 流程图

```mermaid
{mermaid_code}
```

---

## 流程说明

（请在此补充业务规则说明）
"""
    
    return content


def main():
    parser = argparse.ArgumentParser(description='需求流程图生成器')
    parser.add_argument('--input', '-i', help='PRD 文件路径')
    parser.add_argument('--dsl', help='DSL 流程描述文件路径')
    parser.add_argument('--output', '-o', default='flowchart.md', help='输出路径')
    parser.add_argument('--title', '-t', default='业务流程', help='流程图标题')
    parser.add_argument('--template', '-T', help='自定义模板路径')
    args = parser.parse_args()
    
    # 确定输入方式
    if args.dsl:
        dsl_path = Path(args.dsl)
        if not dsl_path.exists():
            print(f"[错误] DSL 文件不存在: {dsl_path}")
            sys.exit(1)
        
        print("[信息] 正在解析 DSL 流程描述...")
        flow_data = parse_dsl(dsl_path)
        source = f"DSL: {dsl_path.name}"
        
    elif args.input:
        prd_path = Path(args.input)
        if not prd_path.exists():
            print(f"[错误] PRD 文件不存在: {prd_path}")
            sys.exit(1)
        
        print("[信息] 正在从 PRD 提取流程...")
        dsl_content = extract_flow_from_prd(prd_path)
        
        if dsl_content:
            # 创建临时 DSL 文件
            temp_dsl = Path("temp_flow.dsl")
            temp_dsl.write_text(dsl_content, encoding='utf-8')
            flow_data = parse_dsl(temp_dsl)
            temp_dsl.unlink()
        else:
            # 生成默认流程
            flow_data = {
                "nodes": {
                    "A": "([开始])",
                    "B": "[执行业务操作]",
                    "C": "([结束])"
                },
                "edges": [("A", "B", None), ("B", "C", None)]
            }
        
        source = f"PRD: {prd_path.name}"
        
    else:
        print("[错误] 请提供 --input 或 --dsl 参数")
        sys.exit(1)
    
    # 生成流程图
    print("[信息] 正在生成 Mermaid 流程图...")
    template_path = Path(args.template) if args.template else DEFAULT_TEMPLATE
    flowchart = generate_flowchart(flow_data, args.title, source, template_path)
    
    # 保存
    output_path = Path(args.output)
    output_path.write_text(flowchart, encoding='utf-8')
    
    print(f"[成功] 流程图已生成: {output_path.absolute()}")
    print(f"\n📊 统计:")
    print(f"  - 节点数: {len(flow_data['nodes'])}")
    print(f"  - 连接数: {len(flow_data['edges'])}")
    print(f"\n💡 提示：在支持 Mermaid 的平台上查看渲染后的流程图")


if __name__ == "__main__":
    main()
