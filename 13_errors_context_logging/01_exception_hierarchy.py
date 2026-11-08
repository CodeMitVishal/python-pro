"""Module 13 · Exceptions like a pro

Exceptions are classes in a family tree:
  BaseException
   ├── KeyboardInterrupt, SystemExit      (don't catch these by accident!)
   └── Exception                          (everything you normally handle)
        ├── ValueError, TypeError, KeyError, ...
        └── YOUR OWN errors

Catching a parent catches all its children. So catch as SPECIFIC as you can.

TEACHING NOTES
  Why it matters  Errors will happen; good code decides where to handle them and what to tell
                  the caller.
  Picture it      An exception is a ball thrown up the call stack until someone catches it.
  Watch out       Never 'except: pass'; catch the narrowest exception you can actually handle.
  In real jobs    Domain errors (OutOfStock) mapped to HTTP codes in one exception handler.
  Interview       Q: How do you design custom exceptions?
                  A: One base class per app with specific subclasses; raise ... from e to keep
                     the cause.

Run it:  python 13_errors_context_logging/01_exception_hierarchy.py
"""

# --- 1. Your own exception family --------------------------------------------------
class ShopError(Exception):
    """Base class: callers can catch every shop error with one except."""


class OutOfStock(ShopError):
    def __init__(self, item, wanted, left):
        super().__init__(f"only {left} x {item} left, you asked for {wanted}")
        self.item, self.wanted, self.left = item, wanted, left   # extra data for callers


class PaymentDeclined(ShopError):
    pass


stock = {"laptop": 2}

def buy(item, qty, card_ok=True):
    if stock.get(item, 0) < qty:
        raise OutOfStock(item, qty, stock.get(item, 0))
    if not card_ok:
        raise PaymentDeclined("card was declined")
    stock[item] -= qty
    return f"bought {qty} x {item}"


for args in [("laptop", 1), ("laptop", 5), ("laptop", 1, False)]:
    try:
        print(buy(*args))
    except OutOfStock as e:            # most specific first
        print(f"Out of stock: {e} (left: {e.left})")
    except ShopError as e:             # then the family
        print(f"Shop error ({type(e).__name__}): {e}")

# --- 2. Catch several types in one except ------------------------------------------
for raw in ["42", "abc", None]:
    try:
        print(int(raw) * 2)
    except (ValueError, TypeError) as e:
        print(f"bad input {raw!r}: {type(e).__name__}")

# --- 3. Exception chaining: raise ... from ... keeps the original cause ---------------
def load_config(text):
    try:
        return int(text)
    except ValueError as e:
        raise ShopError("config is broken") from e    # the traceback shows BOTH errors

try:
    load_config("oops")
except ShopError as e:
    print(f"{e} <- caused by {type(e.__cause__).__name__}: {e.__cause__}")

# --- 4. EAFP vs LBYL ---------------------------------------------------------------------
# LBYL "look before you leap":  if key in d: value = d[key]
# EAFP "easier to ask forgiveness than permission" (the Pythonic default):
prices = {"tea": 2.5}
try:
    price = prices["coffee"]
except KeyError:
    price = None
print("coffee price:", price)

# --- 5. Never do this -------------------------------------------------------------------
# try: ...
# except:            <- bare except also catches Ctrl+C and SystemExit
#     pass           <- and hides the bug forever
