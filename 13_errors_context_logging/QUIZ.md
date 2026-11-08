# Python Pro – Module 13 Knowledge Check
**Errors, context managers & logging**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson file to revisit.

---

### Part A – Multiple choice

**1. Why give your custom exceptions a shared base class like `ShopError`?**
- A) It's required
- B) Callers can catch the whole family with one `except`
- C) It makes them faster
- D) It hides the error messages

**2. You have `except ShopError` before `except OutOfStock`. What happens to an `OutOfStock`?**
- A) The `OutOfStock` block handles it
- B) The `ShopError` block catches it first, so the specific block never runs
- C) Both run
- D) It isn't caught

**3. What does `raise NewError(...) from e` do?**
- A) Hides the original error
- B) Keeps the original error as the cause, so the traceback shows both
- C) Retries the code
- D) Converts `e` to a string

**4. Why is a bare `except:` dangerous?**
- A) It's slower
- B) It also catches `KeyboardInterrupt` and `SystemExit`, and hides bugs
- C) It only catches `ValueError`
- D) It isn't allowed

**5. What does "EAFP" mean?**
- A) Check everything with `if` first
- B) Try it, and handle the exception if it fails
- C) Never use exceptions
- D) Log every error

**6. Which methods make a class usable in a `with` statement?**
- A) `__init__` and `__del__`
- B) `__enter__` and `__exit__`
- C) `__open__` and `__close__`
- D) `__iter__` and `__next__`

**7. In a `@contextmanager` function, where does the body of the `with` block run?**
- A) Before the function starts
- B) At the `yield`
- C) After `return`
- D) In a separate thread

**8. What does `__exit__` returning `True` do?**
- A) Re-raises the exception
- B) Swallows the exception
- C) Logs the exception
- D) Nothing

**9. Which logging levels appear with `level=logging.WARNING`?**
- A) Only WARNING
- B) WARNING, ERROR and CRITICAL
- C) Everything
- D) DEBUG and INFO

**10. Why `log.info("user %s", name)` instead of an f-string?**
- A) f-strings don't work in logging
- B) The text is only built if the message is actually shown
- C) It's required syntax
- D) It encrypts the name

**11. Which call logs an error AND the full traceback?**
- A) `log.error()`
- B) `log.exception()` inside an `except` block
- C) `print()`
- D) `log.debug()`

---

### Part B – What's the output?

**12.**
```python
from contextlib import contextmanager

@contextmanager
def tag(name):
    print(f"<{name}>")
    yield
    print(f"</{name}>")

with tag("b"):
    print("hi")
```

**13.**
```python
from contextlib import suppress
with suppress(KeyError):
    {}["x"]
    print("A")
print("B")
```

---

### Part C – Fix it

**14.** The file stays open if `process()` raises. Fix it:
```python
f = open("data.txt")
process(f.read())
f.close()
```

**15.** This rollback context manager swallows every error silently. Fix it:
```python
@contextmanager
def atomic(db):
    snap = dict(db)
    try:
        yield
    except Exception:
        db.clear(); db.update(snap)
```

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | One `except ShopError` handles every child. | `01_exception_hierarchy.py` |
| 2 | B | Put the most specific `except` first. | `01_exception_hierarchy.py` |
| 3 | B | Exception chaining keeps `__cause__`. | `01_exception_hierarchy.py` |
| 4 | B | Catch specific exceptions instead. | `01_exception_hierarchy.py` |
| 5 | B | "Easier to ask forgiveness than permission." | `01_exception_hierarchy.py` |
| 6 | B | The context manager protocol. | `02_context_managers.py` |
| 7 | B | Before `yield` = enter, after = exit. | `02_context_managers.py` |
| 8 | B | Usually return False and let errors through. | `02_context_managers.py` |
| 9 | B | That level and everything above it. | `03_logging.py` |
| 10 | B | Lazy formatting. | `03_logging.py` |
| 11 | B | Level ERROR plus the traceback. | `03_logging.py` |
| 12 | `<b>`, `hi`, `</b>` | Enter, body, exit. | `02_context_managers.py` |
| 13 | `B` | The KeyError skips `print("A")` and is suppressed. | `02_context_managers.py` |
| 14 | `with open("data.txt") as f: process(f.read())` | `with` always closes the file. | `02_context_managers.py` |
| 15 | Add `raise` at the end of the `except` block. | Roll back, then re-raise. | `ex13_bank_transfer.py` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
