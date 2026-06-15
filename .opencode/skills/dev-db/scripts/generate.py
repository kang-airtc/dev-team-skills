#!/usr/bin/env python3
"""dev-db: Generate SQLAlchemy 2.x ORM model from model-spec.md."""

import argparse
import re
from pathlib import Path


def parse_spec(spec_path: str) -> dict:
    content = Path(spec_path).read_text(encoding="utf-8")
    spec = {}

    # Table name
    m = re.search(r"## 表名\s*\n(\w+)", content)
    if not m:
        raise ValueError("model-spec.md 中未找到 ## 表名")
    spec["table"] = m.group(1).strip()

    # Model class name: snake_case → CamelCase
    spec["model"] = "".join(w.capitalize() for w in spec["table"].split("_"))

    # Field table
    fields = []
    table_m = re.search(r"## 字段定义.*?\n((?:\|.+\n)+)", content, re.DOTALL)
    if table_m:
        for line in table_m.group(1).strip().splitlines():
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if len(cells) < 3:
                continue
            if cells[0] in ("字段名", "---", ":---") or cells[0].startswith("-"):
                continue
            name, typ, constraint = cells[0], cells[1], cells[2]
            desc = cells[3] if len(cells) > 3 else ""
            fields.append({"name": name, "type": typ, "constraint": constraint, "desc": desc})
    spec["fields"] = fields

    # Notes
    spec["timezone"] = "timezone=True" in content

    return spec


def sa_type(typ: str, constraint: str, timezone: bool) -> tuple:
    """Return (mapped_type_str, column_type_str, extra_kwargs) for a field."""
    typ = typ.lower()
    is_nullable = "可空" in constraint or "optional" in constraint.lower()
    is_pk = "主键" in constraint

    # Column type
    if is_pk:
        col_type = "Integer()"
        mapped_t = "int"
    elif re.match(r"varchar\((\d+)\)", typ):
        n = re.match(r"varchar\((\d+)\)", typ).group(1)
        col_type = f"String({n})"
        mapped_t = "str"
    elif typ == "text":
        col_type = "Text"
        mapped_t = "str"
    elif typ == "bool" or typ == "boolean":
        col_type = "Boolean"
        mapped_t = "bool"
    elif re.match(r"datetime", typ):
        tz = "timezone=True" if timezone else ""
        col_type = f"DateTime({tz})" if tz else "DateTime()"
        mapped_t = "datetime"
    elif typ == "int" or typ == "integer":
        col_type = "Integer()"
        mapped_t = "int"
    else:
        col_type = "String(255)"
        mapped_t = "str"

    # Mapped annotation
    if is_nullable:
        mapped_ann = f"Optional[{mapped_t}]"
    else:
        mapped_ann = mapped_t

    return mapped_ann, col_type, is_nullable


def generate_model(spec: dict) -> str:
    table = spec["table"]
    model = spec["model"]
    fields = spec["fields"]
    tz = spec["timezone"]

    lines = [
        "from __future__ import annotations",
        "",
        "from datetime import datetime",
        "from typing import Optional",
        "",
        "from sqlalchemy import Boolean, DateTime, Index, Integer, String, Text, func",
        "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column",
        "",
        "",
        "class Base(DeclarativeBase):",
        "    pass",
        "",
        "",
        f"class {model}(Base):",
        f'    __tablename__ = "{table}"',
    ]

    # Collect indexes
    indexes = []
    for f in fields:
        name = f["name"]
        c = f["constraint"]
        if "唯一" in c and "带索引" in c:
            indexes.append(f'        Index("ix_{table}_{name}", "{name}", unique=True),')
        elif "带索引" in c or "索引" in c.replace("唯一", ""):
            indexes.append(f'        Index("ix_{table}_{name}", "{name}"),')

    if indexes:
        lines.append("    __table_args__ = (")
        lines += indexes
        lines.append("    )")
    lines.append("")

    # Skip auto timestamp fields — we handle them specially
    auto_fields = {"created_at", "updated_at"}

    for f in fields:
        name = f["name"]
        typ = f["type"]
        c = f["constraint"]

        if name in auto_fields:
            continue

        is_pk = "主键" in c
        is_nullable = "可空" in c
        is_unique = "唯一" in c

        mapped_ann, col_type, _ = sa_type(typ, c, tz)

        if is_pk:
            lines.append(f"    {name}: Mapped[{mapped_ann}] = mapped_column(primary_key=True, autoincrement=True)")
        elif typ.lower() == "bool" or typ.lower() == "boolean":
            default_val = "True" if "默认 true" in c.lower() or "默认true" in c.lower() else "False"
            lines.append(f"    {name}: Mapped[{mapped_ann}] = mapped_column({col_type}, default={default_val}, nullable=False)")
        elif is_nullable:
            lines.append(f"    {name}: Mapped[{mapped_ann}] = mapped_column({col_type})")
        else:
            if is_unique:
                lines.append(f"    {name}: Mapped[{mapped_ann}] = mapped_column({col_type}, nullable=False, unique=True)")
            else:
                lines.append(f"    {name}: Mapped[{mapped_ann}] = mapped_column({col_type}, nullable=False)")

    # Auto timestamp fields
    tz_arg = "timezone=True" if tz else ""
    dt_col = f"DateTime({tz_arg})" if tz else "DateTime()"
    lines += [
        f"    created_at: Mapped[datetime] = mapped_column(",
        f"        {dt_col}, nullable=False, server_default=func.now(),",
        f"    )",
        f"    updated_at: Mapped[datetime] = mapped_column(",
        f"        {dt_col}, nullable=False,",
        f"        server_default=func.now(), onupdate=func.now(),",
        f"    )",
        "",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate SQLAlchemy 2.x ORM model")
    parser.add_argument("--input", required=True, help="Path to model-spec.md")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    args = parser.parse_args()

    spec = parse_spec(args.input)
    table = spec["table"]

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{table}_model.py"
    content = generate_model(spec)
    (out_dir / filename).write_text(content, encoding="utf-8")

    print("已生成：")
    print(f"  {args.output_dir}/{filename}")


if __name__ == "__main__":
    main()
