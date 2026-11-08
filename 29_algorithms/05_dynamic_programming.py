"""Module 29 · Dynamic programming: solve big problems from small, REMEMBERED ones

Use DP when a problem has:
  1. OVERLAPPING SUBPROBLEMS  - the same smaller question comes up again and again
  2. OPTIMAL SUBSTRUCTURE     - the best answer is built from best answers to smaller parts

Two styles:
  TOP-DOWN  - recursion + a cache (@lru_cache)              easy to write
  BOTTOM-UP - fill a table from the smallest case upwards    no recursion limit, often faster

Run it:  python 29_algorithms/05_dynamic_programming.py
"""
from functools import lru_cache


# --- 1. Coin change: fewest coins to pay an amount --------------------------------------------
def min_coins(coins: list[int], amount: int) -> int:
    best = [0] + [float("inf")] * amount          # best[a] = fewest coins for amount a
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                best[a] = min(best[a], best[a - c] + 1)
    return -1 if best[amount] == float("inf") else int(best[amount])


print("coins for 63 cents with [1, 5, 10, 25]:", min_coins([1, 5, 10, 25], 63))   # 6 (25+25+10+1+1+1)
print("greedy fails with [1, 3, 4] for 6:   ", min_coins([1, 3, 4], 6), "(3+3, not 4+1+1)")


# --- 2. Edit distance: how many edits turn one word into another (spell checkers, diff tools) ---------
@lru_cache(maxsize=None)
def edit_distance(a: str, b: str) -> int:
    if not a:
        return len(b)
    if not b:
        return len(a)
    if a[0] == b[0]:
        return edit_distance(a[1:], b[1:])
    return 1 + min(edit_distance(a[1:], b),          # delete
                   edit_distance(a, b[1:]),          # insert
                   edit_distance(a[1:], b[1:]))      # replace


for wrong in ["pyhton", "pythn", "jython"]:
    print(f"edit distance python <-> {wrong}: {edit_distance('python', wrong)}")


# --- 3. Longest common subsequence: what two sequences share, in order ----------------------------------
def lcs(a: str, b: str) -> str:
    table = [[""] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) - 1, -1, -1):
        for j in range(len(b) - 1, -1, -1):
            if a[i] == b[j]:
                table[i][j] = a[i] + table[i + 1][j + 1]
            else:
                table[i][j] = max(table[i + 1][j], table[i][j + 1], key=len)
    return table[0][0]


print("LCS of 'ACCGGTCG' and 'GTCGTTCG':", lcs("ACCGGTCG", "GTCGTTCG"))


# --- 4. 0/1 knapsack: best value that fits in a bag (budgeting, resource planning) ----------------------------
def knapsack(items: list[tuple[str, int, int]], capacity: int) -> tuple[int, list[str]]:
    """items: (name, weight, value). Each item can be taken at most once."""
    best = [[0] * (capacity + 1) for _ in range(len(items) + 1)]
    for i, (_, w, v) in enumerate(items, start=1):
        for cap in range(capacity + 1):
            best[i][cap] = best[i - 1][cap]                       # skip item i
            if w <= cap:
                best[i][cap] = max(best[i][cap], best[i - 1][cap - w] + v)   # or take it
    chosen, cap = [], capacity                                   # walk back to see what was taken
    for i in range(len(items), 0, -1):
        if best[i][cap] != best[i - 1][cap]:
            name, w, _ = items[i - 1]
            chosen.append(name)
            cap -= w
    return best[-1][capacity], chosen[::-1]


gear = [("laptop", 3, 2000), ("camera", 2, 1500), ("drone", 4, 2500), ("tripod", 1, 300)]
print("knapsack (capacity 6 kg):", knapsack(gear, 6))
