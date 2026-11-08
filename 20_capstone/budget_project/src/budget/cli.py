"""Command-line interface (Module 14): parse arguments, call the service, print results."""
import argparse
import logging
import os
from datetime import date

from budget.repository import SqliteExpenseRepository
from budget.service import BudgetError, BudgetService

LIMITS = {"food": 400.0, "fun": 150.0}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="budget", description="Track your expenses.")
    p.add_argument("-v", "--verbose", action="store_true", help="show log messages")
    sub = p.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="record an expense")
    add.add_argument("amount", type=float)
    add.add_argument("category")
    add.add_argument("note", nargs="?", default="")
    add.add_argument("--date", type=date.fromisoformat, default=None, help="YYYY-MM-DD")

    show = sub.add_parser("summary", help="totals for a month")
    show.add_argument("--month", default=date.today().strftime("%Y-%m"), help="YYYY-MM")

    rm = sub.add_parser("remove", help="delete an expense")
    rm.add_argument("id", type=int)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    service = BudgetService(SqliteExpenseRepository(os.environ.get("BUDGET_DB", "budget.db")),
                            LIMITS)
    try:
        if args.command == "add":
            e = service.add_expense(args.amount, args.category, args.note, args.date)
            print(f"#{e.id}  {e.spent_on}  {e.amount:>8.2f}  {e.category:<10} {e.note}")
        elif args.command == "summary":
            year, month = map(int, args.month.split("-"))
            s = service.summary(year, month)
            print(f"{s.year}-{s.month:02d}: total {s.total:.2f}")
            for cat, amount in s.by_category.items():
                flag = "  <- over budget!" if cat in s.over_budget else ""
                print(f"  {cat:<10} {amount:>8.2f}{flag}")
        elif args.command == "remove":
            service.remove(args.id)
            print(f"removed #{args.id}")
    except BudgetError as e:
        print(f"error: {e}")
        return 1
    return 0
