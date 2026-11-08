"""Module 15 · Generic classes, typed decorators and @overload

1. Generic[T] classes: one container class, precisely typed for whatever it holds
2. ParamSpec: decorators that KEEP the wrapped function's signature for mypy
3. @overload: different return types depending on the arguments

Check it:  mypy 15_typing_quality/05_generics_and_typed_decorators.py

TEACHING NOTES
  Why it matters  Reusable containers and decorators lose type information unless you use
                  generics.
  Picture it      A TypeVar is a placeholder: whatever type goes in, the same type comes out.
  Watch out       Decorators without ParamSpec erase the wrapped function's signature for type
                  checkers.
  In real jobs    Generic Repository[T], Page[T] responses, typed decorators in shared
                  libraries.
  Interview       Q: What is a TypeVar / generic?
                  A: A type placeholder linking inputs and outputs, e.g. def first(xs: list[T])
                     -> T.

Run it:    python 15_typing_quality/05_generics_and_typed_decorators.py
"""
import functools
import time
from collections.abc import Callable
from typing import Generic, ParamSpec, TypeVar, overload

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")


# --- 1. A generic class: Stack[int] holds ints, Stack[str] holds strs ---------------------------
class Stack(Generic[T]):                     # Python 3.12+: class Stack[T]: ...
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()


numbers: Stack[int] = Stack()
numbers.push(1)
numbers.push(2)
print(numbers.pop() + 10)                    # mypy knows pop() returns int
# numbers.push("three")  -> mypy: Argument 1 has incompatible type "str"; expected "int"


# --- 2. A typed decorator: ParamSpec keeps the parameters, R keeps the return type ----------------
def timed(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"[timed] {func.__name__}: {(time.perf_counter() - start) * 1000:.2f} ms")
    return wrapper


@timed
def greet(name: str, excited: bool = False) -> str:
    return f"Hello, {name}{'!' if excited else '.'}"


print(greet("Vishal", excited=True).upper())   # mypy still knows: (str, bool) -> str
# greet(42) -> mypy error, because the decorator kept the real signature
# (without ParamSpec, decorated functions become "(*Any, **Any) -> Any" and lose all checking)


# --- 3. @overload: the return type depends on the argument type -----------------------------------
@overload
def parse(value: str) -> int: ...
@overload
def parse(value: list[str]) -> list[int]: ...
def parse(value: str | list[str]) -> int | list[int]:
    if isinstance(value, str):
        return int(value)
    return [int(v) for v in value]


total: int = parse("41") + 1                 # mypy knows this is an int
items: list[int] = parse(["1", "2"])         # ...and this is a list[int]
print(total, items)
