"""Module 9 · Dicts and sets under the hood (hashing)

A dict doesn't search for a key. It runs the key through hash(), which
turns it into a number, and that number points straight to the slot where
the value lives. That's why lookups are O(1).

The rule that follows: keys (and set items) must be HASHABLE, which in
practice means immutable: str, int, float, tuple, frozenset. Not list,
dict or set.

TEACHING NOTES
  Why it matters  Fast lookups and de-duplication are everywhere in backends; dicts and sets
                  give O(1) for both.
  Picture it      A wall of numbered lockers: the key's hash says which locker to open, so
                  nothing is searched.
  Watch out       Keys must be hashable (no lists/dicts); .copy() is shallow, so nested data is
                  still shared.
  In real jobs    Caching by ID, counting events, 'have I processed this order already?' checks.
  Interview       Q: How does a dict work internally?
                  A: A hash table: hash(key) picks a slot, O(1) average for get/set/delete;
                     insertion order is preserved.

Run it:  python 09_data_structures/03_dicts_and_sets.py
"""

# --- 1. hash() turns a value into a number --------------------------------------
print(hash("python") == hash("python"))   # True: same value, same hash (in one run)
print(hash((1, 2)) == hash((1, 2)))       # True: tuples are hashable
# hash([1, 2]) -> TypeError: unhashable type: 'list'

# --- 2. Dicts keep insertion order (guaranteed since Python 3.7) -----------------
stock = {"apples": 5}
stock["pears"] = 2
stock["kiwis"] = 9
print(list(stock))                         # ['apples', 'pears', 'kiwis']

# --- 3. Safe access ---------------------------------------------------------------
print(stock.get("mango", 0))               # 0  (no KeyError)
stock.setdefault("mango", 0)               # add the key only if it's missing
stock["mango"] += 3
print(stock["mango"])                      # 3

# --- 4. Useful dict methods --------------------------------------------------------
print(stock.pop("kiwis"))                  # 9  (remove and return the value)
stock.update({"apples": 10, "lemons": 4})  # add/overwrite several keys at once
print(stock)                               # {'apples': 10, 'pears': 2, 'mango': 3, 'lemons': 4}

# --- 5. Sets: unique items + maths-style operations --------------------------------
python_devs = {"Vishal", "Raj", "Li"}
cloud_devs = {"Li", "Sam", "Vishal"}

print(sorted(python_devs | cloud_devs))    # union: in either      ['Li', 'Raj', 'Sam', 'Vishal']
print(sorted(python_devs & cloud_devs))    # intersection: in both ['Li', 'Vishal']
print(sorted(python_devs - cloud_devs))    # difference: only Python devs ['Raj']
print(sorted(python_devs ^ cloud_devs))    # symmetric difference: in one only ['Raj', 'Sam']

# --- 6. Remove duplicates but KEEP the order ------------------------------------------
visits = ["home", "blog", "home", "shop", "blog"]
print(list(dict.fromkeys(visits)))         # ['home', 'blog', 'shop']
# set(visits) also removes duplicates, but the order is not guaranteed.

# --- 7. frozenset: an immutable set, so it can be a dict key ---------------------------
team_scores = {frozenset({"Vishal", "Li"}): 42}
print(team_scores[frozenset({"Li", "Vishal"})])   # 42 (order inside doesn't matter)
