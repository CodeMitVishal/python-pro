# Module 13 · Errors, context managers & logging

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-13.pdf) · [Interview Q&A](INTERVIEW.md)

Fail safely and leave a clear trail: custom exception families, guaranteed clean-up with `with`, and logging instead of print.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Exceptions like a pro | [`01_exception_hierarchy.py`](01_exception_hierarchy.py) | custom families, `raise ... from`, EAFP |
| Context managers | [`02_context_managers.py`](02_context_managers.py) | `__enter__`/`__exit__`, `@contextmanager`, rollback |
| logging | [`03_logging.py`](03_logging.py) | levels, formats, handlers, `log.exception()` |
| Demo: robust order importer | [`04_demo_order_importer.py`](04_demo_order_importer.py) | skip bad rows, or roll back the whole batch |
| ExitStack & exception groups | [`05_exitstack_and_groups.py`](05_exitstack_and_groups.py) | many context managers at once, `except*` |
| Debugging like a pro | [`06_debugging_like_a_pro.py`](06_debugging_like_a_pro.py) | `pdb`/`breakpoint()`, post-mortem, `faulthandler`, VS Code launch.json |

```bash
python 13_errors_context_logging/01_exception_hierarchy.py
```

## Exercise: Safe bank transfers

A custom `InsufficientFunds` error and an `atomic()` context manager that rolls back failed transfers.

- Start here: [`exercises/ex13_bank_transfer.py`](../exercises/ex13_bank_transfer.py)
- Solution: [`solutions/ex13_bank_transfer.py`](../solutions/ex13_bank_transfer.py)

## Knowledge check

Preparing for interviews? Read the [Module 13 interview questions](INTERVIEW.md): short answers you can say out loud.

Test yourself with the [Module 13 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 14 · Project structure & packaging](../14_packaging/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
