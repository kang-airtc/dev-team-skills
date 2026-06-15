#!/usr/bin/env python3
"""dev-arch: 根据 Markdown 架构描述，生成 draw.io 格式的架构图"""

import argparse
import re
import sys
import uuid
from pathlib import Path
from xml.sax.saxutils import escape


# 三种预设样式：填充色、字体色、边框色
STYLES = {
    'layered': {
        'fill': '#dae8fc',
        'stroke': '#6c8ebf',
    },
    'microservice': {
        'fill': '#d5e8d4',
        'stroke': '#82b366',
    },
    'mvc': {
        'fill': '#fff2cc',
        'stroke': '#d6b656',
    },
}

# 单个组件矩形的尺寸
NODE_W, NODE_H = 140, 60
GAP_X, GAP_Y = 60, 80
COLS = 3  # 每行组件数


def parse_spec(text: str):
    """解析 Markdown，提取 components 和 deps。

    返回：
        components: [(id, label), ...]
        deps:       [(src_id, dst_id), ...]
    """
    components = []
    deps = []
    section = None

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith('## 组件'):
            section = 'components'
            continue
        if stripped.startswith('## 依赖'):
            section = 'deps'
            continue
        if stripped.startswith('## '):
            section = None
            continue

        if section == 'components' and stripped.startswith('- '):
            # 格式：- id: 描述（描述可省）
            m = re.match(r'-\s+([\w-]+)\s*[:：]?\s*(.*)', stripped)
            if m:
                cid = m.group(1)
                label = m.group(2).strip() or cid
                components.append((cid, label))

        if section == 'deps' and stripped.startswith('- '):
            # 格式：- src -> dst
            m = re.match(r'-\s+([\w-]+)\s*->\s*([\w-]+)', stripped)
            if m:
                deps.append((m.group(1), m.group(2)))

    return components, deps


def build_drawio(components, deps, style_name='layered') -> str:
    """生成 draw.io XML 字符串"""
    style = STYLES.get(style_name, STYLES['layered'])
    node_style = (
        f'rounded=0;whiteSpace=wrap;html=1;'
        f'fillColor={style["fill"]};strokeColor={style["stroke"]};'
        f'fontSize=14;'
    )
    edge_style = (
        f'endArrow=classic;html=1;rounded=0;'
        f'strokeColor={style["stroke"]};fontSize=12;'
    )

    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    id_map = {}  # 组件 id → draw.io cell id

    # 组件矩形（按 COLS 列网格布局）
    for idx, (cid, label) in enumerate(components):
        cell_id = f'c{idx + 2}'
        id_map[cid] = cell_id
        col = idx % COLS
        row = idx // COLS
        x = col * (NODE_W + GAP_X) + 40
        y = row * (NODE_H + GAP_Y) + 40
        cells.append(
            f'<mxCell id="{cell_id}" value="{escape(label)}" '
            f'style="{node_style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" as="geometry"/>'
            f'</mxCell>'
        )

    # 依赖箭头
    for idx, (src, dst) in enumerate(deps):
        src_id = id_map.get(src)
        dst_id = id_map.get(dst)
        if not src_id or not dst_id:
            print(f'警告：依赖 {src} -> {dst} 中有未声明的组件', file=sys.stderr)
            continue
        edge_id = f'e{idx + 100}'
        cells.append(
            f'<mxCell id="{edge_id}" style="{edge_style}" '
            f'edge="1" parent="1" source="{src_id}" target="{dst_id}">'
            f'<mxGeometry relative="1" as="geometry"/>'
            f'</mxCell>'
        )

    diagram_id = uuid.uuid4().hex[:12]
    return (
        '<mxfile host="app.diagrams.net">'
        f'<diagram id="{diagram_id}" name="Architecture">'
        '<mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" '
        'tooltips="1" connect="1" arrows="1" fold="1" page="1" '
        'pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">'
        '<root>'
        + ''.join(cells)
        + '</root>'
        '</mxGraphModel>'
        '</diagram>'
        '</mxfile>'
    )


def main():
    parser = argparse.ArgumentParser(description='生成 draw.io 架构图')
    parser.add_argument('--input', '-i', required=True, help='架构描述 Markdown 文件')
    parser.add_argument('--output', '-o', required=True, help='输出 .drawio 路径')
    parser.add_argument('--style', '-s', default='layered',
                        choices=list(STYLES.keys()),
                        help='预设样式（默认 layered）')
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f'错误：输入文件不存在 {in_path}', file=sys.stderr)
        sys.exit(1)

    components, deps = parse_spec(in_path.read_text(encoding='utf-8'))
    if not components:
        print('错误：未解析到任何组件，请检查输入格式', file=sys.stderr)
        sys.exit(1)

    xml = build_drawio(components, deps, args.style)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(xml, encoding='utf-8')

    print(f'已生成：{out_path}（{len(components)} 个组件，{len(deps)} 条依赖）')


if __name__ == '__main__':
    main()
