"""Module 15 · Type hints: say what your code expects

Type hints are labels: "this parameter is a str, this returns a float".
Python does NOT check them at runtime. Tools do:
  - your editor (autocomplete, red squiggles)
  - mypy (finds bugs before you run anything)  -> lesson 03
They're also documentation that can never go out of date.

TEACHING NOTES
  Why it matters  The classic None bug ('NoneType has no attribute...') is caught before running
                  when functions have hints.
  Picture it      Type hints are labels on boxes: they say what should go in and what comes out.
  Watch out       Hints are NOT checked at runtime; run mypy (or pyright) to get the benefit.
  In real jobs    FastAPI and Pydantic read hints to validate requests; mypy runs in CI.
  Interview       Q: Are type hints enforced in Python?
                  A: No; Python stores them but ignores them. Checkers like mypy and libraries
                     like Pydantic use them.

Run it:  python 15_typing_quality/01_type_hints_basics.py
"""

# --- 1. Variables and functions --------------------------------------------------
age: int = 30
name: str = "Vishal"

def greet(name: str, excited: bool = False) -> str:
    return f"Hello, {name}{'!' if excited else '.'}"

print(greet(name, excited=True))

# --- 2. Collections: say what's INSIDE (Python 3.9+ syntax) ---------------------------
scores: list[int] = [91, 78, 85]
prices: dict[str, float] = {"tea": 2.5}
point: tuple[int, int] = (3, 7)           # exactly two ints
tags: set[str] = {"python", "pro"}

def average(values: list[float]) -> float:
    return sum(values) / len(values)

print(average([1.0, 2.0, 4.5]))           # 2.5

# --- 3. "Might be None": X | None (Python 3.10+; older code says Optional[X]) ------------
def find_price(item: str) -> float | None:
    return prices.get(item)                # returns None when missing

price = find_price("coffee")
if price is not None:                      # mypy makes you handle the None case
    print(price * 2)
else:
    print("not on the menu")

# --- 4. Functions that return nothing ------------------------------------------------
def log(message: str) -> None:
    print(f"[log] {message}")

log("typed!")

# --- 5. Type aliases: give a long type a short name ------------------------------------
Matrix = list[list[float]]

def identity(n: int) -> Matrix:
    return [[1.0 if r == c else 0.0 for c in range(n)] for r in range(n)]

print(identity(2))                         # [[1.0, 0.0], [0.0, 1.0]]

# --- 6. Hints are NOT enforced at runtime ------------------------------------------------
print(greet(123))                          # runs fine: Hello, 123.  (mypy would complain)
print(greet.__annotations__)               # the hints are stored, just not checked
