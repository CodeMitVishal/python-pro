from datetime import date

import pytest

from budget.service import BudgetError, BudgetService

NOV = date(2026, 11, 5)


def test_add_expense_gets_an_id(service: BudgetService) -> None:
    e = service.add_expense(12.345, "food", "  lunch  ", NOV)
    assert e.id == 1
    assert e.amount == 12.35          # rounded to cents
    assert e.note == "lunch"          # trimmed


@pytest.mark.parametrize(("amount", "category"), [(0, "food"), (-5, "food"), (10, "pizza")])
def test_invalid_expenses_are_rejected(service: BudgetService, amount: float,
                                       category: str) -> None:
    with pytest.raises(BudgetError):
        service.add_expense(amount, category, spent_on=NOV)


def test_summary_groups_and_flags_over_budget(service: BudgetService) -> None:
    service.add_expense(80, "food", spent_on=NOV)
    service.add_expense(30, "food", spent_on=NOV)
    service.add_expense(500, "rent", spent_on=NOV)
    service.add_expense(999, "fun", spent_on=date(2026, 12, 1))   # other month: ignored
    s = service.summary(2026, 11)
    assert s.total == 610
    assert s.by_category == {"rent": 500, "food": 110}             # biggest first
    assert s.over_budget == ["food"]                               # limit is 100


def test_remove_unknown_id_raises(service: BudgetService) -> None:
    with pytest.raises(BudgetError, match="no expense"):
        service.remove(42)
