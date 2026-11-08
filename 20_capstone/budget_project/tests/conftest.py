import pytest

from budget.repository import SqliteExpenseRepository
from budget.service import BudgetService


@pytest.fixture
def service() -> BudgetService:
    """A fresh, isolated service with an in-memory database for every test."""
    return BudgetService(SqliteExpenseRepository(":memory:"), {"food": 100.0})
