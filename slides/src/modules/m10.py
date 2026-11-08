"""Slides · Module 10 · Advanced functions"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 10 · Advanced functions"
SLIDES = [
 cover("10", "Advanced functions", "Closures and decorators are the #1 \"advanced Python\" interview topic, and every web framework is built on them.",
       [("*args, **kwargs, keyword-only", "01_args_and_kwargs.py"), ("Scope &amp; closures", "02_scope_and_closures.py"),
        ("Functions are objects", "03_first_class_functions.py"), ("Decorators", "04_decorators.py"),
        ("functools: cache, partial", "05_functools.py"), ("Demo: resilient API client", "06_demo_api_client.py"),
        ("Recursion", "07_recursion.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 # ------------------------------------------------------------------ ARGS / KWARGS
 why(M, "*args and **kwargs", "Functions that accept any number of arguments",
     "<b>print()</b> takes 1, 2 or 10 values. A logging wrapper must pass <b>whatever</b> it receives on to the real function.<br><br>"
     "You can't write a parameter for every possible argument.",
     "<b>*args</b> packs extra positional values into a <b>tuple</b>. <b>**kwargs</b> packs extra named values into a <b>dict</b>."),

 code_out(M, "*args and **kwargs", "See what the function receives", '''
def show(first, *args, **kwargs):
    print("first :", first)
    print("args  :", args)
    print("kwargs:", kwargs)

show(1, 2, 3, user="vishal", debug=True)

nums = [4, 5]
opts = {"user": "li"}
show(*nums, **opts)       # * and ** UNPACK when calling''',
     steps=["Named parameters are filled <b>first</b>.", "Extra positional values go to <b>args</b> (a tuple).",
            "Extra keyword values go to <b>kwargs</b> (a dict).", "At the call site, <b>*</b> and <b>**</b> do the opposite: unpack."]),

 code_out(M, "Keyword-only parameters", "Force callers to write the name", '''
def connect(host, *, timeout=5, retries=3):
    return f"{host} timeout={timeout} retries={retries}"

print(connect("db.local", timeout=10))

try:
    connect("db.local", 10)          # which one is 10?!
except TypeError as e:
    print("TypeError:", e)''',
     steps=["Everything after a bare <b>*</b> must be passed <b>by name</b>.",
            "<b>connect(\"db\", 10, 3)</b> is unreadable; <b>timeout=10</b> is clear.",
            "Many library APIs use this, e.g. <b>sorted(items, key=..., reverse=...)</b>."]),

 mistake(M, "Parameters", "The mutable default argument trap",
     '''
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags

print(add_tag("a"))   # ['a']
print(add_tag("b"))   # ['a', 'b']  ???''',
     "The default list is created <b>once</b>, when Python reads the <b>def</b>. Every call shares and grows the same list.",
     '''
def add_tag(tag, tags=None):
    if tags is None:
        tags = []         # a NEW list per call
    tags.append(tag)
    return tags

print(add_tag("b"))   # ['b']''',
     "Use <b>None</b> as the default and create the list inside. This is asked in many interviews."),

 # ------------------------------------------------------------------ FIRST-CLASS FUNCTIONS
 picture(M, "Functions are objects", "A function is a value, like a number",
     "&#128230; Without the brackets, <b>len</b> is just an object you can hand around. With <b>()</b> you <b>call</b> it. "
     "So you can store functions, pass them in, and return them.",
     [("store it", "handlers = {\"csv\": read_csv}"), ("pass it", "sorted(users, key=get_age)"),
      ("return it", "make_multiplier(2) returns a function")],
     "This is the foundation for callbacks, closures and decorators."),

 code_out(M, "Functions are objects", "Pick behaviour at runtime", '''
def to_upper(s): return s.upper()
def to_title(s): return s.title()

FORMATTERS = {"upper": to_upper, "title": to_title}

style = "title"                       # e.g. from a config file
print(FORMATTERS[style]("hello world"))

users = [("vishal", 31), ("li", 25), ("sam", 40)]
print(sorted(users, key=lambda u: u[1]))
print(max(users, key=lambda u: u[1])[0])''',
     steps=["A <b>dict of functions</b> replaces a long if/elif chain.",
            "<b>key=</b> takes a function: \"sort by what this returns\".",
            "<b>lambda</b> = a small function without a name, for one-liners only."]),

 # ------------------------------------------------------------------ CLOSURES
 why(M, "Closures", "A function that remembers",
     "You want a <b>counter</b> for each user: it must keep its number between calls.<br><br>"
     "A <b>global variable</b> is shared by everyone (bug!). A <b>class</b> works, but is a lot of code for one number.",
     "Let a function <u>create</u> another function. The inner function keeps the outer variables alive. That's a <b>closure</b>."),

 picture(M, "Closures", "Picture it: a backpack",
     "&#127890; When an inner function is created, Python packs the outer variables it uses into a "
     "<b>backpack</b>. The function carries the backpack everywhere, even after the outer function has finished.",
     [("make_counter()", "runs once and creates <b>count = 0</b>"),
      ("returns next_number", "the inner function + its backpack {count}"),
      ("c1()  c1()  c1()", "each call opens the SAME backpack: 1, 2, 3")],
     "Call make_counter() again and you get a <b>new</b> function with a <b>new</b> backpack."),

 code_out(M, "Closures", "Build it and run it",
     '''
def make_counter():
    count = 0                  # lives in the backpack

    def next_number():
        nonlocal count         # change the OUTER count
        count += 1
        return count

    return next_number         # the function, not a call!

c1 = make_counter()
c2 = make_counter()
print(c1(), c1(), c1())
print(c2())
print(c1.__closure__[0].cell_contents)''',
     '''
1 2 3
1
3''',
     ["<b>make_counter()</b> returns a function.", "c1 and c2 have <b>separate</b> backpacks.",
      "<b>__closure__</b> lets you look inside the backpack."], code_w=960),

 trace(M, "Closures", "What happens on each line", ["Line", "c1's count", "c2's count", "Printed"],
       [["c1 = make_counter()", "0", "-", ""], ["c2 = make_counter()", "0", "0", ""],
        ["c1()", "1", "0", "1"], ["c1()", "2", "0", "2"], ["c1()", "3", "0", "3"], ["c2()", "3", "1", "1"]],
       "Same code, two independent states. That is exactly what a tiny class would give you, without the class."),

 mistake(M, "Closures", "Bug #1: changing an outer variable",
     '''
def make_counter():
    count = 0
    def next_number():
        count += 1      # UnboundLocalError!
        return count
    return next_number''',
     "<b>count += 1</b> means \"assign\", so Python treats count as a NEW local variable that has no value yet.",
     '''
def make_counter():
    count = 0
    def next_number():
        nonlocal count  # use the outer one
        count += 1
        return count
    return next_number''',
     "<b>nonlocal</b> says: \"this name belongs to the enclosing function\". Reading needs nothing; assigning needs nonlocal."),

 mistake(M, "Closures", "Bug #2: closures in a loop (late binding)",
     '''
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])

# [2, 2, 2]  ???''',
     "The backpack stores the <b>variable i</b>, not its value. When you call the functions, the loop has finished and i is 2.",
     '''
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])

# [0, 1, 2]''',
     "A <b>default argument</b> is evaluated <b>now</b>, so each function gets its own copy of i."),

 # ------------------------------------------------------------------ DECORATORS
 why(M, "Decorators", "Add behaviour without touching the code",
     "Your boss asks: <b>\"log how long each of our 40 API functions takes.\"</b><br><br>"
     "Copy-pasting timing code into 40 functions is slow, ugly and easy to get wrong.",
     "Write the timing code <b>once</b> as a wrapper, then put <b>@timer</b> on top of any function.",
     '''
@timer
def get_orders(user_id): ...'''),

 picture(M, "Decorators", "Picture it: gift wrapping",
     "&#127873; A decorator <b>wraps</b> your function like gift paper. Callers still call the same name, "
     "but now they get the <b>wrapper</b>, which does something before and after the real function.",
     [("caller", "get_orders(7)"), ("wrapper: before", "start the clock"),
      ("original function", "fetches the orders"), ("wrapper: after", "print the time, return the result")],
     "<b>@timer</b> above a def is just short for <b>get_orders = timer(get_orders)</b>."),

 code_out(M, "Decorators", "Your first real decorator",
     '''
import functools, time

def timer(func):
    @functools.wraps(func)            # keep name + docstring
    def wrapper(*args, **kwargs):     # accept ANY arguments
        start = time.perf_counter()
        result = func(*args, **kwargs)
        ms = (time.perf_counter() - start) * 1000
        print(f"{func.__name__} took {ms:.0f} ms")
        return result                 # don't forget!
    return wrapper

@timer
def slow_add(a, b):
    time.sleep(0.05)
    return a + b

print(slow_add(2, 3))''',
     '''
slow_add took 50 ms
5''',
     ["<b>timer</b> receives the function.", "<b>wrapper</b> runs before + after it.",
      "<b>*args, **kwargs</b> pass every argument through.", "<b>return result</b>, or the caller gets None."],
     code_w=1000),

 picture(M, "Decorators", "Decorators WITH arguments: one more layer",
     "<b>@retry(times=3)</b> first <b>calls</b> retry(times=3). That call must return a normal decorator. "
     "So you need three functions, like boxes inside boxes.",
     [("retry(times)", "remembers the settings (a closure!)"),
      ("decorator(func)", "receives the function"),
      ("wrapper(*args)", "runs on every call, uses times")],
     "Reading order: settings &#8594; function &#8594; call."),

 code_out(M, "Decorators", "@retry: the classic interview exercise",
     '''
def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    print(f"attempt {attempt} failed")
            raise ConnectionError("gave up")
        return wrapper
    return decorator

@retry(times=3)
def download():   # fails twice, then works
    ...''',
     '''
attempt 1 failed
attempt 2 failed
data.csv downloaded''',
     ["Only catch errors that a retry can fix (<b>network</b>), never bugs.",
      "Real projects add a <b>delay</b> that grows: 1 s, 2 s, 4 s."], code_w=980),

 mistake(M, "Decorators", "Bug: forgetting functools.wraps",
     '''
def timer(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@timer
def get_user(): """Load a user."""

print(get_user.__name__)   # wrapper  ???''',
     "Every decorated function now looks like <b>wrapper</b>: logs, error messages, docs and FastAPI routes get confused.",
     '''
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

print(get_user.__name__)   # get_user
print(get_user.__doc__)    # Load a user.''',
     "<b>@functools.wraps(func)</b> copies the name, docstring and signature onto the wrapper. Always add it."),

 job(M, "Decorators", "You will meet decorators on day one", [
     ("FastAPI / Flask: routes", '''
@app.get("/orders/{order_id}")
def read_order(order_id: int): ...'''),
     ("Django: permissions", '''
@login_required
def dashboard(request): ...'''),
     ("Caching expensive work", '''
@functools.lru_cache(maxsize=1024)
def exchange_rate(currency): ...'''),
     ("pytest: test setup", '''
@pytest.fixture
def client(): return TestClient(app)'''),
 ]),

 # ------------------------------------------------------------------ FUNCTOOLS
 code_out(M, "functools.lru_cache", "Remember results: from 21,891 calls to 21", '''
from functools import lru_cache

calls = 0
def fib(n):
    global calls; calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)
fib(20); print("plain :", calls, "calls")

calls = 0
@lru_cache(maxsize=None)
def fib(n):
    global calls; calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)
fib(20); print("cached:", calls, "calls")
print(fib.cache_info())''',
     steps=["<b>Memoisation</b>: same arguments, so return the stored result.",
            "Arguments must be <b>hashable</b> (no lists, no dicts).",
            "Never cache data that <b>changes</b> (DB rows, prices, time)."]),

 code_out(M, "functools.partial", "Pre-fill some arguments", '''
from functools import partial

def send(channel, message, urgent=False):
    flag = "!!" if urgent else ""
    return f"[{channel}] {flag}{message}"

alert = partial(send, "ops", urgent=True)
print(alert("disk 95% full"))

to_int = partial(int, base=2)
print(to_int("1010"))''',
     steps=["<b>partial</b> returns a new function with some arguments fixed.",
            "Great for callbacks that must take fewer arguments.",
            "Like a closure, but with no code to write."]),

 # ------------------------------------------------------------------ RECURSION
 picture(M, "Recursion", "A function that calls itself",
     "&#129670; Like <b>Russian dolls</b>: open a doll, find a smaller one, until the smallest doll can't be opened. "
     "That smallest doll is the <b>base case</b>.",
     [("factorial(3)", "3 * factorial(2)"), ("factorial(2)", "2 * factorial(1)"),
      ("factorial(1)", "base case: return 1"), ("back up", "2 * 1 = 2, then 3 * 2 = 6")],
     "Each call waits on the <b>call stack</b> until the smaller call returns."),

 code_out(M, "Recursion", "Walk a nested folder tree", '''
tree = {"src": {"app.py": 120, "utils": {"db.py": 80, "auth.py": 60}},
        "README.md": 10}

def total_size(node):
    if isinstance(node, int):        # base case: a file
        return node
    return sum(total_size(child)     # smaller problem
               for child in node.values())

print(total_size(tree), "KB")''',
     steps=["Recursion fits <b>nested</b> data: folders, JSON, menus, comment threads.",
            "Every recursive function needs a <b>base case</b>.",
            "Python stops at about <b>1,000</b> levels: <b>RecursionError</b>."]),

 interview(M, "What is a decorator, and how does it work?",
     ["A decorator is a function that <b>takes a function and returns a new function</b> that adds behaviour.",
      "<b>@timer</b> on top of a def is just <b>f = timer(f)</b>.",
      "The wrapper is a <b>closure</b>: it remembers the original function.",
      "I always use <b>functools.wraps</b> to keep the name and docstring.",
      "I use them for logging, timing, caching, retries and access checks."],
     '''
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(time.perf_counter() - start)
    return wrapper''',
     "\"Write one that takes arguments\" (3 levels: settings, function, call) and \"In which order do stacked decorators run?\" (bottom one wraps first)."),

 interview(M, "What is a closure? Give a real example.",
     ["An inner function that <b>remembers variables from its enclosing scope</b>, even after the outer function returned.",
      "Python stores them in <b>cells</b>: you can see them in <b>func.__closure__</b>.",
      "To <b>change</b> such a variable you need <b>nonlocal</b>.",
      "Real example: a <b>dependency factory</b> in FastAPI, <b>require_role(\"admin\")</b>, returns a checker that remembers the role."],
     '''
def require_role(role):
    def checker(user=Depends(current_user)):
        if user.role != role:
            raise HTTPException(403)
        return user
    return checker''',
     "\"What is the late-binding problem?\" (capture with i=i) and \"Closure or class: when do you use which?\" (one or two values: closure; more state or methods: class)."),

 recap(M, "Module 10 in 6 lines",
     ["<b>*args</b> = tuple of extras, <b>**kwargs</b> = dict of extras; never use a mutable default.",
      "Functions are objects: store them, pass them (<b>key=</b>), return them.",
      "A <b>closure</b> remembers outer variables; assigning needs <b>nonlocal</b>.",
      "<b>@deco</b> = <b>f = deco(f)</b>; always <b>functools.wraps</b>; arguments need 3 levels.",
      "<b>lru_cache</b> for repeated pure calls; <b>partial</b> to pre-fill arguments.",
      "Recursion needs a <b>base case</b>; deep data needs a loop and a stack."],
     "Do <b>exercises/ex10</b>, then write <b>@log_calls</b> that prints the arguments and the result of any function."),
]
