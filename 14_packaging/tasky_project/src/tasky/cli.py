"""The interface layer: parse command-line arguments and print results.
All real work is delegated to store.py."""
import argparse
import os
from pathlib import Path

from tasky.store import TaskStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tasky", description="A tiny to-do list.")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="add a task")
    add.add_argument("title")
    sub.add_parser("list", help="show all tasks")
    done = sub.add_parser("done", help="mark a task as done")
    done.add_argument("id", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = TaskStore(Path(os.environ.get("TASKY_FILE", "tasks.json")))

    if args.command == "add":
        task = store.add(args.title)
        print(f"added #{task.id}: {task.title}")
    elif args.command == "list":
        tasks = store.load()
        if not tasks:
            print("no tasks yet")
        for t in tasks:
            print(f"[{'x' if t.done else ' '}] #{t.id} {t.title}")
    elif args.command == "done":
        try:
            task = store.complete(args.id)
        except KeyError as e:
            print(f"error: {e.args[0]}")
            return 1                         # non-zero exit code = failure (scripts can check it)
        print(f"completed #{task.id}: {task.title}")
    return 0
