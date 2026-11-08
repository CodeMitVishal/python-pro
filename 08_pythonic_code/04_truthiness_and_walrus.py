"""Module 8 · Truthiness, conditional expressions and the walrus operator

Every value in Python is either "truthy" or "falsy" when you put it in an
if. Knowing which is which lets you write short, clear conditions.

TEACHING NOTES
  Why it matters  if items: is short and clear, but it treats 0, '' and [] as 'missing', which
                  causes real bugs.
  Picture it      Every value answers yes/no to bool(): empty and zero say no, everything else
                  says yes.
  Watch out       When 0 or '' are valid values, test with 'is None', not 'if not x'.
  In real jobs    while (chunk := f.read(8192)): reads a file in chunks; 'if not user:' guards
                  in views.
  Interview       Q: What values are falsy in Python?
                  A: 0, 0.0, '', empty containers ([], {}, set()), None and False. Everything
                     else is truthy.

Run it:  python 08_pythonic_code/04_truthiness_and_walrus.py
"""

# --- 1. Falsy values: everything "empty" or "zero" ---------------------------
falsy = [0, 0.0, "", [], {}, set(), None, False]
print([bool(v) for v in falsy])     # [False, False, False, False, False, False, False, False]
# Everything else is truthy: 1, -5, "hi", [0], {"a": 1}, ...

# --- 2. Check for "empty" the Pythonic way -------------------------------------
cart = []
if not cart:                        # instead of: if len(cart) == 0:
    print("Your cart is empty")

# --- 3. Compare with None using "is", never == ----------------------------------
result = None
if result is None:                  # None is a single object, so "is" is exact
    print("No result yet")

# --- 4. Default values with "or" ------------------------------------------------
name = ""
display = name or "Guest"           # "or" returns the first truthy value
print(display)                      # Guest
# Careful: 0 is falsy too, so  count or 10  turns a real 0 into 10.

# --- 5. Conditional expression (one-line if/else) ------------------------------
age = 20
status = "adult" if age >= 18 else "minor"
print(status)                       # adult

# --- 6. Chained comparisons read like maths ------------------------------------
score = 72
print(50 <= score < 80)             # True  (instead of: score >= 50 and score < 80)

# --- 7. The walrus operator := assigns AND uses a value in one go -------------
# Without walrus you repeat yourself:
#   line = input(); while line != "quit": ...; line = input()
words = ["python", "is", "fun", "quit", "ignored"]
stream = iter(words)
while (word := next(stream)) != "quit":   # assign word, then compare it
    print(word.upper())             # PYTHON / IS / FUN

# Also handy to avoid calling something twice:
data = [3, 8, 1, 9, 4]
if (n := len(data)) > 3:
    print(f"List is long ({n} items)")

# --- 8. Short-circuit: "and"/"or" stop as soon as the answer is known -----------
user = None
print(user and user["name"])        # None: stops before user["name"] would crash
