# Module 8 · Pythonic code

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-08.pdf) · [Interview Q&A](INTERVIEW.md)

**Same results, half the code.** Learn the small tools that make Python
code short, clear and idiomatic: the way experienced Python developers write it.

## Lessons

Run them in this order. Each file is commented line by line and shows the
expected output next to every `print`.

| Lesson | File | Key idea |
|---|---|---|
| Comprehensions | [`01_comprehensions.py`](01_comprehensions.py) | build lists, dicts and sets in one line |
| Unpacking | [`02_unpacking.py`](02_unpacking.py) | `a, b = b, a`, `first, *rest = xs`, `**dict` |
| Looping like a pro | [`03_looping_like_a_pro.py`](03_looping_like_a_pro.py) | `enumerate`, `zip`, `sorted(key=)`, `any`/`all` |
| Truthiness & walrus | [`04_truthiness_and_walrus.py`](04_truthiness_and_walrus.py) | falsy values, `is None`, `:=` |
| Strings like a pro | [`05_strings_like_a_pro.py`](05_strings_like_a_pro.py) | f-string formatting, `join`, `split` |
| Demo: grade report | [`06_demo_grade_report.py`](06_demo_grade_report.py) | everything above in one program |
| Pattern matching | [`07_pattern_matching.py`](07_pattern_matching.py) | `match`/`case` on values, sequences, dicts and classes |
| Regular expressions | [`08_regex.py`](08_regex.py) | search, named groups, `sub`, validation |

```bash
python 08_pythonic_code/01_comprehensions.py
```

## Exercise: Refactor to Pythonic code

Nine working-but-clunky functions. Rewrite each one with the tool that fits.

- Start here: [`exercises/ex08_refactor_to_pythonic.py`](../exercises/ex08_refactor_to_pythonic.py)
- Solution: [`solutions/ex08_refactor_to_pythonic.py`](../solutions/ex08_refactor_to_pythonic.py)

## Knowledge check

Preparing for interviews? Read the [Module 8 interview questions](INTERVIEW.md): short answers you can say out loud.


Test yourself with the [Module 8 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 9 · Data structures deep dive](../09_data_structures/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
