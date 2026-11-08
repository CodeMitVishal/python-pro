"""Exercise 19 · Make it fast

Three functions return the RIGHT answers, but far too slowly on real data.
Rewrite each one so it gives the same result within the time budget.
Measure before and after! (Hint: think about the data structure first.)

  1. find_duplicates(items)       -> sorted list of values that appear more than once
  2. common_customers(a, b)       -> sorted list of customers in BOTH lists
  3. fib(n)                       -> the n-th Fibonacci number (n up to 300)

Run it to check your work:
    python exercises/ex19_make_it_fast.py

Stuck? Compare with solutions/ex19_make_it_fast.py
"""
import time


def find_duplicates(items):
    dupes = []
    for i, x in enumerate(items):
        if x in items[i + 1:] and x not in dupes:      # copies + scans the list every time
            dupes.append(x)
    return sorted(dupes)


def common_customers(a, b):
    return sorted([c for c in a if c in b])            # `in` on a list: O(len(b)) each time


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)     # recomputes the same values again and again


# --- Checks: do not change anything below this line ----------------------------------
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
    assert result == [7, 42], result
    assert t < 0.1, f"find_duplicates took {t:.2f} s (budget 0.1 s)"

    a = [f"c{i}" for i in range(0, 40_000, 2)]
    b = [f"c{i}" for i in range(0, 40_000, 3)]
    result, t = _timed(common_customers, a, b)
    assert len(result) == 6667
    assert t < 0.1, f"common_customers took {t:.2f} s (budget 0.1 s)"

    _, t = _timed(fib, 30)                 # a quick probe first: the slow version takes ~1 s here
    assert t < 0.1, f"fib(30) took {t:.2f} s: stop recomputing the same values"
    result, t = _timed(fib, 300)
    assert result == 222232244629420445529739893461909967206666939096499764990979600
    assert t < 0.1, f"fib(300) took too long"
    print("All checks passed!")
