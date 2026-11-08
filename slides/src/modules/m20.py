"""Slides · Module 20 · Capstone: budget"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 20 · Capstone"
SLIDES = [
 cover("20", "Capstone: budget", "One small project built like a professional one, with every core module working together.",
       [("The project", "budget_project/"), ("Architecture", "budget_project/README.md"),
        ("Service + repository", "src/budget/service.py"), ("CLI + API", "cli.py · api.py"),
        ("Tests", "budget_project/tests/"), ("Challenges", "ex20_capstone_challenges.md")], M),

 why(M, "Architecture", "Why structure matters more than clever code",
     "Version 1 put SQL, input parsing and business rules in one 300-line function. Adding an API meant <b>copy-pasting</b> it all. "
     "Testing it needed a real database.",
     "Split the code into <b>layers</b>. Each layer has one job and talks only to the layer below."),

 picture(M, "Architecture", "Clean layers",
     "&#127970; Like a <b>restaurant</b>: waiters (CLI, API) take orders, the kitchen (service) cooks by the rules, "
     "the store room (repository) holds the ingredients. Waiters never walk into the store room.",
     [("cli.py / api.py", "parse input, call the service, show output"), ("service.py", "business rules, validation, alerts"),
      ("repository.py", "the ONLY place with SQL"), ("SQLite", "or Postgres, or a fake in tests")],
     "The service depends on a <b>Protocol</b>, not on SQLite: that's dependency injection."),

 code_out(M, "Service + repository", "The core pattern in 20 lines", '''
from collections import defaultdict
from dataclasses import dataclass

@dataclass(frozen=True)
class Expense:
    amount: float
    category: str
class MemoryRepo:                          # a fake for tests
    def __init__(self): self.items = []
    def add(self, e): self.items.append(e)
    def all(self): return list(self.items)
class BudgetService:
    def __init__(self, repo): self.repo = repo      # injected
    def add(self, amount, category):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.repo.add(Expense(amount, category))
    def summary(self):
        totals = defaultdict(float)
        for e in self.repo.all():
            totals[e.category] += e.amount
        return dict(sorted(totals.items(), key=lambda kv: -kv[1]))
svc = BudgetService(MemoryRepo())
svc.add(320, "food"); svc.add(80, "transport"); svc.add(45, "food")
print(svc.summary())''',
     steps=["The service never sees SQL.", "Tests pass a <b>MemoryRepo</b>; production passes a <b>SqliteRepo</b>.",
            "CLI and API both call the <b>same</b> service."]),

 trace(M, "Module map", "Where every module shows up", ["Module", "In the capstone"],
       [["8 Pythonic · 9 Data structures", "comprehensions, <span class=\"m\">sorted(key=)</span>, <span class=\"m\">@dataclass(frozen=True)</span>, <span class=\"m\">defaultdict</span>"],
        ["10 Functions · 12 OOP", "FastAPI decorators, <span class=\"m\">Protocol</span>, dependency injection"],
        ["13 Errors &amp; logging", "<span class=\"m\">BudgetError</span>, <span class=\"m\">raise ... from</span>, <span class=\"m\">getLogger(__name__)</span>"],
        ["14 Packaging · 15 Typing", "src layout, <span class=\"m\">pyproject.toml</span>, the <span class=\"m\">budget</span> command, <span class=\"m\">mypy --strict</span>"],
        ["16 Testing", "fixtures, parametrize, <span class=\"m\">TestClient</span> API tests"],
        ["18 Data &amp; APIs", "SQLite repository, FastAPI app"]],
       "Read <b>budget_project/README.md</b> first, then the code top-down: cli &#8594; service &#8594; repository."),

 job(M, "Capstone", "Run it like a real project", [
     ("Install and use the CLI", '''
pip install -e ".[dev]"
budget add 320 food "groceries"
budget summary --month 2026-11'''),
     ("Serve the API", '''
uvicorn budget.api:app --reload
# open http://127.0.0.1:8000/docs'''),
     ("The quality gate", '''
pytest -q
mypy --strict src
ruff check .'''),
     ("Show it off", '''
README + architecture diagram
+ tests passing = a portfolio project'''),
 ]),

 interview(M, "Walk me through the architecture of a project you built.",
     ["Start with the <b>goal</b>: \"track expenses from a CLI and a REST API\".",
      "Draw the <b>layers</b>: interface (CLI/API) &#8594; service (rules) &#8594; repository (SQL) &#8594; DB.",
      "Explain one <b>design decision</b> and its trade-off: a Protocol + DI made the service testable without a DB.",
      "Mention <b>quality</b>: tests with fixtures, mypy --strict, ruff, CI.",
      "End with what you'd <b>improve next</b>: Postgres, auth, Docker, monitoring."],
     None,
     "\"Why the repository pattern?\" (all SQL in one place, swappable storage, easy fakes in tests, the service stays pure)."),

 recap(M, "Core track done: what you can do now",
     ["Write <b>Pythonic</b>, typed, tested code.",
      "Pick the right <b>data structure</b> and explain its Big-O.",
      "Use closures, decorators, generators and context managers.",
      "Design with <b>layers</b>, Protocols and dependency injection.",
      "Package a CLI, call APIs, use SQL, serve FastAPI.",
      "Measure and fix performance, and use concurrency well."],
     "Do the challenges in <b>exercises/ex20_capstone_challenges.md</b>, then start the web track (Module 21)."),
]
