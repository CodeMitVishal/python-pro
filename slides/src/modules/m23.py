"""Slides · Module 23 · SQLAlchemy 2.0 & Alembic"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 23 · SQLAlchemy 2.0 &amp; Alembic"
SLIDES = [
 cover("23", "SQLAlchemy 2.0 &amp; Alembic", "Use an ORM like a pro: models, queries, the N+1 trap, indexes, transactions and migrations.",
       [("Models", "models.py"), ("ORM CRUD", "01_orm_crud.py"), ("N+1 &amp; loading", "02_n_plus_1_and_loading.py"),
        ("SQLAlchemy + FastAPI", "03_sqlalchemy_with_fastapi.py"), ("Alembic migrations", "04_alembic_migrations.py"),
        ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "ORM", "Why an ORM?",
     "Hand-written SQL strings everywhere: typos found only at runtime, copy-pasted joins, and every row comes back as a tuple you index by number.",
     "An <b>ORM</b> maps tables to <b>Python classes</b>. You query with Python, get objects back, and the ORM writes safe, parameterised SQL."),

 code_out(M, "Models and CRUD", "Models, a session, and a query", '''
from sqlalchemy import ForeignKey, create_engine, func, select
from sqlalchemy.orm import (DeclarativeBase, Mapped, Session,
                            mapped_column, relationship)

class Base(DeclarativeBase): pass

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), index=True)
    author: Mapped[Author] = relationship(back_populates="books")

engine = create_engine("sqlite://")
Base.metadata.create_all(engine)
with Session(engine) as s:
    s.add(Author(name="Ramalho", books=[Book(title="Fluent Python")]))
    s.commit()
    stmt = select(Author.name, func.count(Book.id)).join(Book).group_by(Author.id)
    print(s.execute(stmt).all())''',
     steps=["<b>Mapped[...]</b> type hints define the columns.", "A <b>Session</b> is a unit of work: add, then commit.",
            "<b>select()</b> builds SQL with joins and group by."]),

 picture(M, "N+1", "The N+1 query problem",
     "&#128034; You load 50 authors with <b>1 query</b>, then touch <b>author.books</b> in a loop: the ORM quietly runs <b>1 more query per author</b>. "
     "51 queries, a slow page, and it gets worse as data grows.",
     [("1 query", "SELECT * FROM authors"), ("for a in authors:", "a.books ..."), ("+ N queries", "SELECT * FROM books WHERE author_id = ?"),
      ("fix", "selectinload: 2 queries total")]),

 code_out(M, "N+1", "Count the queries, then fix it", '''
from sqlalchemy import event, select
from sqlalchemy.orm import Session, selectinload

queries = 0
@event.listens_for(engine, "before_cursor_execute")
def count(*args): global queries; queries += 1

with Session(engine) as s:
    s.add_all([Author(name=f"author{i}", books=[Book(title="t")]) for i in range(50)])
    s.commit()

for options in ([], [selectinload(Author.books)]):
    queries = 0
    with Session(engine) as s:
        for a in s.scalars(select(Author).options(*options)):
            len(a.books)                    # touch the relationship
    print("eager" if options else "lazy ", "->", queries, "queries")''',
     setup='''from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
class Base(DeclarativeBase): pass
class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    books: Mapped[list["Book"]] = relationship()
class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
engine = create_engine("sqlite://")
Base.metadata.create_all(engine)''',
     steps=["Lazy loading: <b>1 + N</b> queries.", "<b>selectinload</b>: 2 queries (one IN-list). <b>joinedload</b>: 1 JOIN.",
            "Django: <b>select_related</b> / <b>prefetch_related</b>."]),

 trace(M, "Indexes", "Indexes: why some queries are 1000&times; faster", ["", "Without an index", "With an index"],
       [["How the DB finds rows", "reads <b>every</b> row (full table scan)", "walks a <b>B-tree</b> straight to them"],
        ["Cost", "O(n)", "O(log n)"],
        ["Add one on", "&#8212;", "foreign keys, columns in WHERE / JOIN / ORDER BY, unique fields"],
        ["Price you pay", "&#8212;", "slower INSERT/UPDATE, extra disk"],
        ["Check it", "<span class=\"m\">EXPLAIN</span> shows \"Seq Scan\"", "<span class=\"m\">EXPLAIN</span> shows \"Index Scan\""]],
       "Composite index <b>(user_id, created_at)</b> helps \"orders of a user, newest first\"; the column order matters."),

 code_out(M, "Indexes", "See the query plan change", '''
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, email TEXT, total REAL)")
db.executemany("INSERT INTO orders (email, total) VALUES (?, ?)",
               [(f"user{i}@mail.com", i) for i in range(50_000)])

q = "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE email = 'user42@mail.com'"
print("before:", db.execute(q).fetchone()[-1])

db.execute("CREATE INDEX ix_orders_email ON orders (email)")
print("after :", db.execute(q).fetchone()[-1])''',
     steps=["<b>SCAN</b> = read every row.", "<b>SEARCH ... USING INDEX</b> = jump to the row.",
            "In SQLAlchemy: <b>mapped_column(index=True)</b>."]),

 trace(M, "Transactions", "Isolation levels: what can go wrong concurrently", ["Level", "Prevents", "Still possible"],
       [["READ UNCOMMITTED", "&#8212;", "dirty reads (seeing uncommitted data)"],
        ["<b>READ COMMITTED</b> (Postgres default)", "dirty reads", "non-repeatable reads, phantoms"],
        ["REPEATABLE READ", "+ non-repeatable reads", "phantoms (in theory; not in Postgres)"],
        ["SERIALIZABLE", "everything", "transactions may fail and need a retry"]],
       "Lost update fix: <b>SELECT ... FOR UPDATE</b> (<span class=\"m\">.with_for_update()</span>), an atomic <b>UPDATE x = x - 1</b>, or a version column."),

 code_out(M, "SQLAlchemy + FastAPI", "One session per request", '''
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

def get_db():
    with Session(engine) as session:      # opened per request
        yield session                     # closed afterwards

DB = Annotated[Session, Depends(get_db)]
app = FastAPI()

@app.post("/authors", status_code=201)
def create(name: str, db: DB):
    db.add(Author(name=name))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "author exists")
    return {"name": name}

c = TestClient(app)
print(c.post("/authors?name=vishal").status_code, c.post("/authors?name=vishal").status_code)''',
     setup='''from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.pool import StaticPool
class Base(DeclarativeBase): pass
class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
Base.metadata.create_all(engine)''',
     steps=["A <b>yield</b> dependency = session per request, always closed.", "Unique constraint violated &#8594; <b>409 Conflict</b>.",
            "Tests override <b>get_db</b> with a test database."]),

 picture(M, "Alembic", "Migrations: version control for your schema",
     "&#128221; Your code changes the model (a new column); production already has data. A <b>migration</b> is a small script that changes the "
     "live schema step by step, <b>without losing data</b>, and can be rolled back.",
     [("edit models.py", "add Book.isbn"), ("alembic revision --autogenerate", "creates a migration file; review it!"),
      ("alembic upgrade head", "apply in CI/CD"), ("alembic downgrade -1", "undo if needed")]),

 job(M, "Databases", "Database work in real jobs", [
     ("Find slow queries", '''
EXPLAIN ANALYZE SELECT ... ;   -- Postgres
echo=True / django-debug-toolbar'''),
     ("Safe deploys", '''
add nullable column -> backfill -> make NOT NULL
(never rename a live column in one step)'''),
     ("Avoid lost updates", '''
UPDATE stock SET qty = qty - 1
WHERE id = :id AND qty > 0'''),
     ("Connection pooling", '''
create_engine(url, pool_size=10,
              pool_pre_ping=True)'''),
 ]),

 interview(M, "What is the N+1 problem and how do you fix it?",
     ["You load N parent rows with 1 query, then accessing a relationship in a loop triggers <b>one extra query per row</b>.",
      "Symptoms: pages get slower as data grows; the query log shows the same SELECT repeated.",
      "Fix with <b>eager loading</b>: SQLAlchemy <b>selectinload</b> / <b>joinedload</b>; Django <b>select_related</b> (FK, JOIN) / <b>prefetch_related</b> (many, IN query).",
      "Catch it in tests by <b>counting queries</b>."],
     None,
     "\"What is an index and when would you NOT add one?\" (a B-tree for fast lookups; skip it on tiny tables, low-selectivity columns, or write-heavy tables where it slows inserts)."),

 interview(M, "How do you change a database schema in production safely?",
     ["Use <b>migrations</b> (Alembic / Django migrations) in version control, applied automatically in CI/CD.",
      "Make changes <b>backwards compatible</b>: the old and new code run side by side during a deploy.",
      "Expand &#8594; migrate &#8594; contract: add the new column, backfill, switch the code, then drop the old one later.",
      "Review autogenerated migrations; test <b>upgrade and downgrade</b>; back up first; watch for long table locks."],
     None,
     "\"Explain transaction isolation levels\" and \"How do you prevent two users buying the last item?\" (row lock with SELECT ... FOR UPDATE, or an atomic conditional UPDATE)."),

 recap(M, "Module 23 in 6 lines",
     ["Models with <b>Mapped[...]</b>; a <b>Session</b> per unit of work; <b>select()</b> to query.",
      "N+1: lazy loading in a loop. Fix with <b>selectinload</b> / <b>joinedload</b>.",
      "<b>Indexes</b> on foreign keys and filtered columns; check with <b>EXPLAIN</b>.",
      "Transactions + isolation levels; prevent lost updates with locks or atomic updates.",
      "FastAPI: a <b>yield</b> dependency gives one session per request.",
      "<b>Alembic</b> migrations, reviewed, reversible, backwards compatible."],
     "Run <b>02_n_plus_1_and_loading.py</b>, then add an index and compare EXPLAIN before and after."),
]
