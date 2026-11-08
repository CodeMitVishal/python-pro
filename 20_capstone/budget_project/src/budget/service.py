"""Business rules: validation, summaries, budget alerts.

No SQL, no HTTP, no printing here, so this is the easiest code to test and the
code that both the CLI and the API share.
"""
import logging
from collections import defaultdict
from dataclasses import dataclass
from datetime import date

from budget.models import CATEGORIES, Category, Expense
from budget.repository import ExpenseRepository

log = logging.getLogger(__name__)


class BudgetError(Exception):
    """Raised for invalid input, so callers can show a friendly message."""


@dataclass(frozen=True)
class MonthSummary:
    year: int
    month: int
    total: float
    by_category: dict[str, float]
    over_budget: list[str]


class BudgetService:
    def __init__(self, repo: ExpenseRepository, limits: dict[str, float] | None = None) -> None:
        self.repo = repo                       # injected: real SQLite, or a fake in tests
        self.limits = limits or {}

    def add_expense(self, amount: float, category: str, note: str = "",
                    spent_on: date | None = None) -> Expense:
        if amount <= 0:
            raise BudgetError("amount must be positive")
        if category not in CATEGORIES:
            raise BudgetError(f"unknown category {category!r}, use one of: {', '.join(CATEGORIES)}")
        cat: Category = category  # type: ignore[assignment]   # checked just above
        expense = self.repo.add(Expense(None, round(amount, 2), cat, note.strip(),
                                        spent_on or date.today()))
        log.info("added expense #%s: %.2f %s", expense.id, expense.amount, expense.category)
        return expense

    def summary(self, year: int, month: int) -> MonthSummary:
        totals: dict[str, float] = defaultdict(float)
        for e in self.repo.list_month(year, month):
            totals[e.category] += e.amount
        by_category = {c: round(v, 2) for c, v in sorted(totals.items(), key=lambda kv: -kv[1])}
        over = [c for c, limit in self.limits.items() if by_category.get(c, 0) > limit]
        if over:
            log.warning("over budget in %s", ", ".join(over))
        return MonthSummary(year, month, round(sum(by_category.values()), 2), by_category, over)

    def remove(self, expense_id: int) -> None:
        if not self.repo.delete(expense_id):
            raise BudgetError(f"no expense with id {expense_id}")
