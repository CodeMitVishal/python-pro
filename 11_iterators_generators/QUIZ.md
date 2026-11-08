# Python Pro – Module 11 Knowledge Check
**Iterators & generators**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson file to revisit.

---

### Part A – Multiple choice

**1. What's the difference between an iterable and an iterator?**
- A) There is none
- B) An iterable can hand out an iterator; the iterator remembers the position and gives `next()` items
- C) An iterator is always a list
- D) An iterable is always infinite

**2. What does `next()` raise when an iterator has no more items?**
- A) `IndexError`
- B) `ValueError`
- C) `StopIteration`
- D) `None`

**3. Which two methods make a class an iterator?**
- A) `__init__` and `__len__`
- B) `__iter__` and `__next__`
- C) `__getitem__` and `__setitem__`
- D) `__enter__` and `__exit__`

**4. What happens when you call a function that contains `yield`?**
- A) It runs to the end and returns a list
- B) It returns a generator object; the body hasn't run yet
- C) It raises an error
- D) It runs until the first `return`

**5. What does `yield` do?**
- A) Ends the function for good
- B) Hands out a value and pauses, keeping local variables
- C) Prints a value
- D) Returns a list

**6. Why is `(x * x for x in range(10**6))` better than `[x * x for x in range(10**6)]` for a `sum`?**
- A) It's shorter
- B) It makes values one at a time, so memory stays tiny
- C) It's sorted
- D) It runs on several CPUs

**7. You loop over a generator twice. What happens the second time?**
- A) It starts again
- B) Nothing: it's already used up
- C) It raises an error
- D) It runs backwards

**8. What does `yield from other` do?**
- A) Yields the iterable `other` as one item
- B) Yields each item of `other`, one by one
- C) Imports `other`
- D) Stops the generator

**9. Which `itertools` function takes the first n items of any iterator?**
- A) `chain`
- B) `islice`
- C) `cycle`
- D) `groupby`

**10. What must you do before `itertools.groupby`?**
- A) Nothing
- B) Sort by the same key, because it only groups neighbours
- C) Convert to a set
- D) Reverse the list

---

### Part B – What's the output?

**11.**
```python
def gen():
    yield 1
    yield 2

g = gen()
print(list(g), list(g))
```

**12.**
```python
from itertools import accumulate, chain
print(list(accumulate([1, 2, 3])), list(chain("ab", [1])))
```

**13.**
```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

print(next(countdown(3)), sum(countdown(3)))
```

---

### Part C – Fix it

**14.** This "streams" a huge file but still runs out of memory. Why?
```python
def read_lines(path):
    with open(path) as f:
        return f.readlines()
```

**15.** Write `squares(n)` as a generator that yields the squares from `1` to `n`.

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | `iter(iterable)` → iterator; `next(iterator)` → item. | `01_iteration_protocol.py` |
| 2 | C | `for` catches it to know when to stop. | `01_iteration_protocol.py` |
| 3 | B | `__iter__` returns self, `__next__` returns the next item. | `01_iteration_protocol.py` |
| 4 | B | Nothing runs until the first `next()`. | `02_generators.py` |
| 5 | B | It pauses and resumes from the same spot. | `02_generators.py` |
| 6 | B | 200 bytes vs 8 MB in the lesson. | `02_generators.py` |
| 7 | B | Generators can be looped once. | `02_generators.py` |
| 8 | B | It delegates to another iterable. | `02_generators.py` |
| 9 | B | `islice(it, n)`. | `03_pipelines.py`, `04_itertools.py` |
| 10 | B | It groups consecutive equal keys. | `04_itertools.py` |
| 11 | `[1, 2] []` | The second `list(g)` gets nothing. | `02_generators.py` |
| 12 | `[1, 3, 6] ['a', 'b', 1]` | Running totals; chained iterables. | `04_itertools.py` |
| 13 | `3 6` | Two separate generators: first item 3, sum 3+2+1. | `02_generators.py` |
| 14 | `readlines()` loads the whole file. Use `for line in f: yield line`. | Yield line by line. | `03_pipelines.py` |
| 15 | `def squares(n):` / `for i in range(1, n + 1): yield i * i` | One value at a time. | `02_generators.py` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
