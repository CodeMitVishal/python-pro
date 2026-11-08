"""Slides · Module 8 · Pythonic code"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 8 · Pythonic code"
SLIDES = [
 cover("08", "Pythonic code", "Write Python the way experienced developers do: shorter, clearer, and fewer bugs.",
       [("Comprehensions", "01_comprehensions.py"), ("Unpacking", "02_unpacking.py"),
        ("Looping like a pro", "03_looping_like_a_pro.py"), ("Truthiness &amp; walrus", "04_truthiness_and_walrus.py"),
        ("Strings like a pro", "05_strings_like_a_pro.py"), ("Pattern matching", "07_pattern_matching.py"),
        ("Regular expressions", "08_regex.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Pythonic code", "What does \"Pythonic\" mean?",
     "Two programs can give the same result. One is <b>12 lines</b> of index juggling; the other is <b>3 clear lines</b>.<br><br>"
     "In code reviews and interviews, people judge you on the second kind.",
     "Pythonic = using the language's own tools (<b>comprehensions, unpacking, enumerate, zip</b>) so the code reads like English."),

 # ------------------------------------------------------------------ COMPREHENSIONS
 picture(M, "Comprehensions", "A loop squeezed into one line",
     "&#127981; Think of a <b>factory line</b>: items come in (<b>for</b>), a quality check throws some out (<b>if</b>), "
     "and each good item is shaped (<b>expression</b>) before it goes in the box.",
     [("for p in prices", "take every item"), ("if p > 10", "keep only some (optional)"),
      ("p * 1.19", "shape each one"), ("[ ... ]", "collect into a new list")],
     "Read it in this order: <b>[ shape  for item in items  if check ]</b>"),

 code_out(M, "Comprehensions", "Lists, dicts and sets in one line", '''
prices = [5, 12, 30, 8]

# the long way
with_vat = []
for p in prices:
    if p > 10:
        with_vat.append(round(p * 1.19, 2))
print(with_vat)

# the Pythonic way
print([round(p * 1.19, 2) for p in prices if p > 10])

names = ["vishal", "li", "sam"]
print({n: len(n) for n in names})        # dict
print({len(n) for n in names})           # set: no duplicates''',
     steps=["Same result, <b>one line</b>, and it's faster.", "<b>{k: v for ...}</b> builds a dict.",
            "<b>{x for ...}</b> builds a set; <b>(x for ...)</b> is a lazy generator (Module 11)."]),

 mistake(M, "Comprehensions", "When NOT to use a comprehension",
     '''
[print(u) for u in users]          # side effect

grid = [[c for c in row if c]
        for row in data if row
        if len(row) > 2]           # unreadable''',
     "A comprehension <b>builds a list</b>. Using it only to print or save throws that list away. Deep nesting is hard to read.",
     '''
for u in users:                    # a plain loop
    print(u)

def clean(row):                    # name the step
    return [c for c in row if c]

grid = [clean(r) for r in data if len(r) > 2]''',
     "Rule: if you need a <b>result</b>, use a comprehension. If you need an <b>action</b>, or it doesn't fit in one line, write a loop."),

 # ------------------------------------------------------------------ UNPACKING
 code_out(M, "Unpacking", "Take values out of a sequence by position", '''
a, b = 1, 2
a, b = b, a                    # swap: no temp variable
print(a, b)

first, *middle, last = [10, 20, 30, 40, 50]
print(first, middle, last)

name, (city, zip_code) = "Vishal", ("Augsburg", "86150")
print(name, city, zip_code)

defaults = {"theme": "light", "lang": "en"}
user = {"lang": "de"}
print({**defaults, **user})    # merge: right side wins''',
     steps=["The right side is built <b>first</b>, then assigned: that's why swapping works.",
            "<b>*name</b> collects \"the rest\" into a list.", "<b>{**a, **b}</b> merges dicts (also <b>a | b</b> in 3.9+)."]),

 # ------------------------------------------------------------------ LOOPING
 mistake(M, "Looping like a pro", "Stop writing range(len(...))",
     '''
names = ["vishal", "li"]
scores = [91, 78]
for i in range(len(names)):
    print(i, names[i], scores[i])''',
     "Index juggling is noisy and breaks easily (IndexError when the lists have different lengths).",
     '''
for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(i, name, score)''',
     "<b>enumerate</b> gives the counter, <b>zip</b> walks several lists together. No indexes, no IndexError."),

 code_out(M, "Looping like a pro", "Sort, search and check without loops", '''
users = [{"name": "vishal", "age": 31}, {"name": "li", "age": 25},
         {"name": "sam", "age": 40}]

by_age = sorted(users, key=lambda u: u["age"])
print([u["name"] for u in by_age])

print(max(users, key=lambda u: u["age"])["name"])
print(any(u["age"] > 35 for u in users))   # at least one?
print(all(u["age"] > 18 for u in users))   # every one?
print(sum(u["age"] for u in users) / len(users))''',
     steps=["<b>key=</b> says <b>what</b> to compare.", "<b>any</b> / <b>all</b> stop as soon as the answer is known.",
            "<b>sorted()</b> returns a new list; <b>.sort()</b> changes the list in place."]),

 # ------------------------------------------------------------------ TRUTHINESS + WALRUS
 code_out(M, "Truthiness", "Every value is either truthy or falsy", '''
for value in [0, "", [], {}, None, "0", [0], -1]:
    print(f"{value!r:6} -> {bool(value)}")''',
     steps=["<b>Falsy</b>: zero, empty containers, <b>None</b>, <b>False</b>.", "Everything else is <b>truthy</b>, even <b>\"0\"</b> and <b>[0]</b>.",
            "So <b>if items:</b> means \"if the list is not empty\"."]),

 mistake(M, "Truthiness", "When \"if x\" is a bug",
     '''
def apply_discount(price, discount=None):
    if not discount:              # 0 is falsy!
        discount = 0.10           # default 10%
    return price * (1 - discount)

print(apply_discount(100, 0))     # 90.0  ???''',
     "A real <b>0</b> (no discount) is falsy, so the code silently replaces it with 10%. Customers get a discount they shouldn't.",
     '''
def apply_discount(price, discount=None):
    if discount is None:          # only "missing"
        discount = 0.10
    return price * (1 - discount)

print(apply_discount(100, 0))     # 100''',
     "Test for <b>None</b> with <b>is None</b> when 0, \"\" or [] are valid values."),

 code_out(M, "Walrus :=", "Assign and test in one step", '''
import re

lines = ["GET /home 200", "GET /admin 403", "POST /login 500"]
for line in lines:
    if (m := re.search(r"(\\d{3})$", line)) and m.group(1) >= "400":
        print("problem:", line)

data = [3, 8, 1, 9]
if (n := len(data)) > 3:
    print(f"list too long ({n} items)")''',
     steps=["<b>:=</b> stores the value <b>and</b> returns it.", "Avoids computing the same thing twice.",
            "Use it in <b>if</b> and <b>while</b>; don't sprinkle it everywhere."]),

 # ------------------------------------------------------------------ STRINGS
 code_out(M, "Strings like a pro", "f-strings can format anything", '''
name, price, ratio, n = "Lamp", 1234.5, 0.4567, 7

print(f"{name:<8}|{price:>12,.2f}|")   # align + thousands
print(f"{ratio:.1%}")                   # percentage
print(f"{n:03d}")                       # zero padding
print(f"{price=}")                      # debug print (3.8+)

words = ["fast", "clear", "pythonic"]
print(", ".join(words))
print("a,b,,c".split(","))''',
     steps=["<b>:&lt;8</b> left, <b>:&gt;12</b> right, <b>,.2f</b> thousands + 2 decimals.",
            "<b>{x=}</b> prints the name and the value: great for debugging.",
            "<b>join</b> glues a list into one string; <b>split</b> does the opposite."]),

 mistake(M, "Strings like a pro", "Building a string in a loop",
     '''
report = ""
for row in rows:
    report += row + "\\n"   # copies the whole
                            # string every time''',
     "Strings are <b>immutable</b>: every <b>+=</b> creates a new, longer string. With 100,000 rows that's very slow (quadratic).",
     '''
report = "\\n".join(rows)

# or collect parts first
parts = [f"{r.id}: {r.total}" for r in rows]
report = "\\n".join(parts)''',
     "Collect pieces in a <b>list</b>, then <b>join</b> once. Linear time."),

 # ------------------------------------------------------------------ MATCH + REGEX
 code_out(M, "Pattern matching (3.10+)", "match / case: branch on the SHAPE of data", '''
def handle(event):
    match event:
        case {"type": "order", "items": [first, *rest]}:
            return f"order: {first} (+{len(rest)} more)"
        case {"type": "refund", "amount": float(a)} if a > 0:
            return f"refund {a:.2f} EUR"
        case {"type": "ping"}:
            return "pong"
        case _:
            return "unknown event"

print(handle({"type": "order", "items": ["lamp", "cable", "plug"]}))
print(handle({"type": "refund", "amount": 19.9}))
print(handle({"type": "ping", "extra": 1}))
print(handle({"oops": True}))''',
     steps=["Matches <b>dicts</b> (extra keys allowed), <b>lists</b>, <b>types</b> and <b>classes</b>.",
            "A name in a pattern <b>captures</b> the value.", "<b>if</b> after a pattern is a <b>guard</b>; <b>_</b> matches anything."]),

 code_out(M, "Regular expressions", "Find patterns in text", '''
import re

log = "2026-11-08 12:01 ERROR user=vishal ip=10.0.0.7 took=532ms"

m = re.search(r"(?P<level>[A-Z]+) user=(?P<user>\\w+)", log)
print(m["level"], m["user"])

print(re.findall(r"\\d+ms", log))
print(re.sub(r"ip=\\S+", "ip=***", log))

EMAIL = re.compile(r"^[\\w.+-]+@[\\w-]+\\.[\\w.]+$")
print(bool(EMAIL.match("vishal@example.com")), bool(EMAIL.match("nope@")))''',
     steps=["<b>(?P&lt;name&gt;...)</b> = a named group you read with <b>m[\"name\"]</b>.",
            "<b>findall</b> = every match; <b>sub</b> = search and replace.", "Always use raw strings: <b>r\"...\"</b>."]),

 job(M, "Pythonic code", "Where you'll use this every day", [
     ("Turn DB rows into API JSON", '''
return [{"id": o.id, "total": o.total}
        for o in orders if o.paid]'''),
     ("Merge config and defaults", '''
settings = {**DEFAULTS, **env_settings}'''),
     ("Mask secrets in logs", '''
re.sub(r"token=\\S+", "token=***", line)'''),
     ("Route webhook events", '''
match payload:
    case {"event": "payment.succeeded"}: ...'''),
 ]),

 interview(M, "What's the difference between is and ==?",
     ["<b>==</b> compares <b>values</b>: do these two objects contain the same data?",
      "<b>is</b> compares <b>identity</b>: are these the <b>same object</b> in memory (same id)?",
      "Use <b>is</b> only for singletons: <b>None</b>, <b>True</b>, <b>False</b>.",
      "Small ints and short strings may be cached, so <b>is</b> can look right by accident. Never rely on it."],
     '''
a = [1, 2]
b = [1, 2]
print(a == b)    # True   same values
print(a is b)    # False  two objects
print(a is a)    # True
x = None
print(x is None) # the right way''',
     "\"What is a list comprehension vs a generator expression?\" ([] builds the whole list now; () makes values lazily, one by one)."),

 interview(M, "How do you make code more Pythonic?",
     ["Use <b>comprehensions</b> instead of append loops, when building a result.",
      "<b>enumerate</b> and <b>zip</b> instead of <b>range(len(...))</b>.",
      "<b>Unpacking</b>, <b>f-strings</b>, <b>join</b>, and <b>sorted(key=...)</b>.",
      "<b>EAFP</b>: try the operation and catch the error, instead of checking everything first.",
      "Follow <b>PEP 8</b> and let <b>ruff</b> point out the rest (Module 15)."],
     None,
     "\"What does EAFP vs LBYL mean?\" (Easier to Ask Forgiveness than Permission vs Look Before You Leap: Python prefers try/except)."),

 recap(M, "Module 8 in 6 lines",
     ["<b>[shape for x in xs if check]</b>, but use a loop for side effects.",
      "<b>a, b = b, a</b>; <b>first, *rest = xs</b>; <b>{**a, **b}</b>.",
      "<b>enumerate</b>, <b>zip</b>, <b>sorted(key=)</b>, <b>any</b>/<b>all</b>: no index juggling.",
      "Empty and zero are falsy; use <b>is None</b> when 0 is valid.",
      "f-strings format everything; build big strings with <b>join</b>.",
      "<b>match/case</b> for shapes, <b>re</b> with named groups for text."],
     "Do <b>exercises/ex08_refactor_to_pythonic.py</b>: turn clumsy code into Pythonic code."),
]
