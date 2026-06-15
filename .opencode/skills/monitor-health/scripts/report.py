#!/usr/bin/env python3
"""
系统健康报告生成器

整合容器、日志、备份、资源四个维度，按 5 维加权打分（满分 100）。
分数本身是启发式入口，不是 SLA。
"""

import argparse
import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path


def run_shell(cmd: str) -> str:
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return ""


def list_containers(name_filter: str | None) -> list[dict]:
    """列出运行中容器（可按名称前缀过滤）"""
    fl = f' --filter "name={name_filter}"' if name_filter else ""
    output = run_shell(f"docker ps{fl} --format '{{{{json .}}}}'")
    out = []
    for line in output.splitlines():
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            pass
    return out


def inspect_container(name: str) -> dict:
    """读取容器健康/重启次数/资源占用"""
    health_cmd = (
        f"docker inspect --format='{{{{if .State.Health}}}}{{{{.State.Health.Status}}}}"
        f"{{{{else}}}}-{{{{end}}}}' {name}"
    )
    restart = run_shell(f"docker inspect --format='{{{{.RestartCount}}}}' {name}")
    health = run_shell(health_cmd) or "-"
    stats = run_shell(
        f"docker stats --no-stream --format '{{{{.CPUPerc}}}}|{{{{.MemPerc}}}}' {name}"
    )
    cpu_str, mem_str = ("0%", "0%")
    if "|" in stats:
        cpu_str, mem_str = stats.split("|", 1)

    def parse_pct(s: str) -> float:
        s = s.strip().rstrip("%")
        try:
            return float(s)
        except ValueError:
            return 0.0

    return {
        "name": name,
        "health": health,
        "restart": int(restart) if restart.isdigit() else 0,
        "cpu": parse_pct(cpu_str),
        "mem": parse_pct(mem_str),
    }


def count_log_errors(name: str, since: str = "1h") -> int:
    out = run_shell(
        f"docker logs --since {since} {name} 2>&1 | grep -ciE 'error|fatal|exception'"
    )
    try:
        return int(out)
    except ValueError:
        return 0


def find_recent_backup(backup_dir: Path | None, max_age_hours: int = 24) -> dict | None:
    """在 backup_dir 找最近一次备份；返回 {file, size_bytes, age_hours}"""
    if not backup_dir or not backup_dir.exists():
        return None
    candidates = sorted(
        backup_dir.glob("*.sql"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        return None
    latest = candidates[0]
    age = datetime.now() - datetime.fromtimestamp(latest.stat().st_mtime)
    age_hours = age.total_seconds() / 3600
    return {
        "file": latest.name,
        "size_bytes": latest.stat().st_size,
        "age_hours": age_hours,
    }


def score_containers(containers: list[dict], details: list[dict]) -> tuple[int, list[str]]:
    """容器健康（满分 30）。每个非 running 或 unhealthy 扣 10 分。"""
    notes = []
    score = 30
    for c, d in zip(containers, details):
        state = c.get("State", "running")
        if state != "running":
            score -= 10
            notes.append(f"`{c.get('Names')}` 状态 = {state}（-10）")
        elif d["health"] == "unhealthy":
            score -= 10
            notes.append(f"`{c.get('Names')}` healthcheck = unhealthy（-10）")
    if score == 30 and containers:
        notes.append("✅ 所有容器 healthy")
    return max(0, score), notes


def score_restarts(details: list[dict]) -> tuple[int, list[str]]:
    """重启次数（满分 20）。每次重启 -2，下限 0。"""
    total = sum(d["restart"] for d in details)
    score = max(0, 20 - total * 2)
    if total == 0:
        return score, ["✅ 24h 内无容器重启"]
    notes = []
    for d in details:
        if d["restart"] > 0:
            notes.append(f"`{d['name']}` 重启 {d['restart']} 次（-{d['restart'] * 2}）")
    notes.insert(0, f"累计重启 {total} 次")
    return score, notes


def score_log_errors(per_container: dict[str, int]) -> tuple[int, list[str]]:
    """日志 ERROR（满分 25）。每条 -1，下限 0。"""
    total = sum(per_container.values())
    score = max(0, 25 - total)
    if total == 0:
        return score, ["✅ 1h 内无 ERROR/FATAL/Exception"]
    notes = [f"1h 内累计 {total} 条 ERROR（-{min(total, 25)}）"]
    for name, n in per_container.items():
        if n > 0:
            notes.append(f"`{name}` {n} 条")
    return score, notes


def score_backup(backup: dict | None, min_size: int) -> tuple[int, list[str]]:
    """备份成功（满分 15）。文件存在 + 大小达标 + 24h 内 = 15。"""
    if backup is None:
        return 0, ["⚠️ 未找到最近备份"]
    if backup["size_bytes"] <= min_size:
        return 0, [f"❌ 备份大小 {backup['size_bytes']}B ≤ {min_size}B"]
    if backup["age_hours"] > 24:
        return 0, [f"❌ 最近备份 {backup['age_hours']:.1f}h 前，超过 24h"]
    return 15, [
        f"✅ 备份正常（{backup['file']}, {backup['size_bytes']}B, {backup['age_hours']:.1f}h 前）"
    ]


def score_resources(details: list[dict]) -> tuple[int, list[str]]:
    """资源压力（满分 10）。容器 CPU/Mem 都 < 80% = 10；每超 1 个扣 2 分。"""
    notes = []
    over = 0
    for d in details:
        if d["cpu"] >= 80 or d["mem"] >= 80:
            over += 1
            notes.append(f"`{d['name']}` CPU={d['cpu']:.1f}% Mem={d['mem']:.1f}%（-2）")
    score = max(0, 10 - over * 2)
    if over == 0:
        notes.append("✅ 所有容器 CPU/Mem 均 < 80%")
    return score, notes


def overall_status(score: int) -> tuple[str, str]:
    if score >= 90:
        return "🟢", "优秀"
    elif score >= 70:
        return "🟢", "健康"
    elif score >= 50:
        return "🟡", "需关注"
    return "🔴", "严重"


def derive_actions(
    containers_notes: list[str],
    restart_notes: list[str],
    log_notes: list[str],
    backup_notes: list[str],
    resource_notes: list[str],
) -> tuple[list[str], list[str], list[str]]:
    """按时间紧急度分层（立即 / 今日 / 本周）"""
    immediate = []
    today = []
    weekly = []
    for n in containers_notes:
        if "状态" in n or "unhealthy" in n:
            immediate.append(n)
    for n in backup_notes:
        if n.startswith("❌") or n.startswith("⚠️"):
            immediate.append(n)
    for n in log_notes:
        if "1h" in n and "✅" not in n:
            today.append(n)
    for n in restart_notes:
        if "✅" not in n and "累计" in n:
            today.append(n)
    for n in resource_notes:
        if n.startswith("`"):
            today.append(n)
    if not immediate and not today:
        weekly.append("系统稳定，可继续观察重启次数与磁盘水位的长期趋势")
    return immediate, today, weekly


def build_report(args) -> str:
    name_filter = args.name_filter
    backup_dir = Path(args.backup_dir) if args.backup_dir else None

    containers = list_containers(name_filter)
    details = [inspect_container(c["Names"]) for c in containers]

    log_errors = {}
    for c in containers:
        n = count_log_errors(c["Names"], args.since)
        if n > 0:
            log_errors[c["Names"]] = n

    backup = find_recent_backup(backup_dir, args.backup_max_age)

    s_cont, n_cont = score_containers(containers, details)
    s_rest, n_rest = score_restarts(details)
    s_log, n_log = score_log_errors(log_errors)
    s_bak, n_bak = score_backup(backup, args.backup_min_size)
    s_res, n_res = score_resources(details)

    total = s_cont + s_rest + s_log + s_bak + s_res
    icon, label = overall_status(total)

    immediate, today, weekly = derive_actions(n_cont, n_rest, n_log, n_bak, n_res)

    lines = [
        "# 系统健康报告",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**检查范围**: 容器 / 重启 / 日志（{args.since}）/ 备份 / 资源",
        "",
        "---",
        "",
        f"## 综合健康分: {icon} {total} / 100（{label}）",
        "",
        "| 维度 | 得分 | 满分 | 说明 |",
        "|---|---|---|---|",
        f"| 容器健康 | {s_cont} | 30 | {'；'.join(n_cont) or '-'} |",
        f"| 重启次数 | {s_rest} | 20 | {'；'.join(n_rest) or '-'} |",
        f"| 日志 ERROR | {s_log} | 25 | {'；'.join(n_log) or '-'} |",
        f"| 备份成功 | {s_bak} | 15 | {'；'.join(n_bak) or '-'} |",
        f"| 资源压力 | {s_res} | 10 | {'；'.join(n_res) or '-'} |",
        "",
        "---",
        "",
        "## 容器明细",
        "",
        "| 容器 | Health | Restart | CPU | Mem |",
        "|---|---|---|---|---|",
    ]

    for d in details:
        lines.append(
            f"| {d['name']} | {d['health']} | {d['restart']} | {d['cpu']:.2f}% | {d['mem']:.2f}% |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 行动建议",
        "",
    ])

    def render_block(title: str, items: list[str]):
        lines.append(f"### {title}")
        lines.append("")
        if items:
            for it in items:
                lines.append(f"- {it}")
        else:
            lines.append("- 无")
        lines.append("")

    render_block("立即（30 分钟内）", immediate)
    render_block("今日内", today)
    render_block("本周内", weekly)

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="系统健康报告生成器（5 维评分）")
    parser.add_argument("--output", "-o", default="health-report.md", help="输出路径")
    parser.add_argument("--since", default="1h", help="日志时间窗（如 1h / 24h）")
    parser.add_argument(
        "--name-filter",
        default=None,
        help="按容器名前缀过滤（例如 release-demo）",
    )
    parser.add_argument(
        "--backup-dir",
        default=None,
        help="备份目录路径；不传则备份维度计 0",
    )
    parser.add_argument(
        "--backup-min-size",
        type=int,
        default=256,
        help="备份文件最小可信字节数（默认 256）",
    )
    parser.add_argument(
        "--backup-max-age",
        type=int,
        default=24,
        help="备份最大允许小时数（默认 24h）",
    )
    args = parser.parse_args()

    print("🏥 生成系统健康报告...")
    report = build_report(args)
    Path(args.output).write_text(report, encoding="utf-8")
    print(f"[成功] 健康报告已生成: {args.output}")


if __name__ == "__main__":
    main()
