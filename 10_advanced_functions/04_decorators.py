"""Module 10 · Decorators, built step by step

A decorator is a function that takes a function and returns a NEW function
that adds behaviour before/after the original: timing, logging, caching,
retries, access checks...

    @timer                 is exactly the same as      slow_task = timer(slow_task)
    def slow_task(): ...

Run it:  python 10_advanced_functions/04_decorators.py
"""
import functools
import time

# --- Step 1: a wrapper by hand (closures + first-class functions) -----------------
def shout_result(func):
    def wrapper():
        return func().upper()
    return wrapper

def greet():
    return "hello"

greet = shout_result(greet)       # replace greet with the wrapped version
print(greet())                    # HELLO

# --- Step 2: the @ syntax does that assignment for you ---------------------------
@shout_result
def farewell():
    return "bye"

print(farewell())                 # BYE

# --- Step 3: a real decorator: any arguments + functools.wraps -------------------
def timer(func):
    @functools.wraps(func)        # keep the original name and docstring
    def wrapper(*args, **kwargs): # accept ANY arguments...
        start = time.perf_counter()
        result = func(*args, **kwargs)        # ...and pass them through
        ms = (time.perf_counter() - start) * 1000
        print(f"[timer] {func.__name__} took {ms:.1f} ms")
        return result             # never forget to return the result!
    return wrapper

@timer
def slow_add(a, b):
    """Add two numbers, slowly."""
    time.sleep(0.05)
    return a + b

print(slow_add(2, 3))             # [timer] slow_add took ~50 ms / 5
print(slow_add.__name__, "-", slow_add.__doc__)   # slow_add - Add two numbers, slowly.

# --- Step 4: a decorator WITH arguments = one more layer -------------------------
def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    print(f"[retry] attempt {attempt} failed: {e}")
            raise ConnectionError(f"gave up after {times} attempts")
        return wrapper
    return decorator

calls = {"n": 0}

@retry(times=3)
def flaky_download():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("timeout")
    return "data.csv downloaded"

print(flaky_download())           # 2 failures, then: data.csv downloaded

# --- Step 5: stacking: the decorator closest to def runs first --------------------
@timer
@retry(times=2)
def ping():
    return "pong"

print(ping())                     # timer wraps retry, which wraps ping
