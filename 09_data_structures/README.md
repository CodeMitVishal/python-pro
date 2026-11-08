# Module 9 · Data structures deep dive

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-09.pdf) · [Interview Q&A](INTERVIEW.md)

**Pick the right container and your code stays fast.** See how lists, dicts
and sets work inside, measure the difference with Big-O, and meet the
specialised tools in `collections` and `dataclasses`.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Big-O | [`01_big_o.py`](01_big_o.py) | measure list vs set lookups: O(n) vs O(1) |
| Lists & tuples under the hood | [`02_lists_and_tuples.py`](02_lists_and_tuples.py) | dynamic arrays, append vs insert, copy traps |
| Dicts, sets & hashing | [`03_dicts_and_sets.py`](03_dicts_and_sets.py) | `hash()`, hashable keys, set operations |
| The collections module | [`04_collections.py`](04_collections.py) | `Counter`, `defaultdict`, `deque`, `namedtuple` |
| dataclasses | [`05_dataclasses.py`](05_dataclasses.py) | `@dataclass`, `field`, `frozen`, `order` |
| Demo: log analyzer | [`06_demo_log_analyzer.py`](06_demo_log_analyzer.py) | one question, one right data structure |
| Enums | [`07_enums.py`](07_enums.py) | `StrEnum`, `IntEnum`, `Flag`, enums in `match` |
| heapq & bisect | [`08_heapq_and_bisect.py`](08_heapq_and_bisect.py) | priority queues, top-k, sorted inserts |

```bash
python 09_data_structures/01_big_o.py
```

`01_big_o.py` times real lookups, so your numbers will differ from the
slides, but the pattern is always the same.

## Exercise: Library tracker

Fill in 6 TODOs, each with the data structure that fits the job.

- Start here: [`exercises/ex09_library_tracker.py`](../exercises/ex09_library_tracker.py)
- Solution: [`solutions/ex09_library_tracker.py`](../solutions/ex09_library_tracker.py)

## Knowledge check

Preparing for interviews? Read the [Module 9 interview questions](INTERVIEW.md): short answers you can say out loud.

Test yourself with the [Module 9 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 10 · Advanced functions](../10_advanced_functions/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
