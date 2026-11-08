"""Slides · Module 29 · Algorithms & data structures"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 29 · Algorithms &amp; data structures"
SLIDES = [
 cover("29", "Algorithms &amp; data structures", "The classics behind every coding interview, built from scratch and timed so you see Big-O.",
       [("Sorting &amp; searching", "01_sorting_and_searching.py"), ("Stacks, queues, linked lists", "02_stacks_queues_linked_lists.py"),
        ("Trees", "03_trees.py"), ("Graphs", "04_graphs.py"), ("Dynamic programming", "05_dynamic_programming.py"),
        ("Problem-solving patterns", "06_problem_solving_patterns.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Coding interviews", "Why companies still ask algorithms",
     "In a live coding round you get <b>45 minutes</b> and a problem like \"find two numbers that add up to a target\". "
     "The brute force works, but the interviewer asks: <b>\"Can you do better?\"</b>",
     "Most problems are one of <b>~8 patterns</b>. Recognise the pattern, and O(n&#178;) becomes O(n)."),

 trace(M, "The process", "How to solve any coding question", ["Step", "Say / do"],
       [["<b>1 Clarify</b>", "restate the problem; ask about input size, duplicates, empty input"],
        ["<b>2 Examples</b>", "walk through 1-2 small examples by hand"],
        ["<b>3 Brute force</b>", "say the simple solution and its Big-O first"],
        ["<b>4 Optimise</b>", "spot the pattern: hash map? two pointers? sort first? BFS?"],
        ["<b>5 Code</b>", "clean names, small helper functions, talk while you type"],
        ["<b>6 Test</b>", "run your examples + edge cases; state time and space complexity"]],
       "Interviewers grade your <b>communication</b> as much as the code."),

 code_out(M, "Sorting and searching", "Binary search: halve the problem each step", '''
def binary_search(items, target):
    lo, hi, steps = 0, len(items) - 1, 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid, steps
        if items[mid] < target:
            lo = mid + 1                 # throw away the left half
        else:
            hi = mid - 1                 # throw away the right half
    return -1, steps

data = list(range(0, 2_000_000, 2))      # 1,000,000 sorted numbers
print(binary_search(data, 1_337_000))
print(binary_search(data, 7))''',
     steps=["Only works on <b>sorted</b> data.", "1,000,000 items &#8594; at most <b>~20</b> steps: O(log n).",
            "In real code: <b>bisect</b>. Python's <b>sorted()</b> is Timsort, O(n log n), stable."]),

 trace(M, "Data structures", "Pick the structure from the question", ["The question says...", "Use", "Why"],
       [["\"have I seen it?\", counts, pairs", "<b>dict / set</b>", "O(1) lookup"],
        ["\"undo\", brackets, \"most recent\"", "<b>stack</b> (list)", "last in, first out"],
        ["\"in order of arrival\", BFS", "<b>queue</b> (deque)", "first in, first out, O(1) both ends"],
        ["\"top k\", \"smallest first\", scheduling", "<b>heap</b> (heapq)", "O(log n) push/pop"],
        ["sorted data, ranges", "<b>binary search</b> / BST", "O(log n)"],
        ["connections, networks, grids", "<b>graph</b> (dict of lists)", "BFS / DFS"]]),

 code_out(M, "Stacks", "Balanced brackets with a stack", '''
def is_balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)                       # push an opener
        elif ch in pairs and (not stack or stack.pop() != pairs[ch]):
            return False                           # wrong closer
    return not stack                               # nothing left open

for s in ["(a[1] + b) * {c}", "(]", "((x)"]:
    print(f"{s:18} {is_balanced(s)}")''',
     steps=["Push openers; every closer must match the <b>top</b>.", "O(n) time, O(n) space.",
            "Same idea: HTML tag validation, undo history, call stacks."]),

 picture(M, "Trees", "Binary search trees",
     "&#127795; Every node has up to 2 children: <b>smaller</b> values go left, <b>larger</b> go right. "
     "Searching follows one path from the root, so a balanced tree answers in O(log n).",
     [("insert 50, 30, 70, 20, 40", "50 is the root"), ("search 40", "50 &#8594; left 30 &#8594; right 40"),
      ("in-order traversal", "left, node, right = SORTED"), ("sorted inserts", "a long chain: O(n)!")],
     "Databases use the same idea: <b>B-tree indexes</b> (Module 23)."),

 code_out(M, "Graphs", "BFS: the shortest path in hops", '''
from collections import deque

friends = {"vishal": ["raj", "li"], "raj": ["vishal", "sam"],
           "li": ["vishal", "sam", "priya"], "sam": ["raj", "li", "mia"],
           "priya": ["li"], "mia": ["sam"]}

def shortest_path(graph, start, goal):
    queue, came_from = deque([start]), {start: None}
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = came_from[node]
            return path[::-1]
        for nxt in graph[node]:
            if nxt not in came_from:
                came_from[nxt] = node
                queue.append(nxt)
    return []

print(shortest_path(friends, "vishal", "mia"))''',
     steps=["BFS explores in <b>rings</b>: 1 hop, then 2 hops...", "Never visit a node twice (<b>came_from</b>).",
            "Weighted edges (km, ms)? <b>Dijkstra</b> with a heap (lesson 04)."]),

 code_out(M, "Dynamic programming", "Coin change: when greedy fails", '''
def greedy(coins, amount):
    used = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            amount -= c; used.append(c)
    return used

def min_coins(coins, amount):
    best = [0] + [float("inf")] * amount      # best[a] = fewest coins for a
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                best[a] = min(best[a], best[a - c] + 1)
    return best[amount]

print("greedy:", greedy([1, 3, 4], 6))
print("DP    :", min_coins([1, 3, 4], 6), "coins (3 + 3)")''',
     steps=["DP = solve small subproblems once, store, reuse.", "Signals: \"fewest / most / number of ways\", overlapping subproblems.",
            "Top-down: recursion + <b>@cache</b>; bottom-up: a table."]),

 code_out(M, "Patterns", "Hash map + sliding window: two classics in O(n)", '''
def two_sum(nums, target):
    seen = {}                                  # value -> index
    for i, n in enumerate(nums):
        if target - n in seen:
            return seen[target - n], i
        seen[n] = i

def longest_unique(s):
    last, start, best = {}, 0, ""
    for i, ch in enumerate(s):
        if last.get(ch, -1) >= start:          # repeat inside the window
            start = last[ch] + 1               # move the left edge
        last[ch] = i
        best = max(best, s[start:i + 1], key=len)
    return best

print(two_sum([2, 7, 11, 15], 9))
print(longest_unique("abcabcbb"), longest_unique("pwwkew"))''',
     steps=["<b>Hash map</b>: \"have I seen target - n?\" in O(1).", "<b>Sliding window</b>: grow the right edge, shrink the left on a repeat.",
            "Also: two pointers, prefix sums, BFS/DFS, DP."]),

 mistake(M, "Interviews", "Jumping straight into code",
     '''
# reads the question, types for 30 minutes,
# silent, optimises nothing, never tests
def solve(x):
    ...''',
     "Even a correct answer can fail the round: the interviewer can't follow your thinking and you miss edge cases.",
     '''
# 1. "So the input is ..., output is ..."
# 2. "Brute force is O(n^2) because ..."
# 3. "With a dict I can do it in O(n)"
# 4. code, talking through it
# 5. test: [], [x], duplicates, negatives''',
     "Think out loud, brute force first, then optimise, then <b>test</b>, then state Big-O."),

 interview(M, "Two sum: find indices of two numbers that add up to target.",
     ["Brute force: check every pair: <b>O(n&#178;)</b> time, O(1) space.",
      "Better: one pass with a <b>dict</b> of value &#8594; index; for each n, check whether <b>target - n</b> is already in it.",
      "That's <b>O(n)</b> time and O(n) space.",
      "Edge cases: no solution (return None), duplicates (store after checking), negative numbers (fine)."],
     '''
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return seen[target - n], i
        seen[n] = i
    return None''',
     "\"What if the array is sorted?\" (two pointers from both ends: O(n) time, O(1) space)."),

 recap(M, "Module 29 in 6 lines",
     ["Process: clarify &#8594; examples &#8594; brute force &#8594; optimise &#8594; code &#8594; test &#8594; Big-O.",
      "Binary search: sorted data, O(log n).",
      "Stack, queue (deque), heap, dict/set: pick from the question's words.",
      "BST in-order = sorted; BFS = shortest path in hops; Dijkstra for weights.",
      "DP: overlapping subproblems; greedy can be wrong.",
      "Patterns: hash map, two pointers, sliding window, prefix sums."],
     "Do <b>exercises/ex29_interview_problems.py</b>: 6 classics with a time limit, so brute force won't pass."),
]
