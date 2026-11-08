# Module 10 · Advanced functions

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-10.pdf) · [Interview Q&A](INTERVIEW.md)

Functions are objects. Learn to pass them around, make them remember (closures) and wrap them with new behaviour (decorators): the tools behind every Python framework.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Parameters like a pro | [`01_args_and_kwargs.py`](01_args_and_kwargs.py) | `*args`, `**kwargs`, keyword-only, the mutable-default trap |
| Scope & closures | [`02_scope_and_closures.py`](02_scope_and_closures.py) | LEGB, `nonlocal`, functions that remember |
| Functions are objects | [`03_first_class_functions.py`](03_first_class_functions.py) | pass, store and return functions; `partial` |
| Decorators | [`04_decorators.py`](04_decorators.py) | build `@timer` and `@retry(times=3)` step by step |
| functools | [`05_functools.py`](05_functools.py) | `lru_cache`, `reduce`, `singledispatch` |
| Demo: resilient API client | [`06_demo_api_client.py`](06_demo_api_client.py) | stacked decorators: log, cache, retry |
| Recursion | [`07_recursion.py`](07_recursion.py) | base case, call stack, memoisation, `RecursionError` |

```bash
python 10_advanced_functions/01_args_and_kwargs.py
```

## Exercise: Write your own decorators

`@count_calls`, `@require_positive` and a hand-made `@memoize`.

- Start here: [`exercises/ex10_decorators.py`](../exercises/ex10_decorators.py)
- Solution: [`solutions/ex10_decorators.py`](../solutions/ex10_decorators.py)

## Knowledge check

Preparing for interviews? Read the [Module 10 interview questions](INTERVIEW.md): short answers you can say out loud.


Test yourself with the [Module 10 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 11 · Iterators & generators](../11_iterators_generators/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
