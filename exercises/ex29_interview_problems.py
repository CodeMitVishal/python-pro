"""Exercise 29 · Six classic interview problems

Solve each function, aiming for the time complexity shown. Write the brute force
first if that helps, then improve it with the right pattern from Module 29.

  1. two_sum(nums, target)            -> indices (i, j), i < j            O(n)    hash map
  2. valid_brackets(text)             -> True if ()[]{} are balanced      O(n)    stack
  3. merge_intervals(intervals)       -> overlapping intervals merged     O(n log n) sort
  4. longest_unique_substring(s)      -> its LENGTH                       O(n)    sliding window
  5. count_islands(grid)              -> number of islands of "1"s        O(rows*cols) BFS/DFS
  6. min_coins(coins, amount)         -> fewest coins, or -1              O(amount*coins) DP

Run it to check your work:
    python exercises/ex29_interview_problems.py

Stuck? Compare with solutions/ex29_interview_problems.py
"""


def two_sum(nums, target):
    """TODO 1"""


def valid_brackets(text):
    """TODO 2"""


def merge_intervals(intervals):
    """TODO 3: [[1, 3], [2, 6], [8, 10]] -> [[1, 6], [8, 10]]"""


def longest_unique_substring(s):
    """TODO 4"""


def count_islands(grid):
    """TODO 5: grid is a list of strings like ["110", "010", "001"]; islands connect up/down/left/right"""


def min_coins(coins, amount):
    """TODO 6"""


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    assert two_sum([3, 2, 4], 6) == (1, 2)
    assert two_sum([1, 2], 7) is None
    assert valid_brackets("{[()()]}") and not valid_brackets("([)]") and not valid_brackets("((")
    assert merge_intervals([[8, 10], [1, 3], [2, 6], [15, 18], [17, 20]]) == [[1, 6], [8, 10], [15, 20]]
    assert merge_intervals([]) == []
    assert longest_unique_substring("abcabcbb") == 3 and longest_unique_substring("bbbb") == 1
    assert longest_unique_substring("") == 0
    assert count_islands(["11000", "11000", "00100", "00011"]) == 3
    assert count_islands(["111", "010", "111"]) == 1
    assert min_coins([1, 3, 4], 6) == 2 and min_coins([2], 3) == -1 and min_coins([1], 0) == 0

    import time
    start = time.perf_counter()
    assert two_sum(list(range(200_000)), 399_997) == (199_998, 199_999)
    assert longest_unique_substring("abcdefghij" * 20_000) == 10
    assert time.perf_counter() - start < 1.0, "too slow: use a hash map / sliding window, not nested loops"
    print("All checks passed!")
