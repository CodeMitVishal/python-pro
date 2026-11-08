"""Slides · Module 13 · Errors, context managers & logging"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 13 · Errors, context managers &amp; logging"
SLIDES = [
 cover("13", "Errors, context managers &amp; logging", "Production code fails safely, cleans up after itself, and tells you what happened.",
       [("Exceptions like a pro", "01_exception_hierarchy.py"), ("Context managers", "02_context_managers.py"),
        ("logging", "03_logging.py"), ("Demo: robust order importer", "04_demo_order_importer.py"),
        ("ExitStack &amp; exception groups", "05_exitstack_and_groups.py"), ("Debugging like a pro", "06_debugging_like_a_pro.py"),
        ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Exceptions", "Errors are messages, not disasters",
     "A payment API times out. Bad code <b>crashes</b> the whole import, or worse, catches everything and <b>silently</b> continues with wrong data.<br><br>"
     "Good code decides: <b>retry, skip this row, roll back, or stop</b>.",
     "Raise <b>specific</b> exceptions, catch only what you can <b>handle</b>, and let the rest go up to someone who can."),

 picture(M, "Exceptions", "What happens when an error is raised",
     "&#127936; An exception is like a ball thrown <b>up the call stack</b>. Each function can catch it (<b>except</b>) or let it fly. "
     "If nobody catches it, the program stops and prints a <b>traceback</b>.",
     [("charge_card()", "raise PaymentError"), ("place_order()", "no except: passes it up"),
      ("api_handler()", "except PaymentError: return 402"), ("user", "sees a clear message")]),

 code_out(M, "Exceptions", "try / except / else / finally", '''
def parse_amount(text):
    try:
        value = float(text)
    except ValueError:
        print(f"  {text!r} is not a number")
        return None
    else:                       # only if NO exception
        print(f"  parsed {value}")
        return value
    finally:                    # ALWAYS, even after return
        print("  (cleanup)")

parse_amount("19.99")
parse_amount("abc")''',
     steps=["<b>except</b>: handle a specific error.", "<b>else</b>: the success path, kept out of the try block.",
            "<b>finally</b>: always runs; good for cleanup (but prefer <b>with</b>)."]),

 code_out(M, "Exceptions", "Your own exception family", '''
class ShopError(Exception):
    """Base for everything our app raises."""

class OutOfStock(ShopError):
    def __init__(self, item, wanted, left):
        super().__init__(f"{item}: wanted {wanted}, only {left} left")
        self.item = item

class PaymentFailed(ShopError): ...

def checkout(item, qty):
    try:
        raise ConnectionError("gateway timeout")   # low-level
    except ConnectionError as e:
        raise PaymentFailed("card not charged") from e

try:
    checkout("lamp", 1)
except ShopError as e:              # catch the whole family
    print(type(e).__name__, "-", e)
    print("cause:", repr(e.__cause__))

print(OutOfStock("lamp", 3, 1))''',
     steps=["One <b>base class</b> lets callers catch all your errors at once.",
            "<b>raise ... from e</b> keeps the original cause in the traceback.",
            "Add useful fields (<b>item</b>) for the handler."]),

 mistake(M, "Exceptions", "Swallowing every error",
     '''
try:
    total = compute_invoice(order)
    send_email(order.customer, total)
except:                    # catches EVERYTHING
    pass                   # ...and hides it''',
     "A bare <b>except</b> also catches typos (NameError), Ctrl+C and real bugs. The invoice silently isn't sent and nobody knows why.",
     '''
try:
    total = compute_invoice(order)
except InvalidOrder as e:
    log.warning("skipping order %s: %s", order.id, e)
    return
send_email(order.customer, total)   # errors here surface''',
     "Catch the <b>narrowest</b> exception you can handle, <b>log</b> it, and keep the try block small."),

 # ------------------------------------------------------------------ CONTEXT MANAGERS
 picture(M, "Context managers", "with = guaranteed clean-up",
     "&#128682; Like a <b>door that closes itself</b>: whatever happens inside the room, even an exception, "
     "the door is closed when you leave. Files, DB transactions, locks and HTTP sessions all work this way.",
     [("with open(p) as f:", "__enter__: open, return f"), ("your code", "may succeed or raise"),
      ("__exit__", "ALWAYS runs: close the file"), ("exception?", "is passed on (unless handled)")]),

 code_out(M, "Context managers", "Write one with @contextmanager", '''
from contextlib import contextmanager

@contextmanager
def transaction(db):
    try:
        yield db
        db.append("COMMIT")
    except Exception:
        db.append("ROLLBACK")
        raise

log = []
with transaction(log) as db:
    db.append("INSERT 1")
print(log)

log = []
try:
    with transaction(log) as db:
        db.append("INSERT 1")
        raise ValueError("row 2 is broken")
except ValueError as e:
    print("error:", e)
print(log)''',
     steps=["Code before <b>yield</b> = setup; after = teardown.", "On an error: <b>roll back</b>, then re-raise.",
            "Same idea as Django's <b>transaction.atomic()</b>."]),

 # ------------------------------------------------------------------ LOGGING
 mistake(M, "logging", "print() is not logging",
     '''
print("user logged in")
print("ERROR: payment failed", e)''',
     "No time, no level, no module name, can't be switched off, can't be sent to a log service. In production you're blind.",
     '''
import logging
log = logging.getLogger(__name__)

log.info("user %s logged in", user_id)
log.exception("payment failed for order %s", oid)''',
     "Levels, timestamps, module names, filtering and handlers. <b>log.exception</b> adds the full traceback."),

 code_out(M, "logging", "Configure once, log everywhere", '''
import logging, sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
    datefmt="%H:%M:%S", stream=sys.stdout)

log = logging.getLogger("shop.orders")
log.debug("cart contents: ...")          # below INFO: hidden
log.info("order %s placed", 1042)
log.warning("stock low for %s", "lamp")
try:
    1 / 0
except ZeroDivisionError:
    log.error("could not compute discount")''',
     output="12:01:07 INFO    shop.orders: order 1042 placed\n12:01:07 WARNING shop.orders: stock low for lamp\n12:01:07 ERROR   shop.orders: could not compute discount",
     steps=["Levels: <b>DEBUG &lt; INFO &lt; WARNING &lt; ERROR &lt; CRITICAL</b>.", "Use <b>%s</b> arguments, not f-strings: formatting is skipped when the level is off.",
            "One logger per module: <b>getLogger(__name__)</b>."]),

 # ------------------------------------------------------------------ DEBUGGING
 trace(M, "Debugging", "Debugging like a pro", ["Tool", "Use it when", "How"],
       [["<b>breakpoint()</b>", "you want to stop and look around", "n next · s step in · c continue · p x print · q quit"],
        ["<b>post-mortem</b>", "it crashed: inspect where", "<span class=\"m\">python -m pdb script.py</span>"],
        ["<b>VS Code debugger</b>", "web apps and tests", "launch.json for uvicorn / pytest, click to set breakpoints"],
        ["<b>log.exception()</b>", "it fails in production", "full traceback in the logs"],
        ["<b>faulthandler</b>", "it hangs or segfaults", "<span class=\"m\">python -X faulthandler app.py</span>"]],
       "Read tracebacks <b>bottom-up</b>: the last line is the error, the line above is where it happened."),

 job(M, "Errors and logging", "In real web services", [
     ("Map domain errors to HTTP", '''
@app.exception_handler(OutOfStock)
def out_of_stock(req, exc):
    return JSONResponse({"detail": str(exc)}, 409)'''),
     ("Atomic DB writes", '''
with transaction.atomic():      # Django
    order.save(); stock.save()'''),
     ("Structured logs for search", '''
log.info("order placed", extra={"order_id": 1042})'''),
     ("Never leak internals", '''
except Exception:
    log.exception("unexpected")
    raise HTTPException(500, "Internal error")'''),
 ]),

 interview(M, "How do you handle exceptions in a production API?",
     ["Define a <b>custom exception hierarchy</b> for business errors (OutOfStock, PaymentFailed).",
      "Catch <b>specific</b> exceptions where you can act on them: retry, skip, roll back.",
      "Map them to <b>HTTP status codes</b> in one place (exception handlers / middleware).",
      "Let unexpected errors bubble up to a global handler that <b>logs the traceback</b> and returns a generic 500.",
      "Use <b>raise ... from e</b> to keep the cause; never <b>except: pass</b>."],
     None,
     "\"What's the difference between Exception and BaseException?\" (BaseException also covers KeyboardInterrupt and SystemExit, which you normally must not catch)."),

 interview(M, "What is a context manager? Write one.",
     ["An object that guarantees <b>setup and teardown</b> around a block: <b>__enter__</b> and <b>__exit__</b>.",
      "<b>__exit__</b> runs even if the block raises; returning True would swallow the exception.",
      "Examples: files, locks, DB transactions, <b>requests.Session</b>, temporary settings in tests.",
      "Quickest way: <b>@contextmanager</b> with try / yield / finally."],
     '''
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        self.took = time.perf_counter() - self.start
        return False        # don't hide errors''',
     "\"How do you manage several resources at once?\" (several items in one with statement, or contextlib.ExitStack for a dynamic number)."),

 recap(M, "Module 13 in 6 lines",
     ["Catch the <b>narrowest</b> exception you can handle; never <b>except: pass</b>.",
      "<b>else</b> = success path, <b>finally</b> = always.",
      "Your own <b>exception family</b>; <b>raise ... from e</b> keeps the cause.",
      "<b>with</b> guarantees clean-up; <b>@contextmanager</b> writes one in 6 lines.",
      "<b>logging</b>, not print: levels, <b>getLogger(__name__)</b>, <b>log.exception</b>.",
      "Debug with <b>breakpoint()</b>; read tracebacks bottom-up."],
     "Do <b>exercises/ex13_bank_transfer.py</b>: a transfer that rolls back on any error."),
]
