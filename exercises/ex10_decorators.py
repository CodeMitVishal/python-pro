"""Exercise 10 · Write your own decorators

Fill in the three decorators. Each one must work on ANY function
(use *args and **kwargs) and keep the original name (use functools.wraps).

  1. count_calls       -> store how many times the function was called
                          in an attribute: func.calls
  2. require_positive  -> raise ValueError if ANY positional number is < 0
  3. memoize           -> remember results in a dict keyed by args
                          (don't use lru_cache, build it yourself!)

Run it to check your work:
    python exercises/ex10_decorators.py

Stuck? Compare with solutions/ex10_decorators.py
"""
import functools


def count_calls(func):
    """TODO 1"""
    return func


def require_positive(func):
    """TODO 2"""
    return func


def memoize(func):
    """TODO 3"""
    return func


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    @count_calls
    def hello():
        return "hi"

    hello(); hello(); hello()
    assert hello.calls == 3, "hello.calls should be 3"
    assert hello.__name__ == "hello", "use functools.wraps"

    @require_positive
    def area(w, h):
        return w * h

    assert area(2, 3) == 6
    try:
        area(-2, 3)
        raise AssertionError("area(-2, 3) should raise ValueError")
    except ValueError:
        pass

    runs = []

    @memoize
    def slow_square(n):
        runs.append(n)
        return n * n

    assert slow_square(4) == 16 and slow_square(4) == 16
    assert runs == [4], "the second call must come from the cache"
    print("All checks passed!")
