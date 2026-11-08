"""Module 15 · mypy: find bugs WITHOUT running the code

This file runs without errors... today. But it hides 3 bugs that will crash
in production with the "wrong" data. mypy finds all of them in a second.

Run it:          python 15_typing_quality/03_mypy_catches_bugs.py
Then check it:   pip install mypy
                 mypy 15_typing_quality/03_mypy_catches_bugs.py

Expected mypy output (3 errors):
  error: Item "None" of "dict[str, Any] | None" has no attribute "get"   [union-attr]
  error: Unsupported operand types for + ("str" and "int")               [operator]
  error: Argument 1 to "send_invoice" has incompatible type "float"; expected "str"  [arg-type]
"""
from typing import Any

USERS: dict[int, dict[str, Any]] = {1: {"name": "Vishal", "plan": "pro"}}


def find_user(user_id: int) -> dict[str, Any] | None:
    return USERS.get(user_id)


def plan_of(user_id: int) -> str:
    user = find_user(user_id)
    return user.get("plan", "free")        # BUG 1: user can be None -> AttributeError for id 2


def label(count: int) -> str:
    if count > 100:
        return "Orders: " + count          # BUG 2: str + int -> TypeError, but only if count > 100
    return f"Orders: {count}"


def send_invoice(email: str) -> None:
    print(f"invoice sent to {email}")


def bill(total: float) -> None:
    send_invoice(total)                    # BUG 3: wrong argument (meant the user's email)


print(plan_of(1))          # pro          <- works with the data we tried...
print(label(5))            # Orders: 5
bill(19.99)                # invoice sent to 19.99   <- "works", but is nonsense
# plan_of(2) or label(500) would crash. mypy finds these without running anything.
