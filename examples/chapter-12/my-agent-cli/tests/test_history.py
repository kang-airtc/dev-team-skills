import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from history import HistoryStore, HISTORY_LIMIT


@pytest.fixture
def tmp_store(tmp_path):
    return HistoryStore(path=tmp_path / "history.json")


# ---------- Task 1: append 超出限制自动截断 ----------

def test_append_trims_to_limit(tmp_store):
    for i in range(HISTORY_LIMIT + 1):   # 写入 21 条
        tmp_store.append(f"q{i}", f"a{i}")
    entries = tmp_store.list_all()
    assert len(entries) == HISTORY_LIMIT  # 只剩 20 条
    assert entries[0]["question"] == "q1" # q0 被删掉


# ---------- Task 2: clear 清空历史 ----------

def test_clear_empties_history(tmp_store):
    tmp_store.append("hello", "world")
    tmp_store.clear()
    assert tmp_store.list_all() == []


# ---------- Task 3: 首次读取不存在文件返回空列表 ----------

def test_empty_on_missing_file(tmp_store):
    assert tmp_store.list_all() == []


# ---------- Task 4: append 写入内容结构正确 ----------

def test_append_entry_structure(tmp_store):
    tmp_store.append("test question", "test answer")
    entries = tmp_store.list_all()
    assert len(entries) == 1
    assert entries[0]["question"] == "test question"
    assert entries[0]["answer"] == "test answer"
    assert "timestamp" in entries[0]
