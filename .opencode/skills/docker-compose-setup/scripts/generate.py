#!/usr/bin/env python3
"""docker-compose-setup: render Dockerfile / compose / up.sh from project-spec.yaml.

读取 project-spec.yaml，套 templates/ 下的字符串模板，生成三服务（frontend / backend /
db）的最小可运行容器化骨架到目标目录。模板用 ${KEY} 占位符，generate.py 只替换显式
已知的 KEY，docker-compose 自身的 ${VAR:-default} 形式因 KEY 命名不匹配而原样保留。
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "templates"


def parse_spec(spec_path: Path) -> dict:
    text = spec_path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    return _yaml_lite(text)


def _yaml_lite(text: str) -> dict:
    """Minimal nested-dict YAML parser; covers project-spec.yaml shape only."""
    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value == "":
            new: dict = {}
            parent[key] = new
            stack.append((indent, new))
        else:
            parent[key] = value
    return root


def build_substitutions(spec: dict) -> dict:
    frontend = spec.get("frontend", {}) or {}
    backend = spec.get("backend", {}) or {}
    db = spec.get("db", {}) or {}

    framework = (frontend.get("framework") or "nginx-static").strip()
    container_port = str(frontend.get("container_port") or (3000 if framework == "nextjs" else 80))

    return {
        "NODE_VERSION": str(frontend.get("node_version") or "18"),
        "FRONTEND_PORT": str(frontend.get("port") or 3000),
        "CONTAINER_PORT": container_port,
        "PYTHON_VERSION": str(backend.get("python_version") or "3.11"),
        "BACKEND_PORT": str(backend.get("port") or 8000),
        "BACKEND_MODULE": str(backend.get("module") or "main:app"),
        "DB_VERSION": str(db.get("version") or "15-alpine"),
        "DB_NAME": str(db.get("database") or "demo"),
        "DB_USER": str(db.get("user") or "demo"),
        "DB_HOST_PORT": str(db.get("host_port") or 5433),
    }, framework


def render(template_path: Path, subs: dict) -> str:
    text = template_path.read_text(encoding="utf-8")
    for key, value in subs.items():
        text = text.replace(f"${{{key}}}", value)
    return text


def write(path: Path, content: str, force: bool, executable: bool = False) -> str:
    if path.exists() and not force:
        return f"skip (exists): {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(0o755)
    return f"wrote: {path}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Docker / compose scaffolding from project-spec.yaml")
    parser.add_argument("--spec", "-s", default="project-spec.yaml", help="project-spec.yaml path")
    parser.add_argument("--output", "-o", default=".", help="output directory")
    parser.add_argument("--force", "-f", action="store_true", help="overwrite existing files")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"❌ spec not found: {spec_path}", file=sys.stderr)
        return 1

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    spec = parse_spec(spec_path)
    subs, framework = build_substitutions(spec)

    frontend_template = TEMPLATES / f"Dockerfile.frontend.{framework}"
    if not frontend_template.exists():
        print(f"❌ unsupported frontend framework: {framework}", file=sys.stderr)
        print(f"   available: {sorted(p.name for p in TEMPLATES.glob('Dockerfile.frontend.*'))}", file=sys.stderr)
        return 2

    actions = []
    actions.append(write(out_dir / "frontend" / "Dockerfile", render(frontend_template, subs), args.force))
    actions.append(write(out_dir / "backend" / "Dockerfile", render(TEMPLATES / "Dockerfile.backend.fastapi", subs), args.force))
    actions.append(write(out_dir / "docker-compose.yml", render(TEMPLATES / "docker-compose.yml", subs), args.force))
    actions.append(write(out_dir / "scripts" / "up.sh", render(TEMPLATES / "up.sh", subs), args.force, executable=True))
    actions.append(write(out_dir / "scripts" / "down.sh", render(TEMPLATES / "down.sh", subs), args.force, executable=True))

    placeholder_dockerfile = out_dir / "Dockerfile"
    if not placeholder_dockerfile.exists() or args.force:
        placeholder_dockerfile.write_text(
            "# 可选根镜像：供 deploy-check 演示根目录构建；业务镜像在 backend/、frontend/ 下\n"
            "FROM alpine:3.19\n"
            f"RUN echo \"{spec.get('project', 'app')} placeholder\"\n"
            "CMD [\"true\"]\n",
            encoding="utf-8",
        )
        actions.append(f"wrote: {placeholder_dockerfile}")

    for line in actions:
        print(line)

    print(f"\n✅ docker-compose-setup 完成（framework={framework}），下一步：cd {out_dir} && bash scripts/up.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
