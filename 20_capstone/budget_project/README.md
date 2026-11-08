# budget: the Python Pro capstone

Track expenses from the **command line** or a **REST API**. Small, but built
like a professional project: every module of Python Pro shows up somewhere.

## Architecture

```
          ┌──────────── cli.py ────────────┐     ┌──────────── api.py ────────────┐
          │ argparse → call service → print│     │ FastAPI → call service → JSON  │
          └───────────────┬────────────────┘     └───────────────┬────────────────┘
                          └──────────────┬───────────────────────┘
                                         ▼
                              service.py  (business rules)
                     validation · summaries · budget alerts · logging
                                         │  depends on a Protocol, not on SQLite
                                         ▼
                            repository.py  (the only SQL)
                                         │
                                         ▼
                                   SQLite database
```

Each layer only talks to the one below it. The service, where the important
logic lives, has no idea whether it's called from a terminal or over HTTP,
or whether data lives in SQLite or a fake. That's why it's easy to test.

## Where each module shows up

| Module | Where |
|---|---|
| 8 Pythonic code | comprehensions and `sorted(key=...)` in `service.summary` |
| 9 Data structures | `@dataclass(frozen=True)`, `defaultdict(float)` |
| 10 Functions | FastAPI's decorators and dependency functions |
| 12 OOP | `Protocol` + dependency injection (`BudgetService(repo)`) |
| 13 Errors & logging | `BudgetError`, `raise ... from`, `logging.getLogger(__name__)` |
| 14 Packaging | src layout, `pyproject.toml`, the `budget` command |
| 15 Typing & quality | `mypy --strict` and `ruff` configured in `pyproject.toml` |
| 16 Testing | `tests/`: fixtures, parametrize, API tests with `TestClient` |
| 18 Data & APIs | the SQLite repository and the FastAPI app |

## Run it

```bash
cd 20_capstone/budget_project
```

```bash
pip install -e ".[dev]"
```

```bash
budget add 320 food "groceries" --date 2026-11-02
```

```bash
budget summary --month 2026-11
```

```bash
uvicorn budget.api:app --reload
```

Then open http://127.0.0.1:8000/docs for the interactive API.

## Check the quality

```bash
pytest
```

```bash
mypy
```

```bash
ruff check .
```

All three should pass. Keep it that way while you add features!

## Your turn

The challenges are in [`exercises/ex20_capstone_challenges.md`](../../exercises/ex20_capstone_challenges.md).
