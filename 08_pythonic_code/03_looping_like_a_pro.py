"""Module 8 · Looping like a pro

Python gives you small built-in tools so you almost never need
range(len(...)) or manual counters. Learn these and your loops get
shorter, safer and easier to read.

Run it:  python 08_pythonic_code/03_looping_like_a_pro.py
"""

names = ["Vishal", "Raj", "Li"]
scores = [91, 78, 85]

# --- 1. enumerate: the position AND the item --------------------------------
# Instead of: for i in range(len(names)): print(i, names[i])
for position, name in enumerate(names, start=1):
    print(position, name)                 # 1 Vishal / 2 Raj / 3 Li

# --- 2. zip: walk two (or more) lists side by side ---------------------------
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

# zip stops at the SHORTEST list. strict=True raises an error instead,
# which catches lists that are accidentally different lengths.
print(dict(zip(names, scores)))           # {'Vishal': 91, 'Raj': 78, 'Li': 85}

# --- 3. sorted with key: sort by anything -------------------------------------
pairs = list(zip(names, scores))
best_first = sorted(pairs, key=lambda pair: pair[1], reverse=True)
print(best_first)                         # [('Vishal', 91), ('Li', 85), ('Raj', 78)]

by_length = sorted(names, key=len)
print(by_length)                          # ['Li', 'Raj', 'Vishal']

# sorted() returns a NEW list; list.sort() changes the list in place.

# --- 4. reversed: loop backwards without copying ------------------------------
for name in reversed(names):
    print(name, end=" ")                  # Li Raj Vishal
print()

# --- 5. any / all: answer yes/no questions about a whole list -----------------
print(any(s < 80 for s in scores))        # True:  at least one score below 80
print(all(s >= 50 for s in scores))       # True:  every score is a pass

# --- 6. min / max / sum with key ----------------------------------------------
top = max(pairs, key=lambda pair: pair[1])
print(top)                                # ('Vishal', 91)

# --- 7. Loop over a dictionary the right way ----------------------------------
ages = {"Vishal": 30, "Raj": 27}
for name, age in ages.items():            # keys and values together
    print(name, age)

# --- 8. for ... else: "else" runs only if the loop did NOT break --------------
for score in scores:
    if score < 50:
        print("Someone failed")
        break
else:
    print("Everyone passed")              # runs, because we never hit break
