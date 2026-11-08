"""Module 19 · Python's memory model: names, objects and references

Everything in Python is an OBJECT living in memory, with:
  an identity (id), a type, and a value.
Variables are just NAMES pointing to objects. CPython counts how many
references point to each object, and frees it when the count drops to 0.

TEACHING NOTES
  Why it matters  Surprising bugs (a list changing 'by itself') come from not knowing how names
                  and objects work.
  Picture it      Variables are sticky notes on objects, not boxes; b = a adds a second note to
                  the same object.
  Watch out       Functions receive references: mutating a list argument changes the caller's
                  list.
  In real jobs    Debugging shared-state bugs and memory leaks in long-running services.
  Interview       Q: How does Python manage memory?
                  A: Reference counting frees objects at zero; a cyclic GC handles reference
                     cycles.

Run it:  python 19_performance_internals/01_memory_model.py
"""
import copy
import gc
import sys

# --- 1. Names point to objects -----------------------------------------------------
a = [1, 2, 3]
b = a                                   # a second name for the SAME object
print(id(a) == id(b), a is b)           # True True
b.append(4)
print(a)                                # [1, 2, 3, 4]

# --- 2. Reference counting ------------------------------------------------------------
data = ["big", "list"]
print(sys.getrefcount(data))            # 2: `data` + the temporary argument to getrefcount
alias = data
print(sys.getrefcount(data))            # 3
del alias                               # removes a NAME, not the object
print(sys.getrefcount(data))            # 2
# When the count reaches 0, CPython frees the memory immediately.

# --- 3. Mutable vs immutable ---------------------------------------------------------
x = 10
y = x
y += 1                                  # ints are immutable: y now points to a NEW object 11
print(x, y)                             # 10 11

nums = [1, 2]
same = nums
same += [3]                             # lists are mutable: changed IN PLACE
print(nums)                             # [1, 2, 3]

# --- 4. is vs == , and CPython's small-int cache --------------------------------------------
p, q = 256, 256
print(p is q)                           # True: CPython caches -5..256
p, q = int("1000"), int("1000")
print(p == q, p is q)                   # True False: equal values, different objects
# Rule: use == for values. Use `is` only for None, True, False.

# --- 5. Function arguments: the object is passed, not a copy -----------------------------
def add_item(lst):
    lst.append("added")                 # changes the caller's list!

items = []
add_item(items)
print(items)                            # ['added']

# --- 6. Shallow vs deep copy (recap from Module 9) ------------------------------------------
nested = {"tags": ["a"]}
shallow, deep = copy.copy(nested), copy.deepcopy(nested)
nested["tags"].append("b")
print(shallow["tags"], deep["tags"])    # ['a', 'b'] ['a']

# --- 7. Reference cycles: the garbage collector cleans those up -----------------------------
class Node:
    def __init__(self):
        self.other = None

n1, n2 = Node(), Node()
n1.other, n2.other = n2, n1             # each keeps the other alive (refcount never hits 0)
del n1, n2
print("collected objects:", gc.collect() >= 2)   # True: the cycle detector freed them
