"""Module 15 · Advanced typing: precise types for real code

  Literal     -> only these exact values
  TypedDict   -> a dict with known keys (great for JSON)
  Callable    -> "a function that takes X and returns Y"
  TypeVar     -> generics: "whatever type goes in, comes out"
  Protocol    -> "anything with these methods" (Module 12)
  Final       -> a constant that must not be reassigned

TEACHING NOTES
  Why it matters  Real code passes dicts, callbacks and 'one of these strings'; precise types
                  catch mistakes there.
  Picture it      Literal is a fixed menu, TypedDict a form with known fields, Callable a
                  function-shaped hole.
  Watch out       Avoid Any: it switches checking off; prefer object, a Union, or a Protocol.
  In real jobs    Typed JSON payloads, sort-order parameters, callback signatures in libraries.
  Interview       Q: Any vs object?
                  A: Any disables checking; object accepts anything but allows almost nothing
                     until you narrow it.

Run it:  python 15_typing_quality/02_advanced_typing.py
"""
from typing import Callable, Final, Literal, TypedDict, TypeVar

# --- Literal: restrict to exact values ---------------------------------------------
Level = Literal["debug", "info", "error"]

def log(level: Level, msg: str) -> None:
    print(f"{level.upper()}: {msg}")

log("info", "server started")          # log("warn", ...) -> mypy error: not allowed

# --- TypedDict: the shape of a dict -----------------------------------------------
class User(TypedDict):
    name: str
    age: int
    email: str | None

def describe(u: User) -> str:
    return f"{u['name']} ({u['age']})"

print(describe({"name": "Vishal", "age": 30, "email": None}))
# describe({"name": "Raj"}) -> mypy error: missing keys "age", "email"

# --- Callable: functions as parameters ------------------------------------------
def apply(func: Callable[[float], float], values: list[float]) -> list[float]:
    return [func(v) for v in values]

print(apply(lambda v: v * 1.19, [10.0, 20.0]))

# --- TypeVar: generic functions --------------------------------------------------
T = TypeVar("T")

def first(items: list[T]) -> T:        # list[str] in -> str out, list[int] in -> int out
    return items[0]

name = first(["Vishal", "Raj"])        # mypy knows name is a str
print(name.upper())

# Python 3.12+ has a shorter syntax for the same thing:
#   def first[T](items: list[T]) -> T: ...

# --- Final: constants ---------------------------------------------------------------
MAX_RETRIES: Final = 3
# MAX_RETRIES = 5 -> mypy error: cannot assign to final name
print(f"retries: {MAX_RETRIES}")
