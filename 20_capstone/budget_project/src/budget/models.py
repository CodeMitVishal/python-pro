"""Domain models: plain data, no database or web code (Module 9 dataclasses + Module 15 typing)."""
from dataclasses import dataclass
from datetime import date
from typing import Literal, get_args

Category = Literal["food", "rent", "transport", "fun", "other"]
CATEGORIES: tuple[str, ...] = get_args(Category)


@dataclass(frozen=True)
class Expense:
    id: int | None          # None until the repository saves it
    amount: float
    category: Category
    note: str
    spent_on: date
