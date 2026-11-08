# Module 10 · Interview questions (with answers)

These are the questions interviewers really ask about functions. Each one has a short answer you can say out loud, a code sample, and the follow-up question that usually comes next.

[← Module 10](README.md) · [Quiz](QUIZ.md)

---

### 1. What are `*args` and `**kwargs`?

**Say:** `*args` collects extra **positional** arguments into a tuple. `**kwargs` collects extra **keyword** arguments into a dict. I use them in wrappers and decorators to pass every argument through unchanged.

```python
def log_call(*args, **kwargs):
    print(args, kwargs)

log_call(1, 2, user="vishal")   # (1, 2) {'user': 'vishal'}
```

**Follow-up:** *"What does a bare `*` in a signature mean?"* Everything after it is **keyword-only**: `def connect(host, *, timeout=5)` forces `timeout=` to be written by name.

---

### 2. What is the mutable default argument trap?

**Say:** Default values are created **once**, when the function is defined. A default `[]` or `{}` is shared by every call, so it keeps growing. Use `None` and create the list inside.

```python
def add_tag(tag, tags=None):     # not tags=[]
    tags = [] if tags is None else tags
    tags.append(tag)
    return tags
```

---

### 3. What is a closure?

**Say:** An inner function that **remembers variables from its enclosing function**, even after that function has returned. Python keeps them in cells (`func.__closure__`). To **change** such a variable you need `nonlocal`.

```python
def make_counter():
    count = 0
    def next_number():
        nonlocal count
        count += 1
        return count
    return next_number
```

**Follow-up:** *"Closure or class?"* A closure suits one or two values. When there's more state or there are several methods, use a class.

---

### 4. Explain LEGB.

**Say:** It's the order Python looks up a name: **L**ocal, **E**nclosing function, **G**lobal (module), **B**uilt-in. The first match wins. Assigning to a name makes it local unless you declare it `global` or `nonlocal`.

---

### 5. Why does `[lambda: i for i in range(3)]` return `[2, 2, 2]`?

**Say:** It's **late binding**. Each lambda remembers the **variable** `i`, not its value. By the time you call them, the loop has finished and `i` is 2. Fix it with a default argument, `lambda i=i: i`, which is evaluated right away.

---

### 6. What is a decorator? Write one.

**Say:** A function that **takes a function and returns a new function** with extra behaviour. `@timer` above a `def` is just `f = timer(f)`. The wrapper is a closure. I always add `functools.wraps`.

```python
import functools, time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__}: {time.perf_counter() - start:.3f}s")
    return wrapper
```

**Follow-up:** *"Why `functools.wraps`?"* Without it, every decorated function is called `wrapper` and loses its docstring and signature. That breaks logs, debugging, docs and frameworks that inspect signatures, such as FastAPI and pytest.

---

### 7. Write a decorator that takes arguments, e.g. `@retry(times=3)`.

**Say:** It needs **three levels**: the outer function takes the settings, returns a decorator that takes the function, which returns the wrapper that runs on each call.

```python
def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    if attempt == times:
                        raise
        return wrapper
    return decorator
```

**Follow-up:** *"What would you add for production?"* Exponential backoff with jitter, retrying only on **transient** errors, logging every attempt, and a maximum total time.

---

### 8. In which order do stacked decorators run?

**Say:** They **apply bottom-up** and **run top-down**. With `@a` above `@b` above `def f`, Python builds `f = a(b(f))`. When you call `f`, `a`'s wrapper runs first, then `b`'s, then `f`.

---

### 9. Where have you used decorators in real projects?

**Say:** Routes (`@app.get` in FastAPI/Flask), auth (`@login_required` in Django), caching (`@lru_cache`, `@cache`), test setup (`@pytest.fixture`), `@property` and `@classmethod` in classes, and my own `@timer`/`@retry` around external API calls.

---

### 10. What does `functools.lru_cache` do, and when is it dangerous?

**Say:** It **memoises**: it stores results keyed by the arguments, so a repeated call returns instantly. The arguments must be **hashable**. It's dangerous when the result can change (database data, the current time) because you'd serve stale values. It's also dangerous on methods, where it keeps `self` alive (a memory leak).

```python
@functools.lru_cache(maxsize=1024)
def fib(n): return n if n < 2 else fib(n - 1) + fib(n - 2)
```

---

### 11. What is recursion, and what are its limits in Python?

**Say:** A function that calls itself on a **smaller** problem until it hits a **base case**. Python has **no tail-call optimisation** and a default recursion limit of about 1000 frames, so very deep recursion raises `RecursionError`. For deep data, I use a loop with an explicit stack.

---

### 12. What does "functions are first-class objects" mean?

**Say:** A function is a normal object. You can store it in a variable, a list or a dict, pass it as an argument (`sorted(users, key=get_age)`), and return it from another function. That's what makes callbacks, decorators and dispatch tables possible.

```python
HANDLERS = {"csv": read_csv, "json": read_json}
data = HANDLERS[file_type](path)     # pick behaviour at runtime
```

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
