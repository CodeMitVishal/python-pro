"""Module 19 · Measuring and saving memory

  sys.getsizeof   -> size of ONE object (not what it points to)
  tracemalloc     -> which LINES of your code allocated the most memory
  __slots__       -> smaller objects when you have millions of them
  generators      -> process data without holding it all (Module 11)

Run it:  python 19_performance_internals/04_memory_tricks.py
"""
import sys
import tracemalloc

# --- 1. getsizeof is shallow --------------------------------------------------------------
words = ["python"] * 1000
print(sys.getsizeof(words), "bytes for the list itself (just 1000 references)")
print(sys.getsizeof("python"), "bytes for one string object")

# --- 2. __slots__: millions of small objects ---------------------------------------------
class PointDict:
    def __init__(self, x, y):
        self.x, self.y = x, y            # stored in a per-object __dict__


class PointSlots:
    __slots__ = ("x", "y")               # fixed fields, no __dict__

    def __init__(self, x, y):
        self.x, self.y = x, y


def measure(cls, n=200_000):
    tracemalloc.start()
    objs = [cls(i, i) for i in range(n)]
    current, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del objs
    return current / 1_000_000


print(f"\n200,000 points with __dict__:  {measure(PointDict):6.1f} MB")
print(f"200,000 points with __slots__: {measure(PointSlots):6.1f} MB")

# --- 3. tracemalloc: find the lines that allocate the most ---------------------------------
tracemalloc.start()
squares = [n * n for n in range(300_000)]                        # big
text = ",".join(str(n) for n in range(100_000))                 # medium
small = {i: str(i) for i in range(1_000)}                        # small
snapshot = tracemalloc.take_snapshot()
tracemalloc.stop()

print("\nTop 3 allocations by line:")
for stat in snapshot.statistics("lineno")[:3]:
    frame = stat.traceback[0]
    print(f"  line {frame.lineno:>3}: {stat.size / 1_000_000:5.2f} MB")

# --- 4. Generators vs lists (recap) ------------------------------------------------------------
print(f"\nlist of 1M squares:  {sys.getsizeof([n * n for n in range(1_000_000)]):>10,} bytes")
print(f"generator of them:   {sys.getsizeof(n * n for n in range(1_000_000)):>10,} bytes")
