"""Module 8 · Strings like a pro

f-strings can format numbers, pad columns and even debug for you.
join and split turn lists into text and back.

Run it:  python 08_pythonic_code/05_strings_like_a_pro.py
"""

price = 1234.5678
ratio = 0.4567

# --- 1. f-string format specs:  {value:spec} -----------------------------------
print(f"{price:.2f}")        # 1234.57     (2 decimals)
print(f"{price:,.2f}")       # 1,234.57    (thousands separator)
print(f"{ratio:.1%}")        # 45.7%       (as a percentage)
print(f"{42:05d}")           # 00042       (pad with zeros to width 5)

# --- 2. Alignment: < left, > right, ^ centre ----------------------------------
for item, cost in [("Coffee", 3.5), ("Laptop", 899.0)]:
    print(f"{item:<10}|{cost:>10.2f}|")
# Coffee    |      3.50|
# Laptop    |    899.00|

# --- 3. Debug with = : prints the expression AND its value ---------------------
user = "Vishal"
print(f"{user=}")            # user='Vishal'
print(f"{len(user) * 2 = }") # len(user) * 2 = 12

# --- 4. join: list -> string (much faster than + in a loop) ---------------------
words = ["learn", "python", "daily"]
print(" ".join(words))       # learn python daily
print(", ".join(words))      # learn, python, daily

# --- 5. split: string -> list -------------------------------------------------
csv_line = "Vishal,30,Augsburg"
name, age, city = csv_line.split(",")    # split + unpack in one go
print(name, int(age) + 1, city)          # Vishal 31 Augsburg

# --- 6. Handy string methods ----------------------------------------------------
messy = "   Hello World   "
print(messy.strip())                      # Hello World
print("report.pdf".endswith(".pdf"))      # True
print("Python".lower().startswith("py"))  # True
print("a-b-c".replace("-", " "))          # a b c
print("42".isdigit())                     # True: safe check before int()

# Strings are immutable: every method returns a NEW string.
# Build big strings with a list + "".join(...), not with += in a loop.
