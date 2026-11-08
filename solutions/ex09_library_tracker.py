"""Solution · Exercise 9: Library tracker

Run it:  python solutions/ex09_library_tracker.py
"""
from collections import Counter, defaultdict, deque
from dataclasses import dataclass


@dataclass
class Book:
    isbn: str
    title: str
    author: str


BOOKS_DATA = [
    ("111", "Fluent Python", "Ramalho"),
    ("222", "Clean Code", "Martin"),
    ("333", "Clean Architecture", "Martin"),
    ("444", "Python Tricks", "Bader"),
]

LOANS = [
    ("vishal", "111"), ("raj", "222"), ("li", "111"),
    ("vishal", "333"), ("sam", "111"), ("raj", "444"), ("li", "222"),
]


def build_index(books):
    # dict comprehension: isbn -> Book, so index[isbn] is O(1)
    return {book.isbn: book for book in books}


def most_borrowed(loans, n):
    # Counter counts the ISBNs; most_common(n) sorts by count for us
    return Counter(isbn for _, isbn in loans).most_common(n)


def titles_by_author(books):
    # defaultdict(list) creates the empty list the first time we see an author
    grouped = defaultdict(list)
    for book in books:
        grouped[book.author].append(book.title)
    return grouped


def unique_borrowers(loans):
    # set comprehension: duplicates disappear automatically
    return {person for person, _ in loans}


class ReturnLog:
    def __init__(self):
        self.recent = deque(maxlen=3)   # old items drop off the front by themselves

    def returned(self, isbn):
        self.recent.append(isbn)

    def last(self):
        return list(self.recent)


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
    assert Book("1", "A", "B") == Book("1", "A", "B")
    print("All checks passed!")
