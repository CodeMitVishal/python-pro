"""Module 8 · Comprehensions

A comprehension builds a new list, dict or set in ONE readable line.
It replaces the classic "make an empty list, loop, append" pattern.

Shape:   [ what_to_keep   for item in things   if condition ]
           ^ expression     ^ the loop           ^ optional filter

Run it:  python 08_pythonic_code/01_comprehensions.py
"""

prices = [12.5, 40.0, 7.25, 99.9, 3.0]

# --- 1. The old way: 4 lines -------------------------------------------
with_tax = []
for p in prices:
    with_tax.append(round(p * 1.19, 2))
print(with_tax)              # [14.88, 47.6, 8.63, 118.88, 3.57]

# --- 2. The Pythonic way: 1 line, same result --------------------------
with_tax = [round(p * 1.19, 2) for p in prices]
print(with_tax)              # [14.88, 47.6, 8.63, 118.88, 3.57]

# --- 3. Add a filter with if ---------------------------------------------
cheap = [p for p in prices if p < 20]
print(cheap)                 # [12.5, 7.25, 3.0]

# --- 4. if/else goes BEFORE the for (it chooses the value, not a filter) --
labels = ["cheap" if p < 20 else "pricey" for p in prices]
print(labels)                # ['cheap', 'pricey', 'cheap', 'pricey', 'cheap']

# --- 5. Dict comprehension: {key: value for ...} ------------------------
names = ["vishal", "raj", "li"]
name_lengths = {name: len(name) for name in names}
print(name_lengths)          # {'vishal': 6, 'raj': 3, 'li': 2}

# Flip a dictionary (keys <-> values)
codes = {"DE": "Germany", "IN": "India"}
by_country = {country: code for code, country in codes.items()}
print(by_country)            # {'Germany': 'DE', 'India': 'IN'}

# --- 6. Set comprehension: {value for ...} removes duplicates ------------
emails = ["A@x.com", "a@x.com", "b@y.com"]
unique = {e.lower() for e in emails}
print(sorted(unique))        # ['a@x.com', 'b@y.com']

# --- 7. Nested loops: read left to right, like the normal for loops ------
grid = [(row, col) for row in range(2) for col in range(3)]
print(grid)                  # [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]

# Flatten a list of lists
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [n for row in matrix for n in row]
print(flat)                  # [1, 2, 3, 4, 5, 6]

# --- 8. Generator expression: ( ) instead of [ ] -------------------------
# It does NOT build a list in memory; it hands out one value at a time.
# Perfect when you only need a total, a max, any(), all()...
total = sum(p * 1.19 for p in prices)
print(round(total, 2))       # 193.55

# --- Rule of thumb ---------------------------------------------------------
# Use a comprehension when it fits on one line and reads like English.
# If you need several ifs, nested logic or side effects (print, save),
# write a normal for loop instead. Readable beats clever.
