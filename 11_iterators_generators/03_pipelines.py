"""Module 11 · Lazy pipelines: chain generators like an assembly line

Each stage takes an iterable, does ONE job and yields results to the next
stage. No stage builds a full list, so the pipeline handles a 10 GB file
with the same memory as a 10 line file.

    read_lines -> parse -> only_errors -> pick_fields -> first 3

TEACHING NOTES
  Why it matters  Big data processing becomes simple when each step is a small, lazy, testable
                  function.
  Picture it      An assembly line: each station takes items from the previous one, does one
                  job, passes them on.
  Watch out       Nothing runs until something consumes the pipeline (list, sum, for).
  In real jobs    Log processing, ETL jobs, data clean-up scripts.
  Interview       Q: How would you process a huge log file?
                  A: A lazy pipeline: read lines -> parse -> filter -> aggregate, one line in
                     memory at a time.

Run it:  python 11_iterators_generators/03_pipelines.py
"""
from itertools import islice

LOG = """2026-11-01 INFO  app started
2026-11-01 ERROR db timeout after 30s
2026-11-02 INFO  user vishal logged in
2026-11-02 ERROR payment failed for order 42
2026-11-03 WARN  disk 80% full
2026-11-03 ERROR db timeout after 30s
2026-11-04 ERROR cache miss storm"""


def read_lines(text):
    """Stage 1: one line at a time (with a real file: for line in open(path))."""
    for line in text.splitlines():
        print(f"    read: {line[:22]}...")     # shows the laziness
        yield line


def parse(lines):
    """Stage 2: split each line into (date, level, message)."""
    for line in lines:
        date, level, message = line.split(maxsplit=2)
        yield date, level, message


def only(level, records):
    """Stage 3: keep one level."""
    return (r for r in records if r[1] == level)   # a generator expression works too


def messages(records):
    """Stage 4: keep just the text."""
    for date, _, message in records:
        yield f"{date}: {message}"


pipeline = messages(only("ERROR", parse(read_lines(LOG))))
print("Pipeline built, nothing has run yet:", pipeline)

print("\nFirst 2 errors:")
for msg in islice(pipeline, 2):        # take only 2, then stop
    print("  =>", msg)
# Look at the "read:" lines: the pipeline read just 4 lines to find 2 errors,
# and never touched the rest of the log. That's lazy evaluation.
