# Module 29 · Interview questions (with answers)

[← Module 29](README.md) · [Quiz](QUIZ.md)

---

### 1. How do you approach a coding question?

**Say:**
1. Clarify the input, output and constraints.
2. Work through small examples by hand.
3. State the brute force and its Big-O.
4. Find the pattern and optimise.
5. Code while you talk.
6. Test edge cases (empty, one item, duplicates, negatives).
7. State the time and space complexity.

---

### 2. What is Big-O? Give examples.

**Say:** How the work grows as the input grows, ignoring constants.
- O(1): dict lookup.
- O(log n): binary search.
- O(n): one loop.
- O(n log n): sorting.
- O(n²): nested loops over the same data.
- O(2ⁿ): naive recursion on subsets.

---

### 3. Which sorting algorithms do you know? What does Python use?

**Say:** Bubble and insertion sort are O(n²), with insertion sort fast on nearly-sorted data. Merge sort is O(n log n) and stable but needs extra memory. Quick sort is O(n log n) on average and O(n²) worst case. Python uses **Timsort**, a hybrid of merge and insertion sort: O(n log n), **stable**, and very fast on partly sorted data.

---

### 4. Stack vs queue? How do you implement them in Python?

**Say:** A stack is LIFO: use a `list` with `append` and `pop`. A queue is FIFO: use `collections.deque` with `append` and `popleft` (O(1)). Don't use `list.pop(0)`, which is O(n).

---

### 5. BFS vs DFS?

**Say:** **BFS** uses a queue and explores level by level, so it finds the **shortest path in unweighted graphs**. **DFS** uses a stack or recursion and goes deep first; it's used for connectivity, cycle detection and topological sort. Both are O(V + E). For weighted edges, use **Dijkstra** with a heap.

---

### 6. What is dynamic programming?

**Say:** Solving problems with **overlapping subproblems** and **optimal substructure** by computing each subproblem once and storing it. Top-down uses recursion with memoisation (`@cache`); bottom-up fills a table. Examples: coin change, edit distance, longest common subsequence, knapsack.

---

### 7. Reverse a linked list.

```python
def reverse(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev
```

**Say:** Walk the list once and flip each `next` pointer: O(n) time, O(1) space.

---

### 8. Find the first non-repeating character in a string.

```python
from collections import Counter
def first_unique(s):
    counts = Counter(s)
    return next((ch for ch in s if counts[ch] == 1), None)
```

**Say:** Two passes, O(n) time, O(k) space for k distinct characters.

---

### 9. Detect a cycle in a linked list.

**Say:** Floyd's tortoise and hare: a slow pointer moves 1 step and a fast pointer moves 2. If they ever meet, there's a cycle. O(n) time, O(1) space. (Or keep a set of seen nodes: O(n) space.)

---

### 10. Merge overlapping intervals.

```python
def merge(intervals):
    out = []
    for start, end in sorted(intervals):
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out
```

**Say:** Sort by start, O(n log n), then merge neighbours in one pass.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
