"""Module 11 · How a for loop really works (the iteration protocol)

ITERABLE : something you can loop over (list, str, dict, file...).
           It has __iter__(), which hands out an iterator.
ITERATOR : the thing that remembers WHERE you are.
           It has __next__(), which returns the next item, or raises
           StopIteration when there is nothing left.

    for x in things:        is really:     it = iter(things)
        print(x)                           while True:
                                               try: x = next(it)
                                               except StopIteration: break
                                               print(x)

TEACHING NOTES
  Why it matters  Every for loop, comprehension and sum() uses the same protocol; knowing it
                  explains generators.
  Picture it      A ticket dispenser: iter() gives you the dispenser, next() hands out one
                  ticket, StopIteration = empty.
  Watch out       Iterators are single-use: looping a second time gives nothing.
  In real jobs    Custom iterable classes for paginated API results or DB cursors.
  Interview       Q: Iterable vs iterator?
                  A: An iterable can create iterators (__iter__); an iterator has __next__ and
                     remembers its position.

Run it:  python 11_iterators_generators/01_iteration_protocol.py
"""

# --- 1. Drive a for loop by hand --------------------------------------------------
colors = ["red", "green", "blue"]
it = iter(colors)              # ask the list for an iterator
print(next(it))                # red
print(next(it))                # green
print(next(it))                # blue
try:
    next(it)
except StopIteration:
    print("StopIteration: the iterator is used up")

# --- 2. An iterator is used up after one pass ------------------------------------
it = iter([1, 2, 3])
print(list(it))                # [1, 2, 3]
print(list(it))                # []  <- nothing left; a LIST can be looped again, its iterator can't

# --- 3. Build your own iterator class ----------------------------------------------
class Countdown:
    """Counts down from start to 1."""

    def __init__(self, start):
        self.current = start

    def __iter__(self):        # "I am my own iterator"
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration        # tells the for loop to stop
        value = self.current
        self.current -= 1
        return value

for n in Countdown(3):
    print(n, end=" ")          # 3 2 1
print()

# --- 4. Many built-ins return iterators, not lists --------------------------------
pairs = zip("ab", [1, 2])
print(pairs)                   # <zip object ...>: lazy, nothing computed yet
print(list(pairs))             # [('a', 1), ('b', 2)]
# map, filter, enumerate, zip, reversed, dict.items(), open(file)... are all lazy.
