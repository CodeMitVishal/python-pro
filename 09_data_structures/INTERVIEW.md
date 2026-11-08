# Module 9 · Interview questions (with answers)

Short answers you can say out loud, with code and the usual follow-up.

[← Module 9](README.md) · [Quiz](QUIZ.md)

---

### 1. List vs tuple: what's the difference?

**Say:** A list is **mutable** and holds many items of the same kind. A tuple is **immutable** and holds a fixed record. Tuples are hashable when their items are, so they can be dict keys or set members. They are also slightly smaller and faster, and they tell the reader "this won't change".

---

### 2. How does a dict work internally? Why are lookups O(1)?

**Say:** It's a **hash table**. Python computes `hash(key)` and uses it to jump straight to a slot, so get, set and delete are **O(1) on average**. Collisions are resolved by probing other slots and comparing keys with `==`. Keys must be hashable. Since Python 3.7, dicts keep insertion order.

**Follow-up:** *"What makes an object hashable?"* It has a `__hash__` that never changes during its lifetime and an `__eq__` that agrees with it (equal objects must have equal hashes). Mutable built-ins (list, dict, set) aren't hashable.

---

### 3. Mutable vs immutable types?

**Say:** **Immutable** objects can't change after they're created: int, float, str, tuple, frozenset, bytes. **Mutable** ones can: list, dict, set, and most custom objects. This matters for dict keys, for default arguments, and when you pass objects to functions, because a function can change your list.

---

### 4. Shallow copy vs deep copy?

**Say:** A shallow copy (`x.copy()`, `list(x)`, `x[:]`, `copy.copy`) creates a new outer container but **shares** the nested objects. `copy.deepcopy` copies everything recursively.

```python
a = [[1], [2]]
b = a.copy()
b[0].append(9)
print(a)   # [[1, 9], [2]]
```

---

### 5. What's the time complexity of common list and dict operations?

| Operation | list | dict / set |
|---|---|---|
| index / lookup by key | O(1) | O(1) |
| `x in ...` | **O(n)** | **O(1)** |
| append / add | O(1) amortised | O(1) |
| insert or pop at the front | **O(n)** | - |
| sort | O(n log n) | - |

---

### 6. When would you use a set?

**Say:** For fast **membership tests** ("have I seen this ID?"), for **removing duplicates**, and for **set maths**: intersection `&`, union `|`, difference `-`. Note that a set has no order and holds only hashable items.

---

### 7. Name some classes from `collections` and when to use them.

**Say:**
- `Counter` counts things and has `most_common()`.
- `defaultdict(list)` groups items without "if key not in" checks.
- `deque` is a queue or stack with O(1) operations at both ends; `maxlen` keeps the last N items.
- `namedtuple` is a lightweight immutable record.
- `OrderedDict` has `move_to_end()`, which makes it handy for LRU caches.

---

### 8. What does `@dataclass` generate? How do you make one immutable?

**Say:** It generates `__init__`, `__repr__` and `__eq__` from the type-annotated fields (plus ordering with `order=True`). `frozen=True` makes instances immutable and hashable. A mutable default must use `field(default_factory=list)`.

**Follow-up:** *"dataclass vs pydantic?"* A dataclass doesn't validate input. Pydantic validates and converts external data (API bodies, config), so use it at the boundaries of your app.

---

### 9. How would you get the top 3 of a million numbers efficiently?

**Say:** `heapq.nlargest(3, nums)`. It keeps a small heap of size k, so it runs in O(n log k) instead of sorting everything in O(n log n).

---

### 10. Why use an Enum instead of string constants?

**Say:** An Enum gives a **closed set** of valid values. A typo raises an error immediately instead of silently creating a new "status". IDEs can autocomplete it, and you can iterate over all options. `StrEnum` (3.11+) still compares equal to its string, so it works directly with JSON and databases.

---

### 11. How would you implement an LRU cache?

**Say:** In real code, `functools.lru_cache`. By hand, an `OrderedDict`: on every `get`, call `move_to_end(key)`; on `put`, if it's over capacity, call `popitem(last=False)` to remove the least recently used item. Both operations are O(1).

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
