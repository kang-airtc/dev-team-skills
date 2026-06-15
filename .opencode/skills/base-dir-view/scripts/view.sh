#!/usr/bin/env bash
# base-dir-view: 列出目录的树形结构（含文件大小和修改时间）
set -uo pipefail

TARGET="${1:-.}"
MAX_DEPTH="${2:-3}"

if [[ ! -d "$TARGET" ]]; then
  echo "错误：'$TARGET' 不是有效目录" >&2
  exit 1
fi

# 跨平台获取修改日期：macOS 用 date -r，Linux 用 stat -c
get_mtime() {
  date -r "$1" '+%Y-%m-%d' 2>/dev/null \
    || stat -c '%y' "$1" 2>/dev/null | cut -d' ' -f1
}

# 是否是要跳过的噪声目录
is_excluded() {
  case "$(basename "$1")" in
    node_modules|.git|venv|__pycache__|.next|dist|build|.DS_Store) return 0 ;;
    *) return 1 ;;
  esac
}

# 打印一个条目（缩进 + 名字 + 大小 + 修改日期）
print_entry() {
  local path="$1" depth="$2"
  local indent
  indent=$(printf '%*s' "$((depth * 2))" '')
  local name
  name=$(basename "$path")
  local size
  size=$(du -sh "$path" 2>/dev/null | cut -f1)
  local mtime
  mtime=$(get_mtime "$path")
  if [[ -d "$path" ]]; then
    echo "${indent}${name}/  (${size}, ${mtime})"
  else
    echo "${indent}${name}  (${size}, ${mtime})"
  fi
}

# 递归遍历
walk() {
  local dir="$1" depth="$2"
  (( depth > MAX_DEPTH )) && return

  local entries
  entries=$(ls -A "$dir" 2>/dev/null | sort) || return

  while IFS= read -r entry; do
    [[ -z "$entry" ]] && continue
    local path="$dir/$entry"
    if is_excluded "$path"; then
      continue
    fi
    print_entry "$path" "$depth"
    if [[ -d "$path" ]]; then
      walk "$path" $((depth + 1))
    fi
  done <<< "$entries"
  return 0
}

# 先打印根目录本身，再递归子节点
print_entry "$TARGET" 0
walk "$TARGET" 1
