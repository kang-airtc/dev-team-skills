#!/usr/bin/env python3
"""
日志根因分析器
聚合容器日志，按时间线分析错误模式
"""

import argparse
import re
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def get_container_logs(container: str, since: str) -> list:
    """获取容器日志"""
    try:
        result = subprocess.run(
            ["docker", "logs", "--since", since, container],
            capture_output=True,
            text=True
        )
        logs = []
        for line in result.stdout.splitlines():
            if re.search(r'ERROR|FATAL|Exception|timeout|refused', line, re.IGNORECASE):
                # 尝试提取时间
                time_match = re.search(r'(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})', line)
                timestamp = time_match.group(1) if time_match else "未知"
                
                logs.append({
                    "timestamp": timestamp,
                    "container": container,
                    "message": line.strip()
                })
        return logs
    except:
        return []


def analyze_logs(logs: list) -> dict:
    """分析日志"""
    # 按时间排序
    sorted_logs = sorted(logs, key=lambda x: x["timestamp"])
    
    # 错误聚类
    error_patterns = defaultdict(int)
    for log in logs:
        # 提取错误类型
        if "database" in log["message"].lower() or "connection" in log["message"].lower():
            error_patterns["数据库连接错误"] += 1
        elif "timeout" in log["message"].lower():
            error_patterns["超时错误"] += 1
        elif "memory" in log["message"].lower():
            error_patterns["内存错误"] += 1
        else:
            error_patterns["其他错误"] += 1
    
    return {
        "timeline": sorted_logs,
        "patterns": dict(error_patterns)
    }


def generate_report(analysis: dict) -> str:
    """生成分析报告"""
    lines = [
        "# 日志根因分析报告",
        "",
        f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        ""
    ]
    
    # 时间线
    if analysis["timeline"]:
        lines.extend([
            "## 错误时间线",
            "",
            "| 时间 | 容器 | 错误 |",
            "|------|------|------|"
        ])
        
        for log in analysis["timeline"][:20]:  # 最多显示20条
            message = log["message"][:80]
            lines.append(f"| {log['timestamp']} | {log['container']} | {message} |")
        
        lines.append("")
    
    # 错误聚类
    if analysis["patterns"]:
        lines.extend([
            "## 错误统计",
            "",
            "| 错误类型 | 次数 |",
            "|---------|------|"
        ])
        
        for pattern, count in sorted(analysis["patterns"].items(), key=lambda x: -x[1]):
            lines.append(f"| {pattern} | {count} |")
        
        lines.append("")
    
    # 根因推断
    lines.extend([
        "## 根因推断",
        "",
        "基于时间线和错误模式分析：",
        "",
        "🔴 **可能根因**: ",
        ""
    ])
    
    # 简单的根因推断逻辑
    if not analysis["timeline"]:
        lines.append("✅ 未发现错误日志，系统运行正常")
    elif "数据库连接错误" in analysis["patterns"]:
        lines.append("- 数据库连接问题可能是根因")
        lines.append("- 建议检查数据库连接池配置")
    elif "超时错误" in analysis["patterns"]:
        lines.append("- 超时错误可能是根因")
        lines.append("- 建议检查网络延迟或服务性能")
    else:
        lines.append("- 需要进一步人工分析")
    
    lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='日志根因分析器')
    parser.add_argument('--since', default='1h', help='时间范围')
    parser.add_argument('--container', '-c', help='指定容器')
    parser.add_argument('--output', '-o', default='incident-log-analysis.md', help='输出路径')
    args = parser.parse_args()
    
    print(f"🔍 分析日志（最近 {args.since}）...")
    
    # 获取容器列表
    if args.container:
        containers = [args.container]
    else:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        containers = [c for c in result.stdout.splitlines() if c]
    
    # 收集日志
    all_logs = []
    for container in containers:
        logs = get_container_logs(container, args.since)
        all_logs.extend(logs)
        print(f"   {container}: {len(logs)} 条错误日志")
    
    # 分析
    analysis = analyze_logs(all_logs)
    
    # 生成报告
    report = generate_report(analysis)
    
    output_path = Path(args.output)
    output_path.write_text(report, encoding='utf-8')
    
    print(f"[成功] 分析报告已生成: {output_path}")


if __name__ == "__main__":
    main()
