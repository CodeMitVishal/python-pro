"""Module 29 · Problem-solving patterns (how to crack coding interviews)

Most interview problems are variations of a few patterns. Recognise the pattern
and the O(n²) brute force becomes O(n).

  HASH MAP      "have I seen this before?" in O(1)      two sum, anagrams, duplicates
  TWO POINTERS  walk from both ends of SORTED data       pair sums, palindromes
  SLIDING WINDOW a moving range over an array/string     longest substring, max sum of k
  PREFIX SUMS   precompute running totals                range sums in O(1)

A reliable process: 1. restate the problem + examples  2. brute force first
3. find the pattern  4. code it  5. test edge cases (empty, one item, duplicates)
6. state the time and space complexity.

Run it:  python 29_algorithms/06_problem_solving_patterns.py
"""
from collections import defaultdict
from itertools import accumulate


# --- 1. Hash map: two sum in O(n) instead of O(n²) ----------------------------------------------
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}                     # value -> index
    for i, n in enumerate(nums):
        if target - n in seen:
            return seen[target - n], i
        seen[n] = i
    return None


print("two_sum:", two_sum([2, 7, 11, 15], 9))     # (0, 1)


def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)      # same letters -> same key
    return list(groups.values())


print("anagrams:", group_anagrams(["listen", "silent", "enlist", "google", "gogole", "cat"]))


# --- 2. Two pointers -----------------------------------------------------------------------------------
def is_palindrome(text: str) -> bool:
    chars = [c.lower() for c in text if c.isalnum()]
    left, right = 0, len(chars) - 1
    while left < right:
        if chars[left] != chars[right]:
            return False
        left, right = left + 1, right - 1
    return True


print("palindrome:", is_palindrome("A man, a plan, a canal: Panama"))


# --- 3. Sliding window: longest substring without repeating characters --------------------------------
def longest_unique(s: str) -> str:
    last_seen: dict[str, int] = {}
    start = best_start = best_len = 0
    for i, ch in enumerate(s):
        if last_seen.get(ch, -1) >= start:        # repeat inside the window: move the left edge
            start = last_seen[ch] + 1
        last_seen[ch] = i
        if i - start + 1 > best_len:
            best_start, best_len = start, i - start + 1
    return s[best_start:best_start + best_len]


print("longest unique:", longest_unique("abcabcbb"), "|", longest_unique("pwwkew"))


def max_sum_of_k(nums: list[int], k: int) -> int:
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]           # slide: add the new item, drop the old
        best = max(best, window)
    return best


print("best 3-day sales:", max_sum_of_k([3, 8, 1, 9, 4, 7, 2], 3))   # 20 (9+4+7)

# --- 4. Prefix sums: many range-sum questions, each in O(1) ----------------------------------------------
daily = [5, 3, 8, 6, 2, 7, 4]
prefix = [0, *accumulate(daily)]                  # prefix[i] = sum of the first i days


def range_sum(i: int, j: int) -> int:             # days i..j inclusive
    return prefix[j + 1] - prefix[i]


print("sales days 2-5:", range_sum(2, 5))          # 8 + 6 + 2 + 7 = 23
