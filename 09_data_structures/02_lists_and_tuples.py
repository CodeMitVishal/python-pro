"""Module 9 · Lists and tuples under the hood

A list is a "dynamic array": a row of slots in memory, each slot holding a
REFERENCE to an object. Python keeps some spare slots at the end, so
append() is fast. Inserting at the front is slow, because every item has
to shift one place to the right.

A tuple is a fixed-size, read-only row. Use it for data that belongs
together and shouldn't change: coordinates, RGB colours, database rows.

TEACHING NOTES
  Why it matters  Choosing list vs tuple tells readers whether data can change, and affects
                  speed and hashability.
  Picture it      A list is a shopping list you edit; a tuple is a printed receipt: fixed once
                  made.
  Watch out       list.insert(0, x) and pop(0) are O(n); use collections.deque for queues.
  In real jobs    Tuples as dict keys (coordinates, composite IDs), lists for collections of
                  rows.
  Interview       Q: List vs tuple?
                  A: List: mutable, many items of one kind. Tuple: immutable, a fixed record,
                     hashable, slightly faster.

Run it:  python 09_data_structures/02_lists_and_tuples.py
"""
import sys
import timeit
from collections import deque

# --- 1. Spare capacity: the list grows in jumps, not one slot at a time -------
items = []
last_size = sys.getsizeof(items)
for i in range(20):
    items.append(i)
    size = sys.getsizeof(items)
    if size != last_size:                 # memory only grows now and then
        print(f"after {len(items):>2} items -> {size} bytes")
        last_size = size

# --- 2. append (end) vs insert(0) (front) ---------------------------------------
n = 20_000
t_end = timeit.timeit("for i in range(n): a.append(i)", setup="a = []", globals={"n": n}, number=1)
t_front = timeit.timeit("for i in range(n): a.insert(0, i)", setup="a = []", globals={"n": n}, number=1)
print(f"append x{n:,}:    {t_end * 1000:7.1f} ms")
print(f"insert(0) x{n:,}: {t_front * 1000:7.1f} ms   <- every insert shifts all items")

# Need fast adds/removes at BOTH ends? Use a deque (Module 9, lesson 4).
q = deque([2, 3])
q.appendleft(1)                            # O(1) at the front
print(list(q))                             # [1, 2, 3]

# --- 3. Tuples: immutable and lighter ---------------------------------------------
point = (3, 7)
# point[0] = 5  -> TypeError: 'tuple' object does not support item assignment
print(sys.getsizeof([3, 7]), "bytes as list,", sys.getsizeof((3, 7)), "bytes as tuple")

# A one-item tuple needs a trailing comma
single = (5,)
print(type(single).__name__, type((5)).__name__)   # tuple int

# --- 4. Tuples can be dict keys or set items; lists cannot ---------------------
distances = {("Berlin", "Munich"): 585}
print(distances[("Berlin", "Munich")])      # 585
# {["Berlin", "Munich"]: 585} -> TypeError: unhashable type: 'list'

# --- 5. Copy traps: = copies the REFERENCE, not the list -----------------------
a = [1, 2, 3]
b = a                                       # same list, two names
c = a.copy()                                # a new list (shallow copy)
a.append(4)
print(b, c)                                 # [1, 2, 3, 4] [1, 2, 3]

# Shallow copy only copies the outer list. Inner lists are still shared:
grid = [[0, 0], [0, 0]]
shallow = grid.copy()
shallow[0][0] = 9
print(grid)                                 # [[9, 0], [0, 0]]  <- surprise!
import copy
deep = copy.deepcopy(grid)                  # copies everything, all the way down
deep[0][0] = 1
print(grid)                                 # [[9, 0], [0, 0]]  (unchanged)
