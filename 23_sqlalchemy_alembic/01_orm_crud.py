"""Module 23 · SQLAlchemy ORM: tables as Python classes

  pip install sqlalchemy

An ORM (Object-Relational Mapper) lets you work with rows as Python objects.
SQLAlchemy writes the SQL, protects you from SQL injection, and the SAME code
works on SQLite, PostgreSQL, MySQL, SQL Server and Azure SQL.

  engine   -> knows HOW to connect to the database
  Session  -> a unit of work: track changes, then commit them together
  select() -> build queries in Python

TEACHING NOTES
  Why it matters  Hand-written SQL strings everywhere are hard to maintain; an ORM gives typed,
                  safe queries.
  Picture it      The ORM is a translator between Python objects and table rows.
  Watch out       Commit inside a Session; objects outside it may be detached and can't lazy-
                  load.
  In real jobs    Models with Mapped[...], select() queries in services and repositories.
  Interview       Q: What is an ORM, and what are its downsides?
                  A: Maps tables to classes; less boilerplate and safe SQL, but it can hide slow
                     queries like N+1.

Run it:  python 23_sqlalchemy_alembic/01_orm_crud.py
"""
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from models import Author, Base, Book

engine = create_engine("sqlite:///:memory:", echo=False)   # echo=True prints every SQL statement
Base.metadata.create_all(engine)                            # CREATE TABLE ... (Alembic does this in real apps)

# --- CREATE -------------------------------------------------------------------------------------
with Session(engine) as session:                            # the session is closed automatically
    ramalho = Author(name="Luciano Ramalho", country="BR")
    martin = Author(name="Robert C. Martin", country="US")
    ramalho.books.append(Book(title="Fluent Python", price=49.9))   # relationship sets author_id
    martin.books += [Book(title="Clean Code", price=34.5),
                     Book(title="Clean Architecture", price=29.9)]
    session.add_all([ramalho, martin])
    session.commit()                                        # one transaction for everything
    print("ids assigned:", [b.id for b in martin.books])    # [2, 3]

# --- READ ----------------------------------------------------------------------------------------
with Session(engine) as session:
    cheap = session.scalars(
        select(Book).where(Book.price < 40).order_by(Book.price)
    ).all()
    print("cheap books:", cheap)

    book = session.get(Book, 1)                              # by primary key
    print("book 1:", book.title, "by", book.author.name)    # follow the relationship

    # JOIN + GROUP BY: books and average price per author
    rows = session.execute(
        select(Author.name, func.count(Book.id), func.avg(Book.price))
        .join(Author.books)
        .group_by(Author.name)
        .order_by(Author.name)
    ).all()
    for name, count, avg in rows:
        print(f"  {name:<18} {count} book(s), avg {avg:.2f}")

    # Parameters are bound safely, even with "evil" input
    evil = "x' OR '1'='1"
    print("injection attempt:", session.scalars(select(Book).where(Book.title == evil)).all())

# --- UPDATE + DELETE ---------------------------------------------------------------------------------
with Session(engine) as session:
    book = session.scalars(select(Book).where(Book.title == "Clean Code")).one()
    book.price = 29.0                                        # just change the attribute...
    martin = session.scalars(select(Author).where(Author.name.like("Robert%"))).one()
    session.delete(martin)                                   # cascade deletes his books too
    session.commit()                                         # ...the session writes the UPDATE/DELETEs

with Session(engine) as session:
    print("books left:", session.scalars(select(Book.title)).all())   # ['Fluent Python']
