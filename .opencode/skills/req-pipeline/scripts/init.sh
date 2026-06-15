#!/bin/bash
# 初始化需求管理项目

if [ $# -lt 1 ]; then
    echo "用法: $0 <项目名称>"
    echo "示例: $0 my-project"
    exit 1
fi

PROJECT_NAME="$1"
OUTPUT_DIR="./projects/$PROJECT_NAME"

if [ -d "$OUTPUT_DIR" ]; then
    echo "[警告] 项目已存在: $OUTPUT_DIR"
    read -p "是否覆盖? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "已取消"
        exit 0
    fi
fi

mkdir -p "$OUTPUT_DIR"

echo "✅ 项目初始化完成: $OUTPUT_DIR"
echo ""
echo "请在该目录下放置以下文件:"
echo "  0-raw-requirement.txt  - 原始需求描述"
echo ""
echo "然后运行: ./run-all.sh \"$PROJECT_NAME\" \"$OUTPUT_DIR/0-raw-requirement.txt\""
