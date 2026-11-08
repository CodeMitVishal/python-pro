"""Module 13 · Debugging like a pro

Beyond print(): the tools experienced developers reach for.

  1. pdb / breakpoint()       pause anywhere, inspect, step through
  2. post-mortem debugging    open the debugger AT the crash, after the fact
  3. traceback + logging      capture the full stack in production logs
  4. assert                   catch impossible states early (in dev and tests)
  5. faulthandler             tracebacks even when Python itself hangs or crashes
  6. VS Code launch.json      one click to debug a FastAPI server or pytest test

Run it:  python 13_errors_context_logging/06_debugging_like_a_pro.py
"""
import faulthandler
import logging
import sys
import traceback

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stdout)
log = logging.getLogger("debug-demo")

# --- 1. pdb cheat sheet (type these at the (Pdb) prompt) ---------------------------------------
PDB = """
  p expr / pp expr   print / pretty-print a value     l / ll   list code around / whole function
  n                  next line (step OVER calls)      s        step INTO a call
  c                  continue to the next breakpoint  r        run until this function returns
  w                  where: show the call stack       u / d    move up / down the stack
  b file.py:42       set a breakpoint                 b 42, x > 10   conditional breakpoint
  !x = 5             run any Python statement         q        quit
"""
print("pdb commands:" + PDB)
# breakpoint() opens pdb. PYTHONBREAKPOINT=0 disables every breakpoint() call (e.g. in CI).


# --- 2. Post-mortem: inspect the program AT the crash ---------------------------------------------
def parse_orders(lines):
    totals = []
    for line in lines:
        qty, price = line.split(",")
        totals.append(int(qty) * float(price))
    return totals


try:
    parse_orders(["2,9.99", "3,4.50", "oops"])
except ValueError:
    # In a terminal you'd now call:  import pdb; pdb.post_mortem()
    # -> it opens AT the failing line, with `line` still set to "oops".
    # Same from the command line:    python -m pdb script.py  (it stops when it crashes)
    tb = sys.exc_info()[2]
    while tb.tb_next:
        tb = tb.tb_next
    print("post-mortem view: crashed with line =", repr(tb.tb_frame.f_locals["line"]))


# --- 3. Production: log the full traceback, not just the message ------------------------------------
try:
    parse_orders(["1,x"])
except ValueError:
    log.exception("order import failed")         # ERROR + the whole stack, in your log system
    one_line = traceback.format_exc().strip().splitlines()[-1]
    print("short form for an alert:", one_line)


# --- 4. assert: document and check what MUST be true -----------------------------------------------------
def apply_discount(price, percent):
    assert 0 <= percent <= 100, f"percent out of range: {percent}"
    return price * (1 - percent / 100)


try:
    apply_discount(10, 150)
except AssertionError as e:
    print("assert caught a bug early:", e)
# Note: `python -O` removes asserts, so never use them to validate USER input (raise instead).

# --- 5. faulthandler: tracebacks for hangs and hard crashes -----------------------------------------------
faulthandler.enable()          # or: python -X faulthandler app.py
print("faulthandler enabled:", faulthandler.is_enabled())
# faulthandler.dump_traceback_later(30) prints every thread's stack if the app is stuck for 30 s.

# --- 6. VS Code: debug a FastAPI server or one test with F5 -------------------------------------------------
LAUNCH_JSON = """
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    { "name": "FastAPI (taskboard)", "type": "debugpy", "request": "launch",
      "module": "uvicorn", "args": ["taskboard.main:app", "--reload"], "jinja": true },
    { "name": "Current test file", "type": "debugpy", "request": "launch",
      "module": "pytest", "args": ["${file}", "-x", "-q"] }
  ]
}"""
print("VS Code launch.json:" + LAUNCH_JSON)
