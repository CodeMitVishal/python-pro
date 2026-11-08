"""REST API (Module 18): the same service, exposed over HTTP.

Run:  uvicorn budget.api:app --reload      then open http://127.0.0.1:8000/docs
"""
import os
from datetime import date
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from budget.repository import SqliteExpenseRepository
from budget.service import BudgetError, BudgetService

app = FastAPI(title="Budget API", version="1.0.0")
_service = BudgetService(SqliteExpenseRepository(os.environ.get("BUDGET_DB", ":memory:")),
                         {"food": 400.0, "fun": 150.0})


def get_service() -> BudgetService:
    """A FastAPI dependency: tests override it with a fresh in-memory service."""
    return _service


Service = Annotated[BudgetService, Depends(get_service)]   # FastAPI injects it per request


class ExpenseIn(BaseModel):
    amount: float = Field(gt=0)
    category: str
    note: str = ""
    spent_on: date | None = None


class ExpenseOut(BaseModel):
    id: int
    amount: float
    category: str
    note: str
    spent_on: date


@app.post("/expenses", status_code=201)
def add_expense(body: ExpenseIn, service: Service) -> ExpenseOut:
    try:
        e = service.add_expense(body.amount, body.category, body.note, body.spent_on)
    except BudgetError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    assert e.id is not None
    return ExpenseOut(id=e.id, amount=e.amount, category=e.category, note=e.note,
                      spent_on=e.spent_on)


@app.get("/summary/{year}/{month}")
def summary(year: int, month: int, service: Service) -> dict[str, object]:
    s = service.summary(year, month)
    return {"total": s.total, "by_category": s.by_category, "over_budget": s.over_budget}


@app.delete("/expenses/{expense_id}", status_code=204)
def remove(expense_id: int, service: Service) -> None:
    try:
        service.remove(expense_id)
    except BudgetError as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
