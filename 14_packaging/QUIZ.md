# Python Pro – Module 14 Knowledge Check
**Project structure & packaging**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson or file to revisit.

---

### Part A – Multiple choice

**1. What's the difference between a module and a package?**
- A) There is none
- B) A module is one `.py` file; a package is a folder of modules
- C) A package is always on PyPI
- D) A module must have a class

**2. You import the same module in 5 files. How many times does its top-level code run?**
- A) 5
- B) Once; later imports reuse `sys.modules`
- C) Never
- D) Every time a function is called

**3. Where does Python look for modules?**
- A) Only the current folder
- B) The folders in `sys.path`, in order
- C) The internet
- D) The Windows registry

**4. What is `if __name__ == "__main__":` for?**
- A) It makes the code faster
- B) Code below it runs only when the file is run directly, not when it's imported
- C) It's required in every file
- D) It defines the main class

**5. Which file describes a modern Python project (name, version, dependencies, commands)?**
- A) `setup.cfg` only
- B) `pyproject.toml`
- C) `requirements.txt`
- D) `__init__.py`

**6. What does `pip install -e .` do?**
- A) Installs from PyPI
- B) An editable install: code changes apply without reinstalling
- C) Deletes the package
- D) Installs only the tests

**7. What does `[project.scripts] tasky = "tasky.cli:main"` create?**
- A) A test
- B) A `tasky` terminal command that calls `main()` in `tasky/cli.py`
- C) A new package
- D) A virtual environment

**8. Which file makes `python -m tasky` work?**
- A) `__init__.py`
- B) `__main__.py`
- C) `cli.py`
- D) `pyproject.toml`

**9. Why keep `store.py` (logic) separate from `cli.py` (argparse + print)?**
- A) Python requires it
- B) The logic can be reused and tested without the command line
- C) It's faster
- D) argparse only works in cli.py

**10. In argparse, what does `action="store_true"` create?**
- A) A required argument
- B) A flag that's `False` by default and `True` when given
- C) A subcommand
- D) A list of values

**11. Why should `main()` return a non-zero exit code on failure?**
- A) It's faster
- B) Scripts and CI pipelines can detect that the command failed
- C) It prints the error
- D) It isn't needed

---

### Part B – What's the output?

**12.** `parser.add_argument("--times", type=int, default=1)`. The user types `--times 3`. What is `args.times`?

**13.**
```python
# helpers.py
print("loading helpers")
def hi(): return "hi"

# main.py
import helpers
import helpers
print(helpers.hi())
```
What does `python main.py` print?

---

### Part C – Fix it

**14.** Importing `report.py` in a test immediately sends 1,000 emails. Fix the end of the file:
```python
def main():
    send_all_emails()

main()
```

**15.** Write the `pyproject.toml` line that installs `requests` 2.31 or newer as a dependency.

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | A package groups modules. | `01_modules_and_imports.py` |
| 2 | B | Modules are cached in `sys.modules`. | `01_modules_and_imports.py` |
| 3 | B | The script's folder first, then the rest of `sys.path`. | `01_modules_and_imports.py` |
| 4 | B | It's `"__main__"` only when run directly. | `01_modules_and_imports.py` |
| 5 | B | The modern standard. | `tasky_project/pyproject.toml` |
| 6 | B | It links to your source folder. | `tasky_project/README.md` |
| 7 | B | An entry-point console script. | `tasky_project/pyproject.toml` |
| 8 | B | `python -m pkg` runs `pkg/__main__.py`. | `tasky_project/src/tasky/__main__.py` |
| 9 | B | Separate logic from interface. | `tasky_project/src/tasky/` |
| 10 | B | A boolean flag. | `02_cli_with_argparse.py` |
| 11 | B | Exit code 0 = success, anything else = failure. | `tasky_project/src/tasky/cli.py` |
| 12 | `3`, an int | `type=int` converts it. | `02_cli_with_argparse.py` |
| 13 | `loading helpers` once, then `hi` | The second import is cached. | `01_modules_and_imports.py` |
| 14 | `if __name__ == "__main__":` then `main()` | Importing no longer runs it. | `01_modules_and_imports.py` |
| 15 | `dependencies = ["requests>=2.31"]` | Under `[project]`. | `tasky_project/pyproject.toml` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
