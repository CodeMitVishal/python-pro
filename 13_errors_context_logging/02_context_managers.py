"""Module 13 · Context managers: guaranteed setup and clean-up

    with thing as x:      ->  x = thing.__enter__()
        body                  try: body
                              finally: thing.__exit__(...)   # ALWAYS runs

Files, locks, database transactions, timers, temporary settings... anything
that must be "undone" afterwards, even if the body crashes.

TEACHING NOTES
  Why it matters  Files, DB transactions and locks must be released even when errors happen.
  Picture it      A door that closes itself: whatever happens in the room, it shuts when you
                  leave.
  Watch out       Put teardown in finally (or after yield inside try/finally) so it always runs.
  In real jobs    transaction.atomic(), open(), requests.Session(), temporary settings in tests.
  Interview       Q: What is a context manager?
                  A: An object with __enter__/__exit__ that guarantees setup and cleanup around
                     a with block.

Run it:  python 13_errors_context_logging/02_context_managers.py
"""
import os
import tempfile
import time
from contextlib import contextmanager, suppress
from pathlib import Path


# --- 1. A context manager as a class ------------------------------------------------
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self                         # this becomes the "as" variable

    def __exit__(self, exc_type, exc, tb):
        self.ms = (time.perf_counter() - self.start) * 1000
        print(f"[timer] block took {self.ms:.1f} ms")
        return False                        # False = don't swallow exceptions


with Timer() as t:
    sum(range(1_000_000))
print(f"measured: {t.ms > 0}")              # True


# --- 2. The same idea with @contextmanager: code before yield = enter, after = exit ---
@contextmanager
def working_directory(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield path                          # the body of the with-block runs here
    finally:
        os.chdir(old)                       # restored even if the body raises


with tempfile.TemporaryDirectory() as tmp:   # a built-in context manager
    with working_directory(tmp):
        Path("notes.txt").write_text("hi")  # written inside the temp folder
        print("inside:", sorted(os.listdir(".")))   # ['notes.txt']
    print("back home:", os.getcwd() != tmp)          # True
# the temp folder and notes.txt are deleted automatically here


# --- 3. Clean-up runs even when the block fails ------------------------------------------
@contextmanager
def transaction(log):
    log.append("BEGIN")
    try:
        yield
        log.append("COMMIT")
    except Exception:
        log.append("ROLLBACK")
        raise                               # re-raise so the caller still sees the error


log = []
try:
    with transaction(log):
        raise ValueError("bad row")
except ValueError:
    pass
print(log)                                  # ['BEGIN', 'ROLLBACK']


# --- 4. contextlib.suppress: ignore one specific, expected error --------------------------
with suppress(FileNotFoundError):
    os.remove("does_not_exist.tmp")         # no try/except/pass needed
print("still running")
