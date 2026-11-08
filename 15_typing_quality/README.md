# Module 15 · Type hints & code quality

[← Back to the course](../README.md) · [Slides](../slides/python-pro-slides.pdf)

Catch bugs before you run the code. Type hints, mypy and ruff are what make big Python codebases maintainable.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Type hints | [`01_type_hints_basics.py`](01_type_hints_basics.py) | `list[int]`, `X | None`, aliases |
| Advanced typing | [`02_advanced_typing.py`](02_advanced_typing.py) | `Literal`, `TypedDict`, `Callable`, `TypeVar`, `Final` |
| mypy catches bugs | [`03_mypy_catches_bugs.py`](03_mypy_catches_bugs.py) | 3 hidden crashes found without running anything |
| ruff & style | [`04_ruff_and_style.py`](04_ruff_and_style.py) | linting vs formatting, messy vs clean code |

Install the tools:

```bash
pip install mypy ruff
```

```bash
mypy 15_typing_quality/03_mypy_catches_bugs.py
```

```bash
ruff check 15_typing_quality/04_ruff_and_style.py
```

## Exercise: Add type hints, let mypy find the bug

Type an untyped module until `mypy --strict` passes, and fix the bug it reveals.

- Start here: [`exercises/ex15_add_type_hints.py`](../exercises/ex15_add_type_hints.py)
- Solution: [`solutions/ex15_add_type_hints.py`](../solutions/ex15_add_type_hints.py)

## Knowledge check

Test yourself with the [Module 15 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 16 · Testing with pytest](../16_testing/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
