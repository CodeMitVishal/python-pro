"""Module 15 · Code quality: linting and formatting with ruff

  LINTER    finds likely bugs (unused imports, == None, bare except...)
  FORMATTER rewrites layout (spaces, quotes, line breaks) so everyone's code looks the same

ruff does both, extremely fast:
    pip install ruff
    ruff check 15_typing_quality/04_ruff_and_style.py          <- list the problems
    ruff check --fix 15_typing_quality/04_ruff_and_style.py    <- fix the safe ones
    ruff format --diff 15_typing_quality/04_ruff_and_style.py  <- preview the formatting

The function below WORKS but is deliberately messy. Run ruff on it and compare
with the clean version underneath.

Run it:  python 15_typing_quality/04_ruff_and_style.py
"""
import os, sys          # E401: two imports on one line; F401: both unused
import json


def messy_total( items ,discount = None ):
    total=0
    for i in range(len(items)):
        if items[i]["price"] == None:             # E711: comparison to None
            continue
        total+=items[i]["price"]*items[i]["qty"]
    if discount != None:
        total = total-total*discount
    try:
        return round(total,2)
    except:                                       # E722: bare except
        return 0


def clean_total(items: list[dict], discount: float | None = None) -> float:
    """Sum price * qty for every item with a price, then apply an optional discount."""
    priced = [item for item in items if item["price"] is not None]
    total = sum(item["price"] * item["qty"] for item in priced)
    if discount is not None:
        total *= 1 - discount
    return round(total, 2)


cart = [{"price": 10.0, "qty": 2}, {"price": None, "qty": 1}, {"price": 5.5, "qty": 1}]
print(messy_total(cart, 0.1), clean_total(cart, 0.1))     # 22.95 22.95
print(json.dumps({"same_result": messy_total(cart) == clean_total(cart)}))

# Good habits that tools can't enforce:
#  - names that say what things ARE: `unpaid_invoices`, not `lst2`
#  - small functions that do one thing
#  - docstrings on public functions: what it does, not how
#  - comments explain WHY, the code already says WHAT
