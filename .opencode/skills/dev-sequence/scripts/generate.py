#!/usr/bin/env python3
"""dev-sequence: 根据 Markdown 消息流描述，生成 draw.io 格式的时序图"""

import argparse
import re
import sys
import uuid
from pathlib import Path
from xml.sax.saxutils import escape


# 布局参数
ROLE_W, ROLE_H = 110, 40
ROLE_GAP = 70                  # 角色之间的水平间距
ROLE_Y = 40                    # 角色框的 y 坐标
LIFELINE_TOP = ROLE_Y + ROLE_H # lifeline 起点
MSG_START_Y = LIFELINE_TOP + 30
MSG_GAP = 40                   # 每条消息间的纵向间距

ROLE_STYLE = (
    'rounded=0;whiteSpace=wrap;html=1;'
    'fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=13;'
)
LIFELINE_STYLE = (
    'endArrow=none;html=1;dashed=1;dashPattern=4 4;'
    'strokeColor=#999999;'
)
MSG_STYLE = (
    'endArrow=classic;html=1;rounded=0;'
    'strokeColor=#333333;fontSize=11;'
)


def parse_spec(text: str):
    """解析 Markdown，提取 roles 和 messages。"""
    roles = []           # [(id, label), ...]
    messages = []        # [(src_id, dst_id, label), ...]
    section = None

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith('## 角色'):
            section = 'roles'
            continue
        if stripped.startswith('## 消息'):
            section = 'messages'
            continue
        if stripped.startswith('## '):
            section = None
            continue

        if section == 'roles' and stripped.startswith('- '):
            # 格式：- id: 描述（描述可省）
            m = re.match(r'-\s+([\w-]+)\s*[:：]?\s*(.*)', stripped)
            if m:
                rid = m.group(1)
                label = m.group(2).strip() or rid
                roles.append((rid, label))

        if section == 'messages' and stripped.startswith('- '):
            # 格式：- src -> dst: 消息内容
            m = re.match(r'-\s+([\w-]+)\s*->\s*([\w-]+)\s*[:：]\s*(.*)', stripped)
            if m:
                messages.append((m.group(1), m.group(2), m.group(3).strip()))

    return roles, messages


def build_drawio(roles, messages) -> str:
    if not roles:
        return ''

    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

    # 计算各角色中心 x 坐标
    role_x = {}
    for idx, (rid, label) in enumerate(roles):
        x = idx * (ROLE_W + ROLE_GAP) + 40
        role_x[rid] = x + ROLE_W // 2  # 中心 x

        # 角色框
        cells.append(
            f'<mxCell id="r{idx}" value="{escape(label)}" '
            f'style="{ROLE_STYLE}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{ROLE_Y}" width="{ROLE_W}" height="{ROLE_H}" as="geometry"/>'
            f'</mxCell>'
        )

    # 计算 lifeline 总长度（最后一条消息 y + 余量）
    lifeline_bottom = MSG_START_Y + max(len(messages), 1) * MSG_GAP + 40

    # 每个角色一条 lifeline（虚线）
    for idx, (rid, _) in enumerate(roles):
        cx = role_x[rid]
        cells.append(
            f'<mxCell id="ll{idx}" style="{LIFELINE_STYLE}" '
            f'edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{cx}" y="{LIFELINE_TOP}" as="sourcePoint"/>'
            f'<mxPoint x="{cx}" y="{lifeline_bottom}" as="targetPoint"/>'
            f'</mxGeometry>'
            f'</mxCell>'
        )

    # 消息箭头
    for idx, (src, dst, label) in enumerate(messages):
        if src not in role_x:
            print(f'警告：消息中的角色 {src} 未在 ## 角色 中声明', file=sys.stderr)
            continue
        if dst not in role_x:
            print(f'警告：消息中的角色 {dst} 未在 ## 角色 中声明', file=sys.stderr)
            continue
        sx = role_x[src]
        dx = role_x[dst]
        my = MSG_START_Y + idx * MSG_GAP
        cells.append(
            f'<mxCell id="m{idx}" value="{escape(label)}" '
            f'style="{MSG_STYLE}" edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{sx}" y="{my}" as="sourcePoint"/>'
            f'<mxPoint x="{dx}" y="{my}" as="targetPoint"/>'
            f'</mxGeometry>'
            f'</mxCell>'
        )

    diagram_id = uuid.uuid4().hex[:12]
    return (
        '<mxfile host="app.diagrams.net">'
        f'<diagram id="{diagram_id}" name="Sequence">'
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
    parser = argparse.ArgumentParser(description='生成 draw.io 时序图')
    parser.add_argument('--input', '-i', required=True, help='消息流描述 Markdown 文件')
    parser.add_argument('--output', '-o', required=True, help='输出 .drawio 路径')
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f'错误：输入文件不存在 {in_path}', file=sys.stderr)
        sys.exit(1)

    roles, messages = parse_spec(in_path.read_text(encoding='utf-8'))
    if not roles:
        print('错误：未解析到任何角色，请检查输入格式', file=sys.stderr)
        sys.exit(1)

    xml = build_drawio(roles, messages)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(xml, encoding='utf-8')

    print(f'已生成：{out_path}（{len(roles)} 个角色，{len(messages)} 条消息）')


if __name__ == '__main__':
    main()
