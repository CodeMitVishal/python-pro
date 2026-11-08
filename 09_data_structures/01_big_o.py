"""Module 9 · Big-O: why the right data structure matters

Big-O describes how the work grows when the data grows.
  O(1)  constant  : same speed for 10 items or 10 million  (dict/set lookup)
  O(n)  linear    : twice the data, twice the time          (searching a list)
  O(n²) quadratic : twice the data, FOUR times the time     (a loop inside a loop)

We measure it with timeit so you can SEE the difference.

Run it:  python 09_data_structures/01_big_o.py
"""
import timeit

for size in [1_000, 100_000, 1_000_000]:
    numbers_list = list(range(size))
    numbers_set = set(numbers_list)
    target = size - 1                       # worst case: the very last item

    # timeit runs the statement many times and returns the total seconds
    t_list = timeit.timeit(lambda: target in numbers_list, number=200)
    t_set = timeit.timeit(lambda: target in numbers_set, number=200)

    print(f"{size:>9,} items | list 'in': {t_list * 1000:8.2f} ms "
          f"| set 'in': {t_set * 1000:6.3f} ms")

# What you'll see:
#  - The list time grows with the size: it checks items one by one -> O(n).
#  - The set time stays tiny: it jumps straight to the right spot -> O(1).
#
# Cheat sheet (average case):
#   list: index a[i] O(1) · append O(1) · insert(0, x) O(n) · x in list O(n)
#   dict: d[key] O(1) · d[key] = v O(1) · key in d O(1)
#   set : add O(1) · x in s O(1) · union/intersection O(len)
#
# Rule: if you check "is X in here?" many times, use a set or dict.
