# Module 14 · Publishing to PyPI and modern tooling

## 1. Build and publish a package

Your `pyproject.toml` already describes the package (see `tasky_project/`). Publishing is two steps:

```bash
pip install build twine
```

```bash
python -m build
```

This creates `dist/tasky-0.1.0.tar.gz` (source) and `dist/tasky-0.1.0-py3-none-any.whl` (a wheel: ready to install).

```bash
twine upload --repository testpypi dist/*
```

Always try **TestPyPI** first (test.pypi.org). When it works, upload to the real PyPI with `twine upload dist/*`, and anyone can `pip install tasky`.

Good habits:
- **Semantic versioning**: `MAJOR.MINOR.PATCH`. Breaking change → MAJOR, new feature → MINOR, bug fix → PATCH.
- Never re-upload the same version. Bump the version in `pyproject.toml` first.
- Publish from CI with **trusted publishing** (GitHub Actions + PyPI, no API token stored anywhere).

## 2. uv: a very fast all-in-one tool

[uv](https://docs.astral.sh/uv/) replaces pip, venv, pip-tools and pyenv, and is 10–100× faster.

| Task | pip/venv | uv |
|---|---|---|
| create a venv | `python -m venv .venv` | `uv venv` |
| install deps | `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| new project | write pyproject by hand | `uv init tasky` |
| add a dependency | edit pyproject + pip install | `uv add requests` |
| exact, locked versions | pip freeze | `uv lock` → `uv.lock` |
| run in the project env | activate, then run | `uv run pytest` |
| install a Python version | download installer | `uv python install 3.12` |

The ideas are the same as Modules 4 and 14. uv just does them faster and with a lock file.

## 3. pre-commit: quality checks before every commit

`pre-commit` runs tools like ruff and mypy automatically on `git commit`, so broken code never even reaches CI.

```bash
pip install pre-commit
```

```bash
pre-commit install
```

The configuration lives in `.pre-commit-config.yaml`. There's an example in [`tasky_project/.pre-commit-config.yaml`](tasky_project/.pre-commit-config.yaml):
- trims whitespace and checks YAML;
- runs `ruff` (lint + autofix) and `ruff-format`;
- runs `mypy`;
- blocks commits that add big files or private keys.

Run it on every file once:

```bash
pre-commit run --all-files
```
