# Module 8 · Interview questions (with answers)

Short answers you can say out loud, with code and the usual follow-up.

[← Module 8](README.md) · [Quiz](QUIZ.md)

---

### 1. What's the difference between `is` and `==`?

**Say:** `==` compares **values**. `is` compares **identity**: are both names the same object (same `id()`)? Use `is` only for singletons such as `None`, `True` and `False`.

```python
a, b = [1, 2], [1, 2]
a == b   # True
a is b   # False
```

**Follow-up:** *"Why does `256 is 256` give True but `257 is 257` may not?"* CPython caches small integers (-5..256) as an implementation detail. Never rely on it.

---

### 2. List comprehension vs generator expression?

**Say:** `[x for x in xs]` builds the **whole list now**. `(x for x in xs)` makes a **lazy generator** that produces values one at a time. Use the generator for large data or when you only loop once, e.g. `sum(x * x for x in nums)`.

---

### 3. What are truthy and falsy values?

**Say:** Falsy values are `0`, `0.0`, `""`, empty containers (`[]`, `{}`, `set()`), `None` and `False`. Everything else is truthy. So `if items:` means "not empty". When 0 or an empty string is a **valid** value, test with `is None` instead.

---

### 4. What is EAFP vs LBYL?

**Say:** **LBYL** (Look Before You Leap) checks first: `if key in d: ...`. **EAFP** (Easier to Ask Forgiveness than Permission) just tries and catches the error. Python prefers EAFP: it's shorter, and it avoids race conditions (a file can disappear between the check and the open).

```python
try:
    value = config["timeout"]
except KeyError:
    value = 30
```

---

### 5. How do you swap two variables? How does it work?

**Say:** `a, b = b, a`. The right side builds a tuple **first**, then it's unpacked into the names on the left, so no temporary variable is needed.

---

### 6. What does `*` do in `first, *rest = items`?

**Say:** It's **extended unpacking**. `first` gets the first item and `rest` collects the remaining items into a **list**. It can sit anywhere: `first, *middle, last = items`.

---

### 7. Why is `"".join(parts)` better than `+=` in a loop?

**Say:** Strings are immutable. Each `+=` builds a **new** string and copies everything so far, which makes it O(n²) overall. Collecting the parts in a list and joining once is O(n).

---

### 8. What is the walrus operator?

**Say:** `:=` assigns **and** returns a value inside an expression (Python 3.8+). It avoids computing something twice, e.g. `if (n := len(data)) > 10:` or `while chunk := f.read(8192):`.

---

### 9. When would you use `match`/`case` instead of `if`/`elif`?

**Say:** When you branch on the **structure** of data: JSON events, API payloads, command tuples, AST nodes. It can destructure dicts, lists and classes and bind variables in one step. For simple value comparisons, `if`/`elif` or a dict lookup is still fine.

---

### 10. How do you sort a list of dicts by a field, descending?

```python
users.sort(key=lambda u: u["age"], reverse=True)       # in place
top = sorted(users, key=itemgetter("age"), reverse=True)  # new list
```

**Follow-up:** *"Is Python's sort stable?"* Yes. Timsort keeps equal items in their original order, so you can sort by a secondary key first and then by the primary key.

---

### 11. What does `re.compile` give you, and what are named groups?

**Say:** `re.compile` pre-builds a pattern you reuse many times. A named group, `(?P<user>\w+)`, lets you read the match as `m["user"]` instead of `m.group(2)`, which is clearer and survives pattern changes. Always use raw strings `r"..."`.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
