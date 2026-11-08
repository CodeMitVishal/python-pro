"""Module 12 · Dunder ("magic") methods: make your objects feel built-in

Python calls special methods behind the scenes:
  print(x)  -> x.__str__()       len(x)    -> x.__len__()
  repr(x)   -> x.__repr__()      x[i]      -> x.__getitem__(i)
  a == b    -> a.__eq__(b)       a + b     -> a.__add__(b)
  a < b     -> a.__lt__(b)       item in x -> x.__contains__(item)
Implement them and your class works with print, len, +, ==, sorted, in, for...

TEACHING NOTES
  Why it matters  Objects that print as <object at 0x...> and can't be added or compared feel
                  broken.
  Picture it      Dunder methods are hooks: Python calls them behind +, ==, len(), print() and
                  for loops.
  Watch out       If you define __eq__, also define __hash__ (or the object becomes unhashable).
  In real jobs    Money and Vector types, Django model __str__, rich comparisons for sorting.
  Interview       Q: __str__ vs __repr__?
                  A: __repr__ is unambiguous for developers (shell, logs); __str__ is friendly
                     text for users.

Run it:  python 12_advanced_oop/01_dunder_methods.py
"""
from functools import total_ordering


@total_ordering                      # define __eq__ + __lt__, get <=, >, >= for free
class Money:
    def __init__(self, amount, currency="EUR"):
        self.amount = round(amount, 2)
        self.currency = currency

    def __repr__(self):              # for developers: unambiguous, ideally valid code
        return f"Money({self.amount}, {self.currency!r})"

    def __str__(self):               # for users: pretty
        return f"{self.amount:,.2f} {self.currency}"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented    # let Python try the other side / fail politely
        return (self.amount, self.currency) == (other.amount, other.currency)

    def __hash__(self):              # objects that are equal must hash the same
        return hash((self.amount, self.currency))

    def __lt__(self, other):
        return self.amount < other.amount

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("can't add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __bool__(self):              # Money(0) is falsy
        return self.amount != 0


a, b = Money(10.5), Money(4.25)
print(a + b)                         # 14.75 EUR        (__add__ + __str__)
print(repr(a))                       # Money(10.5, 'EUR')
print(a == Money(10.5), a > b)       # True True        (__eq__, total_ordering)
print(sorted([a, b, Money(1)]))      # [Money(1, 'EUR'), Money(4.25, 'EUR'), Money(10.5, 'EUR')]
print(bool(Money(0)))                # False
print(len({a, Money(10.5)}))         # 1: equal objects -> one set entry (__hash__)


class Playlist:
    """A container: len, indexing, slicing, 'in' and for-loops all work."""

    def __init__(self, *songs):
        self._songs = list(songs)

    def __len__(self):
        return len(self._songs)

    def __getitem__(self, index):    # also makes the object iterable and sliceable
        return self._songs[index]

    def __contains__(self, song):
        return song.lower() in (s.lower() for s in self._songs)


p = Playlist("Intro", "Main Theme", "Outro")
print(len(p), p[0], p[-1], p[:2])    # 3 Intro Outro ['Intro', 'Main Theme']
print("main theme" in p)             # True (case-insensitive, thanks to __contains__)
for song in p:
    print(" -", song)
