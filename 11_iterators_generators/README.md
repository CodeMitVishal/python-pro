# Module 11 · Iterators & generators

[← Back to the course](../README.md) · [Slides](../slides/python-pro-slides.pdf)

Process data one item at a time. Generators let you handle a 10 GB file with the memory of a 10-line one, and build lazy pipelines.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| How for really works | [`01_iteration_protocol.py`](01_iteration_protocol.py) | `iter()`, `next()`, `StopIteration`, your own iterator |
| Generators | [`02_generators.py`](02_generators.py) | `yield` pauses and resumes; 200 bytes vs 8 MB |
| Lazy pipelines | [`03_pipelines.py`](03_pipelines.py) | chain generators like an assembly line |
| itertools | [`04_itertools.py`](04_itertools.py) | `islice`, `chain`, `groupby`, `pairwise`, `product`... |
| Demo: a 200,000-row CSV | [`05_demo_big_csv.py`](05_demo_big_csv.py) | 56 MB eager vs 0.05 MB lazy, measured |
| send() & async generators | [`06_send_and_async_generators.py`](06_send_and_async_generators.py) | two-way generators, `async for`, streaming pages |

```bash
python 11_iterators_generators/01_iteration_protocol.py
```

## Exercise: Write lazy generators

`chunked()`, `running_average()` and `valid_numbers()`; they must work on endless streams.

- Start here: [`exercises/ex11_generators.py`](../exercises/ex11_generators.py)
- Solution: [`solutions/ex11_generators.py`](../solutions/ex11_generators.py)

## Knowledge check

Test yourself with the [Module 11 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 12 · Advanced OOP](../12_advanced_oop/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
