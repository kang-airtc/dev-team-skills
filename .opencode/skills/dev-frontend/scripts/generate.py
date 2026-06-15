#!/usr/bin/env python3
"""dev-frontend: 根据 page-spec.md 生成 Next.js App Router 页面骨架"""

import argparse
import re
from pathlib import Path


def parse_spec(text: str) -> dict:
    """解析 page-spec.md，返回结构化字段"""
    result = {
        'title': '',
        'route': '',
        'page_type': '',
        'data_source': '',
        'service_module': '',
        'service_func': '',
        'page_heading': '',
        'empty_state': '暂无数据',
        'container': 'div',
        'slug_link': None,
    }

    section = None
    for line in text.splitlines():
        stripped = line.strip()

        # 提取标题
        m = re.match(r'^#\s+页面描述[：:]\s*(.+)', stripped)
        if m:
            result['title'] = m.group(1).strip()
            continue

        if stripped.startswith('## 路由'):
            section = 'route'
            continue
        if stripped.startswith('## 页面类型'):
            section = 'type'
            continue
        if stripped.startswith('## 数据来源'):
            section = 'data'
            continue
        if stripped.startswith('## 展示内容'):
            section = 'content'
            continue
        if stripped.startswith('## UI 约束'):
            section = 'ui'
            continue
        if stripped.startswith('## '):
            section = None
            continue

        if not stripped:
            continue

        if section == 'route':
            result['route'] = stripped

        if section == 'type':
            result['page_type'] = stripped

        if section == 'data':
            result['data_source'] = stripped
            # 提取 service 模块与函数名，如 @/services/news 中的 listNews
            m = re.search(r'@/services/([\w-]+).*?(\w+)\s*函数', stripped)
            if m:
                result['service_module'] = m.group(1)
                result['service_func'] = m.group(2)

        if section == 'content':
            if stripped.startswith('- ') and '页面标题' in stripped:
                result['page_heading'] = re.sub(r'.*页面标题[：:]\s*', '', stripped)
            if stripped.startswith('- ') and '空状态' in stripped:
                result['empty_state'] = re.sub(r'.*空状态[：:]\s*', '', stripped)

        if section == 'ui':
            if '@/components/Container' in stripped:
                result['container'] = 'Container'
            m = re.search(r'跳转\s+(/\S+/\{(\w+)\})', stripped)
            if m:
                result['slug_link'] = m.group(1)

    return result


def generate_tsx(spec: dict) -> str:
    """生成 TSX 骨架代码"""
    title = spec['title'] or '页面'
    service_module = spec['service_module'] or 'module'
    service_func = spec['service_func'] or 'listItems'
    page_heading = spec['page_heading'] or title
    empty_state = spec['empty_state']
    container = spec['container']
    slug_link = spec['slug_link']

    # 组件名：从路由倒数第二段派生英文名（跳过 page.tsx），fallback 用 service 模块名
    route = spec.get('route', '')
    route_parts = [p for p in re.sub(r'\.\w+$', '', route).split('/') if p and not p.startswith('(') and p != 'page']
    if route_parts and re.match(r'^[a-zA-Z]', route_parts[-1]):
        component_name = route_parts[-1].capitalize().replace('-', '') + 'Page'
    elif service_module:
        component_name = service_module.capitalize() + 'Page'
    else:
        component_name = 'Page'

    # item 类型名
    item_type = service_module.capitalize() + 'Item'

    # 卡片链接
    if slug_link:
        card_element = f'<Link key={{item.id}} href={{`{slug_link.replace("{slug}", "${item.slug}")}`}} className="block">\n          {{/* TODO: 卡片内容 */}}\n        </Link>'
        link_import = 'import Link from "next/link";\n'
    else:
        card_element = '<div key={item.id}>\n          {/* TODO: 卡片内容 */}\n        </div>'
        link_import = ''

    container_open = f'<{container}>' if container != 'div' else '<div className="max-w-5xl mx-auto px-4 py-8">'
    container_close = f'</{container}>' if container != 'div' else '</div>'
    container_import = f'import {{ {container} }} from "@/components/{container}";\n' if container != 'div' else ''

    tsx = f'''"use client";

import {{ useState, useEffect }} from "react";
{link_import}import {{ {service_func} }} from "@/services/{service_module}";
{container_import}import type {{ {item_type} }} from "@/services/{service_module}";

export default function {component_name}() {{
  const [items, setItems] = useState<{item_type}[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {{
    {service_func}({{ limit: 10, offset: 0 }})
      .then((res) => {{
        setItems(res.data.items);
      }})
      .catch((err) => {{
        setError(err?.message ?? "加载失败");
      }})
      .finally(() => {{
        setLoading(false);
      }});
  }}, []);

  return (
    {container_open}
      <h1 className="text-3xl font-bold mb-8">{page_heading}</h1>

      {{/* loading 骨架屏 */}}
      {{loading && (
        <div className="space-y-4">
          {{Array.from({{ length: 3 }}).map((_, i) => (
            <div key={{i}} className="h-32 bg-gray-100 rounded-lg animate-pulse" />
          ))}}
        </div>
      )}}

      {{/* 错误状态 */}}
      {{error && (
        <p className="text-red-500 text-center py-8">{{error}}</p>
      )}}

      {{/* 空状态 */}}
      {{!loading && !error && items.length === 0 && (
        <p className="text-gray-500 text-center py-16">{empty_state}</p>
      )}}

      {{/* 列表 */}}
      {{!loading && !error && items.length > 0 && (
        <div className="space-y-6">
          {{items.map((item) => (
            {card_element}
          ))}}
        </div>
      )}}
    {container_close}
  );
}}
'''
    return tsx


def main():
    parser = argparse.ArgumentParser(description='生成 Next.js 页面骨架')
    parser.add_argument('--input', '-i', required=True, help='页面描述 Markdown 文件')
    parser.add_argument('--output', '-o', required=True, help='输出 .tsx 路径')
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f'错误：输入文件不存在 {in_path}')
        raise SystemExit(1)

    spec = parse_spec(in_path.read_text(encoding='utf-8'))
    tsx = generate_tsx(spec)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(tsx, encoding='utf-8')
    print(f'已生成：{out_path}')


if __name__ == '__main__':
    main()
