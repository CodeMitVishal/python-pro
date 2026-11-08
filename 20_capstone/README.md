# Module 20 · Capstone project

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-20.pdf)

Everything together: `budget`, a tested, typed, packaged expense tracker with a CLI and a REST API, built in clean layers.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| The project | [`budget_project/`](budget_project/) | src layout, service layer, repository, CLI, API |
| Architecture & module map | [`budget_project/README.md`](budget_project/README.md) | which module shows up where |
| Tests | [`budget_project/tests/`](budget_project/tests/) | service and API tests with fixtures |

```bash
pip install -e "20_capstone/budget_project[dev]"
```

```bash
budget add 320 food "groceries"
```

```bash
budget summary
```

From inside `budget_project`, `pytest`, `mypy` and `ruff check .` must all pass.

## Exercise: Capstone challenges

8 features in 3 levels: CSV export, filtered endpoints, recurring expenses, a second repository and more.

- Start here: [`exercises/ex20_capstone_challenges.md`](../exercises/ex20_capstone_challenges.md)

## Knowledge check

Take the [final exam](QUIZ.md): 20 questions across the whole course.

**Next up:** the web development track → [Module 21 · HTTP fundamentals, Flask & Jinja2](../21_web_flask/README.md)

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
