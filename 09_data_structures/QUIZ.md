# Python Pro – Module 9 Knowledge Check
**Data structures deep dive**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson file to revisit.

---

### Part A – Multiple choice

**1. What does O(n) mean?**
- A) The time stays the same no matter the size
- B) The time grows in step with the number of items
- C) The time grows with the square of the items
- D) The code runs n times faster

**2. You check "is this ID in the collection?" 1 million times. What should the collection be?**
- A) A list
- B) A tuple
- C) A set
- D) A string

**3. Why is `list.insert(0, x)` slow on a big list?**
- A) Lists are sorted on every insert
- B) Every existing item has to shift one place right
- C) Python copies the list to disk
- D) It isn't slow

**4. Which is best for fast adds and removes at BOTH ends?**
- A) `list`
- B) `tuple`
- C) `collections.deque`
- D) `dict`

**5. Which can be a dictionary key?**
- A) `[1, 2]`
- B) `{"a": 1}`
- C) `(1, 2)`
- D) `{1, 2}`

**6. How does a dict find a key so fast?**
- A) It searches from the start
- B) It uses `hash(key)` to jump to the right slot
- C) It keeps keys sorted and uses binary search
- D) It caches the last key

**7. `{"a", "b"} & {"b", "c"}` gives:**
- A) `{"a", "b", "c"}`
- B) `{"b"}`
- C) `{"a", "c"}`
- D) `{"a"}`

**8. Which removes duplicates AND keeps the original order?**
- A) `set(items)`
- B) `sorted(set(items))`
- C) `list(dict.fromkeys(items))`
- D) `items.unique()`

**9. What does `Counter(words).most_common(1)` return?**
- A) The rarest word
- B) A list with the most frequent `(word, count)` pair
- C) The number of unique words
- D) A sorted list of words

**10. Why use `defaultdict(list)`?**
- A) It sorts the lists
- B) Missing keys start as an empty list automatically
- C) It's faster than a list
- D) It removes duplicates

**11. `deque(maxlen=3)` after appending 1, 2, 3, 4 holds:**
- A) `[1, 2, 3]`
- B) `[2, 3, 4]`
- C) `[1, 2, 3, 4]`
- D) An error

**12. What does `@dataclass` write for you?**
- A) `__init__`, `__repr__` and `__eq__`
- B) A database table
- C) Getters and setters only
- D) Nothing; it's just a comment

**13. Why is `items: list = []` not allowed in a dataclass?**
- A) Lists can't be fields
- B) Every object would share ONE list; use `field(default_factory=list)`
- C) Type hints can't be lists
- D) It is allowed

---

### Part B – What's the output?

**14.**
```python
a = [1, 2, 3]
b = a
c = a.copy()
a.append(4)
print(b, c)
```

**15.**
```python
grid = [[0, 0], [0, 0]]
copy_ = grid.copy()
copy_[0][0] = 9
print(grid[0][0])
```

**16.**
```python
from collections import Counter
print(Counter("banana").most_common(2))
```

---

### Part C – Fix it

**17.** This is slow for 100,000 users. Make it fast:
```python
banned = ["bob", "eve", ...]        # 50,000 names
for user in users:                  # 100,000 users
    if user in banned:
        block(user)
```

**18.** Shorten this with the right tool:
```python
groups = {}
for name, team in people:
    if team not in groups:
        groups[team] = []
    groups[team].append(name)
```

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | Linear: twice the data, twice the time. | `01_big_o.py` |
| 2 | C | `in` on a set is O(1); on a list it's O(n). | `01_big_o.py` |
| 3 | B | A list is an array of slots; everything shifts. | `02_lists_and_tuples.py` |
| 4 | C | `deque` is O(1) at both ends. | `04_collections.py` |
| 5 | C | Keys must be hashable (immutable). | `03_dicts_and_sets.py` |
| 6 | B | Hashing jumps straight to the slot: O(1). | `03_dicts_and_sets.py` |
| 7 | B | `&` is the intersection: items in both. | `03_dicts_and_sets.py` |
| 8 | C | Dicts keep insertion order. | `03_dicts_and_sets.py` |
| 9 | B | `[('word', count)]`, most frequent first. | `04_collections.py` |
| 10 | B | No more "if key not in dict". | `04_collections.py` |
| 11 | B | The oldest item drops off the front. | `04_collections.py` |
| 12 | A | It generates them from the field list. | `05_dataclasses.py` |
| 13 | B | `default_factory` makes a new list per object. | `05_dataclasses.py` |
| 14 | `[1, 2, 3, 4] [1, 2, 3]` | `b` is the same list; `c` is a copy. | `02_lists_and_tuples.py` |
| 15 | `9` | A shallow copy shares the inner lists; use `copy.deepcopy`. | `02_lists_and_tuples.py` |
| 16 | `[('a', 3), ('n', 2)]` | Counts each letter. | `04_collections.py` |
| 17 | `banned = set(banned)` before the loop. | 100,000 O(1) lookups instead of O(n) each. | `01_big_o.py` |
| 18 | `groups = defaultdict(list)` then just `groups[team].append(name)`. | Missing keys are created for you. | `04_collections.py` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
