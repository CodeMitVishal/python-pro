"""Module 10 · Scope (LEGB) and closures

When Python sees a name, it looks in 4 places, in this order:
  L  Local      - inside the current function
  E  Enclosing  - inside any outer function
  G  Global     - at the top level of the file
  B  Built-in   - print, len, sum, ...

A CLOSURE is an inner function that remembers variables from the outer
function, even after the outer function has finished.

TEACHING NOTES
  Why it matters  Per-user counters and configurable functions need state without globals or a
                  whole class.
  Picture it      A closure carries a backpack: the outer variables it uses travel with it after
                  the outer function returns.
  Watch out       Assigning to an outer variable needs nonlocal; lambdas in a loop all see the
                  LAST loop value.
  In real jobs    Decorators, callbacks, and FastAPI dependency factories like
                  require_role('admin').
  Interview       Q: What is a closure?
                  A: An inner function that remembers variables from its enclosing scope;
                     changing them needs nonlocal.

Run it:  python 10_advanced_functions/02_scope_and_closures.py
"""

# --- 1. LEGB in action ------------------------------------------------------------
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)              # local: found in L first
    inner()
    print(x)                  # enclosing

outer()
print(x)                      # global

# --- 2. Reading a global is fine; ASSIGNING to it needs "global" --------------------
counter = 0

def bump():
    global counter            # without this, counter += 1 -> UnboundLocalError
    counter += 1

bump(); bump()
print(counter)                # 2   (but prefer returning values over globals!)

# --- 3. A closure: a function that remembers ----------------------------------------
def make_multiplier(factor):
    def multiply(n):
        return n * factor     # "factor" comes from the enclosing scope
    return multiply           # return the function itself, not a result

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5), triple(5))   # 10 15   each closure keeps its own factor
print(double.__closure__[0].cell_contents)   # 2  <- the remembered value

# --- 4. nonlocal: change a variable of the enclosing function ------------------------
def make_counter():
    count = 0
    def next_number():
        nonlocal count        # we want to UPDATE the outer count, not make a new one
        count += 1
        return count
    return next_number

c1, c2 = make_counter(), make_counter()
print(c1(), c1(), c1(), c2())   # 1 2 3 1   each counter has its own state

# --- 5. The late-binding trap -------------------------------------------------------
buggy = [lambda: i for i in range(3)]
print([f() for f in buggy])   # [2, 2, 2]  <- every lambda sees the LAST i

fixed = [lambda i=i: i for i in range(3)]   # default arg captures i NOW
print([f() for f in fixed])   # [0, 1, 2]
