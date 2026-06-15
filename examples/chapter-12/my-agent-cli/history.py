import json
import pathlib
from datetime import datetime, timezone

HISTORY_DIR = pathlib.Path.home() / ".my-agent-cli"
HISTORY_FILE = HISTORY_DIR / "history.json"
HISTORY_LIMIT = 20


class HistoryStore:
    def __init__(self, path: pathlib.Path = HISTORY_FILE):
        self.path = path

    def _load(self) -> list:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, entries: list) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(entries, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def append(self, question: str, answer: str) -> None:
        entries = self._load()
        entries.append(
            {
                "question": question,
                "answer": answer,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
        if len(entries) > HISTORY_LIMIT:
            entries = entries[-HISTORY_LIMIT:]
        self._save(entries)

    def list_all(self) -> list:
        return self._load()

    def clear(self) -> None:
        self._save([])
