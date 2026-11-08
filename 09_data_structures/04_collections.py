"""Module 9 · The collections module: specialised containers

Four tools that remove a lot of boilerplate:
  Counter     -> count things
  defaultdict -> a dict that creates missing values for you
  deque       -> fast adds/removes at both ends, with an optional max length
  namedtuple  -> a tuple whose fields have names

TEACHING NOTES
  Why it matters  Counting, grouping and queues are so common that the standard library has
                  ready-made containers.
  Picture it      Counter is a tally sheet, defaultdict a filing cabinet that creates missing
                  folders, deque a two-ended tube.
  Watch out       Counter and defaultdict create keys when you READ a missing key with [ ]; use
                  .get() to just look.
  In real jobs    Counter(e.status for e in events) for dashboards; deque(maxlen=100) for
                  recent-activity feeds.
  Interview       Q: Which collections classes do you use and why?
                  A: Counter (counting), defaultdict (grouping), deque (O(1) queues), namedtuple
                     (light records).

Run it:  python 09_data_structures/04_collections.py
"""
from collections import Counter, defaultdict, deque, namedtuple

# --- 1. Counter ------------------------------------------------------------------
words = "the cat and the hat and the bat".split()
counts = Counter(words)
print(counts.most_common(2))              # [('the', 3), ('and', 2)]
print(counts["dog"])                      # 0: missing keys count as zero
counts.update(["cat", "cat"])             # add more counts
print(counts["cat"])                      # 3

# --- 2. defaultdict: group items without "if key not in dict" -----------------------
people = [("Vishal", "Cloud"), ("Raj", "Data"), ("Li", "Cloud")]

# Without defaultdict:
by_team = {}
for name, team in people:
    if team not in by_team:
        by_team[team] = []
    by_team[team].append(name)

# With defaultdict(list): a missing key starts as an empty list automatically
by_team = defaultdict(list)
for name, team in people:
    by_team[team].append(name)
print(dict(by_team))                      # {'Cloud': ['Vishal', 'Li'], 'Data': ['Raj']}

# defaultdict(int) is a quick counter: missing keys start at 0
letters = defaultdict(int)
for ch in "banana":
    letters[ch] += 1
print(dict(letters))                      # {'b': 1, 'a': 3, 'n': 2}

# --- 3. deque: a double-ended queue ---------------------------------------------------
recent = deque(maxlen=3)                  # keeps only the last 3 items
for page in ["home", "blog", "shop", "cart"]:
    recent.append(page)
print(list(recent))                       # ['blog', 'shop', 'cart']  ('home' fell out)

tasks = deque(["write", "test"])
tasks.appendleft("plan")                  # O(1) at the front (a list would be O(n))
print(tasks.popleft(), list(tasks))       # plan ['write', 'test']

# --- 4. namedtuple: readable fields, still a lightweight tuple ------------------------
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 7)
print(p.x, p.y)                           # 3 7  (instead of p[0], p[1])
x, y = p                                  # still unpacks like a tuple
print(p._replace(x=10))                   # Point(x=10, y=7): a new tuple, p is unchanged
