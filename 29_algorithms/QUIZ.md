# Python Pro – Module 29 Knowledge Check
**Algorithms & data structures**

The answer key is at the bottom, and each answer says which lesson file to revisit.

---

**1. What's the time complexity of bubble sort, and of merge sort?**
- A) O(n) and O(n²)
- B) O(n²) and O(n log n)
- C) O(log n) and O(n)
- D) Both O(n log n)

**2. What does a "stable" sort guarantee?**
- A) It never crashes
- B) Items with equal keys keep their original order
- C) It uses no extra memory
- D) It's always O(n)

**3. What must be true before you can use binary search?**
- A) The data has no duplicates
- B) The data is sorted
- C) The data is a linked list
- D) The data is small

**4. Which structure fits "undo the last action"?**
- A) Queue
- B) Stack (last in, first out)
- C) Set
- D) Heap

**5. Why use `collections.deque` instead of a list for a queue?**
- A) It's sorted
- B) `popleft()` is O(1); `list.pop(0)` is O(n)
- C) It uses less memory
- D) Lists can't be queues

**6. Which traversal of a BST prints its values sorted?**
- A) pre-order
- B) in-order
- C) post-order
- D) level-order

**7. Why can a BST become as slow as a linked list?**
- A) Too many nodes
- B) Inserting already sorted data makes it one long branch: O(n)
- C) Python has no pointers
- D) Recursion limits

**8. Shortest path in an UNWEIGHTED graph?**
- A) DFS
- B) BFS
- C) Dijkstra only
- D) Binary search

**9. What does Dijkstra need that BFS doesn't?**
- A) A stack
- B) A priority queue (heap), for weighted edges
- C) Sorting first
- D) Recursion

**10. What is topological sort used for?**
- A) Sorting numbers
- B) Ordering tasks so that every dependency comes first
- C) Finding cycles only
- D) Shortest paths

**11. Which two properties suggest dynamic programming?**
- A) Sorted input and no duplicates
- B) Overlapping subproblems and optimal substructure
- C) Recursion and loops
- D) Graphs and trees

**12. Why does greedy coin change fail for coins [1, 3, 4] and amount 6?**
- A) It doesn't fail
- B) Greedy takes 4+1+1 (3 coins); the best is 3+3 (2 coins)
- C) 6 can't be paid
- D) Greedy is too slow

**13. Which pattern solves "longest substring without repeating characters" in O(n)?**
- A) Two nested loops
- B) Sliding window + a hash map of last positions
- C) Binary search
- D) Sorting

**14. Why does a hash map turn two-sum from O(n²) into O(n)?**
- A) It sorts the list
- B) "Have I seen target - n?" is an O(1) lookup instead of a second loop
- C) It uses less memory
- D) It's parallel

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Revisit |
|---|--------|---------|
| 1 | B | `01_sorting_and_searching.py` |
| 2 | B | `01_sorting_and_searching.py` |
| 3 | B | `01_sorting_and_searching.py` |
| 4 | B | `02_stacks_queues_linked_lists.py` |
| 5 | B | `02_stacks_queues_linked_lists.py` |
| 6 | B | `03_trees.py` |
| 7 | B | `03_trees.py` |
| 8 | B | `04_graphs.py` |
| 9 | B | `04_graphs.py` |
| 10 | B | `04_graphs.py` |
| 11 | B | `05_dynamic_programming.py` |
| 12 | B | `05_dynamic_programming.py` |
| 13 | B | `06_problem_solving_patterns.py` |
| 14 | B | `06_problem_solving_patterns.py` |

</details>

---

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
