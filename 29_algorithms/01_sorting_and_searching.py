"""Module 29 · Sorting and searching: the algorithms behind sorted() and `in`

You'll use sorted() in real code (it's Timsort: O(n log n), stable, written in C).
But interviews and real problem-solving need you to understand HOW sorting works,
and why some algorithms are O(n²) and others O(n log n).

Run it:  python 29_algorithms/01_sorting_and_searching.py
"""
import bisect
import random
import timeit
from functools import partial


# --- 1. Bubble sort: O(n²), compare neighbours, swap, repeat --------------------------------
def bubble_sort(items: list[int]) -> list[int]:
    a = items[:]
    for end in range(len(a) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:                          # already sorted: stop early
            break
    return a


# --- 2. Insertion sort: O(n²), but fast for SMALL or nearly-sorted lists --------------------------
def insertion_sort(items: list[int]) -> list[int]:
    a = items[:]
    for i in range(1, len(a)):
        current, j = a[i], i - 1
        while j >= 0 and a[j] > current:         # shift bigger items one place right
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = current
    return a


# --- 3. Merge sort: O(n log n), divide in halves, sort each, MERGE ---------------------------------
def merge_sort(items: list[int]) -> list[int]:
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left, right = merge_sort(items[:mid]), merge_sort(items[mid:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):      # take the smaller front item each time
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    return merged + left[i:] + right[j:]


# --- 4. Quick sort: O(n log n) on average, partition around a pivot ---------------------------------
def quick_sort(items: list[int]) -> list[int]:
    if len(items) <= 1:
        return items
    pivot = random.choice(items)                 # a random pivot avoids the O(n²) worst case
    return (quick_sort([x for x in items if x < pivot]) + [x for x in items if x == pivot]
            + quick_sort([x for x in items if x > pivot]))


data = [5, 2, 9, 1, 5, 6]
for sort in (bubble_sort, insertion_sort, merge_sort, quick_sort):
    print(f"{sort.__name__:<15} {sort(data)}")

random.seed(1)
big = [random.randint(0, 10_000) for _ in range(2_000)]
print("\nSorting 2,000 numbers:")
for sort in (bubble_sort, insertion_sort, merge_sort, quick_sort, sorted):
    t = timeit.timeit(partial(sort, big), number=3) / 3     # partial binds THIS sort now
    print(f"  {sort.__name__:<15} {t * 1000:8.2f} ms")

# --- 5. Stable sorting: equal keys keep their original order ----------------------------------------------
people = [("raj", 30), ("li", 25), ("vishal", 30), ("sam", 25)]
print("\nby age (stable):", sorted(people, key=lambda p: p[1]))   # li before sam, raj before vishal


# --- 6. Searching: linear O(n) vs binary O(log n) (only on SORTED data) ------------------------------------
def binary_search(a: list[int], target: int) -> int:
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


nums = list(range(0, 1_000_000, 2))
print("binary search 999,998:", binary_search(nums, 999_998), "| steps needed: ~20 instead of 500,000")
print("bisect does it for you:", bisect.bisect_left(nums, 999_998))
