"""Data access: the ONLY module that knows about SQL (Module 18 repository pattern).

The service talks to the ExpenseRepository Protocol, so tests or a future
PostgreSQL version can swap in another implementation (Module 12, dependency inversion).
"""
import sqlite3
from datetime import date
from typing import Protocol

from budget.models import Expense


class ExpenseRepository(Protocol):
    def add(self, expense: Expense) -> Expense: ...
    def list_month(self, year: int, month: int) -> list[Expense]: ...
    def delete(self, expense_id: int) -> bool: ...


class SqliteExpenseRepository:
    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        with self.conn:
            self.conn.execute(
                """CREATE TABLE IF NOT EXISTS expenses (
                       id       INTEGER PRIMARY KEY,
                       amount   REAL NOT NULL CHECK (amount > 0),
                       category TEXT NOT NULL,
                       note     TEXT NOT NULL DEFAULT '',
                       spent_on TEXT NOT NULL            -- ISO date: YYYY-MM-DD
                   )"""
            )

    def add(self, expense: Expense) -> Expense:
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO expenses (amount, category, note, spent_on) VALUES (?, ?, ?, ?)",
                (expense.amount, expense.category, expense.note, expense.spent_on.isoformat()),
            )
        return Expense(cur.lastrowid, expense.amount, expense.category, expense.note,
                       expense.spent_on)

    def list_month(self, year: int, month: int) -> list[Expense]:
        prefix = f"{year:04d}-{month:02d}-%"
        rows = self.conn.execute(
            "SELECT * FROM expenses WHERE spent_on LIKE ? ORDER BY spent_on, id", (prefix,)
        )
        return [
            Expense(r["id"], r["amount"], r["category"], r["note"],
                    date.fromisoformat(r["spent_on"]))
            for r in rows
        ]

    def delete(self, expense_id: int) -> bool:
        with self.conn:
            cur = self.conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        return cur.rowcount > 0
