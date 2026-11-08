"""Generate the slides for Modules 10-20 and insert them into python-pro-slides.html.

Each slide is described as compact data below and rendered with a few layouts
(title, code + notes, table, cards, exercise) that match the hand-written
Module 8-9 slides. Re-run after editing; the generated block is replaced.

    python slides/src/build_module_slides.py
"""
import html
import re
from pathlib import Path

DECK = Path(__file__).with_name("python-pro-slides.html")
START, END = "<!-- GENERATED:START -->", "<!-- GENERATED:END -->"
REPO = "github.com/CodeMitVishal/python-pro"

KW = ("def|class|return|for|in|if|elif|else|with|as|import|from|async|await|yield|try|except|"
      "finally|raise|lambda|None|True|False|not|and|or|is|while|nonlocal|global|pass|del")
TOKENS = re.compile(rf"""(?P<s>f?"[^"\n]*"|f?'[^'\n]*')|(?P<c>\#[^\n]*)|(?P<k>\b(?:{KW})\b)|(?P<o>.|\n)""")


def hl(code: str) -> str:
    """Tiny syntax highlighter: strings, comments, keywords."""
    out = []
    for m in TOKENS.finditer(code.strip("\n")):
        text = html.escape(m.group())
        kind = m.lastgroup
        out.append(text if kind == "o" else f'<span class="{kind}">{text}</span>')
    return "".join(out)


def fit(src: str, box_width: int, size: int) -> int:
    """Shrink the font so the longest code line fits the box (mono chars are ~0.6em wide)."""
    longest = max((len(line) for line in src.strip(chr(10)).splitlines()), default=1)
    return max(16, min(size, int((box_width - 76) / (longest * 0.61))))


def foot(label):
    return f'<p class="foot-l">Python Pro · {label}</p><p class="foot-r">{REPO}</p>'


def title(num, name, tagline, toc):
    rows = "".join(f"<div><span>{a}</span><span>{b}</span></div>" for a, b in toc)
    return f"""<section class="dark" style="flex-direction:row;align-items:center;gap:100px">
  <div style="width:640px;display:flex;flex-direction:column;gap:20px">
    <p class="num">MODULE</p><p class="big">{num}</p>
    <h1 style="font-size:{76 if len(name) > 18 else 80}px">{name}</h1>
    <p style="font-size:28px;line-height:1.4">{tagline}</p>
  </div>
  <div style="flex:1" class="toc"><p class="num" style="font-size:22px;margin-bottom:10px">IN THIS MODULE</p>{rows}</div>
  {foot(f"Module {int(num)}")}
</section>"""


def code(mod, eyebrow, h2, src, notes=(), tip=None, width=900, size=25):
    side = "".join(f'<p class="note">{n}</p>' for n in notes)
    if tip:
        side += f'<p class="tip">{tip}</p>'
    return f"""<section>
  <div><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2></div>
  <div class="row"><div class="code" style="width:{width}px;font-size:{fit(src, width, size)}px">{hl(src)}</div>
  <div class="col" style="flex:1">{side}</div></div>
  {foot(mod)}
</section>"""


def table(mod, eyebrow, h2, head, rows, notes=(), tip=None, src=None, width=620):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    side = "".join(f'<p class="note">{n}</p>' for n in notes)
    if src:
        side = f'<div class="code" style="font-size:{fit(src, width, 22)}px">{hl(src)}</div>' + side
    if tip:
        side += f'<p class="tip">{tip}</p>'
    right = f'<div class="col" style="width:{width}px">{side}</div>' if side else ""
    return f"""<section>
  <div><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2></div>
  <div class="row"><table style="flex:1">{th and "<tr>" + th + "</tr>"}{trs}</table>{right}</div>
  {foot(mod)}
</section>"""


def cards(mod, eyebrow, h2, items):
    cs = "".join(
        f'<div class="card"><span class="tag">{t}</span><h3>{h}</h3>'
        f'<div class="code" style="font-size:{fit(c, 760, 22)}px;padding:18px 24px">{hl(c)}</div></div>'
        for t, h, c in items)
    return f"""<section>
  <div><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:28px">{cs}</div>
  {foot(mod)}
</section>"""


def exercise(num, h2, tasks, ex_file, sample, sol=True):
    rows = "".join(f"<tr><td><b>{i}</b></td><td>{t}</td></tr>" for i, t in enumerate(tasks, 1))
    files = f"<b>Starter:</b> exercises/{ex_file}"
    if sol:
        files += f"<br><b>Solution:</b> solutions/{sol if isinstance(sol, str) else ex_file}"
    return f"""<section>
  <div><p class="eyebrow">Exercise {num} · Your turn</p><h2>{h2}</h2></div>
  <div class="row">
    <div class="col" style="flex:1"><p style="font-size:30px;font-weight:700;color:#121826">The task</p><table>{rows}</table></div>
    <div class="col" style="width:600px"><div class="code" style="font-size:{fit(sample, 600, 22)}px">{hl(sample)}</div>
      <div class="tip">{files}</div>
      <p class="note">Done? Open a <b>Pull Request</b> and I'll review your code.</p></div>
  </div>
  {foot(f"Module {num} · Exercise")}
</section>"""


S = []  # all generated slides, in order

# ===================================== Module 10 =====================================
M = "Module 10 · Advanced functions"
S += [
 title("10", "Advanced functions", "Functions are objects: pass them, return them, make them remember, wrap them.",
       [("Parameters like a pro", "01_args_and_kwargs.py"), ("Scope &amp; closures", "02_scope_and_closures.py"),
        ("Functions are objects", "03_first_class_functions.py"), ("Decorators", "04_decorators.py"),
        ("functools", "05_functools.py"), ("Demo: resilient API client", "06_demo_api_client.py"),
        ("Exercise: write decorators", "ex10_decorators.py")]),
 code(M, "Lesson · Parameters", "*args, **kwargs, keyword-only and the trap", '''
def f(a, b=2, *args, c, d=4, **kwargs):
#     |  |     |      |  |     └ extra keywords -> dict
#     |  |     |      └──┴ keyword-only (after *)
#     |  |     └ extra positionals -> tuple
#     |  └ default
#     └ positional

def connect(host, *, port=443): ...
connect("api.io", port=8080)    # must name it

def add(item, basket=None):     # NOT basket=[]
    if basket is None:
        basket = []
    basket.append(item)
    return basket''', ["<b>*args</b> collects extra positional arguments into a <b>tuple</b>, <b>**kwargs</b> extra keywords into a <b>dict</b>.",
                       "Everything after a bare <span class=\"m\">*</span> must be passed <b>by name</b>: call sites explain themselves."],
      tip="⚠️ Default values are created <b>once</b>. A <span class=\"m\" style=\"background:#fff3c4\">[]</span> default is shared by every call. Use <b>None</b>."),
 code(M, "Lesson · Scope &amp; closures", "A function that remembers", '''
def make_counter():
    count = 0
    def next_number():
        nonlocal count      # update the OUTER count
        count += 1
        return count
    return next_number      # the function, not a call

c1, c2 = make_counter(), make_counter()
c1(), c1(), c1(), c2()      # 1 2 3 1''', ["<b>LEGB</b>: Python looks for a name in <b>L</b>ocal → <b>E</b>nclosing → <b>G</b>lobal → <b>B</b>uilt-in.",
                                         "A <b>closure</b> keeps the variables of its outer function alive, even after it returned.",
                                         "Reading an outer variable just works. <b>Assigning</b> needs <span class=\"m\">nonlocal</span> (or <span class=\"m\">global</span>)."],
      tip="⚠️ <span class=\"m\" style=\"background:#fff3c4\">[lambda: i for i in range(3)]</span> all return 2 (late binding). Fix: <b>lambda i=i: i</b>"),
 code(M, "Lesson · Decorators", "Wrap a function to add behaviour", '''
def timer(func):
    @functools.wraps(func)          # keep name + docstring
    def wrapper(*args, **kwargs):   # accept ANY arguments
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.perf_counter() - start:.3f}s")
        return result               # don't forget!
    return wrapper

@timer                              # same as: slow = timer(slow)
def slow(): ...''', ["<b>@decorator</b> above <span class=\"m\">def f</span> means <span class=\"m\">f = decorator(f)</span>.",
                     "Decorator <b>with arguments</b> = one more layer: <span class=\"m\">retry(times)</span> → <span class=\"m\">decorator(func)</span> → <span class=\"m\">wrapper(*args)</span>.",
                     "Stacked decorators: the one <b>closest to def</b> wraps first."], size=24, width=960),
 table(M, "Lesson · functools", "Ready-made tools for functions",
       ["Tool", "What it does", "Example"],
       [["<b>lru_cache</b>", "remembers results (memoization)", "<span class=\"m\">fib(200)</span>: instant"],
        ["<b>partial</b>", "pre-fills arguments", "<span class=\"m\">square = partial(power, exp=2)</span>"],
        ["<b>wraps</b>", "keeps names in decorators", "<span class=\"m\">@functools.wraps(func)</span>"],
        ["<b>reduce</b>", "folds a list into one value", "<span class=\"m\">reduce(mul, [1,2,3,4])</span> → 24"],
        ["<b>singledispatch</b>", "one function, code per type", "<span class=\"m\">describe(21)</span> vs <span class=\"m\">describe([1])</span>"]],
       src='''@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

fib(28)   # 0.064 s -> 0.00003 s''', tip="Only cache <b>pure</b> functions: same input → same output, no side effects."),
 exercise(10, "Write three decorators", ["<span class=\"m\">@count_calls</span>: store the number of calls in <span class=\"m\">func.calls</span>",
                                          "<span class=\"m\">@require_positive</span>: <b>ValueError</b> for negative numbers",
                                          "<span class=\"m\">@memoize</span>: your own cache with a dict (no lru_cache!)",
                                          "Work with any arguments and keep the name: <b>functools.wraps</b>"],
          "ex10_decorators.py", '''@count_calls
def hello(): return "hi"

hello(); hello(); hello()
hello.calls        # 3'''),
]

# ===================================== Module 11 =====================================
M = "Module 11 · Iterators &amp; generators"
S += [
 title("11", "Iterators &amp; generators", "Process data one item at a time: a 10 GB file with the memory of 10 lines.",
       [("How for really works", "01_iteration_protocol.py"), ("Generators", "02_generators.py"),
        ("Lazy pipelines", "03_pipelines.py"), ("itertools", "04_itertools.py"),
        ("Demo: a 200,000-row CSV", "05_demo_big_csv.py"), ("Exercise: lazy generators", "ex11_generators.py")]),
 code(M, "Lesson · The iteration protocol", "What a for loop really does", '''
for x in things:          # is really:
    print(x)

it = iter(things)         # iterable -> iterator
while True:
    try:
        x = next(it)      # next item...
    except StopIteration: # ...until there's none
        break
    print(x)''', ["<b>Iterable</b>: something you can loop over. It hands out an iterator (<span class=\"m\">__iter__</span>).",
                  "<b>Iterator</b>: remembers <b>where you are</b> and gives the next item (<span class=\"m\">__next__</span>).",
                  "An iterator is <b>used up</b> after one pass: <span class=\"m\">list(it)</span> twice gives <span class=\"m\">[]</span> the 2nd time."]),
 code(M, "Lesson · Generators", "yield: hand out a value, pause, resume", '''
def countdown(start):
    while start > 0:
        yield start        # hand out + PAUSE here
        start -= 1         # resume here on next()

list(countdown(3))         # [3, 2, 1]

squares = (n*n for n in range(10**6))  # generator expression
sum(squares)               # one value at a time''',
      ["Calling a generator function runs <b>nothing</b>; it returns a generator object.",
       "Each <span class=\"m\">next()</span> runs to the next <span class=\"m\">yield</span> and keeps all local variables.",
       "<span class=\"m\">yield from xs</span> hands over to another iterable."],
      tip="Memory: a list of 1M squares = <b>8.4 MB</b>, the generator = <b>200 bytes</b>."),
 code(M, "Lesson · Lazy pipelines", "Chain generators like an assembly line", '''
lines   = read_lines(path)          # yields one line at a time
records = parse(lines)              # yields (date, level, msg)
errors  = only("ERROR", records)    # filters lazily
msgs    = messages(errors)          # formats lazily

for m in islice(msgs, 2):           # take 2, then stop
    print(m)
# only 4 lines were ever read!''', ["Nothing runs until something <b>asks</b> for values.",
                                    "Each stage does <b>one job</b>, so it's easy to test and reuse.",
                                    "Demo with a 200,000-row CSV: <b>56 MB</b> (list) vs <b>0.05 MB</b> (generators)."]),
 table(M, "Lesson · itertools", "A toolbox of fast, lazy iterators", ["Tool", "Example", "Result"],
       [["<b>islice</b>", "<span class=\"m\">islice(count(10, 5), 4)</span>", "10 15 20 25"],
        ["<b>chain</b>", "<span class=\"m\">chain([1, 2], \"ab\")</span>", "1 2 'a' 'b'"],
        ["<b>accumulate</b>", "<span class=\"m\">accumulate([5, 10, 20])</span>", "5 15 35"],
        ["<b>pairwise</b>", "<span class=\"m\">pairwise([12, 15, 11])</span>", "(12,15) (15,11)"],
        ["<b>groupby</b>", "sort first, then group neighbours", "DE 150 · IN 100"],
        ["<b>product</b>", "<span class=\"m\">product(\"SM\", [\"red\", \"blue\"])</span>", "every combination"],
        ["<b>combinations</b>", "<span class=\"m\">combinations(names, 2)</span>", "every pair"]],
       tip="⚠️ <b>groupby</b> only groups <b>consecutive</b> items. Sort by the same key first."),
 exercise(11, "Write lazy generators", ["<span class=\"m\">chunked(items, size)</span>: lists of <span class=\"m\">size</span> items",
                                         "<span class=\"m\">running_average(numbers)</span>: the average so far",
                                         "<span class=\"m\">valid_numbers(lines)</span>: ints only, skip the rest",
                                         "Use <b>yield</b>; must work on <b>endless</b> input"],
          "ex11_generators.py", '''list(chunked("abcde", 2))
# [['a','b'], ['c','d'], ['e']]

list(running_average([2, 4, 6]))
# [2.0, 3.0, 4.0]'''),
]

# ===================================== Module 12 =====================================
M = "Module 12 · Advanced OOP"
S += [
 title("12", "Advanced OOP", "Classes that feel built-in, and designs that stay easy to change.",
       [("Dunder methods", "01_dunder_methods.py"), ("Properties", "02_properties.py"),
        ("Class &amp; static methods", "03_class_and_static_methods.py"), ("Inheritance &amp; the MRO", "04_inheritance_and_mro.py"),
        ("ABCs &amp; Protocols", "05_abc_and_protocols.py"), ("Composition &amp; SOLID", "06_composition_and_solid.py"),
        ("Exercise: a Vector class", "ex12_vector.py")]),
 table(M, "Lesson · Dunder methods", "Python calls them for you", ["You write", "Python calls"],
       [["<span class=\"m\">print(x)</span> / <span class=\"m\">repr(x)</span>", "<span class=\"m\">__str__</span> / <span class=\"m\">__repr__</span>"],
        ["<span class=\"m\">a == b</span>, <span class=\"m\">a &lt; b</span>", "<span class=\"m\">__eq__</span>, <span class=\"m\">__lt__</span> (+ @total_ordering)"],
        ["<span class=\"m\">a + b</span>, <span class=\"m\">2 * v</span>", "<span class=\"m\">__add__</span>, <span class=\"m\">__rmul__</span>"],
        ["<span class=\"m\">len(x)</span>, <span class=\"m\">x[i]</span>, <span class=\"m\">for i in x</span>", "<span class=\"m\">__len__</span>, <span class=\"m\">__getitem__</span>"],
        ["<span class=\"m\">item in x</span>", "<span class=\"m\">__contains__</span>"],
        ["<span class=\"m\">{x}</span>, dict key", "<span class=\"m\">__hash__</span>"],
        ["<span class=\"m\">if x:</span>", "<span class=\"m\">__bool__</span>"]],
       src='''Money(10.5) + Money(4.25)
# 14.75 EUR
sorted([Money(9), Money(1)])''', notes=["Can't compare with that type? Return <b>NotImplemented</b>, not False."],
       tip="Defined <b>__eq__</b>? Define <b>__hash__</b> too, or the objects can't go in sets."),
 code(M, "Lesson · Properties &amp; class methods", "Attributes with rules, alternative constructors", '''
class Temperature:
    @property
    def celsius(self):
        return self._celsius
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero!")
        self._celsius = value

class Employee:
    @classmethod
    def from_csv(cls, line):       # cls = the class it's called on
        name, salary = line.split(",")
        return cls(name, int(salary))''', ["<b>@property</b>: looks like an attribute, runs a method: validation, computed or read-only values.",
                                           "<b>@classmethod</b>: alternative constructors. <span class=\"m\">Manager.from_csv()</span> returns a <b>Manager</b>.",
                                           "<b>@staticmethod</b>: a plain helper that lives in the class."], size=23, width=900),
 code(M, "Lesson · Inheritance, MRO, ABCs, Protocols", "One clear order, explicit contracts", '''
class Child(Left, Right): ...
Child.__mro__  # Child, Left, Right, Base, object

class Shape(ABC):                 # nominal: must inherit
    @abstractmethod
    def area(self) -> float: ...

class Notifier(Protocol):         # structural: any class
    def send(self, msg: str) -> None: ...   # with .send() fits''',
      ["<b>super()</b> calls the <b>next class in the MRO</b>, not simply \"my parent\". That's what makes mixins work.",
       "<b>ABC</b>: subclasses that forget an abstract method can't even be created.",
       "<b>Protocol</b>: duck typing with type checking. Great for classes you don't own."]),
 code(M, "Lesson · Composition &amp; SOLID", "Build from parts, inject the details", '''
class Checkout:
    def __init__(self, discount: Discount, notifier: Notifier):
        self.discount = discount        # HAS-A, injected
        self.notifier = notifier

    def pay(self, items):
        total = self.discount.apply(sum(p for _, p in items))
        self.notifier.send(f"charged {total:.2f}")

Checkout(PercentOff(20), ConsoleNotifier()).pay(cart)
Checkout(NoDiscount(), FakeNotifier()).pay(cart)  # in tests''', [
     "<b>S</b>ingle responsibility · <b>O</b>pen for extension · <b>L</b>iskov · <b>I</b>nterface segregation · <b>D</b>ependency inversion",
     "IS-A → inheritance. <b>HAS-A → composition</b>.",
     "New discount rule? A <b>new class</b>. Checkout never changes."], size=23, width=960),
 exercise(12, "A Vector class that feels built-in", ["<span class=\"m\">repr</span>, <span class=\"m\">+</span>, <span class=\"m\">v * 2</span> and <span class=\"m\">2 * v</span>",
                                                     "<span class=\"m\">abs(v)</span>, a read-only <b>length</b> property",
                                                     "<span class=\"m\">==</span> and <b>hashable</b> (works in sets)",
                                                     "<span class=\"m\">x, y = v</span>, <span class=\"m\">bool()</span>, <span class=\"m\">Vector.from_tuple()</span>"],
          "ex12_vector.py", '''v = Vector(3, 4)
v + Vector(1, 1)   # Vector(4, 5)
2 * v              # Vector(6, 8)
abs(v)             # 5.0
x, y = v'''),
]

# ===================================== Module 13 =====================================
M = "Module 13 · Errors, context managers &amp; logging"
S += [
 title("13", "Errors, context managers &amp; logging", "Fail safely, clean up always, leave a clear trail.",
       [("Exceptions like a pro", "01_exception_hierarchy.py"), ("Context managers", "02_context_managers.py"),
        ("logging", "03_logging.py"), ("Demo: robust order importer", "04_demo_order_importer.py"),
        ("Exercise: safe bank transfers", "ex13_bank_transfer.py")]),
 code(M, "Lesson · Exceptions", "Your own exception family", '''
class ShopError(Exception): ...         # the family
class OutOfStock(ShopError):
    def __init__(self, item, left):
        super().__init__(f"only {left} x {item} left")
        self.item, self.left = item, left   # extra data

try:
    buy("laptop", 5)
except OutOfStock as e:     # most specific FIRST
    print(e.left)
except ShopError as e:      # then the family
    ...

raise ShopError("config broken") from err   # keep the cause''',
      ["Catch as <b>specific</b> as possible; a parent catches all its children.",
       "<span class=\"m\">raise ... from e</span> keeps the original error in the traceback.",
       "<b>EAFP</b>: try it, handle the exception. The Pythonic default."],
      tip="⚠️ Never <span class=\"m\" style=\"background:#fff3c4\">except: pass</span>. It also catches Ctrl+C and hides bugs forever.", size=23),
 code(M, "Lesson · Context managers", "Setup and clean-up, guaranteed", '''
@contextmanager
def transaction(db):
    snapshot = dict(db)
    try:
        yield                 # the with-block runs here
    except Exception:
        db.clear(); db.update(snapshot)   # roll back
        raise                 # never swallow the error

with transaction(accounts):
    accounts["raj"] += 30
    withdraw(accounts, "vishal", 30)''',
      ["<span class=\"m\">with x:</span> → <span class=\"m\">__enter__</span>, the body, then <span class=\"m\">__exit__</span>, which <b>always</b> runs.",
       "Code before <span class=\"m\">yield</span> = enter, after = exit.",
       "Files, locks, DB transactions, timers, temp folders, <span class=\"m\">suppress(FileNotFoundError)</span>"]),
 code(M, "Lesson · logging", "print() for grown-ups", '''
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s")
log = logging.getLogger(__name__)    # one per module

log.debug("hidden below INFO")
log.info("order %s created", 1042)   # %s, not f-strings
log.warning("stock low: %d left", 2)
try:
    1 / 0
except ZeroDivisionError:
    log.exception("discount failed")  # + traceback''',
      ["Levels: <b>DEBUG &lt; INFO &lt; WARNING &lt; ERROR &lt; CRITICAL</b>.",
       "Configure <b>once</b> at start-up; add handlers for files or the cloud.",
       "<span class=\"m\">%s</span> arguments: the text is only built if the message is shown."], size=23),
 exercise(13, "Safe bank transfers", ["<span class=\"m\">InsufficientFunds(BankError)</span> with <span class=\"m\">.account .balance .amount</span>",
                                       "<span class=\"m\">withdraw()</span> raises it when the balance is too low",
                                       "<span class=\"m\">atomic(accounts)</span>: snapshot, roll back, <b>re-raise</b>",
                                       "<span class=\"m\">transfer()</span>: no money may appear or disappear"],
          "ex13_bank_transfer.py", '''transfer(accounts, "raj", "vishal", 500)
# InsufficientFunds: raj has 80
accounts   # unchanged: rolled back'''),
]

# ===================================== Module 14 =====================================
M = "Module 14 · Project structure &amp; packaging"
S += [
 title("14", "Project structure &amp; packaging", "From scripts to an installable project with its own command.",
       [("Modules &amp; imports", "01_modules_and_imports.py"), ("CLIs with argparse", "02_cli_with_argparse.py"),
        ("A real package: tasky", "tasky_project/"), ("Exercise: wordtool CLI", "ex14_wordtool_cli.py")]),
 code(M, "Lesson · Modules &amp; imports", "What import really does", '''
import json
# 1. already in sys.modules? reuse it (runs only ONCE)
# 2. otherwise search the folders in sys.path
# 3. run the file, store it in sys.modules

if __name__ == "__main__":   # only when run directly,
    main()                   # not when imported (tests!)

from tasky.store import TaskStore   # absolute: preferred
from .store import TaskStore        # relative: inside a package''',
      ["<b>module</b> = one .py file · <b>package</b> = a folder of modules with <span class=\"m\">__init__.py</span>",
       "<span class=\"m\">__name__</span> is <span class=\"m\">\"__main__\"</span> only for the file you ran.",
       "Avoid <span class=\"m\">from x import *</span>: you can't tell where names come from."]),
 code(M, "Lesson · A real package", "src layout + pyproject.toml", '''
tasky_project/
├── pyproject.toml     # name, version, deps, commands
├── src/tasky/
│   ├── __init__.py    # public API, __version__
│   ├── __main__.py    # python -m tasky
│   ├── cli.py         # argparse -> calls store
│   └── store.py       # the logic (no printing)
└── tests/test_store.py

[project.scripts]
tasky = "tasky.cli:main"    # creates the `tasky` command''',
      ["<span class=\"m\">pip install -e .</span>: an <b>editable</b> install; code changes apply instantly.",
       "Keep <b>logic</b> (store.py) apart from the <b>interface</b> (cli.py): reusable and testable.",
       "Return a <b>non-zero exit code</b> on failure so scripts and CI can tell."],
      tip="$ tasky add \"Record Module 14\"   ·   $ tasky done 1   ·   $ python -m tasky list"),
 exercise(14, "Build a CLI with argparse", ["Subcommand <span class=\"m\">stats TEXT</span>: words, unique, chars",
                                             "Subcommand <span class=\"m\">top TEXT --n 3</span>: the most common words",
                                             "<span class=\"m\">main(argv=None)</span>: testable without a terminal",
                                             "Case-insensitive counting; return exit code 0"],
          "ex14_wordtool_cli.py", '''$ wordtool stats "the cat and the hat"
words: 5, unique: 4, chars: 19

$ wordtool top "the cat and the hat" --n 1
the: 2'''),
]

# ===================================== Module 15 =====================================
M = "Module 15 · Type hints &amp; code quality"
S += [
 title("15", "Type hints &amp; code quality", "Catch bugs before you run anything, and keep code easy to read.",
       [("Type hints", "01_type_hints_basics.py"), ("Advanced typing", "02_advanced_typing.py"),
        ("mypy catches bugs", "03_mypy_catches_bugs.py"), ("ruff &amp; style", "04_ruff_and_style.py"),
        ("Exercise: type it, fix it", "ex15_add_type_hints.py")]),
 table(M, "Lesson · Type hints", "Say what your code expects", ["Type", "Means"],
       [["<span class=\"m\">list[int]</span>, <span class=\"m\">dict[str, float]</span>", "what's <b>inside</b> a collection"],
        ["<span class=\"m\">float | None</span>", "a float, <b>or None</b> (handle it!)"],
        ["<span class=\"m\">Literal[\"info\", \"error\"]</span>", "only these exact values"],
        ["<span class=\"m\">TypedDict</span>", "a dict with known keys (JSON)"],
        ["<span class=\"m\">Callable[[float], float]</span>", "a function float → float"],
        ["<span class=\"m\">TypeVar T</span>: <span class=\"m\">list[T] -> T</span>", "generic: str in, str out"],
        ["<span class=\"m\">Final</span>", "a constant"]],
       src='''def find_price(item: str) -> float | None:
    return prices.get(item)''', notes=["Python does <b>not</b> check hints at runtime. Your editor and <b>mypy</b> do."]),
 code(M, "Lesson · mypy", "3 hidden crashes, found in one second", '''
def plan_of(user_id: int) -> str:
    user = find_user(user_id)        # dict | None
    return user.get("plan", "free")  # crashes for unknown ids

def label(count: int) -> str:
    if count > 100:
        return "Orders: " + count    # str + int

def bill(total: float) -> None:
    send_invoice(total)              # expects an email str''',
      ["<b>$ mypy 03_mypy_catches_bugs.py</b>",
       "<span class=\"m\">Item \"None\" ... has no attribute \"get\"</span>",
       "<span class=\"m\">Unsupported operand types for + (\"str\" and \"int\")</span>",
       "<span class=\"m\">Argument 1 ... incompatible type \"float\"; expected \"str\"</span>"],
      tip="The code runs fine with today's test data. mypy finds the crashes <b>before</b> production does."),
 code(M, "Lesson · ruff", "Lint for bugs, format for consistency", '''
import os, sys                      # E401 + F401 unused
def messy_total( items ,discount = None ):
    for i in range(len(items)):
        if items[i]["price"] == None:   # E711
            continue
    try: ...
    except:                         # E722 bare except
        return 0

$ ruff check file.py      # list problems
$ ruff check --fix        # fix the safe ones
$ ruff format             # rewrite the layout''',
      ["<b>Linter</b>: likely bugs and bad patterns. <b>Formatter</b>: layout only.",
       "Configure once in <span class=\"m\">pyproject.toml</span> or <span class=\"m\">ruff.toml</span>.",
       "Tools can't name things for you: <span class=\"m\">unpaid_invoices</span>, not <span class=\"m\">lst2</span>."]),
 exercise(15, "Type it, let mypy find the bug", ["Add hints to every function, with a <b>TypedDict</b> for orders",
                                                  "Run <span class=\"m\">mypy --strict</span>",
                                                  "Fix the real bug mypy reports",
                                                  "Checks AND mypy --strict must pass"],
          "ex15_add_type_hints.py", '''$ mypy --strict ex15_add_type_hints.py
error: Value of type "Order | None"
       is not indexable
# report([]) would crash!'''),
]

# ===================================== Module 16 =====================================
M = "Module 16 · Testing with pytest"
S += [
 title("16", "Testing with pytest", "Prove your code works, and keep it working when it changes.",
       [("pytest basics", "test_01_basics.py"), ("Fixtures &amp; parametrize", "test_02_fixtures_and_parametrize.py"),
        ("Fakes, mocks &amp; monkeypatch", "test_03_mocking.py"), ("TDD", "test_04_tdd.py"),
        ("Exercise: tests that catch bugs", "ex16_test_password.py")]),
 code(M, "Lesson · pytest basics", "Plain assert, nothing else to learn", '''
def test_discount_takes_percentage_off():
    price = 100.0                        # arrange
    result = apply_discount(price, 20)   # act
    assert result == 80.0                # assert

def test_over_100_is_rejected():
    with pytest.raises(ValueError, match="between 0 and 100"):
        apply_discount(10, 150)

def test_floats():
    assert 0.1 + 0.2 == pytest.approx(0.3)''',
      ["pytest runs files <span class=\"m\">test_*.py</span> and functions <span class=\"m\">test_*</span>.",
       "A failed assert shows <b>both values</b>: <span class=\"m\">assert 6.0 == 7</span>.",
       "Test the <b>edges</b>: 0, empty, the limit, invalid input."],
      tip="$ pytest 16_testing -v   →   31 passed"),
 code(M, "Lesson · Fixtures &amp; parametrize", "Reusable setup, many cases", '''
@pytest.fixture                       # in conftest.py: shared
def sample_cart():
    return {"book": (12.5, 2), "pen": (1.2, 3)}

def test_total(sample_cart):          # asked for by NAME
    assert cart_total(sample_cart) == pytest.approx(28.6)

@pytest.mark.parametrize(("price", "pct", "expected"), [
    (100, 10, 90.0),
    (19.99, 50, 9.99),               # floats!
])
def test_cases(price, pct, expected):
    assert apply_discount(price, pct) == expected''',
      ["A fixture is built <b>fresh for every test</b>, so tests can't affect each other.",
       "<span class=\"m\">tmp_path</span>: a built-in fixture, a temp folder per test.",
       "Each parameter set is reported as its <b>own</b> test."], size=23),
 code(M, "Lesson · Mocks &amp; TDD", "No network in unit tests · red → green → refactor", '''
def describe_weather(city, fetch=fetch_json): ...

def test_hot_city():
    fake = Mock(return_value={"temp_c": 31.4})
    assert describe_weather("Mumbai", fetch=fake) == "Mumbai: 31°C, hot"
    fake.assert_called_once()

def test_api_down():
    fake = Mock(side_effect=TimeoutError("down"))
    with pytest.raises(TimeoutError):
        describe_weather("Oslo", fetch=fake)''',
      ["Real APIs are slow, need a network, and change: tests become <b>flaky</b>.",
       "<b>Inject</b> the dependency, or <span class=\"m\">monkeypatch</span> it for one test.",
       "<b>TDD</b>: write a failing test → make it pass → refactor. <span class=\"m\">slugify()</span> was built that way."], size=23),
 exercise(16, "Write tests that catch bugs", ["<span class=\"m\">is_strong_password()</span> is correct: test every rule",
                                              "8+ chars · upper · lower · digit · no spaces · TypeError",
                                              "Each test breaks <b>only one</b> rule",
                                              "Your tests must catch <b>6/6</b> planted bugs"],
          "ex16_test_password.py", '''$ python ex16_test_password.py
Your tests caught 6/6 bugs.
All checks passed!'''),
]

# ===================================== Module 17 =====================================
M = "Module 17 · Concurrency"
S += [
 title("17", "Concurrency", "Threads for waiting, processes for calculating, asyncio for thousands of tasks.",
       [("Threads", "01_threads.py"), ("Processes", "02_processes.py"), ("asyncio", "03_asyncio_basics.py"),
        ("Demo: price checker", "04_demo_price_checker.py"), ("Exercise: parallel downloads", "ex17_parallel_downloads.py")]),
 table(M, "Lesson · Choosing", "Waiting or calculating?", ["Work", "Example", "Use", "Measured"],
       [["<b>I/O-bound</b> (waiting)", "downloads, DB, files", "<b>threads</b> or <b>asyncio</b>", "4.0 s → <b>0.5 s</b>"],
        ["<b>CPU-bound</b> (calculating)", "maths, images, parsing", "<b>processes</b>", "5.1 s → <b>2.1 s</b>"],
        ["CPU-bound with threads", "", "❌ the GIL", "5.1 s → <b>6.1 s</b>"]],
       src='''with ThreadPoolExecutor(8) as pool:
    results = list(pool.map(download, files))

if __name__ == "__main__":     # required!
    with ProcessPoolExecutor() as pool:
        totals = list(pool.map(count_primes, jobs))''',
       notes=["The <b>GIL</b> lets one thread run Python at a time per process. Separate processes each have their own."],
       width=700),
 code(M, "Lesson · Threads", "Shared data needs a lock", '''
counter = 0
lock = threading.Lock()

def safe_add(n):
    global counter
    for _ in range(n):
        with lock:             # one thread at a time
            counter += 1

# 4 threads x 1000:
#   without the lock: 1204   <- updates lost!
#   with the lock:    4000''', ["A <b>race condition</b>: two threads read, both add 1, both write. One update is lost.",
                                "<span class=\"m\">with lock:</span> makes the read-modify-write happen as one step.",
                                "Simplest of all: <b>don't share</b>. Return results from the pool instead."]),
 code(M, "Lesson · asyncio", "Thousands of waiting tasks on one thread", '''
async def fetch(name, s):
    await asyncio.sleep(s)        # pause, let others run
    return name

async def main():
    results = await asyncio.gather(fetch("x", 1), fetch("y", 1))   # ~1 s
    await asyncio.wait_for(fetch("slow", 5), timeout=0.5)         # TimeoutError
    limit = asyncio.Semaphore(10)                                 # max 10 at once

asyncio.run(main())''',
      ["Switches happen <b>only at await</b>, so race conditions are rarer.",
       "<span class=\"m\">gather</span> = run concurrently · <span class=\"m\">wait_for</span> = timeout · <span class=\"m\">Semaphore</span> = limit."],
      tip="⚠️ One blocking call (<span class=\"m\" style=\"background:#fff3c4\">time.sleep</span>, <span class=\"m\" style=\"background:#fff3c4\">requests.get</span>) freezes the whole loop.",
      size=22, width=1000),
 exercise(17, "Parallel downloads", ["10 downloads × 0.3 s in <b>&lt; 1 s</b> with a <b>ThreadPoolExecutor</b>",
                                      "The same with <b>asyncio.gather</b>",
                                      "Count words with a <b>ProcessPoolExecutor</b>",
                                      "Keep the results in input order"],
          "ex17_parallel_downloads.py", '''$ python ex17_parallel_downloads.py
threads: 0.31 s, asyncio: 0.31 s
All checks passed!'''),
]

# ===================================== Module 18 =====================================
M = "Module 18 · Data, APIs &amp; databases"
S += [
 title("18", "Data, APIs &amp; databases", "Files, web APIs, SQL, and your own REST API with FastAPI.",
       [("Files, CSV &amp; JSON", "01_files_csv_json.py"), ("Calling web APIs", "02_http_requests.py"),
        ("SQLite", "03_sqlite.py"), ("Your own REST API", "04_fastapi_app.py"),
        ("Exercise: a notes database", "ex18_notes_repository.py")]),
 code(M, "Lesson · Web APIs", "Call an API safely", '''
try:
    resp = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": "language:python", "per_page": 3},
        timeout=10)                  # ALWAYS
    resp.raise_for_status()          # 4xx/5xx -> error
    data = resp.json()
except requests.Timeout:
    ...
except requests.RequestException:   # offline, DNS, HTTP
    ...''',
      ["<span class=\"m\">params=</span> encodes query values correctly; never glue strings.",
       "Tokens live in <b>environment variables</b>, never in the code.",
       "<span class=\"m\">pathlib</span> + <span class=\"m\">csv.DictReader</span> + <span class=\"m\">json</span> for files: lesson 01."]),
 code(M, "Lesson · SQLite", "SQL with ? parameters and transactions", '''
conn.execute("SELECT * FROM products WHERE name = ?", (name,))

user_input = "x' OR '1'='1"
f"... WHERE name = '{user_input}'"   # matches 3 rows: INJECTION
"... WHERE name = ?", (user_input,)  # matches 0 rows: safe

with conn:                            # all or nothing
    conn.execute("UPDATE products SET stock = stock - 1 ...")
    conn.execute("INSERT ... duplicate name")   # IntegrityError
# -> the UPDATE was rolled back too''',
      ["SQLite: a full SQL database in <b>one file</b>, built into Python.",
       "<span class=\"m\">conn.row_factory = sqlite3.Row</span> → <span class=\"m\">row[\"name\"]</span>.",
       "The same ideas work for PostgreSQL and MySQL."], size=23),
 code(M, "Lesson · FastAPI", "Type hints become a validated web API", '''
class TodoIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)

@app.post("/todos", status_code=201)
def create_todo(todo: TodoIn) -> Todo: ...

@app.get("/todos/{todo_id}")
def read_todo(todo_id: int) -> Todo:   # 404 if missing
    ...

# POST {"title": ""}  -> 422 (validated for you)
# $ uvicorn 04_fastapi_app:app --reload  -> /docs''',
      ["<b>pydantic</b> models validate the JSON body automatically.",
       "Status codes: <b>201</b> created · <b>204</b> no content · <b>404</b> not found · <b>422</b> invalid.",
       "<span class=\"m\">TestClient</span> calls the API in tests without a server."]),
 exercise(18, "A notes database", ["<span class=\"m\">NotesRepository(path)</span> creates the table",
                                    "<span class=\"m\">add / get / search / delete / count</span>",
                                    "Tags stored as <b>JSON</b> text",
                                    "Only <b>?</b> parameters: the injection check must pass"],
          "ex18_notes_repository.py", '''repo = NotesRepository(":memory:")
nid = repo.add("Shopping", "milk", tags=["home"])
repo.search("MILK")    # case-insensitive
repo.search("x' OR '1'='1")   # []'''),
]

# ===================================== Module 19 =====================================
M = "Module 19 · Performance &amp; internals"
S += [
 title("19", "Performance &amp; internals", "Understand what Python does under the hood, then measure before you optimise.",
       [("The memory model", "01_memory_model.py"), ("Measure first", "02_measure_first.py"),
        ("Speed tricks that matter", "03_speed_tricks.py"), ("Memory tricks", "04_memory_tricks.py"),
        ("Exercise: make it fast", "ex19_make_it_fast.py")]),
 code(M, "Lesson · The memory model", "Names point to objects", '''
a = [1, 2, 3]
b = a              # 2 names, 1 object
b.append(4)        # a sees it too

x = 10; y = x
y += 1             # ints are immutable: y -> NEW object

def add(lst): lst.append(1)   # the object is passed,
add(a)                         # so the caller's list changes

int("1000") is int("1000")     # False: use == for values''',
      ["Every object has an <b>identity</b> (id), a <b>type</b> and a <b>value</b>.",
       "<b>Reference counting</b>: freed the moment the count hits 0; <span class=\"m\">gc</span> cleans up cycles.",
       "Use <span class=\"m\">is</span> only for <span class=\"m\">None</span>, <span class=\"m\">True</span>, <span class=\"m\">False</span>."]),
 table(M, "Lesson · Speed", "Measure first, then fix the biggest thing", ["Fix", "Measured speed-up"],
       [["Better data structure: list <span class=\"m\">in</span> → set/dict", "<b>309×</b>"],
        ["Cache a slow pure function: <span class=\"m\">@lru_cache</span>", "<b>91×</b>"],
        ["<span class=\"m\">\"\".join()</span> instead of <span class=\"m\">+=</span> in a loop", "<b>22×</b>"],
        ["Built-ins (<span class=\"m\">sum</span>, <span class=\"m\">sorted</span>, <span class=\"m\">max</span>) instead of loops", "<b>4×</b>"],
        ["Compute once, outside the loop", "<b>3×</b>"],
        ["<span class=\"m\">__slots__</span> on millions of objects", "24 → 17.6 MB"]],
       src='''$ python -m cProfile -s cumtime app.py

ncalls  cumtime  function
     1    0.222  report
     1    0.172  slow_unique_customers  <- here!''',
       notes=["<b>timeit</b> compares snippets · <b>cProfile</b> finds slow functions · <b>tracemalloc</b> finds memory-hungry lines."], width=700),
 exercise(19, "Make it fast", ["<span class=\"m\">find_duplicates</span>: O(n²) → O(n) with <b>Counter</b>",
                                "<span class=\"m\">common_customers</span>: use <b>set</b> intersection",
                                "<span class=\"m\">fib(300)</span>: stop recomputing with <b>lru_cache</b>",
                                "Each must fit a <b>0.1 s</b> budget"],
          "ex19_make_it_fast.py", '''# before
find_duplicates(big)   # 1.28 s
# after
find_duplicates(big)   # 0.004 s'''),
]

# ===================================== Module 20 =====================================
M = "Module 20 · Capstone"
S += [
 title("20", "Capstone project", "budget: a tested, typed, packaged expense tracker with a CLI and a REST API.",
       [("The project", "budget_project/"), ("Architecture", "budget_project/README.md"),
        ("Tests", "budget_project/tests/"), ("Challenges", "ex20_capstone_challenges.md"),
        ("Final exam", "20_capstone/QUIZ.md")]),
 code(M, "Capstone · Architecture", "Clean layers: each talks only to the one below", '''
  cli.py  (argparse)          api.py  (FastAPI)
        \\                        /
         ▼                      ▼
        service.py   business rules · validation · alerts
               │  depends on a Protocol, not on SQLite
               ▼
        repository.py   the ONLY place with SQL
               │
               ▼
            SQLite''',
      ["The <b>service</b> doesn't know whether it's called from a terminal or over HTTP.",
       "Tests inject an <b>in-memory</b> repository: fast and isolated.",
       "<span class=\"m\">pytest</span> · <span class=\"m\">mypy --strict</span> · <span class=\"m\">ruff</span>: all green."], size=26),
 table(M, "Capstone · Where every module shows up", "Everything you learned, in one project", ["Module", "In budget"],
       [["08 Pythonic · 09 Data structures", "comprehensions, <span class=\"m\">sorted(key=)</span>, frozen dataclass, defaultdict"],
        ["10 Functions · 12 OOP", "FastAPI dependencies, Protocol + dependency injection"],
        ["13 Errors &amp; logging", "<span class=\"m\">BudgetError</span>, <span class=\"m\">raise ... from</span>, <span class=\"m\">getLogger(__name__)</span>"],
        ["14 Packaging", "src layout, <span class=\"m\">pyproject.toml</span>, the <span class=\"m\">budget</span> command"],
        ["15 Typing · 16 Testing", "mypy --strict, ruff, 9 tests with fixtures + TestClient"],
        ["18 Data &amp; APIs", "SQLite repository, FastAPI with pydantic"]],
       src='''$ budget add 320 food "groceries"
$ budget summary --month 2026-11
2026-11: total 1315.50
  rent    900.00
  food    415.50  <- over budget!''', width=640),
 exercise(20, "Capstone challenges", ["⭐ <span class=\"m\">budget list</span> and a transport limit",
                                       "⭐⭐ CSV export · filtered <span class=\"m\">GET /expenses</span> · limits from JSON",
                                       "⭐⭐⭐ recurring expenses (generators) · currency + lru_cache",
                                       "⭐⭐⭐ a second repository behind the same Protocol"],
          "ex20_capstone_challenges.md", '''# for EVERY challenge:
# 1. write the test first
# 2. make it pass
# 3. keep pytest, mypy, ruff green''', sol=False),
]

# Bonus lessons + the web development track (Modules 21-28)
import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent))
from web_track_slides import web_slides  # noqa: E402

S += web_slides(title, code, table, cards, exercise)

# Closing slide
S.append(f"""<section class="dark" style="justify-content:center;gap:30px">
  <p class="num">YOU MADE IT</p>
  <h1>From Foundations to Pro, and the Web 🎓</h1>
  <p style="font-size:34px;color:#E6E9F0;max-width:1400px;line-height:1.4">Take the <b style="color:#F2C14E">final exams</b> in 20_capstone and 28_web_capstone, deploy taskboard, and share it on LinkedIn.</p>
  <div style="display:flex;flex-direction:column;gap:14px;font-size:30px;margin-top:20px">
    <span>🎥 youtube.com/@CodeMitVishal</span><span>⭐ {REPO}</span><span>☕ buymeacoffee.com/codemitvishal</span>
  </div>
  {foot("Thank you!")}
</section>""")

deck = DECK.read_text(encoding="utf-8")
generated = f"{START}\n" + "\n\n".join(S) + f"\n{END}"
if START in deck:
    deck = deck[:deck.index(START)] + generated + deck[deck.index(END) + len(END):]
else:
    deck = deck.replace("</body>", generated + "\n</body>")
DECK.write_text(deck, encoding="utf-8")
print(f"{len(S)} generated slides written to {DECK.name}")
