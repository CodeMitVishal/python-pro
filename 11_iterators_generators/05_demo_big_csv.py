"""Module 11 · Demo: analyse a 200,000-row CSV with almost no memory

We write a big sales CSV, then compute totals two ways and measure the
peak memory with tracemalloc:
  1. load every row into a list first   (eager)
  2. stream the rows with generators     (lazy)

Run it:  python 11_iterators_generators/05_demo_big_csv.py
"""
import csv
import random
import tempfile
import tracemalloc
from pathlib import Path

path = Path(tempfile.gettempdir()) / "python_pro_sales.csv"
random.seed(1)
with open(path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["country", "amount"])
    for _ in range(200_000):
        writer.writerow([random.choice(["DE", "IN", "US"]), round(random.uniform(5, 500), 2)])
print(f"Wrote {path.stat().st_size / 1_000_000:.1f} MB to {path.name}")


def eager_total(p):
    with open(p, newline="") as f:
        rows = list(csv.DictReader(f))              # EVERYTHING in memory
    return sum(float(r["amount"]) for r in rows if r["country"] == "DE")


def read_rows(p):
    with open(p, newline="") as f:
        yield from csv.DictReader(f)                # one row at a time


def lazy_total(p):
    de_amounts = (float(r["amount"]) for r in read_rows(p) if r["country"] == "DE")
    return sum(de_amounts)


for name, func in [("eager (list)", eager_total), ("lazy (generators)", lazy_total)]:
    tracemalloc.start()
    total = func(path)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{name:<18} total DE = {total:>12,.2f}   peak memory = {peak / 1_000_000:6.2f} MB")

path.unlink()                                       # clean up the temp file
