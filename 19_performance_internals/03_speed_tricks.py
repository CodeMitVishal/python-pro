"""Module 19 · Speed tricks that actually matter (measured)

In order of impact:
  1. a better ALGORITHM / DATA STRUCTURE (O(n²) -> O(n))      -> 100x+
  2. don't repeat work: cache, compute once outside the loop  -> 10x
  3. use built-ins written in C: sum, max, sorted, set, join  -> 2-10x
  4. micro tweaks (local variables...)                        -> 1.1x, rarely worth it

Run it:  python 19_performance_internals/03_speed_tricks.py
"""
import timeit
from functools import lru_cache


def bench(label, func, number=20):
    ms = timeit.timeit(func, number=number) / number * 1000
    print(f"  {label:<28} {ms:9.3f} ms")
    return ms


orders = [f"c{i % 2000}" for i in range(20_000)]

# --- 1. Algorithm: list membership vs set ----------------------------------------------
print("1. unique customers")

def unique_list():
    seen = []
    for c in orders:
        if c not in seen:              # O(n) each time -> O(n²) overall
            seen.append(c)
    return seen

def unique_set():
    return list(dict.fromkeys(orders))   # O(n), and keeps the order

slow = bench("list + 'not in'", unique_list, number=3)
fast = bench("dict.fromkeys (hashing)", unique_set)
print(f"  -> {slow / fast:.0f}x faster\n")

# --- 2. Don't repeat work -------------------------------------------------------------------
print("2. repeated work in a loop")
prices = list(range(10_000))

def tax_inside():
    return [p * (1 + 19 / 100) * len(prices) / len(prices) for p in prices]   # recomputed every time

def tax_outside():
    factor = 1 + 19 / 100               # computed ONCE
    return [p * factor for p in prices]

bench("recompute in the loop", tax_inside)
bench("compute once", tax_outside)
print()

# --- 3. Caching an expensive pure function ------------------------------------------------
print("3. caching")

def shipping_cost(country):
    return sum(i * i for i in range(20_000)) % 50 + len(country)   # pretend it's slow

@lru_cache(maxsize=None)
def shipping_cost_cached(country):
    return shipping_cost(country)

countries = ["DE", "IN", "US"] * 30
bench("no cache (90 calls)", lambda: [shipping_cost(c) for c in countries], number=3)
bench("lru_cache (90 calls)", lambda: [shipping_cost_cached(c) for c in countries], number=3)
print()

# --- 4. Built-ins are written in C ------------------------------------------------------
print("4. built-ins vs hand-written loops")
nums = list(range(100_000))

def manual_sum():
    total = 0
    for n in nums:
        total += n
    return total

bench("for loop sum", manual_sum)
bench("sum()", lambda: sum(nums))
