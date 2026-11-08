# Module 19 · Performance & internals

[← Back to the course](../README.md) · [Slides](../slides/python-pro-slides.pdf)

Understand what Python does under the hood, then make code fast the right way: measure first, then fix the real hotspot.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| The memory model | [`01_memory_model.py`](01_memory_model.py) | names vs objects, reference counting, `is` vs `==`, GC |
| Measure first | [`02_measure_first.py`](02_measure_first.py) | `timeit` and `cProfile` |
| Speed tricks that matter | [`03_speed_tricks.py`](03_speed_tricks.py) | 309x from a data structure, caching, built-ins |
| Memory tricks | [`04_memory_tricks.py`](04_memory_tricks.py) | `tracemalloc`, `__slots__`, generators |
| Bytecode, weakref & NumPy | [`05_bytecode_and_numpy.py`](05_bytecode_and_numpy.py) | `dis`, weak caches, vectorisation |

```bash
python 19_performance_internals/01_memory_model.py
```

## Exercise: Make it fast

Speed up three slow functions until they fit a 0.1 s budget.

- Start here: [`exercises/ex19_make_it_fast.py`](../exercises/ex19_make_it_fast.py)
- Solution: [`solutions/ex19_make_it_fast.py`](../solutions/ex19_make_it_fast.py)

## Knowledge check

Test yourself with the [Module 19 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 20 · Capstone project](../20_capstone/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
