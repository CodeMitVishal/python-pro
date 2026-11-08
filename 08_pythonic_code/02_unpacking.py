"""Module 8 · Unpacking

Unpacking pulls values OUT of a list, tuple or dict and into names,
in one step. It makes code shorter and easier to read.

TEACHING NOTES
  Why it matters  Index juggling (row[0], row[1]) is unreadable and breaks when the data shape
                  changes.
  Picture it      Like unpacking a parcel: each item goes straight into its own labelled box.
  Watch out       The number of names must match the number of values, unless one name has a *
                  to collect the rest.
  In real jobs    Merging config: settings = {**DEFAULTS, **env_settings}; swapping values: a, b
                  = b, a.
  Interview       Q: How does a, b = b, a work without a temporary variable?
                  A: The right side builds a tuple first, then it is unpacked into the names on
                     the left.

Run it:  python 08_pythonic_code/02_unpacking.py
"""

# --- 1. Basic unpacking: one name per value -------------------------------
point = (3, 7)
x, y = point
print(x, y)                      # 3 7

# --- 2. Swap two variables without a temp variable ------------------------
a, b = 1, 2
a, b = b, a                      # the right side is built first, then unpacked
print(a, b)                      # 2 1

# --- 3. Star unpacking: * collects "the rest" into a list -----------------
first, *middle, last = [10, 20, 30, 40, 50]
print(first, middle, last)       # 10 [20, 30, 40] 50

head, *tail = "python"
print(head, tail)                # p ['y', 't', 'h', 'o', 'n']

# --- 4. Ignore values you don't need with _ -------------------------------
name, _, city = ("Vishal", 30, "Augsburg")
print(name, city)                # Vishal Augsburg

# --- 5. Unpack inside a for loop -------------------------------------------
scores = [("Vishal", 91), ("Raj", 78)]
for player, score in scores:     # each tuple is unpacked on the fly
    print(f"{player}: {score}")

# --- 6. Unpack into a function call ----------------------------------------
def area(width, height):
    return width * height

size = [4, 5]
print(area(*size))               # 20  (* spreads a list into positional args)

options = {"width": 2, "height": 9}
print(area(**options))           # 18  (** spreads a dict into keyword args)

# --- 7. Merge lists and dicts ------------------------------------------------
odds, evens = [1, 3], [2, 4]
print([*odds, *evens])           # [1, 3, 2, 4]

defaults = {"theme": "dark", "lang": "en"}
user = {"lang": "de"}
settings = {**defaults, **user}  # later keys win
print(settings)                  # {'theme': 'dark', 'lang': 'de'}
print(defaults | user)           # same result with the | operator (Python 3.9+)

# --- 8. A common bug ----------------------------------------------------------
# x, y = [1, 2, 3]   -> ValueError: too many values to unpack (expected 2)
# The number of names must match the number of values, unless you use *.
