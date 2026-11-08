"""Exercise 9 · Library tracker: pick the right data structure

A small library keeps books and a list of loans (who borrowed what).
Fill in each TODO using the data structure that fits the job best.

  Book dataclass -> one clean record per book
  dict index     -> find a book by ISBN in O(1)
  Counter        -> the most borrowed books
  defaultdict    -> titles grouped by author
  set            -> unique borrowers
  deque          -> only the last 3 returns

Run it to check your work:
    python exercises/ex09_library_tracker.py

Stuck? Compare with solutions/ex09_library_tracker.py
"""
from collections import Counter, defaultdict, deque
from dataclasses import dataclass


# TODO 1: turn Book into a dataclass with fields isbn (str), title (str), author (str)
class Book:
    pass


BOOKS_DATA = [
    ("111", "Fluent Python", "Ramalho"),
    ("222", "Clean Code", "Martin"),
    ("333", "Clean Architecture", "Martin"),
    ("444", "Python Tricks", "Bader"),
]

# (borrower, isbn)
LOANS = [
    ("vishal", "111"), ("raj", "222"), ("li", "111"),
    ("vishal", "333"), ("sam", "111"), ("raj", "444"), ("li", "222"),
]


def build_index(books):
    """TODO 2: return a dict {isbn: Book} so lookups are O(1)."""


def most_borrowed(loans, n):
    """TODO 3: return the n most borrowed ISBNs as [(isbn, count), ...]."""


def titles_by_author(books):
    """TODO 4: return {author: [title, ...]} (a defaultdict(list) is perfect)."""


def unique_borrowers(loans):
    """TODO 5: return the set of people who borrowed at least one book."""


class ReturnLog:
    """TODO 6: remember only the LAST 3 returned ISBNs (hint: deque(maxlen=3))."""

    def __init__(self):
        self.recent = None

    def returned(self, isbn):
        pass

    def last(self):
        return list(self.recent)


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    books = [Book(*row) for row in BOOKS_DATA]
    index = build_index(books)
    assert index["222"].title == "Clean Code"
    assert most_borrowed(LOANS, 1) == [("111", 3)]
    by_author = titles_by_author(books)
    assert by_author["Martin"] == ["Clean Code", "Clean Architecture"]
    assert unique_borrowers(LOANS) == {"vishal", "raj", "li", "sam"}
    log = ReturnLog()
    for isbn in ["111", "222", "333", "444"]:
        log.returned(isbn)
    assert log.last() == ["222", "333", "444"]
    assert Book("1", "A", "B") == Book("1", "A", "B"), "Hint: @dataclass gives you __eq__"
    print("All checks passed!")
