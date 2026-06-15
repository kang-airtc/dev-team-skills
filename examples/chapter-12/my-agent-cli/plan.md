# my-agent-cli plan

spec-compliance review 通过（2026-05-05）

> 审查记录：草稿中方法命名为 `list_history()`，与 spec 里"列出历史"的表述不一致。
> 已统一改为 `list_all()`，符合通用命名惯例。

---

## Task 1: HistoryStore — append 超出限制自动截断

- **RED**: `test_append_trims_to_limit` — 写入 21 条，断言 `len == 20`，且最旧一条（q0）已被删除
- **GREEN**: `append()` 写入后若 `len(entries) > HISTORY_LIMIT` 则取末尾 20 条
- commit: `feat: HistoryStore append with auto-trim (limit=20)`

## Task 2: HistoryStore — clear 清空历史

- **RED**: `test_clear_empties_history` — 写入后 clear，`list_all()` 返回 `[]`
- **GREEN**: `clear()` 写入空数组
- commit: `feat: HistoryStore clear`

## Task 3: HistoryStore — 首次读取不存在文件返回空列表

- **RED**: `test_empty_on_missing_file` — `history.json` 不存在时 `list_all()` 返回 `[]`
- **GREEN**: `_load()` 检查文件是否存在
- commit: `feat: HistoryStore safe load on missing file`

## Task 4: HistoryStore — append 写入内容结构正确

- **RED**: `test_append_entry_structure` — 写入一条，断言 `question`、`answer`、`timestamp` 字段存在
- **GREEN**: `append()` 构造正确的 entry dict
- commit: `feat: HistoryStore append entry structure`

## Task 5: cli ask 命令 — 打印 Echo 并写入历史

- **RED**: 调用 `cmd_ask` 后 store 有 1 条记录，question 字段匹配
- **GREEN**: 实现 `cmd_ask`，调用 `mock_ask()` 并写入 store
- commit: `feat: cli ask command`

## Task 6: cli history 命令 — 格式化输出

- **RED**: 有 2 条历史时，stdout 包含 "1." 和 "2."
- **GREEN**: 实现 `cmd_history`，格式为 `{序号}. [{时间戳}] {问题}`
- commit: `feat: cli history command`

## Task 7: cli clear 命令

- **RED**: 调用 `cmd_clear` 后 `store.list_all() == []`
- **GREEN**: 实现 `cmd_clear`，调用 `store.clear()` 并打印确认
- commit: `feat: cli clear command`
