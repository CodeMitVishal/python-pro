"""Module 23 · The N+1 query problem (the #1 ORM performance bug)

Loop over 50 authors and print their books: with lazy loading, the ORM runs
1 query for the authors + 1 query PER author = 51 queries. Over a network to a
real database, that's slow. Tell SQLAlchemy up front what you'll need.

  selectinload(Author.books) -> 2 queries total, however many authors
  joinedload(Book.author)    -> 1 query with a JOIN (good for many-to-one)

Run it:  python 23_sqlalchemy_alembic/02_n_plus_1_and_loading.py
"""
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import Session, joinedload, selectinload

from models import Author, Base, Book

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as s:
    for i in range(50):
        s.add(Author(name=f"Author {i}", books=[Book(title=f"Book {i}-{j}", price=10 + j)
                                                 for j in range(3)]))
    s.commit()

# Count every SQL statement the engine sends
queries = []
event.listen(engine, "before_cursor_execute", lambda *args: queries.append(args[2]))


def count_queries(label, load_option=None):
    queries.clear()
    with Session(engine) as s:
        stmt = select(Author)
        if load_option is not None:
            stmt = stmt.options(load_option)
        total_books = sum(len(a.books) for a in s.scalars(stmt))   # touches a.books for each author
    print(f"{label:<30} {len(queries):>3} queries  ({total_books} books)")


count_queries("lazy loading (default)")                       # 51 queries
count_queries("selectinload(Author.books)", selectinload(Author.books))   # 2 queries

queries.clear()
with Session(engine) as s:
    books = s.scalars(select(Book).options(joinedload(Book.author))).all()
    names = {b.author.name for b in books}
print(f"{'joinedload(Book.author)':<30} {len(queries):>3} queries  ({len(names)} authors)")
queries.clear()
with Session(engine) as s:
    s.scalars(select(Author).options(selectinload(Author.books))).all()
print()
print("The 2nd query selectinload sends:")
print("  " + " ".join(queries[1].split())[:60] + " ... WHERE books.author_id IN (?, ?, ...)")
