"""Module 13 · ExitStack and exception groups

1. contextlib.ExitStack: enter a VARIABLE number of context managers and
   guarantee every one of them is cleaned up (e.g. open N files, N connections).
2. ExceptionGroup + except* (Python 3.11+): report SEVERAL errors at once,
   e.g. when validating a whole form or when several concurrent tasks fail.

TEACHING NOTES
  Why it matters  Sometimes you open a variable number of resources, or several tasks fail at
                  once.
  Picture it      ExitStack is a stack of open doors that it closes in reverse; an
                  ExceptionGroup is a bundle of errors.
  Watch out       except* handles parts of a group; plain except can't match inside a group.
  In real jobs    Opening many files or connections; asyncio.TaskGroup raises ExceptionGroup.
  Interview       Q: What are exception groups?
                  A: ExceptionGroup carries several exceptions (e.g. from TaskGroup); except*
                     handles matching ones.

Run it:  python 13_errors_context_logging/05_exitstack_and_groups.py
"""
import tempfile
from contextlib import ExitStack
from pathlib import Path

# --- 1. ExitStack: open however many files you need, close them all ------------------------
folder = Path(tempfile.mkdtemp())
names = ["jan.csv", "feb.csv", "mar.csv"]
for n in names:
    (folder / n).write_text(f"report {n}\n")

with ExitStack() as stack:
    files = [stack.enter_context(open(folder / n)) for n in names]   # 3 files, one `with`
    print([f.readline().strip() for f in files])
    stack.callback(print, "cleanup callback ran")                    # any function, too
print("all closed:", all(f.closed for f in files))


# --- 2. ExceptionGroup: several errors in one go --------------------------------------------------
def validate_signup(data: dict) -> None:
    errors: list[Exception] = []
    if "@" not in data.get("email", ""):
        errors.append(ValueError("email is invalid"))
    if len(data.get("password", "")) < 10:
        errors.append(ValueError("password is too short"))
    if data.get("age", 0) < 13:
        errors.append(PermissionError("too young to sign up"))
    if errors:
        raise ExceptionGroup("signup failed", errors)


try:
    validate_signup({"email": "nope", "password": "123", "age": 9})
except* ValueError as group:                 # handles ALL the ValueErrors in the group
    for e in group.exceptions:
        print("fix this field:", e)
except* PermissionError as group:            # ...and, separately, the PermissionErrors
    print("blocked:", group.exceptions[0])

# asyncio.TaskGroup (Module 17) raises an ExceptionGroup when several tasks fail.
