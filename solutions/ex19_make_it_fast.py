"""Solution · Exercise 19: Make it fast

All three fixes are about the right data structure or not repeating work,
not about micro-tricks.

Run it:  python solutions/ex19_make_it_fast.py
"""
import time
from collections import Counter
from functools import lru_cache


def find_duplicates(items):
    # O(n): count everything once, keep values seen more than once
    return sorted(x for x, n in Counter(items).items() if n > 1)


def common_customers(a, b):
    # O(len(a) + len(b)): set intersection uses hashing
    return sorted(set(a) & set(b))


@lru_cache(maxsize=None)
def fib(n):
    # each fib(k) is computed once, then served from the cache: O(n)
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def _timed(func, *args):
    start = time.perf_counter()
    result = func(*args)
    return result, time.perf_counter() - start


if __name__ == "__main__":
    assert find_duplicates([3, 1, 3, 2, 1]) == [1, 3]
    assert common_customers(["a", "b", "c"], ["c", "a", "x"]) == ["a", "c"]
    assert fib(10) == 55

    big = list(range(15_000)) + [42, 7, 42]
    result, t = _timed(find_duplicates, big)
    assert result == [7, 42] and t < 0.1

    a = [f"c{i}" for i in range(0, 40_000, 2)]
    b = [f"c{i}" for i in range(0, 40_000, 3)]
    result, t = _timed(common_customers, a, b)
    assert len(result) == 6667 and t < 0.1

    _, t = _timed(fib, 30)                 # a quick probe first: the slow version takes ~1 s here
    assert t < 0.1, f"fib(30) took {t:.2f} s: stop recomputing the same values"
    result, t = _timed(fib, 300)
    assert result == 222232244629420445529739893461909967206666939096499764990979600 and t < 0.1
    print("All checks passed!")
