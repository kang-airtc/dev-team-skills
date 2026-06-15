#!/usr/bin/env python3
"""dev-migrate: Generate Alembic migration script from migration-spec.md."""

import argparse
import hashlib
import re
from datetime import datetime
from pathlib import Path


def parse_spec(spec_path: str) -> dict:
    content = Path(spec_path).read_text(encoding="utf-8")
    spec = {}

    # Title → table name
    m = re.search(r"#.*?新建\s*(\w+)\s*表", content)
    if m:
        spec["table"] = m.group(1).lower()
        spec["action"] = "create"
    else:
        spec["table"] = "unknown"
        spec["action"] = "create"

    # Fields from bullet list: - name: Type, constraint, ...
    fields = []
    indexes = []
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        # Match: - field_name: Type(...), extra
        fm = re.match(r"- (\w+):\s*(.+)", line)
        if not fm:
            continue
        fname = fm.group(1)
        rest = fm.group(2)

        # Primary key
        if "主键" in rest or "primary" in rest.lower():
            fields.append({"name": fname, "sa": "sa.Integer()", "nullable": False,
                           "pk": True, "server_default": None, "default": None})
            continue

        # Detect type
        sa_type = _detect_sa_type(rest)
        nullable = "可空" in rest or "nullable" in rest.lower()
        server_default = None
        if "server_default=now()" in rest:
            server_default = 'sa.text("now()")'
        default = None
        if "默认 true" in rest.lower() or "default=true" in rest.lower():
            default = "True"

        fields.append({
            "name": fname,
            "sa": sa_type,
            "nullable": nullable,
            "pk": False,
            "server_default": server_default,
            "default": default,
        })

        # Index
        ix_m = re.search(r"索引\s*(ix_[\w]+)", rest)
        if ix_m:
            ix_name = ix_m.group(1)
            unique = "唯一" in rest or "unique" in rest.lower()
            indexes.append({"name": ix_name, "col": fname, "unique": unique})

    spec["fields"] = fields
    spec["indexes"] = indexes
    return spec


def _detect_sa_type(rest: str) -> str:
    rest_lower = rest.lower()
    if "string(255)" in rest_lower or "varchar(255)" in rest_lower:
        return "sa.String(length=255)"
    if "string(500)" in rest_lower or "varchar(500)" in rest_lower:
        return "sa.String(length=500)"
    if "string(100)" in rest_lower or "varchar(100)" in rest_lower:
        return "sa.String(length=100)"
    if re.search(r"string\((\d+)\)", rest_lower):
        n = re.search(r"string\((\d+)\)", rest_lower).group(1)
        return f"sa.String(length={n})"
    if "text" in rest_lower:
        return "sa.Text()"
    if "boolean" in rest_lower or "bool" in rest_lower:
        return "sa.Boolean()"
    if "datetime(timezone=true)" in rest_lower or "datetime(tz)" in rest_lower:
        return "sa.DateTime(timezone=True)"
    if "datetime" in rest_lower:
        return "sa.DateTime()"
    if "integer" in rest_lower or "int" in rest_lower:
        return "sa.Integer()"
    return "sa.String(255)"


def generate_migration(spec: dict, timestamp: str, rev_id: str) -> str:
    table = spec["table"]
    fields = spec["fields"]
    indexes = spec["indexes"]

    lines = [
        '"""add_{table}_table',
        "",
        f"Revision ID: {rev_id}",
        f"Revises:",
        f"Create Date: {timestamp}",
        '"""',
        "",
        "import sqlalchemy as sa",
        "from alembic import op",
        "",
        "",
        f'revision = "{rev_id}"',
        'down_revision = None',
        'branch_labels = None',
        'depends_on = None',
        "",
        "",
        "def upgrade() -> None:",
        "    op.create_table(",
        f'        "{table}",',
    ]

    lines[0] = lines[0].replace("{table}", table)

    for f in fields:
        kwargs = []
        if f["pk"]:
            kwargs += ["autoincrement=True", "nullable=False"]
        else:
            kwargs.append(f"nullable={f['nullable']}")
        if f.get("server_default"):
            kwargs.append(f"server_default={f['server_default']}")
        if f.get("default") == "True":
            kwargs.append("default=True")
        kwargs_str = ", ".join(kwargs)
        lines.append(f'        sa.Column("{f["name"]}", {f["sa"]}, {kwargs_str}),')

    # Primary key constraint
    pk_fields = [f["name"] for f in fields if f["pk"]]
    if pk_fields:
        lines.append(f'        sa.PrimaryKeyConstraint("{pk_fields[0]}"),')
    lines.append("    )")

    # Create indexes
    for ix in indexes:
        unique_arg = ", unique=True" if ix["unique"] else ""
        lines.append(f'    op.create_index("{ix["name"]}", "{table}", ["{ix["col"]}"]' + (", unique=True)" if ix["unique"] else ")"))

    lines += ["", "", "def downgrade() -> None:"]

    # Drop indexes in reverse order
    for ix in reversed(indexes):
        lines.append(f'    op.drop_index("{ix["name"]}", table_name="{table}")')

    lines.append(f'    op.drop_table("{table}")')
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Alembic migration script")
    parser.add_argument("--input", required=True, help="Path to migration-spec.md")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    args = parser.parse_args()

    spec = parse_spec(args.input)
    table = spec["table"]

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    file_ts = now.strftime("%Y%m%d%H%M%S")
    rev_id = hashlib.md5(f"{table}{file_ts}".encode()).hexdigest()[:12]

    out_dir = Path(args.output_dir) / "alembic" / "versions"
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{file_ts}_add_{table}_table.py"
    content = generate_migration(spec, timestamp, rev_id)
    (out_dir / filename).write_text(content, encoding="utf-8")

    print("已生成：")
    print(f"  {args.output_dir}/alembic/versions/{filename}")


if __name__ == "__main__":
    main()
