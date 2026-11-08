"""Module 9 · Demo: a web server log analyzer

Picks the right data structure for each question:
  Counter     -> which pages are most popular?
  defaultdict -> which pages did each user visit?
  set         -> how many unique visitors?
  deque       -> what were the last 3 errors?
  dataclass   -> one clean record per log line

TEACHING NOTES
  Why it matters  Log analysis is a classic interview take-home and a daily ops task.
  Picture it      Each structure is a tool on a workbench: Counter counts, defaultdict groups, a
                  set de-duplicates.
  Watch out       Load logs lazily (line by line) when files are big; this demo is small on
                  purpose.
  In real jobs    Finding top error endpoints, slowest requests and suspicious IPs from web
                  server logs.
  Interview       Q: How would you find the 10 most common IPs in a 5 GB log file?
                  A: Stream it line by line, count with a Counter (or a dict), then
                     most_common(10); memory = number of distinct IPs.

Run it:  python 09_data_structures/06_demo_log_analyzer.py
"""
from collections import Counter, defaultdict, deque
from dataclasses import dataclass

LOG = """10:01 vishal GET /home 200
10:02 raj GET /blog 200
10:02 vishal GET /shop 200
10:03 li GET /home 200
10:04 raj GET /cart 500
10:05 sam GET /home 404
10:06 li GET /shop 200
10:07 vishal GET /cart 500
10:08 raj GET /home 200
10:09 li GET /cart 500"""


@dataclass
class Entry:
    time: str
    user: str
    method: str
    path: str
    status: int


# 1. Parse each line into an Entry (split + unpack + int conversion)
entries = []
for line in LOG.splitlines():
    time, user, method, path, status = line.split()
    entries.append(Entry(time, user, method, path, int(status)))

# 2. Ask questions, each with the data structure that fits it
popular = Counter(e.path for e in entries)
pages_by_user = defaultdict(set)
last_errors = deque(maxlen=3)
for e in entries:
    pages_by_user[e.user].add(e.path)
    if e.status >= 500:
        last_errors.append(f"{e.time} {e.path} ({e.user})")
visitors = {e.user for e in entries}

# 3. Report
print("Top pages:")
for path, hits in popular.most_common(3):
    print(f"  {path:<6} {hits} hits")
print(f"\nUnique visitors: {len(visitors)} -> {', '.join(sorted(visitors))}")
print("\nPages per user:")
for user, pages in sorted(pages_by_user.items()):
    print(f"  {user:<7} {', '.join(sorted(pages))}")
print("\nLast 3 server errors:")
for err in last_errors:
    print(f"  {err}")
