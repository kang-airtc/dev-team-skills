#!/usr/bin/env python3
"""dev-frontend-form: 根据 form-spec.md 生成 Next.js 后台 CRUD 表单骨架"""

import argparse
import re
from pathlib import Path


def parse_spec(text: str) -> dict:
    spec = {
        'title': '',
        'module': '',            # 小写，如 news
        'module_cap': '',        # 首字母大写，如 News
        'new_route': '',
        'edit_route': '',
        'fields': [],            # [{'name','type','required','validation'}, ...]
        'create_func': '',
        'update_func': '',
        'redirect': '/dashboard',
    }

    section = None
    for line in text.splitlines():
        stripped = line.strip()

        m = re.match(r'^#\s+表单描述[：:]\s*(.+)', stripped)
        if m:
            spec['title'] = m.group(1).strip()
            continue

        if stripped.startswith('## 路由'):
            section = 'route'
            continue
        if stripped.startswith('## 字段'):
            section = 'fields'
            continue
        if stripped.startswith('## 提交逻辑'):
            section = 'submit'
            continue
        if stripped.startswith('## '):
            section = None
            continue

        if section == 'route':
            m = re.match(r'-\s*新增[：:]\s*(.+)', stripped)
            if m:
                spec['new_route'] = m.group(1).strip()
                # 从路由提取模块名：dashboard/news/new → news
                parts = m.group(1).strip().split('/')
                for i, p in enumerate(parts):
                    if p == 'dashboard' and i + 1 < len(parts):
                        spec['module'] = parts[i + 1]
                        spec['module_cap'] = parts[i + 1].capitalize()
                        break
            m = re.match(r'-\s*编辑[：:]\s*(.+)', stripped)
            if m:
                spec['edit_route'] = m.group(1).strip()

        if section == 'fields':
            # 表格行：| title | text | 是 | 不能为空 |
            m = re.match(r'\|\s*(\w+)\s*\|\s*([\w（）()]+)\s*\|\s*(是|否)\s*\|\s*(.*?)\s*\|', stripped)
            if m and m.group(1) not in ('字段名', '---'):
                spec['fields'].append({
                    'name': m.group(1),
                    'type': m.group(2),
                    'required': m.group(3) == '是',
                    'validation': m.group(4).strip(),
                })

        if section == 'submit':
            m = re.match(r'-\s*新增[：:]\s*调用\s+(\w+)\s+service', stripped)
            if m:
                spec['create_func'] = m.group(1)
            m = re.match(r'-\s*编辑[：:]\s*调用\s+(\w+)\s+service', stripped)
            if m:
                spec['update_func'] = m.group(1)
            m = re.search(r'跳转\s+(/[\w/]+)', stripped)
            if m:
                spec['redirect'] = m.group(1)

    return spec


def render_field_input(field: dict) -> str:
    name = field['name']
    ftype = field['type']
    required = field['required']
    req_attr = ' required' if required else ''

    if 'checkbox' in ftype:
        return (
            f'      <label className="flex items-center gap-2">\n'
            f'        <input type="checkbox" name="{name}"\n'
            f'          checked={{form.{name} as boolean}}\n'
            f'          onChange={{(e) => setForm({{...form, {name}: e.target.checked}})}} />\n'
            f'        <span>{name}</span>\n'
            f'      </label>'
        )
    elif 'textarea' in ftype:
        return (
            f'      <div>\n'
            f'        <label className="block text-sm font-medium mb-1">{name}{" *" if required else ""}</label>\n'
            f'        <textarea name="{name}" value={{form.{name} as string}}{req_attr}\n'
            f'          onChange={{(e) => setForm({{...form, {name}: e.target.value}})}}\n'
            f'          className="w-full border rounded px-3 py-2 text-sm" rows={{4}} />\n'
            f'      </div>'
        )
    else:
        return (
            f'      <div>\n'
            f'        <label className="block text-sm font-medium mb-1">{name}{" *" if required else ""}</label>\n'
            f'        <input type="text" name="{name}" value={{form.{name} as string}}{req_attr}\n'
            f'          onChange={{(e) => setForm({{...form, {name}: e.target.value}})}}\n'
            f'          className="w-full border rounded px-3 py-2 text-sm" />\n'
            f'      </div>'
        )


def generate_form_component(spec: dict) -> str:
    module = spec['module']
    module_cap = spec['module_cap']
    create_func = spec['create_func'] or f'create{module_cap}'
    update_func = spec['update_func'] or f'update{module_cap}'
    redirect = spec['redirect']
    fields = spec['fields']

    # 初始化表单默认值
    defaults = []
    for f in fields:
        if 'checkbox' in f['type']:
            defaults.append(f"  {f['name']}: false,")
        else:
            defaults.append(f"  {f['name']}: '',")
    defaults_str = '\n'.join(defaults)

    # 类型字段
    type_fields = []
    for f in fields:
        if 'checkbox' in f['type']:
            type_fields.append(f"  {f['name']}: boolean;")
        else:
            type_fields.append(f"  {f['name']}: string;")
    type_fields_str = '\n'.join(type_fields)

    # 字段渲染
    field_inputs = '\n'.join(render_field_input(f) for f in fields)

    return f'''"use client";

import {{ useState }} from "react";
import {{ useRouter }} from "next/navigation";
import {{ {create_func}, {update_func} }} from "@/services/{module}";

interface {module_cap}FormData {{
{type_fields_str}
}}

interface {module_cap}FormProps {{
  defaultValues?: Partial<{module_cap}FormData>;
  {module}Id?: number;
}}

export default function {module_cap}Form({{ defaultValues, {module}Id }}: {module_cap}FormProps) {{
  const router = useRouter();
  const [form, setForm] = useState<{module_cap}FormData>({{
{defaults_str}
    ...defaultValues,
  }});
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {{
      if ({module}Id) {{
        await {update_func}({module}Id, form);
      }} else {{
        await {create_func}(form);
      }}
      router.push("{redirect}");
    }} catch (err) {{
      setError(err instanceof Error ? err.message : "保存失败，请重试");
    }} finally {{
      setSubmitting(false);
    }}
  }};

  return (
    <form onSubmit={{handleSubmit}} className="max-w-2xl space-y-4">
      {{error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded text-red-700">
          {{error}}
        </div>
      )}}
{field_inputs}
      <div className="flex gap-3 pt-2">
        <button type="submit" disabled={{submitting}}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
          {{submitting ? "保存中..." : "保存"}}
        </button>
        <button type="button" onClick={{() => router.back()}}
          className="px-4 py-2 border rounded hover:bg-gray-50">
          取消
        </button>
      </div>
    </form>
  );
}}
'''


def generate_new_page(spec: dict) -> str:
    module_cap = spec['module_cap']
    return f'''"use client";

import {module_cap}Form from "@/components/{module_cap}Form";

export default function New{module_cap}Page() {{
  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6">新增{spec["title"].replace("表单描述：", "").replace("管理后台表单", "")}</h1>
      <{module_cap}Form />
    </div>
  );
}}
'''


def generate_edit_page(spec: dict) -> str:
    module = spec['module']
    module_cap = spec['module_cap']
    return f'''"use client";

import {{ useState, useEffect }} from "react";
import {{ useParams }} from "next/navigation";
import {module_cap}Form from "@/components/{module_cap}Form";
import {{ get{module_cap}ById }} from "@/services/{module}";

export default function Edit{module_cap}Page() {{
  const {{ id }} = useParams<{{ id: string }}>();
  const [defaultValues, setDefaultValues] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {{
    get{module_cap}ById(Number(id)).then((res) => {{
      setDefaultValues(res.data);
    }});
  }}, [id]);

  if (!defaultValues) return <p className="p-8 text-gray-500">加载中...</p>;

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6">编辑{spec["title"].replace("表单描述：", "").replace("管理后台表单", "")}</h1>
      <{module_cap}Form defaultValues={{defaultValues}} {module}Id={{Number(id)}} />
    </div>
  );
}}
'''


def main():
    parser = argparse.ArgumentParser(description='生成 CRUD 表单骨架')
    parser.add_argument('--input', '-i', required=True, help='表单描述 Markdown 文件')
    parser.add_argument('--output-dir', '-o', required=True, help='输出目录')
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f'错误：输入文件不存在 {in_path}')
        raise SystemExit(1)

    spec = parse_spec(in_path.read_text(encoding='utf-8'))
    if not spec['module']:
        print('错误：未能从路由中解析模块名')
        raise SystemExit(1)

    out_dir = Path(args.output_dir)

    # 1. 表单组件
    form_path = out_dir / 'components' / f'{spec["module_cap"]}Form.tsx'
    form_path.parent.mkdir(parents=True, exist_ok=True)
    form_path.write_text(generate_form_component(spec), encoding='utf-8')

    # 2. 新增页
    new_path = out_dir / f'app/(admin)/dashboard/{spec["module"]}/new/page.tsx'
    new_path.parent.mkdir(parents=True, exist_ok=True)
    new_path.write_text(generate_new_page(spec), encoding='utf-8')

    # 3. 编辑页
    edit_path = out_dir / f'app/(admin)/dashboard/{spec["module"]}/[id]/edit/page.tsx'
    edit_path.parent.mkdir(parents=True, exist_ok=True)
    edit_path.write_text(generate_edit_page(spec), encoding='utf-8')

    print(f'已生成：')
    print(f'  {form_path}')
    print(f'  {new_path}')
    print(f'  {edit_path}')


if __name__ == '__main__':
    main()
