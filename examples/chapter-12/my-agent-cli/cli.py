import argparse
import sys

from history import HistoryStore


def mock_ask(question: str) -> str:
    return f"Echo: {question}"


def cmd_ask(args, store: HistoryStore) -> int:
    answer = mock_ask(args.question)
    print(answer)
    store.append(args.question, answer)
    return 0


def cmd_history(args, store: HistoryStore) -> int:
    entries = store.list_all()
    if not entries:
        print("（暂无历史记录）")
        return 0
    for i, e in enumerate(entries, 1):
        ts = e["timestamp"][:19].replace("T", " ")
        print(f"{i:3}. [{ts}] {e['question']}")
    return 0


def cmd_clear(args, store: HistoryStore) -> int:
    store.clear()
    print("历史记录已清空。")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="my-agent-cli",
        description="向 AI 提问并本地记录历史",
    )
    sub = parser.add_subparsers(dest="command")

    ask_p = sub.add_parser("ask", help="向 AI 提问")
    ask_p.add_argument("question", help="问题内容")

    sub.add_parser("history", help="查看历史记录")
    sub.add_parser("clear", help="清空历史记录")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 1

    store = HistoryStore()
    dispatch = {"ask": cmd_ask, "history": cmd_history, "clear": cmd_clear}
    return dispatch[args.command](args, store)


if __name__ == "__main__":
    sys.exit(main())
