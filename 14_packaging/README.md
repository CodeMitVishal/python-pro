# Module 14 · Project structure & packaging

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-14.pdf) · [Interview Q&A](INTERVIEW.md)

Turn scripts into a real, installable project with a command-line tool: modules, imports, `pyproject.toml`, the src layout and argparse.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Modules & imports | [`01_modules_and_imports.py`](01_modules_and_imports.py) | `sys.path`, caching, `__name__ == "__main__"` |
| CLIs with argparse | [`02_cli_with_argparse.py`](02_cli_with_argparse.py) | subcommands, flags, types, `--help` |
| A real package: tasky | [`tasky_project/`](tasky_project/) | src layout, `pyproject.toml`, the `tasky` command, tests |
| Publishing & tooling | [`03_publishing_and_tooling.md`](03_publishing_and_tooling.md) | PyPI, uv, pre-commit |

Install the example package:

```bash
pip install -e 14_packaging/tasky_project
```

```bash
tasky add "Learn packaging"
```

See [`tasky_project/README.md`](tasky_project/README.md) for the full walkthrough.

## Exercise: Build a CLI tool

`wordtool stats` and `wordtool top --n 3` with argparse; `main(argv)` makes it testable.

- Start here: [`exercises/ex14_wordtool_cli.py`](../exercises/ex14_wordtool_cli.py)
- Solution: [`solutions/ex14_wordtool_cli.py`](../solutions/ex14_wordtool_cli.py)

## Knowledge check

Preparing for interviews? Read the [Module 14 interview questions](INTERVIEW.md): short answers you can say out loud.


Test yourself with the [Module 14 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 15 · Type hints & code quality](../15_typing_quality/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
