"""Module 23 · The models shared by the lessons: Author 1 ---< N Book.

SQLAlchemy 2.0 style: each class is a table, each Mapped[...] attribute a column.
The type hints define the column types AND help your editor and mypy.
"""
from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    country: Mapped[str | None] = mapped_column(String(2))          # | None -> NULL allowed

    # one author has many books; "author" on Book is the other side
    books: Mapped[list["Book"]] = relationship(back_populates="author",
                                               cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Author({self.name!r})"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    price: Mapped[float]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))   # the link in the DB
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    author: Mapped[Author] = relationship(back_populates="books")      # the link in Python

    def __repr__(self) -> str:
        return f"Book({self.title!r}, {self.price})"
