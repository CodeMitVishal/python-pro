"""Module 10 · Functions are objects ("first-class functions")

In Python a function is a value, just like a number or a list. You can:
  store it in a variable · put it in a list or dict · pass it to another
  function · return it from a function.

That one idea powers callbacks, sorting keys, decorators and strategies.

TEACHING NOTES
  Why it matters  Choosing behaviour at runtime with long if/elif chains is rigid; functions can
                  be passed like data.
  Picture it      Without (), a function is just a value you can hand around; with () you call
                  it.
  Watch out       Pass the function (key=len), not its result (key=len()).
  In real jobs    sorted(key=...), callbacks, dispatch dicts {'csv': read_csv}, strategy
                  objects.
  Interview       Q: What does 'functions are first-class objects' mean?
                  A: Functions can be stored, passed as arguments and returned, like any other
                     object.

Run it:  python 10_advanced_functions/03_first_class_functions.py
"""
from functools import partial

# --- 1. A function is an object with a name and attributes ---------------------
def shout(text):
    return text.upper() + "!"

yell = shout                          # no () -> we copy the function, not call it
print(yell("hi"), yell.__name__)      # HI! shout

# --- 2. Store functions in a dict: a simple "command" dispatcher ------------------
def add(a, b): return a + b
def sub(a, b): return a - b

operations = {"+": add, "-": sub, "*": lambda a, b: a * b}
for op in "+-*":
    print(f"7 {op} 3 = {operations[op](7, 3)}")    # 10, 4, 21

# --- 3. Pass a function in (a "higher-order" function) -----------------------------
def apply_to_all(func, items):
    return [func(x) for x in items]

print(apply_to_all(str.title, ["vishal", "raj"]))   # ['Vishal', 'Raj']

# --- 4. lambda: a tiny unnamed function, for one short expression -----------------
people = [("Vishal", 30), ("Raj", 27), ("Li", 35)]
print(sorted(people, key=lambda p: p[1]))       # sort by age
# Use def as soon as it needs a name, a docstring or more than one expression.

# --- 5. map / filter vs comprehensions ----------------------------------------------
nums = [1, 2, 3, 4]
print(list(map(lambda n: n * n, nums)))          # [1, 4, 9, 16]
print(list(filter(lambda n: n % 2 == 0, nums)))  # [2, 4]
print([n * n for n in nums if n % 2 == 0])       # [4, 16]  <- usually more readable

# --- 6. functools.partial: pre-fill some arguments ----------------------------------
def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)
print(square(5), cube(2))                        # 25 8

# --- 7. Strategy pattern: swap behaviour by passing a different function ------------
def checkout(total, discount=lambda t: t):
    return round(discount(total), 2)

print(checkout(100))                              # 100
print(checkout(100, discount=lambda t: t * 0.9))  # 90.0 (10% off)
