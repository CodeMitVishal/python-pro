"""Solution · Exercise 29: Six classic interview problems

Run it:  python solutions/ex29_interview_problems.py
"""
from collections import deque


def two_sum(nums, target):
    seen = {}                                     # value -> index; O(n) time, O(n) space
    for i, n in enumerate(nums):
        if target - n in seen:
            return seen[target - n], i
        seen[n] = i
    return None


def valid_brackets(text):
    pairs, stack = {")": "(", "]": "[", "}": "{"}, []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs and (not stack or stack.pop() != pairs[ch]):
            return False
    return not stack


def merge_intervals(intervals):
    merged = []
    for start, end in sorted(intervals):          # sort by start: overlaps become neighbours
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def longest_unique_substring(s):
    last, start, best = {}, 0, 0
    for i, ch in enumerate(s):
        if last.get(ch, -1) >= start:
            start = last[ch] + 1                  # shrink the window past the repeat
        last[ch] = i
        best = max(best, i - start + 1)
    return best


def count_islands(grid):
    rows, cols = len(grid), len(grid[0]) if grid else 0
    seen, islands = set(), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                islands += 1                      # a new island: flood-fill it with BFS
                queue = deque([(r, c)])
                seen.add((r, c))
                while queue:
                    y, x = queue.popleft()
                    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == "1" \
                                and (ny, nx) not in seen:
                            seen.add((ny, nx))
                            queue.append((ny, nx))
    return islands


def min_coins(coins, amount):
    best = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return -1 if best[amount] == float("inf") else best[amount]


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
    assert time.perf_counter() - start < 1.0
    print("All checks passed!")
