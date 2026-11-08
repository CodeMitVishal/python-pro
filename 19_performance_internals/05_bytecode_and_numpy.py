"""Module 19 · Bytecode, weak references, and NumPy for number crunching

1. `dis` shows the bytecode CPython really runs: why some code is faster.
2. weakref: refer to an object WITHOUT keeping it alive (caches, observers).
3. NumPy: when pure Python loops are too slow for numbers, vectorise.
   The loop runs in optimised C over a compact array, often 10-100x faster.

Run it:  pip install numpy
         python 19_performance_internals/05_bytecode_and_numpy.py
"""
import dis
import timeit
import weakref


# --- 1. Bytecode ------------------------------------------------------------------------------
def add_tax(price):
    return price * 1.19

print("bytecode of add_tax:")
for ins in dis.get_instructions(add_tax):
    if ins.opname not in ("RESUME", "CACHE"):
        print(f"   {ins.opname:<14} {ins.argrepr}")
# Fewer, simpler instructions run faster. That's why built-ins (written in C) beat loops.


# --- 2. weakref: a cache that doesn't keep objects alive --------------------------------------------
class BigImage:
    def __init__(self, name):
        self.name = name

cache = weakref.WeakValueDictionary()
img = BigImage("banner.png")
cache["banner"] = img
print("\nin cache while used:", "banner" in cache)
del img                                          # the last strong reference is gone
print("in cache after del: ", "banner" in cache)   # the entry vanished by itself


# --- 3. NumPy vs pure Python ----------------------------------------------------------------------------
import numpy as np  # noqa: E402

prices = list(range(1_000_000))
array = np.arange(1_000_000, dtype=np.float64)

t_py = timeit.timeit(lambda: [p * 1.19 for p in prices], number=5) / 5
t_np = timeit.timeit(lambda: array * 1.19, number=5) / 5             # one vectorised operation
print(f"\nadd 19% tax to 1M prices: Python {t_py * 1000:.1f} ms | NumPy {t_np * 1000:.1f} ms "
      f"({t_py / t_np:.0f}x faster)")

# Vectorised thinking: no explicit loops
temps = np.array([12.5, 15.0, 31.2, 28.4, 5.1])
print("hot days:", temps[temps > 25])            # boolean mask instead of a for/if
print("mean / max:", temps.mean().round(2), temps.max())
print("Fahrenheit:", (temps * 9 / 5 + 32).round(1))
# Data analysis builds on this: pandas (tables) and polars use the same idea.
