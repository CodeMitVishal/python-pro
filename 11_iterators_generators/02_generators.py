"""Module 11 · Generators: iterators the easy way

A function with "yield" in it becomes a GENERATOR. Calling it doesn't run
the body; it returns a generator object. Each next() runs the code until
the next yield, hands out that value, and PAUSES right there, keeping all
its local variables. The next next() continues from that exact spot.

TEACHING NOTES
  Why it matters  Loading a 10 GB file into a list crashes the server; you only need one item at
                  a time.
  Picture it      yield is a pause button: the function hands out a value and sleeps until asked
                  for the next one.
  Watch out       Calling a generator function doesn't run it; and a generator is used up after
                  one pass.
  In real jobs    Streaming CSV exports, reading huge files, paginating APIs.
  Interview       Q: What is a generator and why use it?
                  A: A function with yield that produces values lazily; memory stays constant
                     for any data size.

Run it:  python 11_iterators_generators/02_generators.py
"""
import sys

# --- 1. The Countdown class from lesson 01, as a 4-line generator ---------------
def countdown(start):
    while start > 0:
        yield start            # hand out a value and pause here
        start -= 1             # continue from here on the next next()

print(list(countdown(3)))      # [3, 2, 1]

# --- 2. Watch it pause and resume ---------------------------------------------------
def steps():
    print("  -> start")
    yield 1
    print("  -> after first yield")
    yield 2
    print("  -> finished")

gen = steps()                  # nothing printed yet: the body hasn't started
print(next(gen))               # -> start, then 1
print(next(gen))               # -> after first yield, then 2
print(next(gen, "done"))       # -> finished, then the default "done" (no crash)

# --- 3. Memory: a list stores everything, a generator stores one item ----------------
big_list = [n * n for n in range(1_000_000)]
big_gen = (n * n for n in range(1_000_000))     # generator expression
print(f"list:      {sys.getsizeof(big_list):>10,} bytes")
print(f"generator: {sys.getsizeof(big_gen):>10,} bytes")   # tiny, whatever the size
print(sum(big_gen))            # works the same; values are made one at a time

# --- 4. Infinite generators are fine: you just take what you need -------------------
def ids(prefix):
    n = 1
    while True:                # never ends...
        yield f"{prefix}-{n:04d}"
        n += 1

order_ids = ids("ORD")
print([next(order_ids) for _ in range(3)])   # ['ORD-0001', 'ORD-0002', 'ORD-0003']

# --- 5. yield from: hand over to another iterable ------------------------------------
def all_rows():
    yield "header"
    yield from ["row 1", "row 2"]   # same as: for r in [...]: yield r
    yield "footer"

print(list(all_rows()))        # ['header', 'row 1', 'row 2', 'footer']

# Rule: a generator can only be looped ONCE. Need it again? Call the function again.
