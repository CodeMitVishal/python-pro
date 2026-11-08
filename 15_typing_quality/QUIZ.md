# Python Pro – Module 15 Knowledge Check
**Type hints & code quality**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson file to revisit.

---

### Part A – Multiple choice

**1. Does Python check type hints when the code runs?**
- A) Yes, always
- B) No; tools like mypy and your editor check them
- C) Only in functions
- D) Only with `-O`

**2. What's the modern way to write "a list of ints"?**
- A) `List(int)`
- B) `list[int]`
- C) `[int]`
- D) `array<int>`

**3. A function returns a float, or `None` when nothing is found. What's the return type?**
- A) `float`
- B) `float | None`
- C) `None`
- D) `Any`

**4. Which type restricts a value to exactly `"debug"`, `"info"` or `"error"`?**
- A) `str`
- B) `Enum[str]`
- C) `Literal["debug", "info", "error"]`
- D) `Final[str]`

**5. What is `TypedDict` for?**
- A) Making dicts faster
- B) Describing a dict with known keys and value types (for example JSON records)
- C) Sorting dict keys
- D) Freezing a dict

**6. `def first(items: list[T]) -> T`. What does the `TypeVar` express?**
- A) The function returns any type
- B) The return type is the same as the type of the list's items
- C) T must be an int
- D) Nothing

**7. How do you type "a function that takes a float and returns a float"?**
- A) `function(float)`
- B) `Callable[[float], float]`
- C) `lambda[float]`
- D) `def[float, float]`

**8. What does mypy do?**
- A) Runs your code faster
- B) Reads your code and reports type errors without running it
- C) Formats your code
- D) Installs packages

**9. What does `mypy --strict` add?**
- A) Nothing
- B) It requires hints everywhere and enables many extra checks
- C) It runs the tests
- D) It deletes untyped code

**10. What's the difference between a linter and a formatter?**
- A) None
- B) A linter finds likely bugs and bad patterns; a formatter only fixes layout
- C) A formatter finds bugs
- D) A linter compiles the code

**11. Which ruff rule flags `if x == None:`?**
- A) F401
- B) E711
- C) E501
- D) I001

---

### Part B – What does mypy say?

**12.**
```python
def plan(user: dict[str, str] | None) -> str:
    return user["plan"]
```

**13.**
```python
def label(n: int) -> str:
    return "Orders: " + n
```

---

### Part C – Fix it

**14.** Add type hints:
```python
def average(values):
    return sum(values) / len(values) if values else None
```

**15.** mypy reports `Item "None" of "User | None" has no attribute "name"`. Fix it:
```python
def greet(user_id: int) -> str:
    user = find_user(user_id)          # returns User | None
    return f"Hi {user.name}"
```

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | Hints are stored, not enforced. | `01_type_hints_basics.py` |
| 2 | B | Built-in generics since Python 3.9. | `01_type_hints_basics.py` |
| 3 | B | `X \| None` (older code: `Optional[X]`). | `01_type_hints_basics.py` |
| 4 | C | Only those exact values are allowed. | `02_advanced_typing.py` |
| 5 | B | Known keys, known value types. | `02_advanced_typing.py` |
| 6 | B | Generic: str in → str out. | `02_advanced_typing.py` |
| 7 | B | `Callable[[args], return]`. | `02_advanced_typing.py` |
| 8 | B | Static type checking. | `03_mypy_catches_bugs.py` |
| 9 | B | Stricter rules, no missing hints. | `ex15_add_type_hints.py` |
| 10 | B | ruff does both. | `04_ruff_and_style.py` |
| 11 | B | Use `is None`. | `04_ruff_and_style.py` |
| 12 | An error: the value can be `None` (not indexable). | Check `if user is None` first. | `03_mypy_catches_bugs.py` |
| 13 | `Unsupported operand types for + ("str" and "int")` | Use `f"Orders: {n}"`. | `03_mypy_catches_bugs.py` |
| 14 | `def average(values: list[float]) -> float \| None:` | It can return `None`. | `01_type_hints_basics.py` |
| 15 | `if user is None: return "Hi guest"` before using `user.name`. | Handle the `None` case. | `ex15_add_type_hints.py` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
