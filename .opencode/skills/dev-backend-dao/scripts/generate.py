#!/usr/bin/env python3
"""dev-backend-dao: Generate SQLAlchemy 2.x async DAO from dao-spec.md."""

import argparse
import re
from pathlib import Path


def parse_spec(spec_path: str) -> dict:
    content = Path(spec_path).read_text(encoding="utf-8")
    spec = {}

    # Model name
    m = re.search(r"## 模型\s*\n(.+)", content)
    if m:
        model_line = m.group(1).strip()
        spec["model"] = model_line.split("（")[0].strip()
        # CamelCase → snake_case
        spec["module"] = re.sub(r"([A-Z])", lambda x: "_" + x.group(1).lower(), spec["model"]).lstrip("_")
    else:
        raise ValueError("dao-spec.md 中未找到 ## 模型")

    # Method table
    methods = []
    table_m = re.search(r"## 需要的方法.*?\n((?:\|.+\n)+)", content, re.DOTALL)
    if table_m:
        for line in table_m.group(1).strip().splitlines():
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if len(cells) >= 2 and cells[0] not in ("方法", "---", ":---"):
                methods.append({"name": cells[0], "desc": cells[1]})
    spec["methods"] = methods

    # Detect filter fields from desc
    spec["sort_field"] = "published_at"
    spec["filter_field"] = "is_published"
    for m_info in methods:
        if "published_only" in m_info.get("desc", ""):
            spec["has_published_filter"] = True

    return spec


def generate_dao(spec: dict) -> str:
    model = spec["model"]   # e.g. News
    module = spec["module"]  # e.g. news
    sort_field = spec.get("sort_field", "created_at")
    filter_field = spec.get("filter_field", "is_published")

    lines = [
        "from __future__ import annotations",
        "",
        "from typing import List, Optional, Tuple",
        "",
        "from fastapi import Depends",
        "from sqlalchemy import func, select",
        "from sqlalchemy.ext.asyncio import AsyncSession",
        "",
        f"from server.models.{module}_model import {model}",
        "from server.utils.db import get_db_session",
        "",
        "",
        f"class {model}DAO:",
        f'    """Data Access Object for {model}."""',
        "",
        "    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:",
        "        self.session = session",
        "",
    ]

    for m_info in spec["methods"]:
        name = m_info["name"]

        if name == "list_":
            lines += [
                f"    async def list_(",
                f"        self,",
                f"        limit: int = 10,",
                f"        offset: int = 0,",
                f"        published_only: bool = True,",
                f"    ) -> Tuple[List[{model}], int]:",
                f"        stmt = select({model})",
                f"        if published_only:",
                f"            stmt = stmt.where({model}.{filter_field}.is_(True))",
                f"        stmt = stmt.order_by({model}.{sort_field}.desc())",
                f"",
                f"        count_stmt = select(func.count()).select_from(stmt.subquery())",
                f"        total: int = (await self.session.execute(count_stmt)).scalar_one()",
                f"",
                f"        rows = (await self.session.execute(stmt.limit(limit).offset(offset))).scalars().all()",
                f"        return list(rows), total",
                "",
            ]

        elif name == "get_by_id":
            lines += [
                f"    async def get_by_id(self, {module}_id: int) -> Optional[{model}]:",
                f"        stmt = select({model}).where({model}.id == {module}_id)",
                f"        result = await self.session.execute(stmt)",
                f"        return result.scalar_one_or_none()",
                "",
            ]

        elif name == "get_by_slug":
            lines += [
                f"    async def get_by_slug(self, slug: str) -> Optional[{model}]:",
                f"        stmt = select({model}).where({model}.slug == slug)",
                f"        result = await self.session.execute(stmt)",
                f"        return result.scalar_one_or_none()",
                "",
            ]

        elif name == "create":
            lines += [
                f"    async def create(self, **data) -> {model}:",
                f"        obj = {model}(**data)",
                f"        self.session.add(obj)",
                f"        await self.session.commit()",
                f"        await self.session.refresh(obj)",
                f"        return obj",
                "",
            ]

        elif name == "update":
            lines += [
                f"    async def update(self, {module}_id: int, data: dict) -> Optional[{model}]:",
                f"        obj = await self.get_by_id({module}_id)",
                f"        if not obj:",
                f"            return None",
                f"        for key, value in data.items():",
                f"            setattr(obj, key, value)",
                f"        await self.session.commit()",
                f"        await self.session.refresh(obj)",
                f"        return obj",
                "",
            ]

        elif name == "delete":
            lines += [
                f"    async def delete(self, {module}_id: int) -> bool:",
                f"        obj = await self.get_by_id({module}_id)",
                f"        if not obj:",
                f"            return False",
                f"        await self.session.delete(obj)",
                f"        await self.session.commit()",
                f"        return True",
                "",
            ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate SQLAlchemy 2.x async DAO")
    parser.add_argument("--input", required=True, help="Path to dao-spec.md")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    args = parser.parse_args()

    spec = parse_spec(args.input)
    module = spec["module"]

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{module}_dao.py"
    content = generate_dao(spec)
    (out_dir / filename).write_text(content, encoding="utf-8")

    print("已生成：")
    print(f"  {args.output_dir}/{filename}")


if __name__ == "__main__":
    main()
