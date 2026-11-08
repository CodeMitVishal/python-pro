"""Module 10 · functools: ready-made function tools

  lru_cache / cache -> remember results (memoization)
  partial           -> pre-fill arguments            (see lesson 03)
  reduce            -> fold a list into one value
  wraps             -> keep names in decorators      (see lesson 04)
  singledispatch    -> one function, different code per argument type

Run it:  python 10_advanced_functions/05_functools.py
"""
import time
from functools import lru_cache, reduce, singledispatch

# --- 1. Memoization: the slow way ------------------------------------------------
def fib_slow(n):
    return n if n < 2 else fib_slow(n - 1) + fib_slow(n - 2)

start = time.perf_counter()
print(fib_slow(28))                                  # 317811
print(f"no cache:   {time.perf_counter() - start:.3f} s")   # recomputes the same values millions of times

# --- 2. lru_cache remembers every result it has computed ---------------------------
@lru_cache(maxsize=None)          # maxsize=None = unlimited (same as @functools.cache)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

start = time.perf_counter()
print(fib(28))                                       # 317811
print(f"with cache: {time.perf_counter() - start:.6f} s")
print(fib(200))                                      # instant, even for huge n
print(fib.cache_info())           # hits, misses, size: see the cache working
# Only cache PURE functions: same input -> same output, no side effects.

# --- 3. reduce: combine a list into ONE value, step by step --------------------------
nums = [1, 2, 3, 4, 5]
product = reduce(lambda acc, n: acc * n, nums)       # ((((1*2)*3)*4)*5)
print(product)                                       # 120
# For sums use sum(), for joining use "".join(): they're clearer than reduce.

# --- 4. singledispatch: pick the implementation by the type of the first argument ---
@singledispatch
def describe(value):
    return f"something: {value!r}"

@describe.register
def _(value: int):
    return f"an int, doubled is {value * 2}"

@describe.register
def _(value: list):
    return f"a list with {len(value)} items"

print(describe(21))               # an int, doubled is 42
print(describe([1, 2]))           # a list with 2 items
print(describe("hi"))             # something: 'hi'
