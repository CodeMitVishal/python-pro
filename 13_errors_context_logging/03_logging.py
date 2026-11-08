"""Module 13 · logging: print() for grown-ups

Why not print()? Logging gives you:
  - LEVELS so you can turn noise up or down without deleting lines
        DEBUG < INFO < WARNING < ERROR < CRITICAL
  - TIMESTAMPS, the module name and the level on every line
  - OUTPUTS: console, files, cloud services... set once, used everywhere
  - TRACEBACKS with logger.exception()

Run it:  python 13_errors_context_logging/03_logging.py
"""
import logging
import sys
import tempfile
from pathlib import Path

# --- 1. Configure ONCE, at the start of your program ----------------------------------
logging.basicConfig(
    level=logging.INFO,                                  # show INFO and above
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,                                   # default is stderr
)

# --- 2. One logger per module: named after the module ----------------------------------
log = logging.getLogger("shop.orders")                  # in real code: getLogger(__name__)

log.debug("cart contents: %s", ["book"])                 # hidden: below INFO
log.info("order %s created for %s", 1042, "vishal")      # use %s args, not f-strings:
log.warning("stock low: %d left", 2)                     # the text is only built if shown
log.error("payment service returned %d", 503)

# --- 3. Log an exception WITH its traceback ---------------------------------------------
try:
    1 / 0
except ZeroDivisionError:
    log.exception("could not compute the discount")      # level ERROR + full traceback

# --- 4. Also write to a file: add a handler ----------------------------------------------
log_file = Path(tempfile.gettempdir()) / "python_pro_shop.log"
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_handler.setLevel(logging.WARNING)                  # only warnings+ go to the file
file_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
log.addHandler(file_handler)

log.info("this goes to the console only")
log.warning("this goes to the console AND the file")
file_handler.close()
print("file contains:", log_file.read_text(encoding="utf-8").strip())

# --- 5. Change the level at runtime -----------------------------------------------------
log.setLevel(logging.DEBUG)
log.debug("now debug messages show up too")
