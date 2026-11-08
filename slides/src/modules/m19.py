"""Slides · Module 19 · Performance & internals"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 19 · Performance &amp; internals"
SLIDES = [
 cover("19", "Performance &amp; internals", "How Python stores your data, how to find what's slow, and how to fix it: the internals interviewers ask about.",
       [("The memory model", "01_memory_model.py"), ("Measure first", "02_measure_first.py"),
        ("Speed tricks that matter", "03_speed_tricks.py"), ("Saving memory", "04_memory_tricks.py"),
        ("Bytecode, weakref, NumPy", "05_bytecode_and_numpy.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 picture(M, "Memory model", "Names are labels, not boxes",
     "&#127991;&#65039; A variable is a <b>sticky note</b> on an object, not a box that holds it. <b>b = a</b> puts a second note on the "
     "<b>same</b> object. Changing the object through one note shows up through the other.",
     [("a = [1, 2]", "note 'a' on a list object"), ("b = a", "note 'b' on the SAME list"),
      ("b.append(3)", "the one list changes"), ("print(a)", "[1, 2, 3]")]),

 code_out(M, "Memory model", "References, ids and reference counts", '''
import sys

a = [1, 2]
b = a                          # same object
c = [1, 2]                     # equal, different object
b.append(3)
print(a, a is b, a == c, a is c)
print(id(a) == id(b))

print(sys.getrefcount(a) - 1, "references to the list")   # a, b
del b
print(sys.getrefcount(a) - 1, "reference after del b")

def add_item(lst):             # functions get the SAME object
    lst.append("x")
add_item(a)
print(a)''',
     steps=["Python passes <b>references to objects</b> (\"call by sharing\").", "Each object counts its references; at 0 it's freed at once.",
            "Cycles are cleaned up by the <b>garbage collector</b> (<b>gc</b>)."]),

 why(M, "Measure first", "Don't guess where it's slow",
     "A teammate rewrote a function with clever tricks for 2 days. The page was still slow: 95% of the time was a <b>database query in a loop</b>.",
     "<b>Measure first</b>: <b>timeit</b> for small snippets, <b>cProfile</b> to find the slow function, then fix the biggest thing."),

 code_out(M, "Measure first", "cProfile finds the hot spot", '''
import cProfile, pstats, time

def load_user(uid):  time.sleep(0.01); return {"id": uid}
def format_row(u):   return f"{u['id']:>5}"

def report():
    return [format_row(load_user(i)) for i in range(30)]   # N slow calls!

prof = cProfile.Profile()
prof.runcall(report)
stats = pstats.Stats(prof).stats          # {(file, line, name): (..., ncalls, tottime, cumtime, ...)}
print(f"{'function':12} {'ncalls':>6} {'cumtime':>8}")
for (_, _, name), (_, ncalls, _, cumtime, _) in stats.items():
    if name in ("load_user", "format_row"):
        print(f"{name:12} {ncalls:>6} {cumtime:>7.2f}s")''',
     steps=["<b>ncalls</b>: how often; <b>cumtime</b>: total time spent inside.", "<b>load_user</b> eats the time: batch it into one query.",
            "In web apps: also look at the <b>number of SQL queries</b> per request."]),

 trace(M, "Speed tricks", "Fixes that actually matter (biggest first)", ["Fix", "Typical gain", "Example"],
       [["<b>Better algorithm / data structure</b>", "10&#8211;10,000&times;", "list lookup &#8594; set; nested loops &#8594; dict"],
        ["<b>Fewer I/O round trips</b>", "10&#8211;100&times;", "1 query with JOIN instead of N queries"],
        ["<b>Caching</b>", "huge for repeats", "<span class=\"m\">lru_cache</span>, Redis (Module 26)"],
        ["<b>Built-ins and C libraries</b>", "2&#8211;100&times;", "<span class=\"m\">sum()</span>, <span class=\"m\">sorted()</span>, NumPy, pandas"],
        ["<b>Concurrency</b>", "N&times; for waiting", "asyncio / threads (Module 17)"],
        ["Micro-tricks (local variables...)", "a few %", "only in proven hot loops"]]),

 code_out(M, "Speed tricks", "Built-ins and NumPy vs plain loops", '''
import timeit
import numpy as np

nums = list(range(1_000_000))
arr = np.arange(1_000_000)

def loop_sum():
    total = 0
    for n in nums:
        total += n * n
    return total

t_loop = timeit.timeit(loop_sum, number=5) / 5
t_gen = timeit.timeit(lambda: sum(n * n for n in nums), number=5) / 5
t_np = timeit.timeit(lambda: int((arr * arr).sum()), number=5) / 5
print(f"for loop : {t_loop * 1000:6.1f} ms")
print(f"sum(gen) : {t_gen * 1000:6.1f} ms")
print(f"numpy    : {t_np * 1000:6.1f} ms  (~{t_loop / t_np:.0f}x faster)")''',
     steps=["NumPy runs the loop in <b>C</b> on a compact array.", "Use it for numbers; pandas for tables.",
            "Numbers differ per machine; the ranking doesn't."]),

 code_out(M, "Saving memory", "__slots__ and generators", '''
import sys, tracemalloc

class Point:
    def __init__(self, x, y): self.x, self.y = x, y

class SlimPoint:
    __slots__ = ("x", "y")                # no per-object __dict__
    def __init__(self, x, y): self.x, self.y = x, y

for cls in (Point, SlimPoint):
    tracemalloc.start()
    pts = [cls(i, i) for i in range(100_000)]
    size, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{cls.__name__:9} {size / 1e6:5.1f} MB")

print(sys.getsizeof([n for n in range(100_000)]), "bytes as a list")
print(sys.getsizeof(n for n in range(100_000)), "bytes as a generator")''',
     steps=["<b>__slots__</b> saves memory with millions of small objects.", "<b>Generators</b> keep memory flat (Module 11).",
            "<b>tracemalloc</b> measures what your code allocates."]),

 mistake(M, "Performance", "Premature optimisation",
     '''
# "faster" but nobody can read it
r=[*map(lambda t:t[0]*t[1],zip(p,q))]''',
     "Unreadable code for an unmeasured gain. Bugs hide in it, and the real bottleneck (I/O) is still there.",
     '''
totals = [price * qty for price, qty in zip(prices, quantities)]
# then: measure. Is THIS the slow part?''',
     "Write clear code, <b>measure</b>, then optimise the hot spot. \"Premature optimisation is the root of all evil.\""),

 job(M, "Performance", "Performance work in web jobs", [
     ("Find N+1 queries", '''
Order.objects.select_related("user")
             .prefetch_related("items")'''),
     ("Profile one slow endpoint", '''
python -m cProfile -o out.prof app.py
snakeviz out.prof'''),
     ("Cache expensive reads", '''
@cache.memoize(timeout=300)
def exchange_rates(): ...'''),
     ("Move heavy work off the request", '''
generate_pdf.delay(invoice_id)  # Celery'''),
 ]),

 interview(M, "How does Python manage memory?",
     ["Everything is an <b>object</b> on a private heap; variables are <b>references</b> (names) to objects.",
      "CPython uses <b>reference counting</b>: when an object's count drops to 0 it's freed immediately.",
      "A cyclic <b>garbage collector</b> (<b>gc</b>, 3 generations) cleans up reference cycles.",
      "Small objects come from the <b>pymalloc</b> allocator; small ints and some strings are cached (interned).",
      "Arguments are passed by <b>object reference</b>: mutating a list inside a function changes the caller's list."],
     None,
     "\"What is a memory leak in Python?\" (objects still referenced by mistake: global caches, lists that only grow, cycles with __del__; find them with tracemalloc)."),

 interview(M, "Your API endpoint is slow. How do you find and fix it?",
     ["<b>Measure</b>: timings in logs/APM, then profile the endpoint (cProfile, py-spy).",
      "Check the <b>database</b> first: count queries (N+1?), EXPLAIN, missing indexes.",
      "Check <b>external calls</b>: add timeouts, run them concurrently, cache results.",
      "Then the code: better data structures and algorithms, fewer copies.",
      "Move slow work to <b>background jobs</b>; add <b>caching</b> (Redis) and pagination."],
     None,
     "\"What is __slots__ and when would you use it?\" (fixed attributes, no __dict__: less memory for millions of instances, slightly faster attribute access)."),

 recap(M, "Module 19 in 6 lines",
     ["Variables are <b>labels</b>; <b>b = a</b> shares the object.",
      "Reference counting frees objects at 0; <b>gc</b> handles cycles.",
      "<b>Measure first</b>: timeit, cProfile, tracemalloc.",
      "Biggest wins: algorithm, fewer I/O round trips, caching.",
      "Built-ins and <b>NumPy</b> push loops into C.",
      "<b>__slots__</b> and generators save memory."],
     "Do <b>exercises/ex19_make_it_fast.py</b>: make a slow report 100x faster without changing the result."),
]
