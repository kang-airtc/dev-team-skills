#!/usr/bin/env python3
"""dev-backend: Generate FastAPI schema + views skeleton from api-spec.md."""

import argparse
import re
from pathlib import Path


def parse_spec(spec_path: str) -> dict:
    content = Path(spec_path).read_text(encoding="utf-8")
    spec = {}

    # Route prefix → module name
    m = re.search(r"## 路由前缀\s*\n(.+)", content)
    if m:
        spec["prefix"] = m.group(1).strip()
        spec["module"] = spec["prefix"].strip("/").split("/")[-1]
    else:
        raise ValueError("api-spec.md 中未找到 ## 路由前缀")

    # Endpoint table
    endpoints = []
    table_m = re.search(r"## 接口列表.*?\n((?:\|.+\n)+)", content, re.DOTALL)
    if table_m:
        for line in table_m.group(1).strip().splitlines():
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if len(cells) >= 3 and cells[0] not in ("方法", "---", ":---") and not cells[0].startswith("-"):
                endpoints.append({
                    "method": cells[0].upper(),
                    "path": cells[1],
                    "auth": cells[2] == "是",
                    "desc": cells[3] if len(cells) > 3 else "",
                })
    spec["endpoints"] = endpoints

    # Schema: NewsCreate fields
    create_fields = []
    schema_m = re.search(r"## Schema 要求(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if schema_m:
        schema_text = schema_m.group(1)
        create_m = re.search(r"(?:NewsCreate|Create)[：:](.*?)(?=\n-|\Z)", schema_text)
        if create_m:
            for name, req in re.findall(r"(\w+)\((必填|可选)\)", create_m.group(1)):
                create_fields.append({"name": name, "required": req == "必填"})
    spec["create_fields"] = create_fields

    # 404 detail message from 技术约束
    not_found_m = re.search(r'detail="([^"]+)"', content)
    spec["not_found_detail"] = not_found_m.group(1) if not_found_m else f"{spec['module'].capitalize()}不存在"

    return spec


def infer_type(name: str) -> str:
    if name in {"published_at", "created_at", "updated_at", "deleted_at"}:
        return "datetime"
    if name in {"is_published", "is_active", "is_deleted", "is_featured"}:
        return "bool"
    if name in {"id", "sort_order", "view_count", "like_count"}:
        return "int"
    return "str"


def field_line(name: str, required: bool, indent: str = "    ") -> str:
    t = infer_type(name)
    if required:
        return f"{indent}{name}: {t}"
    if t == "bool":
        return f"{indent}{name}: bool = False"
    if t == "int":
        return f"{indent}{name}: Optional[int] = None"
    if t == "datetime":
        return f"{indent}{name}: Optional[datetime] = None"
    return f"{indent}{name}: Optional[str] = None"


def generate_schema(spec: dict) -> str:
    module = spec["module"]
    Model = module.capitalize()
    fields = spec["create_fields"]

    needs_datetime = any(infer_type(f["name"]) == "datetime" for f in fields)

    lines = ["from __future__ import annotations", ""]
    if needs_datetime:
        lines.append("from datetime import datetime")
    lines += ["from typing import List, Optional", "", "from pydantic import BaseModel", "", ""]

    # NewsCreate
    lines.append(f"class {Model}Create(BaseModel):")
    for f in fields:
        lines.append(field_line(f["name"], f["required"]))
    lines += ["", ""]

    # NewsUpdate (all optional)
    lines.append(f"class {Model}Update(BaseModel):  # 所有字段可选（PATCH 语义）")
    for f in fields:
        t = infer_type(f["name"])
        if t == "bool":
            lines.append(f"    {f['name']}: Optional[bool] = None")
        elif t == "datetime":
            lines.append(f"    {f['name']}: Optional[datetime] = None")
        elif t == "int":
            lines.append(f"    {f['name']}: Optional[int] = None")
        else:
            lines.append(f"    {f['name']}: Optional[str] = None")
    lines += ["", ""]

    # NewsResponse
    lines.append(f"class {Model}Response(BaseModel):")
    lines.append('    model_config = {"from_attributes": True}')
    lines.append("")
    lines.append("    id: int")
    for f in fields:
        lines.append(field_line(f["name"], f["required"]))
    lines.append("    created_at: datetime")
    lines.append("    updated_at: datetime")
    lines += ["", ""]

    # NewsListResponse
    lines.append(f"class {Model}ListResponse(BaseModel):")
    lines.append(f"    items: List[{Model}Response]")
    lines.append("    total: int")
    lines.append("")

    return "\n".join(lines)


def _id_param(path: str) -> str:
    m = re.search(r"\{(\w+)\}", path)
    return m.group(1) if m else "id"


def generate_views(spec: dict) -> str:
    module = spec["module"]
    Model = module.capitalize()
    not_found = spec.get("not_found_detail", f"{Model}不存在")

    lines = [
        "from __future__ import annotations",
        "",
        "from fastapi import APIRouter, Depends, HTTPException",
        "",
        f"from server.dao.{module}_dao import {Model}DAO",
        "from server.models.user_model import User",
        "from server.utils.auth import get_current_user",
        "from server.utils.response import ApiResponse",
        f"from .schema import {Model}Create, {Model}ListResponse, {Model}Response, {Model}Update",
        "",
        "",
        "router = APIRouter()",
        "",
    ]

    for ep in spec["endpoints"]:
        method = ep["method"]
        path = ep["path"]
        auth = ep["auth"]
        # "/" becomes "" in decorator (FastAPI convention)
        dec_path = "" if path == "/" else path

        if method == "GET" and path == "/":
            func_name = f"list_{module}"
            resp_type = f"ApiResponse[{Model}ListResponse]"
            params = ["limit: int = 10", "offset: int = 0",
                      f"dao: {Model}DAO = Depends()"]
            body = [
                f"    items, total = await dao.list_(limit=limit, offset=offset)",
                f"    data = {Model}ListResponse(",
                f"        items=[{Model}Response.model_validate(i) for i in items],",
                f"        total=total,",
                f"    )",
                f"    return ApiResponse.success(data=data)",
            ]

        elif method == "GET" and "slug" in path:
            func_name = f"get_{module}_by_slug"
            resp_type = f"ApiResponse[{Model}Response]"
            params = ["slug: str", f"dao: {Model}DAO = Depends()"]
            body = [
                f"    obj = await dao.get_by_slug(slug=slug)",
                f"    if not obj:",
                f'        raise HTTPException(status_code=404, detail="{not_found}")',
                f"    return ApiResponse.success(data={Model}Response.model_validate(obj))",
            ]

        elif method == "GET" and "{" in path:
            id_p = _id_param(path)
            func_name = f"get_{module}"
            resp_type = f"ApiResponse[{Model}Response]"
            params = [f"{id_p}: int", f"dao: {Model}DAO = Depends()"]
            body = [
                f"    obj = await dao.get_by_id({module}_id={id_p})",
                f"    if not obj:",
                f'        raise HTTPException(status_code=404, detail="{not_found}")',
                f"    return ApiResponse.success(data={Model}Response.model_validate(obj))",
            ]

        elif method == "POST":
            func_name = f"create_{module}"
            resp_type = f"ApiResponse[{Model}Response]"
            params = [f"body: {Model}Create", f"dao: {Model}DAO = Depends()"]
            if auth:
                params.append("current_user: User = Depends(get_current_user)")
            body = [
                f"    obj = await dao.create(**body.model_dump())",
                f"    return ApiResponse.success(data={Model}Response.model_validate(obj))",
            ]

        elif method == "PUT":
            id_p = _id_param(path)
            func_name = f"update_{module}"
            resp_type = f"ApiResponse[{Model}Response]"
            params = [f"{id_p}: int", f"body: {Model}Update", f"dao: {Model}DAO = Depends()"]
            if auth:
                params.append("current_user: User = Depends(get_current_user)")
            body = [
                f"    obj = await dao.update({module}_id={id_p}, data=body.model_dump(exclude_none=True))",
                f"    if not obj:",
                f'        raise HTTPException(status_code=404, detail="{not_found}")',
                f"    return ApiResponse.success(data={Model}Response.model_validate(obj))",
            ]

        elif method == "DELETE":
            id_p = _id_param(path)
            func_name = f"delete_{module}"
            resp_type = "ApiResponse[None]"
            params = [f"{id_p}: int", f"dao: {Model}DAO = Depends()"]
            if auth:
                params.append("current_user: User = Depends(get_current_user)")
            body = [
                f"    ok = await dao.delete({module}_id={id_p})",
                f"    if not ok:",
                f'        raise HTTPException(status_code=404, detail="{not_found}")',
                f"    return ApiResponse.success(data=None)",
            ]

        else:
            continue

        dec = method.lower()
        lines.append(f'@router.{dec}("{dec_path}", response_model={resp_type})')
        params_str = ",\n    ".join(params)
        lines.append(f"async def {func_name}(")
        lines.append(f"    {params_str},")
        lines.append(f") -> {resp_type}:")
        lines += body
        lines.append("")

    return "\n".join(lines)


def generate_init(spec: dict) -> str:
    module = spec["module"]
    return f'from .views import router as {module}_router\n\n__all__ = ["{module}_router"]\n'


def main():
    parser = argparse.ArgumentParser(description="Generate FastAPI backend skeleton")
    parser.add_argument("--input", required=True, help="Path to api-spec.md")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    args = parser.parse_args()

    spec = parse_spec(args.input)
    module = spec["module"]

    out_dir = Path(args.output_dir) / "server" / "web" / "api" / module
    out_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "__init__.py": generate_init(spec),
        "schema.py": generate_schema(spec),
        "views.py": generate_views(spec),
    }

    for name, content in files.items():
        (out_dir / name).write_text(content, encoding="utf-8")

    print("已生成：")
    for name in files:
        print(f"  {args.output_dir}/server/web/api/{module}/{name}")


if __name__ == "__main__":
    main()
