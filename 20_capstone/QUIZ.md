# Python Pro – Final Exam
**Modules 8–20: are you a Python pro?**

20 questions across the whole course. Score 16+ and you're ready for real-world
Python work. The answer key says which module to revisit.

---

**1.** Rewrite in one line: `out = []` / `for x in xs:` / `if x > 0: out.append(x * 2)`

**2.** `a, *b = "pro"`. What are `a` and `b`?

**3.** You check `if user_id in ids` 100,000 times. What should `ids` be, and why?

**4.** What's wrong with `items: list = []` in a `@dataclass`?

**5.** What does this print?
```python
def make():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc
f = make(); f(); print(f())
```

**6.** Write a decorator `@twice` that calls the function two times and returns the second result.

**7.** Why does `sum(x * x for x in range(10**8))` barely use any memory?

**8.** What happens if you loop over the same generator object twice?

**9.** You defined `__eq__` on a class. What else do you need so instances work in a `set`?

**10.** `class D(B, C)` where `B` and `C` both inherit from `A`. In what order does `super()` visit the classes?

**11.** ABC or Protocol: you want to accept any object with a `.send(msg)` method, including classes from libraries you can't change. Which one?

**12.** What's wrong with `except: pass`?

**13.** Write the skeleton of a context manager with `@contextmanager` that prints "start" and "end", and makes sure "end" is printed even when the body raises.

**14.** What does `if __name__ == "__main__":` protect against?

**15.** What does `pip install -e .` give you during development?

**16.** mypy says: `Item "None" of "User | None" has no attribute "name"`. What's the fix?

**17.** How do you test that a function raises `ValueError` with pytest?

**18.** Downloading 500 web pages, or resizing 500 images in pure Python: which one uses threads/asyncio, and which uses processes?

**19.** Why is this dangerous, and how do you fix it?
```python
conn.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

**20.** Your program is slow. What's the first thing you do?

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Revisit |
|---|--------|---------|
| 1 | `out = [x * 2 for x in xs if x > 0]` | Module 8 |
| 2 | `a = 'p'`, `b = ['r', 'o']` | Module 8 |
| 3 | A `set`: `in` is O(1) instead of O(n) | Module 9 |
| 4 | It would be shared by every object. Use `field(default_factory=list)` (dataclasses actually refuse it). | Module 9 |
| 5 | `2` | Module 10 |
| 6 | `def twice(f):` / `@functools.wraps(f)` / `def w(*a, **k): f(*a, **k); return f(*a, **k)` / `return w` | Module 10 |
| 7 | It's a generator expression: one value at a time | Module 11 |
| 8 | The second loop gets nothing: generators are used up | Module 11 |
| 9 | `__hash__`, consistent with `__eq__` | Module 12 |
| 10 | D → B → C → A (the MRO) | Module 12 |
| 11 | `Protocol` (structural typing) | Module 12 |
| 12 | It hides every error, even Ctrl+C. Catch specific exceptions. | Module 13 |
| 13 | `print("start")` / `try: yield` / `finally: print("end")` | Module 13 |
| 14 | Code running when the file is imported (tests, process workers) | Modules 14, 17 |
| 15 | An editable install: changes apply without reinstalling | Module 14 |
| 16 | Check `if user is None:` before using `user.name` | Module 15 |
| 17 | `with pytest.raises(ValueError): func(...)` | Module 16 |
| 18 | Downloads: threads/asyncio (waiting). Images: processes (CPU, GIL). | Module 17 |
| 19 | SQL injection. Use `conn.execute("... WHERE email = ?", (email,))` | Module 18 |
| 20 | Measure: profile with cProfile and find the hotspot before changing anything | Module 19 |

</details>

---

🎓 **Finished the course?** Share your capstone on LinkedIn and tag me. I'd love to see it!

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
