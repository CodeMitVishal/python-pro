# Python Pro – Module 19 Knowledge Check
**Performance & internals**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson file to revisit.

---

### Part A – Multiple choice

**1. What is a Python variable?**
- A) A box that holds a value
- B) A name that refers to an object
- C) A memory address you control
- D) A copy of the value

**2. When does CPython free an object's memory right away?**
- A) At the end of the program
- B) When its reference count drops to 0
- C) Every 10 seconds
- D) Never

**3. What cleans up objects that refer to each other in a cycle?**
- A) Reference counting
- B) The garbage collector (`gc`)
- C) `del`
- D) Nothing

**4. `x = 10; y = x; y += 1`. Why is `x` still 10?**
- A) A bug
- B) Ints are immutable: `y += 1` makes `y` point to a new object
- C) `y` is a copy
- D) `+=` doesn't work on ints

**5. You pass a list to a function, and the function appends to it. What happens to the caller's list?**
- A) Nothing: Python passes copies
- B) It changes, because the same object is passed
- C) It raises an error
- D) It's cleared

**6. When should you use `is`?**
- A) To compare any values
- B) Only for identity checks like `is None`
- C) For strings
- D) For numbers

**7. What's the first rule of optimisation?**
- A) Rewrite it in C
- B) Measure first and find the hotspot
- C) Use more threads
- D) Remove comments

**8. Which tool shows which FUNCTIONS take the most time in a program?**
- A) `timeit`
- B) `cProfile`
- C) `tracemalloc`
- D) `sys.getsizeof`

**9. Which change usually gives the biggest speed-up?**
- A) Shorter variable names
- B) A better algorithm or data structure (for example list → set)
- C) Fewer comments
- D) Using `while` instead of `for`

**10. Why is `"".join(words)` much faster than `s += w` in a loop?**
- A) It isn't
- B) Strings are immutable: `+=` creates a new string every time
- C) `join` uses threads
- D) `join` skips words

**11. What does `__slots__` save?**
- A) CPU time only
- B) Memory per object, because there's no per-object `__dict__`
- C) Disk space
- D) Import time

**12. Which tool finds the LINES that allocated the most memory?**
- A) `cProfile`
- B) `tracemalloc`
- C) `gc`
- D) `timeit`

---

### Part B – What's the output?

**13.**
```python
def add(lst):
    lst.append(1)

a = []
add(a); add(a)
print(a)
```

**14.**
```python
p, q = int("1000"), int("1000")
print(p == q, p is q)
```

---

### Part C – Fix it

**15.** This takes minutes for 100,000 emails. Make it O(n):
```python
unique = []
for e in emails:
    if e not in unique:
        unique.append(e)
```

**16.** `price(country)` is a slow pure function that's called 1 million times with only 5 different countries. What's the one-line fix?

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | Names point to objects. | `01_memory_model.py` |
| 2 | B | Reference counting. | `01_memory_model.py` |
| 3 | B | The cycle detector. | `01_memory_model.py` |
| 4 | B | Immutable objects can't change in place. | `01_memory_model.py` |
| 5 | B | The object itself is passed. | `01_memory_model.py` |
| 6 | B | `==` for values. | `01_memory_model.py` |
| 7 | B | Don't guess. | `02_measure_first.py` |
| 8 | B | A function-level profiler. | `02_measure_first.py` |
| 9 | B | 309x in the lesson. | `03_speed_tricks.py` |
| 10 | B | `join` builds the string once. | `02_measure_first.py` |
| 11 | B | 24 MB → 17.6 MB in the lesson. | `04_memory_tricks.py` |
| 12 | B | Memory by line. | `04_memory_tricks.py` |
| 13 | `[1, 1]` | The same list both times. | `01_memory_model.py` |
| 14 | `True False` | Equal values, different objects. | `01_memory_model.py` |
| 15 | `unique = list(dict.fromkeys(emails))` (keeps order), or track a `seen` set. | O(1) lookups. | `03_speed_tricks.py` |
| 16 | Put `@lru_cache(maxsize=None)` on `price`. | 5 real calls, the rest from the cache. | `03_speed_tricks.py` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
