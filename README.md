# Python Pro

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![YouTube: CodeMitVishal](https://img.shields.io/badge/YouTube-CodeMitVishal-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/@CodeMitVishal)
[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-support%20us-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/codemitvishal)

**From Python Foundations to professional Python: deep, but simple.**

You know variables, loops, functions and classes. Now learn how experienced
Python developers actually write code: clean and idiomatic, fast, tested,
typed, packaged and ready for real projects. Every concept is explained step
by step, with a runnable example you can play with.

New to Python? Start with **[Python Foundations](https://github.com/CodeMitVishal/python-foundations)**
(Modules 1–7) first. This course continues from Module 8.

## What's inside every module

| | |
|---|---|
| 📊 **Slides** | 74 slides with diagrams and cheat-sheet tables: [`slides/python-pro-slides.pdf`](slides/python-pro-slides.pdf) |
| 💻 **Runnable lessons** | One small file per idea, commented line by line, with the expected output |
| 🧪 **Exercise + solution** | A starter file with built-in checks, and a worked solution |
| 🧩 **Quiz** | Test yourself; every answer tells you which lesson to revisit |

## Course map

| # | Module | You'll be able to… | Status |
|---|---|---|---|
| 08 | [Pythonic code](08_pythonic_code/README.md) | write short, idiomatic Python | ✅ Ready |
| 09 | [Data structures deep dive](09_data_structures/README.md) | pick the right structure, understand Big-O | ✅ Ready |
| 10 | [Advanced functions](10_advanced_functions/README.md) | write closures and decorators | ✅ Ready |
| 11 | [Iterators & generators](11_iterators_generators/README.md) | process big data lazily | ✅ Ready |
| 12 | [Advanced OOP](12_advanced_oop/README.md) | design clean classes (dunders, ABCs, SOLID) | ✅ Ready |
| 13 | [Errors, context managers & logging](13_errors_context_logging/README.md) | fail safely and log clearly | ✅ Ready |
| 14 | [Project structure & packaging](14_packaging/README.md) | ship an installable command-line tool | ✅ Ready |
| 15 | [Type hints & code quality](15_typing_quality/README.md) | catch bugs before you run the code | ✅ Ready |
| 16 | [Testing with pytest](16_testing/README.md) | prove your code works | ✅ Ready |
| 17 | [Concurrency](17_concurrency/README.md) | use threads, processes and asyncio | ✅ Ready |
| 18 | [Data, APIs & databases](18_data_apis_databases/README.md) | build a REST API backed by a database | ✅ Ready |
| 19 | [Performance & internals](19_performance_internals/README.md) | profile and speed up real code | ✅ Ready |
| 20 | [Capstone project](20_capstone/README.md) | build a full project, end to end | ✅ Ready |

## How to study

1. **Read the slides** for the module (or watch the video when it's out).
2. **Run each lesson file** in order and change things to see what happens.
3. **Do the exercise.** Run it: the built-in checks tell you when you're right.
4. **Take the quiz.** Stuck on a question? The answer key points to the lesson to revisit.

## Quick start

You need **Python 3.10 or newer**. Modules 8–13 use only the standard library.

```bash
git clone https://github.com/CodeMitVishal/python-pro.git
```

```bash
cd python-pro
```

```bash
python 08_pythonic_code/01_comprehensions.py
```

From Module 14 on you'll use pytest, mypy, ruff, requests and FastAPI.
Install them once, ideally inside a virtual environment:

```bash
pip install -r requirements.txt
```

## Submit your exercise

Finished an exercise? Open a **Pull Request** with your solution in your own
folder (for example `submissions/<your-github-name>/ex08.py`) and I'll review
your code.

## Rebuild the slides

The slide source is [`slides/src/python-pro-slides.html`](slides/src/python-pro-slides.html).
Modules 8–9 are written by hand; Modules 10–20 are generated from compact data by
[`slides/src/build_module_slides.py`](slides/src/build_module_slides.py):

```bash
python slides/src/build_module_slides.py
```

Then open the HTML in a browser, or print it to PDF at 1920 × 1080 with no margins.

## Support the channel

If this course helps you:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it ⭐
