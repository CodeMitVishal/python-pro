"""Module 10 · Recursion: a function that calls itself

Every recursive function has two parts:
  BASE CASE      -> the smallest problem, answered directly (this STOPS the recursion)
  RECURSIVE CASE -> shrink the problem and call yourself on the smaller piece

Each call gets its own frame on the CALL STACK (Module 6 memory slides). The
frames pile up until the base case, then unwind one by one.

TEACHING NOTES
  Why it matters  Nested data (folders, JSON, comment threads) is naturally solved by a function
                  that calls itself.
  Picture it      Russian dolls: open one, find a smaller one, until the smallest can't be
                  opened (the base case).
  Watch out       Every recursion needs a base case; Python stops at about 1000 levels with
                  RecursionError.
  In real jobs    Walking JSON/trees, category menus, permission hierarchies; DFS in graphs.
  Interview       Q: Recursion or a loop?
                  A: Recursion fits nested data and is clear; for very deep data use a loop with
                     an explicit stack.

Run it:  python 10_advanced_functions/07_recursion.py
"""
import sys
from functools import lru_cache


# --- 1. The classic: factorial, with the call stack made visible ---------------------------
def factorial(n: int, depth: int = 0) -> int:
    print("  " * depth + f"factorial({n})")
    if n <= 1:                                  # base case
        return 1
    return n * factorial(n - 1, depth + 1)      # recursive case: a smaller problem


print("result:", factorial(4))


# --- 2. Recursion shines on NESTED data: folders, JSON, comment threads, trees ----------------
folder = {"name": "project", "size": 0, "children": [
    {"name": "README.md", "size": 4, "children": []},
    {"name": "src", "size": 0, "children": [
        {"name": "app.py", "size": 12, "children": []},
        {"name": "utils", "size": 0, "children": [{"name": "math.py", "size": 3, "children": []}]},
    ]},
]}


def total_size(node: dict) -> int:
    return node["size"] + sum(total_size(child) for child in node["children"])


def show(node: dict, indent: int = 0) -> None:
    print("  " * indent + node["name"] + ("/" if node["children"] else ""))
    for child in node["children"]:
        show(child, indent + 1)


show(folder)
print("total size:", total_size(folder), "KB")


# --- 3. Divide and conquer: binary search, recursively --------------------------------------------
def binary_search(items: list[int], target: int, lo: int = 0, hi: int | None = None) -> int:
    hi = len(items) - 1 if hi is None else hi
    if lo > hi:
        return -1                                # base case: not found
    mid = (lo + hi) // 2
    if items[mid] == target:
        return mid                               # base case: found
    if items[mid] < target:
        return binary_search(items, target, mid + 1, hi)   # search the right half
    return binary_search(items, target, lo, mid - 1)       # search the left half


print("index of 42:", binary_search(list(range(0, 100, 2)), 42))   # 21


# --- 4. Overlapping subproblems: memoize, or it explodes ---------------------------------------------
calls = 0


def fib(n: int) -> int:
    global calls
    calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)


fib(25)
print(f"fib(25) without memo: {calls:,} calls")


@lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)


fib_memo(25)
print(f"fib(25) with memo:    {fib_memo.cache_info().misses} calls")


# --- 5. The limit: Python stops at ~1000 frames (it has no tail-call optimisation) --------------------
print("recursion limit:", sys.getrecursionlimit())
try:
    def count_down(n): return 0 if n == 0 else count_down(n - 1)
    count_down(5000)
except RecursionError as e:
    print("RecursionError:", e)


def count_down_loop(n: int) -> int:             # the fix: deep recursion -> a loop
    while n > 0:
        n -= 1
    return n


print("loop version handles 5000 easily:", count_down_loop(5000))
# Rule: use recursion for naturally nested problems (trees, divide and conquer);
# use a loop when the depth could be large.
