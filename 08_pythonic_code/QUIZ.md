# Python Pro – Module 8 Knowledge Check
**Pythonic code**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson file to revisit.

---

### Part A – Multiple choice

**1. Which is the Pythonic way to build a list of squares?**
- A) `squares = []` then `for n in nums: squares.append(n*n)`
- B) `squares = [n * n for n in nums]`
- C) `squares = list(n * n)`
- D) `squares = {n * n: n for n in nums}`

**2. Where does `if/else` go when it CHOOSES a value in a comprehension?**
- A) After the `for`: `[x for x in xs if x > 0 else 0]`
- B) Before the `for`: `[x if x > 0 else 0 for x in xs]`
- C) It isn't allowed
- D) Inside `range()`

**3. What does `{e.lower() for e in emails}` create?**
- A) A list
- B) A dict
- C) A set (no duplicates)
- D) A generator

**4. Why use `sum(x * 2 for x in nums)` instead of `sum([x * 2 for x in nums])`?**
- A) It's the only syntax that works
- B) The generator doesn't build a whole list in memory first
- C) It returns a list
- D) It sorts the numbers

**5. `first, *middle, last = [1, 2, 3, 4]`. What is `middle`?**
- A) `2`
- B) `(2, 3)`
- C) `[2, 3]`
- D) An error

**6. How do you swap `a` and `b`?**
- A) `a = b; b = a`
- B) `a, b = b, a`
- C) `swap(a, b)`
- D) `a <-> b`

**7. Which replaces `for i in range(len(names)): print(i, names[i])`?**
- A) `for i, name in enumerate(names): print(i, name)`
- B) `for name in zip(names): print(name)`
- C) `for i in names: print(i)`
- D) `for i, name in names.items(): print(i, name)`

**8. What does `zip([1, 2, 3], ["a", "b"])` give?**
- A) `[(1, 'a'), (2, 'b'), (3, None)]`
- B) `[(1, 'a'), (2, 'b')]`: it stops at the shortest
- C) An error
- D) `{1: 'a', 2: 'b'}`

**9. Which values are falsy?**
- A) `0`, `""`, `[]`, `None`
- B) `"0"`, `[0]`, `" "`
- C) `-1`, `"False"`
- D) Only `False`

**10. What's the right way to check for `None`?**
- A) `if x == None:`
- B) `if x is None:`
- C) `if not x == None:`
- D) `if None(x):`

**11. What does `while (line := read()) != "quit":` do?**
- A) Compares `line` with `read`
- B) Assigns `read()` to `line` and compares it in the same step
- C) It's a syntax error
- D) Runs forever

**12. `f"{1234.5:,.2f}"` gives:**
- A) `1234.50`
- B) `1,234.50`
- C) `1.234,50`
- D) `1,234.5`

**13. What's the best way to build a long string from a list of words?**
- A) `text += word` inside a loop
- B) `" ".join(words)`
- C) `str(words)`
- D) `words.join(" ")`

---

### Part B – What's the output?

**14.**
```python
nums = [3, 8, 1, 6]
print([n for n in nums if n > 2])
print(any(n > 7 for n in nums), all(n > 2 for n in nums))
```

**15.**
```python
names = ["Li", "Vishal", "Raj"]
print(sorted(names, key=len))
print(max(names, key=len))
```

**16.**
```python
for score in [70, 85, 40]:
    if score < 50:
        print("fail found")
        break
else:
    print("all passed")
```

---

### Part C – Fix it (make it Pythonic)

**17.** Rewrite in one line:
```python
result = {}
for k, v in zip(keys, values):
    result[k] = v
```

**18.** This turns a real `0` into `10`. Why, and how do you fix it?
```python
def get_count(count=None):
    return count or 10
```

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | One readable line instead of four. | `01_comprehensions.py` |
| 2 | B | Before `for` it picks the value; after `for` it filters. | `01_comprehensions.py` |
| 3 | C | Curly braces with no `key:` give a set. | `01_comprehensions.py` |
| 4 | B | Generators hand out one value at a time. | `01_comprehensions.py` |
| 5 | C | `*` collects the rest into a list. | `02_unpacking.py` |
| 6 | B | The right side is built first, then unpacked. | `02_unpacking.py` |
| 7 | A | `enumerate` gives position and item. | `03_looping_like_a_pro.py` |
| 8 | B | `zip` stops at the shortest (`strict=True` raises). | `03_looping_like_a_pro.py` |
| 9 | A | Empty and zero values are falsy. | `04_truthiness_and_walrus.py` |
| 10 | B | `None` is a single object; `is` checks identity. | `04_truthiness_and_walrus.py` |
| 11 | B | `:=` assigns and returns the value. | `04_truthiness_and_walrus.py` |
| 12 | B | `,` adds thousands separators, `.2f` two decimals. | `05_strings_like_a_pro.py` |
| 13 | B | `join` builds the string once; `+=` copies every time. | `05_strings_like_a_pro.py` |
| 14 | `[3, 8, 6]` then `True False` | 8 > 7; but 1 is not > 2. | `03_looping_like_a_pro.py` |
| 15 | `['Li', 'Raj', 'Vishal']` then `Vishal` | Sorted and compared by length. | `03_looping_like_a_pro.py` |
| 16 | `fail found` | `break` skips the `else`. | `03_looping_like_a_pro.py` |
| 17 | `result = dict(zip(keys, values))` | `zip` pairs, `dict` collects. | `03_looping_like_a_pro.py` |
| 18 | `0` is falsy, so `or` replaces it. Use `return 10 if count is None else count`. | Only treat `None` as "missing". | `04_truthiness_and_walrus.py` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
