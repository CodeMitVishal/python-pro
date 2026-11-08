"""Exercise 23 · A blog database with the SQLAlchemy ORM

Model a blog and write the queries:

  User  1 ---< N  Post  N >---< N  Tag        (many-to-many via a `post_tags` table)

  1. Models: User(id, name unique), Post(id, title, user_id), Tag(id, name unique),
     plus the post_tags association Table, with relationships on both sides:
     User.posts / Post.author and Post.tags / Tag.posts
  2. publish(session, author_name, title, tag_names): create the post, reuse
     existing tags or create new ones, commit, return the Post
  3. posts_with_tag(session, tag_name) -> list of post titles, sorted
  4. top_authors(session) -> [(name, number_of_posts), ...] most posts first
  5. all_posts_with_tags(session) -> {title: [tag names]}, using AT MOST 2 SQL
     queries in total (hint: selectinload, Module 23 lesson 02)

Run it to check your work:
    pip install sqlalchemy
    python exercises/ex23_blog_orm.py

Stuck? Compare with solutions/ex23_blog_orm.py
"""
from sqlalchemy import Column, ForeignKey, String, Table, create_engine, event, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload


class Base(DeclarativeBase):
    pass


# TODO 1: post_tags table, User, Post, Tag


def publish(session, author_name, title, tag_names):
    """TODO 2"""


def posts_with_tag(session, tag_name):
    """TODO 3"""


def top_authors(session):
    """TODO 4"""


def all_posts_with_tags(session):
    """TODO 5"""


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        s.add_all([User(name="vishal"), User(name="raj")])          # noqa: F821
        s.commit()
        publish(s, "vishal", "Decorators explained", ["python", "advanced"])
        publish(s, "vishal", "FastAPI in depth", ["python", "web"])
        publish(s, "raj", "Docker basics", ["devops"])
        assert s.scalar(select(func.count()).select_from(Tag)) == 4, "reuse existing tags"  # noqa: F821
        assert posts_with_tag(s, "python") == ["Decorators explained", "FastAPI in depth"]
        assert top_authors(s) == [("vishal", 2), ("raj", 1)]

    queries = []
    event.listen(engine, "before_cursor_execute", lambda *a: queries.append(a[2]))
    with Session(engine) as s:
        result = all_posts_with_tags(s)
    assert result["FastAPI in depth"] == ["python", "web"], result
    assert len(queries) <= 2, f"{len(queries)} queries: avoid N+1 with selectinload"
    print("All checks passed!")
