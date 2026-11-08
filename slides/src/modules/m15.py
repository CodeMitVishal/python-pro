"""Slides · Module 15 · Type hints & code quality"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 15 · Type hints &amp; code quality"
SLIDES = [
 cover("15", "Type hints &amp; code quality", "Catch bugs before you run anything, and keep a team's code easy to read.",
       [("Type hint basics", "01_type_hints_basics.py"), ("Advanced typing", "02_advanced_typing.py"),
        ("mypy catches bugs", "03_mypy_catches_bugs.py"), ("ruff: lint + format", "04_ruff_and_style.py"),
        ("Generics, typed decorators, @overload", "05_generics_and_typed_decorators.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Type hints", "Bugs that hide until production",
     "<b>get_user(id)</b> sometimes returns <b>None</b>. Nobody noticed, because the test user always existed. "
     "In production: <b>AttributeError: 'NoneType' object has no attribute 'email'</b> at 3 a.m.",
     "Type hints say what a function <b>expects and returns</b>. A checker (<b>mypy</b>) reads them and finds the bug <b>without running</b> the code."),

 code_out(M, "Type hints", "The basics in one screen", '''
from dataclasses import dataclass

@dataclass
class User:
    id: int
    email: str
    nickname: str | None = None          # may be missing

def find_user(users: list[User], user_id: int) -> User | None:
    return next((u for u in users if u.id == user_id), None)

def greeting(user: User) -> str:
    return f"Hi {user.nickname or user.email}"

users = [User(1, "v@ex.com", "Vishal")]
if (u := find_user(users, 1)) is not None:     # narrow the type
    print(greeting(u))
print(find_user.__annotations__)''',
     steps=["Hints are <b>not enforced</b> at runtime: Python ignores them.", "<b>X | None</b> forces you to handle \"not found\".",
            "After <b>is not None</b>, mypy knows <b>u</b> is a User."]),

 mistake(M, "mypy", "The bug mypy finds for free",
     '''
def find_user(users, user_id):
    for u in users:
        if u.id == user_id:
            return u

user = find_user(users, 42)
print(user.email)    # crashes when not found''',
     "Nothing warns you. The crash appears only when someone asks for a user that doesn't exist.",
     '''
def find_user(users: list[User], user_id: int) -> User | None: ...

user = find_user(users, 42)
print(user.email)
# mypy: error: Item "None" of "User | None"
#       has no attribute "email"''',
     "Run <b>mypy src/</b> in CI. With hints, the mistake is caught at review time, not at 3 a.m."),

 trace(M, "Advanced typing", "Typing tools you'll actually use", ["Tool", "Means", "Example"],
       [["<span class=\"m\">Literal</span>", "only these exact values", "<span class=\"m\">Literal[\"asc\", \"desc\"]</span>"],
        ["<span class=\"m\">TypedDict</span>", "a dict with known keys (JSON)", "<span class=\"m\">class OrderJSON(TypedDict): id: int</span>"],
        ["<span class=\"m\">Protocol</span>", "anything with these methods", "<span class=\"m\">class Notifier(Protocol): def send(...)</span>"],
        ["<span class=\"m\">Callable[[int], str]</span>", "a function taking int, returning str", "callbacks, <span class=\"m\">key=</span>"],
        ["<span class=\"m\">TypeVar / Generic[T]</span>", "\"same type in, same type out\"", "<span class=\"m\">def first(xs: list[T]) -&gt; T</span>"],
        ["<span class=\"m\">Final</span>, <span class=\"m\">ClassVar</span>", "constant / class-level", "<span class=\"m\">MAX_RETRIES: Final = 3</span>"]]),

 code_out(M, "Generics", "Write once, keep the types", '''
from typing import Generic, TypeVar

T = TypeVar("T")

class Page(Generic[T]):
    def __init__(self, items: list[T], total: int) -> None:
        self.items, self.total = items, total

    def first(self) -> T | None:
        return self.items[0] if self.items else None

orders: Page[int] = Page([1042, 1043], total=57)
names: Page[str] = Page(["vishal"], total=1)
print(orders.first(), names.first(), orders.total)
# mypy knows orders.first() is int | None''',
     steps=["<b>Page[int]</b> and <b>Page[str]</b> share one implementation.",
            "Python 3.12 shortcut: <b>class Page[T]:</b> and <b>def first[T](...)</b>."]),

 trace(M, "ruff", "Code quality on autopilot", ["Command", "What it does"],
       [["<span class=\"m\">ruff check .</span>", "finds bugs and smells: unused imports, bare except, mutable defaults"],
        ["<span class=\"m\">ruff check --fix .</span>", "fixes the safe ones automatically"],
        ["<span class=\"m\">ruff format .</span>", "formats like Black: no more style debates in reviews"],
        ["<span class=\"m\">mypy --strict src/</span>", "type checks everything"],
        ["<span class=\"m\">pre-commit</span>", "runs them before every commit"]],
       "In a team: the <b>CI fails</b> if ruff or mypy fail. Reviews then focus on logic, not commas."),

 job(M, "Typing", "Types power your frameworks", [
     ("FastAPI reads hints to validate", '''
@app.get("/orders/{order_id}")
def read(order_id: int, q: str | None = None): ...'''),
     ("Pydantic models = typed JSON", '''
class OrderIn(BaseModel):
    item: str
    qty: int = Field(gt=0)'''),
     ("SQLAlchemy 2.0 typed models", '''
class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)'''),
     ("CI gate", '''
- run: ruff check . && mypy src/'''),
 ]),

 interview(M, "Are type hints enforced in Python? Why use them?",
     ["No: Python ignores them at runtime. They're stored in <b>__annotations__</b>.",
      "Tools use them: <b>mypy/pyright</b> find bugs before running, IDEs autocomplete, and they document the code.",
      "Frameworks <b>do</b> use them at runtime: FastAPI and Pydantic validate and convert data from hints.",
      "Biggest win: <b>Optional</b> handling. <b>X | None</b> forces you to deal with \"not found\"."],
     None,
     "\"What's the difference between Any and object?\" (Any switches type checking off; object accepts anything but lets you do almost nothing with it until you narrow it)."),

 interview(M, "How do you keep code quality high in a team?",
     ["<b>Formatter</b> (ruff format) so style is never discussed.",
      "<b>Linter</b> (ruff check) and <b>type checker</b> (mypy) in <b>pre-commit and CI</b>.",
      "<b>Tests</b> with coverage on critical paths (Module 16).",
      "Small <b>pull requests</b> with code review; clear names; docstrings for public functions.",
      "Track tech debt; refactor in small, tested steps."],
     None,
     "\"What is a Protocol vs an ABC?\" (structural vs nominal typing; see Module 12)."),

 recap(M, "Module 15 in 5 lines",
     ["Hints describe expectations; Python doesn't enforce them, <b>mypy</b> checks them.",
      "<b>X | None</b> + <b>is not None</b> narrowing kills the classic None bug.",
      "<b>Literal</b>, <b>TypedDict</b>, <b>Protocol</b>, <b>Callable</b>, <b>Generic[T]</b> for precise types.",
      "<b>ruff check</b> + <b>ruff format</b> + <b>mypy</b> in pre-commit and CI.",
      "FastAPI, Pydantic and SQLAlchemy all run on type hints."],
     "Do <b>exercises/ex15_add_type_hints.py</b>, then make <b>mypy --strict</b> pass."),
]
