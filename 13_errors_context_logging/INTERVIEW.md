# Module 13 · Interview questions (with answers)

Short answers you can say out loud, with code and the usual follow-up.

[← Module 13](README.md) · [Quiz](QUIZ.md)

---

### 1. Explain `try`/`except`/`else`/`finally`.

**Say:** `try` holds the risky code. `except` handles specific errors. `else` runs only if **no** exception happened, which keeps the success path out of the try block. `finally` **always** runs, even after a `return`, so it's used for cleanup.

---

### 2. Why is a bare `except:` (or `except Exception: pass`) bad?

**Say:** It hides real bugs (typos raise `NameError` too), and a bare `except` even catches `KeyboardInterrupt` and `SystemExit`. Errors disappear silently and data ends up wrong. Catch the narrowest exception you can handle, and log anything unexpected.

---

### 3. `Exception` vs `BaseException`?

**Say:** `BaseException` is the root. It also covers `KeyboardInterrupt`, `SystemExit` and `GeneratorExit`, which normally must not be caught. Your own exceptions inherit from `Exception`.

---

### 4. How do you design custom exceptions?

**Say:** One base class per app (`class ShopError(Exception)`) with specific subclasses (`OutOfStock`, `PaymentFailed`). Add useful attributes. Callers can then catch one specific error or the whole family. At the API boundary, map them to HTTP status codes in one exception handler.

---

### 5. What does `raise ... from e` do?

**Say:** It **chains** exceptions: the new error stores the original in `__cause__`, and the traceback shows both ("The above exception was the direct cause of..."). Use it when you translate a low-level error (ConnectionError) into a domain error (PaymentFailed). `raise X from None` hides the cause on purpose.

---

### 6. What is a context manager? How do you write one?

**Say:** An object with `__enter__` and `__exit__` used in a `with` block, which guarantees setup and cleanup even when the block raises. The quickest way to write one is `@contextlib.contextmanager`:

```python
@contextmanager
def transaction(conn):
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
```

**Follow-up:** *"What does it mean if `__exit__` returns True?"* The exception is suppressed. That's rarely what you want (`contextlib.suppress` does it on purpose).

---

### 7. How do you manage a variable number of resources?

**Say:** `contextlib.ExitStack`. Call `enter_context()` for each file or connection opened in a loop, and they're all closed in reverse order, even if one fails.

---

### 8. Why logging instead of `print()`?

**Say:** Logging gives levels (filter noise in production), timestamps, module names, and handlers (file, stdout, a JSON log service). It can be configured without touching code, and `log.exception()` includes the traceback. Use `logging.getLogger(__name__)` per module and pass arguments lazily: `log.info("order %s", oid)`.

---

### 9. What are the log levels, and what goes where?

**Say:**
- **DEBUG**: details for developers.
- **INFO**: normal business events (order placed).
- **WARNING**: something odd but handled (retrying).
- **ERROR**: an operation failed.
- **CRITICAL**: the app can't continue.

Production usually runs at INFO.

---

### 10. How do you debug a problem in Python?

**Say:**
1. Read the traceback **bottom-up**.
2. Reproduce the problem with a failing test.
3. Use `breakpoint()` or the IDE debugger to inspect values (`n`, `s`, `c`, `p`).
4. For crashes, use post-mortem `python -m pdb`.
5. In production, rely on logs with context (request ID, user ID) and error tracking (Sentry).

Then add a test so the bug never comes back.

---

### 11. What are exception groups and `except*`? (3.11+)

**Say:** An `ExceptionGroup` carries **several** exceptions at once, e.g. from `asyncio.TaskGroup` when several tasks fail. `except* ValueError:` handles the matching ones and lets the rest continue up the stack.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
