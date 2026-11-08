"""Module 9 · heapq and bisect: fast "smallest first" and "keep it sorted"

heapq  -> a priority queue in a plain list. push/pop the SMALLEST item in O(log n),
          instead of sorting the whole list every time (O(n log n)).
          Use it for: task schedulers, "top 10 of a million", Dijkstra, merging sorted streams.
bisect -> binary search in a SORTED list: find the position in O(log n),
          insert while keeping the list sorted.

Run it:  python 09_data_structures/08_heapq_and_bisect.py
"""
import bisect
import heapq
import random

# --- 1. A priority queue: the most urgent job first --------------------------------------
jobs: list[tuple[int, str]] = []
heapq.heappush(jobs, (3, "send newsletter"))
heapq.heappush(jobs, (1, "restart crashed server"))     # lower number = more urgent
heapq.heappush(jobs, (2, "reply to customer"))
while jobs:
    priority, job = heapq.heappop(jobs)                  # always the smallest
    print(priority, job)

# --- 2. Top-k from a huge list without sorting all of it -----------------------------------------
random.seed(1)
scores = [random.randint(0, 1_000_000) for _ in range(1_000_000)]
print("top 3:", heapq.nlargest(3, scores))               # O(n log k), not O(n log n)
products = [{"name": "laptop", "price": 899}, {"name": "pen", "price": 2}, {"name": "mug", "price": 9}]
print("cheapest 2:", [p["name"] for p in heapq.nsmallest(2, products, key=lambda p: p["price"])])

# --- 3. Merge already-sorted streams lazily (e.g. sorted log files) --------------------------------
server_a = [1, 4, 9]
server_b = [2, 3, 10]
print("merged:", list(heapq.merge(server_a, server_b)))

# --- 4. bisect: search and insert in a sorted list -----------------------------------------------------
grades = [50, 60, 70, 80, 90]                            # grade boundaries (sorted!)
letters = "FEDCBA"                                       # <50 F, 50s E, 60s D, 70s C, 80s B, 90+ A


def grade(score: int) -> str:
    return letters[bisect.bisect_right(grades, score)]    # O(log n) lookup


print([grade(s) for s in (33, 60, 77, 95)])              # ['F', 'D', 'C', 'A']

timeline = [10, 20, 40]
bisect.insort(timeline, 30)                               # insert, stay sorted
print(timeline)                                           # [10, 20, 30, 40]
