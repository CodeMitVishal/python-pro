# Module 14 · Interview questions (with answers)

Short answers you can say out loud, with code and the usual follow-up.

[← Module 14](README.md) · [Quiz](QUIZ.md)

---

### 1. Module vs package?

**Say:** A **module** is one `.py` file. A **package** is a folder of modules, usually with `__init__.py`, that you import with dots: `tasky.store`. A **distribution** (what pip installs) can contain several packages.

---

### 2. What does `if __name__ == "__main__":` do?

**Say:** `__name__` is `"__main__"` only for the file you run directly. Imported modules get their own name. Code behind the guard (demos, CLI entry points) therefore doesn't run on import.

---

### 3. How does `import` find a module?

**Say:** It checks the `sys.modules` cache first. If the module isn't there, it searches `sys.path` in order: the script's folder, `PYTHONPATH`, the venv's `site-packages`, then the standard library. The module's code runs **once**; later imports reuse the cached object.

---

### 4. What causes circular imports, and how do you fix them?

**Say:** Two modules import each other at the top level, so one sees the other half-initialised. Fixes, from best to worst:
1. Move the shared code into a third module so dependencies point one way.
2. Import inside a function.
3. For type hints only, use `if TYPE_CHECKING:` plus `from __future__ import annotations`.

---

### 5. Why use virtual environments?

**Say:** Each project gets its **own** interpreter and libraries, so versions don't clash between projects and you don't break the system Python. Create one with `python -m venv .venv` or `uv venv`, and keep it out of git.

---

### 6. `requirements.txt` vs `pyproject.toml` vs a lock file?

**Say:**
- **`pyproject.toml`** is the standard project file: metadata, **direct** dependencies with version ranges, entry points, tool settings.
- A **lock file** (`uv.lock`, `poetry.lock`, or a pip-tools `requirements.txt` with `==` pins and hashes) records the **exact** resolved versions, so CI and production are reproducible.
- A plain `requirements.txt` is the older, simpler way.

---

### 7. What does `pip install -e .` do?

**Say:** It's an **editable** install. The project is installed by linking to your source folder, so code changes take effect without reinstalling, and console scripts from `[project.scripts]` become real commands.

---

### 8. Absolute vs relative imports?

**Say:** An absolute import uses the full path (`from tasky.store import Store`). A relative import (`from .store import Store`) works only inside packages. PEP 8 prefers absolute imports. Relative imports are fine inside a package's own modules.

---

### 9. What is `__init__.py` for?

**Say:** It marks a folder as a regular package and runs on first import. It's commonly used to define the **public API** (`from .store import Store`, `__all__ = [...]`) and the package version. Keep it light, with no heavy work at import time.

---

### 10. How do you build a CLI in Python?

**Say:** `argparse` from the standard library (subcommands, types, choices, auto `--help`), or `click`/`typer` for bigger tools. Expose it through `[project.scripts]` in `pyproject.toml` so `pip install` creates the command. Keep the logic in importable functions so you can test it.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
