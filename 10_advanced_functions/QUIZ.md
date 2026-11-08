# Python Pro – Module 10 Knowledge Check
**Advanced functions**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson file to revisit.

---

### Part A – Multiple choice

**1. In `def f(*args, **kwargs)`, what types are `args` and `kwargs`?**
- A) list and dict
- B) tuple and dict
- C) dict and tuple
- D) tuple and list

**2. In `def connect(host, *, port=443)`, what does the `*` do?**
- A) Collects extra arguments
- B) Makes `port` keyword-only
- C) Makes `host` optional
- D) Multiplies the arguments

**3. Why is `def add(item, basket=[])` a bug?**
- A) Lists can't be default values
- B) The default list is created once and shared by every call
- C) `basket` becomes a tuple
- D) It isn't a bug

**4. In which order does Python look up a name?**
- A) Global, Local, Built-in, Enclosing
- B) Local, Enclosing, Global, Built-in
- C) Built-in, Global, Enclosing, Local
- D) Local, Global only

**5. What is a closure?**
- A) A function that closes files
- B) An inner function that remembers variables from its outer function
- C) A function with no return value
- D) A class with one method

**6. When do you need `nonlocal`?**
- A) To read a global variable
- B) To assign to a variable of the enclosing function
- C) To import a module
- D) To make a variable private

**7. What does `@timer` above `def f():` do?**
- A) Calls `timer` every second
- B) Replaces `f` with `timer(f)`
- C) Adds a type hint
- D) Makes `f` run in the background

**8. Why use `functools.wraps` in a decorator?**
- A) It makes the wrapper faster
- B) It keeps the original function's name and docstring
- C) It adds caching
- D) It's required syntax

**9. A decorator that takes arguments, like `@retry(times=3)`, needs how many nested functions?**
- A) 1
- B) 2
- C) 3
- D) 4

**10. When is `@lru_cache` safe to use?**
- A) On any function
- B) On pure functions: same input, same output, no side effects
- C) Only on methods
- D) Only on functions with no arguments

**11. What does `partial(power, exp=2)` return?**
- A) The number 2
- B) A new function with `exp` already filled in
- C) A tuple
- D) An error

---

### Part B – What's the output?

**12.**
```python
def make_counter():
    count = 0
    def nxt():
        nonlocal count
        count += 1
        return count
    return nxt

a, b = make_counter(), make_counter()
print(a(), a(), b())
```

**13.**
```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])
```

**14.**
```python
def shout(func):
    def wrapper(*args):
        return func(*args).upper()
    return wrapper

@shout
def greet(name):
    return f"hi {name}"

print(greet("vishal"), greet.__name__)
```

---

### Part C – Fix it

**15.** This decorator breaks every function it wraps: they all return `None`. Why?
```python
def log(func):
    def wrapper(*args, **kwargs):
        print("calling", func.__name__)
        func(*args, **kwargs)
    return wrapper
```

**16.** Fix the mutable default:
```python
def register(user, users=[]):
    users.append(user)
    return users
```

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | Extra positionals → tuple, extra keywords → dict. | `01_args_and_kwargs.py` |
| 2 | B | Everything after `*` must be passed by name. | `01_args_and_kwargs.py` |
| 3 | B | Defaults are evaluated once, at definition time. | `01_args_and_kwargs.py` |
| 4 | B | LEGB. | `02_scope_and_closures.py` |
| 5 | B | It keeps the outer variables alive. | `02_scope_and_closures.py` |
| 6 | B | Reading works without it; assigning needs it. | `02_scope_and_closures.py` |
| 7 | B | `@` is shorthand for `f = timer(f)`. | `04_decorators.py` |
| 8 | B | Otherwise every function is called "wrapper". | `04_decorators.py` |
| 9 | C | `retry(times)` → `decorator(func)` → `wrapper(*args)`. | `04_decorators.py` |
| 10 | B | Caching an impure function returns stale results. | `05_functools.py` |
| 11 | B | It pre-fills arguments. | `03_first_class_functions.py` |
| 12 | `1 2 1` | Each counter keeps its own `count`. | `02_scope_and_closures.py` |
| 13 | `[2, 2, 2]` | Late binding: all lambdas see the last `i`. Fix: `lambda i=i: i`. | `02_scope_and_closures.py` |
| 14 | `HI VISHAL wrapper` | Without `functools.wraps`, the name is lost. | `04_decorators.py` |
| 15 | The wrapper doesn't `return func(...)`. | Always return the result. | `04_decorators.py` |
| 16 | `def register(user, users=None):` then `if users is None: users = []`. | A new list on every call. | `01_args_and_kwargs.py` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
