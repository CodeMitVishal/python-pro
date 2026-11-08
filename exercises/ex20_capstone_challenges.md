# Exercise 20 · Capstone challenges

Extend the `budget` project in [`20_capstone/budget_project`](../20_capstone/budget_project).
Each challenge practises a different part of the course. For **every** challenge:

1. Write the test first (Module 16)
2. Make it pass
3. Keep `pytest`, `mypy` and `ruff check .` green (Module 15)

---

### ⭐ Level 1: warm-up

**1. `budget list --month 2026-11`**
Print every expense of the month in a table: id, date, amount, category, note.
*Practises:* argparse subcommands, f-string alignment (Modules 8, 14)

**2. A `transport` limit**
Add `transport: 120` to the budget limits and a test proving the alert fires.
*Practises:* fixtures, parametrize (Module 16)

### ⭐⭐ Level 2: real features

**3. Export to CSV**
`budget export 2026-11 report.csv` writes the month's expenses with `csv.DictWriter`.
Test it with the `tmp_path` fixture.
*Practises:* pathlib, csv, testing files (Modules 16, 18)

**4. `GET /expenses?month=2026-11&category=food`**
A filtered list endpoint. Add a `list_month` filter to the repository's
Protocol, and test with `TestClient`.
*Practises:* FastAPI query parameters, Protocols (Modules 12, 18)

**5. Budget limits in a config file**
Load limits from `budget.json` (fall back to defaults if it's missing). Raise
`BudgetError` with a clear message if the JSON is invalid (`raise ... from`).
*Practises:* exceptions, JSON, EAFP (Module 13)

### ⭐⭐⭐ Level 3: pro

**6. Recurring expenses**
`budget add 900 rent --monthly` stores a rule. A generator
`expand_recurring(rules, year, month)` yields the concrete expenses for any month.
*Practises:* generators, dataclasses (Modules 9, 11)

**7. Currency conversion with caching**
Accept `--currency USD`, convert to EUR with a rate function wrapped in
`@lru_cache`, and mock the rate source in tests.
*Practises:* decorators, caching, mocking (Modules 10, 16, 19)

**8. A second repository**
Write `JsonExpenseRepository` (stores expenses in a JSON file) that satisfies the
same Protocol. Run the SAME service tests against both repositories, with a
parametrized fixture.
*Practises:* dependency inversion, parametrized fixtures (Modules 12, 16)

---

Done? Open a **Pull Request** with your solution in
`submissions/<your-github-name>/` and I'll review your code. 🚀
