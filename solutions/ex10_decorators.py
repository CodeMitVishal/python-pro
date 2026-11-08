"""Solution · Exercise 10: Write your own decorators

Run it:  python solutions/ex10_decorators.py
"""
import functools


def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1               # functions are objects: they can hold attributes
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


def require_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if any(isinstance(a, (int, float)) and a < 0 for a in args):
            raise ValueError(f"{func.__name__}() needs positive numbers, got {args}")
        return func(*args, **kwargs)
    return wrapper


def memoize(func):
    cache = {}                           # lives in the closure, shared by all calls

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:            # args is a tuple, so it can be a dict key
            cache[args] = func(*args)
        return cache[args]
    return wrapper


if __name__ == "__main__":
    @count_calls
    def hello():
        return "hi"

    hello(); hello(); hello()
    assert hello.calls == 3
    assert hello.__name__ == "hello"

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
    assert runs == [4]
    print("All checks passed!")
