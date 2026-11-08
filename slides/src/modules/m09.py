"""Slides · Module 9 · Data structures deep dive"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 9 · Data structures"
SLIDES = [
 cover("09", "Data structures deep dive", "Pick the right container and your code is fast. Pick the wrong one and it crawls.",
       [("Big-O in plain words", "01_big_o.py"), ("Lists vs tuples", "02_lists_and_tuples.py"),
        ("Dicts &amp; sets (hashing)", "03_dicts_and_sets.py"), ("collections", "04_collections.py"),
        ("dataclasses", "05_dataclasses.py"), ("Enums", "07_enums.py"),
        ("heapq &amp; bisect", "08_heapq_and_bisect.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 # ------------------------------------------------------------------ BIG-O
 why(M, "Big-O", "Why the container matters",
     "Your login check does <b>if email in banned_emails</b>. With 10 users it's instant. With 1,000,000 users and a <b>list</b>, every login waits.<br><br>"
     "Same code, same result, but one choice is <b>50,000&times; slower</b>.",
     "<b>Big-O</b> describes how the work grows when the data grows. Learn 4 of them and you can choose well."),

 trace(M, "Big-O", "The 4 you need to know", ["Big-O", "Plain words", "Example", "1,000,000 items"],
       [["<b>O(1)</b>", "same speed, any size", "<span class=\"m\">d[key]</span>, <span class=\"m\">x in set</span>", "1 step"],
        ["<b>O(log n)</b>", "halve the problem each step", "binary search, <span class=\"m\">bisect</span>", "~20 steps"],
        ["<b>O(n)</b>", "look at every item once", "<span class=\"m\">x in list</span>, <span class=\"m\">sum()</span>", "1,000,000 steps"],
        ["<b>O(n&#178;)</b>", "every item &times; every item", "nested loops over the same data", "10&#185;&#178; steps &#9888;"]],
       "Interview habit: after every solution, say its <b>time</b> and <b>space</b> complexity."),

 code_out(M, "Big-O", "Measure it: list vs set lookup", '''
import timeit

emails_list = [f"user{i}@mail.com" for i in range(100_000)]
emails_set = set(emails_list)
target = "user99999@mail.com"           # the worst case for a list

t_list = timeit.timeit(lambda: target in emails_list, number=200)
t_set = timeit.timeit(lambda: target in emails_set, number=200)
print(f"list: {t_list * 1000:7.1f} ms")
print(f"set : {t_set * 1000:7.3f} ms")
print(f"set is ~{t_list / t_set:,.0f}x faster")''',
     output="list:   182.4 ms\nset :   0.006 ms\nset is ~30,000x faster",
     steps=["A list checks items <b>one by one</b>: O(n).", "A set jumps straight to the answer: O(1).",
            "Numbers vary per machine; the <b>gap</b> doesn't."]),

 # ------------------------------------------------------------------ LISTS / TUPLES
 trace(M, "Lists vs tuples", "Same look, different jobs", ["", "list [ ]", "tuple ( )"],
       [["Can change?", "yes: append, remove, sort", "<b>no</b> (immutable)"],
        ["Typical use", "many items of the <b>same kind</b>", "one record with <b>fixed fields</b>"],
        ["Example", "<span class=\"m\">[\"lamp\", \"cable\", \"plug\"]</span>", "<span class=\"m\">(\"Vishal\", \"Augsburg\", 31)</span>"],
        ["Dict key / in a set?", "no (not hashable)", "yes, if its items are hashable"],
        ["Fast operations", "index, append, pop at the end: O(1)", "index: O(1); a bit smaller and faster"],
        ["Slow operations", "insert / pop at the <b>front</b>: O(n)", "&#8212;"]],
       "Need a queue (add at the back, take from the front)? Use <b>collections.deque</b>, not a list."),

 # ------------------------------------------------------------------ DICTS / SETS
 picture(M, "Dicts and sets", "How a dict finds a key instantly",
     "&#128273; Like a <b>wall of numbered lockers</b>. The key's <b>hash</b> says which locker to open, so Python never searches. "
     "That's why keys must be <b>hashable</b> (they must not change).",
     [("key: \"vishal\"", "hash(\"vishal\") gives a big number"), ("% table size", "turns it into a locker number, e.g. 5"),
      ("locker 5", "holds (\"vishal\", 31)"), ("result", "found in 1 step: O(1)")],
     "Sets use the same lockers, but store only keys: perfect for \"have I seen this?\"."),

 code_out(M, "Dicts and sets", "Everyday dict and set moves", '''
stock = {"lamp": 3, "cable": 0}
print(stock.get("plug", 0))              # no KeyError
stock.setdefault("plug", 5)
print(stock)

a = {"python", "sql", "docker"}
b = {"python", "react"}
print(a & b, a | b, a - b, sep="  |  ")

try:
    {[1, 2]: "list as key"}
except TypeError as e:
    print("TypeError:", e)''',
     steps=["<b>.get(key, default)</b> instead of try/except KeyError.", "Set maths: <b>&amp;</b> both, <b>|</b> either, <b>-</b> difference.",
            "Mutable things (lists, dicts) can't be keys."]),

 mistake(M, "Copies", "Shallow copy surprise",
     '''
team = {"members": ["vishal", "li"]}
backup = team.copy()    # shallow!
backup["members"].append("sam")
print(team["members"])
# ['vishal', 'li', 'sam'] ???''',
     "<b>.copy()</b> copies the outer dict, but the inner list is <b>shared</b>. Changing it through the copy changes the original.",
     '''
import copy
backup = copy.deepcopy(team)
backup["members"].append("sam")
print(team["members"])
# ['vishal', 'li']''',
     "Use <b>copy.deepcopy</b> when the data is nested and you will change the copy. A favourite interview question."),

 # ------------------------------------------------------------------ COLLECTIONS
 code_out(M, "collections", "Specialised containers save code", '''
from collections import Counter, defaultdict, deque, namedtuple

words = "to be or not to be".split()
print(Counter(words).most_common(2))

by_letter = defaultdict(list)
for w in words:
    by_letter[w[0]].append(w)          # no "if key not in"
print(dict(by_letter))

recent = deque(maxlen=3)               # keeps the last 3
for page in ["/home", "/shop", "/cart", "/pay"]:
    recent.append(page)
print(list(recent))

Point = namedtuple("Point", "x y")
print(Point(3, 4).x)''',
     steps=["<b>Counter</b>: count anything in one line.", "<b>defaultdict</b>: missing keys get a default.",
            "<b>deque</b>: O(1) at both ends; <b>maxlen</b> drops old items."]),

 # ------------------------------------------------------------------ DATACLASSES
 code_out(M, "dataclasses", "Classes for data without boilerplate", '''
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "EUR"

@dataclass
class Order:
    id: int
    items: list[str] = field(default_factory=list)   # not = []!
    total: Money = Money(0)

o = Order(1, ["lamp"], Money(49.0))
print(o)
print(o == Order(1, ["lamp"], Money(49.0)))''',
     steps=["You get <b>__init__</b>, <b>__repr__</b> and <b>__eq__</b> for free.", "<b>frozen=True</b> = immutable and hashable.",
            "Mutable defaults need <b>field(default_factory=list)</b>."]),

 # ------------------------------------------------------------------ ENUMS + HEAPQ
 code_out(M, "Enums", "A fixed set of named options", '''
from enum import StrEnum

class Status(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"

s = Status("paid")             # from the database / JSON
print(s, s == "paid", s is Status.PAID)
print([x.value for x in Status])

try:
    Status("payed")            # typo: fails loudly
except ValueError as e:
    print("ValueError:", e)''',
     steps=["Typos in plain strings fail <b>silently</b>; enum typos fail <b>loudly</b>.", "<b>StrEnum</b> (3.11+) compares equal to its string: JSON and DB friendly."]),

 code_out(M, "heapq and bisect", "Always get the most urgent item first", '''
import bisect
import heapq

jobs = []
heapq.heappush(jobs, (3, "send newsletter"))
heapq.heappush(jobs, (1, "charge card"))
heapq.heappush(jobs, (2, "email receipt"))
print(heapq.heappop(jobs))             # smallest priority first

print(heapq.nlargest(2, [40, 5, 99, 12, 70]))

scores = [10, 20, 30, 40]
bisect.insort(scores, 25)              # stays sorted
print(scores, bisect.bisect_left(scores, 30))''',
     steps=["A <b>heap</b> pops the smallest in O(log n): task queues, top-k, Dijkstra.",
            "<b>bisect</b> searches and inserts in sorted lists in O(log n)."]),

 job(M, "Data structures", "Where you'll use them at work", [
     ("Dedupe and look up fast", '''
seen = set()
if order_id in seen: return   # idempotency'''),
     ("Count events for a dashboard", '''
Counter(e.status for e in events)'''),
     ("Group rows for a report", '''
by_user = defaultdict(list)
for o in orders: by_user[o.user_id].append(o)'''),
     ("Typed DTOs between layers", '''
@dataclass(frozen=True)
class OrderDTO: id: int; total: Decimal'''),
 ]),

 interview(M, "How does a Python dict work, and why are lookups O(1)?",
     ["A dict is a <b>hash table</b>: Python calls <b>hash(key)</b> and uses it to pick a slot directly.",
      "So lookup, insert and delete are <b>O(1) on average</b>; collisions are rare and handled.",
      "Keys must be <b>hashable</b>: immutable, with a stable hash (str, int, tuple; not list or dict).",
      "Since Python 3.7 dicts <b>keep insertion order</b>.",
      "Sets are the same idea without values."],
     '''
d = {"a": 1}
print(hash("a"))      # used to find the slot
d[(1, 2)] = "ok"      # tuple: hashable
d[[1, 2]] = "no"      # TypeError: unhashable''',
     "\"What happens if two keys have the same hash?\" (a collision: Python probes for another slot and compares with == to find the right key)."),

 interview(M, "List vs tuple? Shallow vs deep copy?",
     ["<b>List</b>: mutable, for many items of the same kind. <b>Tuple</b>: immutable, a fixed record, can be a dict key.",
      "Tuples are a bit smaller and faster, and signal \"this won't change\".",
      "A <b>shallow copy</b> (<b>list(x)</b>, <b>.copy()</b>, <b>x[:]</b>) copies the outer object but <b>shares</b> nested objects.",
      "A <b>deep copy</b> (<b>copy.deepcopy</b>) copies everything recursively."],
     '''
a = [[1, 2], [3]]
b = a.copy()
b[0].append(99)
print(a)        # [[1, 2, 99], [3]]  shared!''',
     "\"Which data structure would you use for an LRU cache?\" (an OrderedDict or dict + deque; or just functools.lru_cache)."),

 recap(M, "Module 9 in 6 lines",
     ["Know <b>O(1)</b>, <b>O(log n)</b>, <b>O(n)</b>, <b>O(n&#178;)</b>, and say them out loud.",
      "Membership checks: <b>set</b>, not list. Lookups by key: <b>dict</b>.",
      "List = many similar items; tuple = a fixed record; queue = <b>deque</b>.",
      "<b>.copy()</b> is shallow; nested data needs <b>deepcopy</b>.",
      "<b>Counter</b>, <b>defaultdict</b>, <b>dataclass</b>, <b>StrEnum</b> remove boilerplate.",
      "<b>heapq</b> for \"most urgent first\", <b>bisect</b> for sorted lists."],
     "Do <b>exercises/ex09_library_tracker.py</b>: pick the right structure for each job."),
]
