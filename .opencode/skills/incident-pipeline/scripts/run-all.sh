#!/bin/bash
# incident-pipeline: 一键故障诊断流水线

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

CONTAINER=""
OUTPUT_DIR="./incident-output"
SEVERITY="P2"
DURATION="30"

while [[ $# -gt 0 ]]; do
    case $1 in
        --container|-c)
            CONTAINER="$2"
            shift 2
            ;;
        --output|-o)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --severity)
            SEVERITY="$2"
            shift 2
            ;;
        --duration)
            DURATION="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

if [[ -z "$CONTAINER" ]]; then
    echo "用法: $0 --container <容器名>"
    exit 1
fi

echo "🚨 启动故障诊断流水线: $CONTAINER"
echo "====================================="

mkdir -p "$OUTPUT_DIR"

# Step 1: 容器诊断
echo "🔍 Step 1/3: 容器诊断..."
bash "$SKILLS_DIR/incident-container/scripts/diagnose.sh" \
    --container "$CONTAINER" \
    --output "$OUTPUT_DIR/1-container-diagnosis.md"
echo ""

# Step 2: 日志分析
echo "📋 Step 2/3: 日志分析..."
python3 "$SKILLS_DIR/incident-log/scripts/analyze.py" \
    --container "$CONTAINER" \
    --since 1h \
    --output "$OUTPUT_DIR/2-log-analysis.md"
echo ""

# Step 3: 生成复盘报告模板
echo "📝 Step 3/3: 生成复盘报告..."
python3 "$SKILLS_DIR/incident-report/scripts/generate.py" \
    --title "$CONTAINER 故障" \
    --severity "$SEVERITY" \
    --duration "$DURATION" \
    --output "$OUTPUT_DIR/3-postmortem.md"
echo ""

# 汇总
DIAG_TIME=$(date '+%Y-%m-%d %H:%M')
cat > "$OUTPUT_DIR/0-summary.md" << EOF
# 故障诊断汇总

**容器**: $CONTAINER
**严重等级**: $SEVERITY
**持续时间**: $DURATION 分钟
**诊断时间**: $DIAG_TIME

---

## 详细报告

- [容器诊断](1-container-diagnosis.md) — 状态快照 + 修复建议
- [日志分析](2-log-analysis.md) — 时间线 + 异常聚类
- [复盘草稿](3-postmortem.md) — 待团队会议补全

## 后续行动

1. 查看容器诊断报告，了解故障现象
2. 分析日志，定位根因
3. 补充复盘报告中的具体信息（时间线、影响范围、根因）
4. 制定改进措施并设定负责人
5. 执行修复并验证恢复状态

EOF

echo "====================================="
echo "✅ 故障诊断完成！"
echo "====================================="
echo ""
echo "产出物: $OUTPUT_DIR/"
