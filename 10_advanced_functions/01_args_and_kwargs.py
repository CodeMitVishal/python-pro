"""Module 10 · Parameters like a pro: *args, **kwargs, keyword-only

A function can accept:
  def f(a, b=2, *args, c, d=4, **kwargs)
        |  |     |      |  |     └ any extra KEYWORD args -> dict
        |  |     |      └──┴ keyword-only (they come after *)
        |  |     └ any extra POSITIONAL args -> tuple
        |  └ default value
        └ normal positional parameter

TEACHING NOTES
  Why it matters  Wrappers, decorators and flexible APIs must accept arguments they don't know
                  in advance.
  Picture it      *args is a bag for extra positional values; **kwargs is a labelled box for
                  extra named ones.
  Watch out       Never use a mutable default (def f(x=[])): it is created once and shared by
                  every call.
  In real jobs    Logging wrappers, decorators, and keyword-only options like connect(host, *,
                  timeout=5).
  Interview       Q: What is the mutable default argument trap?
                  A: Defaults are evaluated once at def time, so a default list is shared; use
                     None and create it inside.

Run it:  python 10_advanced_functions/01_args_and_kwargs.py
"""

# --- 1. *args collects extra positional arguments into a TUPLE ---------------
def total(*numbers):
    print(type(numbers).__name__, numbers)
    return sum(numbers)

print(total(1, 2, 3))            # tuple (1, 2, 3) -> 6
print(total())                   # tuple () -> 0

# --- 2. **kwargs collects extra keyword arguments into a DICT ------------------
def make_user(name, **details):
    return {"name": name, **details}

print(make_user("Vishal", city="Augsburg", role="admin"))
# {'name': 'Vishal', 'city': 'Augsburg', 'role': 'admin'}

# --- 3. Keyword-only parameters: everything after * must be named ---------------
def connect(host, *, port=443, timeout=5):
    return f"{host}:{port} (timeout {timeout}s)"

print(connect("api.example.com", port=8080))   # api.example.com:8080 (timeout 5s)
# connect("api.example.com", 8080) -> TypeError: forces callers to write port=8080,
# which makes call sites self-explaining.

# --- 4. Positional-only parameters: everything before / can't be named ----------
def power(base, exp, /):
    return base ** exp

print(power(2, 10))              # 1024
# power(base=2, exp=10) -> TypeError. Lets you rename the parameters later
# without breaking anybody's code.

# --- 5. Forwarding: pass everything through to another function -----------------
def log_call(func, *args, **kwargs):
    print(f"calling {func.__name__} with {args} {kwargs}")
    return func(*args, **kwargs)

print(log_call(connect, "db.local", timeout=30))
# calling connect with ('db.local',) {'timeout': 30}
# db.local:443 (timeout 30s)

# --- 6. THE classic trap: a mutable default is created ONCE ----------------------
def add_item_buggy(item, basket=[]):        # this list is shared by every call!
    basket.append(item)
    return basket

print(add_item_buggy("apple"))   # ['apple']
print(add_item_buggy("pear"))    # ['apple', 'pear']  <- surprise!

def add_item(item, basket=None):            # the fix: default to None
    if basket is None:
        basket = []                         # a NEW list on every call
    basket.append(item)
    return basket

print(add_item("apple"), add_item("pear"))  # ['apple'] ['pear']
