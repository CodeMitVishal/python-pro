"""Solution · Exercise 23: A blog database with the SQLAlchemy ORM

Run it:  python solutions/ex23_blog_orm.py
"""
from sqlalchemy import Column, ForeignKey, String, Table, create_engine, event, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload


class Base(DeclarativeBase):
    pass


# Many-to-many needs a third table that only holds pairs of ids
post_tags = Table(
    "post_tags", Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped[User] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    posts: Mapped[list[Post]] = relationship(secondary=post_tags, back_populates="tags")


def publish(session, author_name, title, tag_names):
    author = session.scalars(select(User).where(User.name == author_name)).one()
    tags = []
    for name in tag_names:
        tag = session.scalars(select(Tag).where(Tag.name == name)).one_or_none()
        tags.append(tag or Tag(name=name))          # reuse, or create a new one
    post = Post(title=title, author=author, tags=tags)
    session.add(post)
    session.commit()
    return post


def posts_with_tag(session, tag_name):
    stmt = select(Post.title).join(Post.tags).where(Tag.name == tag_name).order_by(Post.title)
    return list(session.scalars(stmt))


def top_authors(session):
    stmt = (select(User.name, func.count(Post.id).label("n"))
            .join(User.posts).group_by(User.name).order_by(func.count(Post.id).desc()))
    return [(name, n) for name, n in session.execute(stmt)]


def all_posts_with_tags(session):
    posts = session.scalars(select(Post).options(selectinload(Post.tags)))   # 1 + 1 queries
    return {p.title: sorted(t.name for t in p.tags) for p in posts}


if __name__ == "__main__":
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        s.add_all([User(name="vishal"), User(name="raj")])
        s.commit()
        publish(s, "vishal", "Decorators explained", ["python", "advanced"])
        publish(s, "vishal", "FastAPI in depth", ["python", "web"])
        publish(s, "raj", "Docker basics", ["devops"])
        assert s.scalar(select(func.count()).select_from(Tag)) == 4
        assert posts_with_tag(s, "python") == ["Decorators explained", "FastAPI in depth"]
        assert top_authors(s) == [("vishal", 2), ("raj", 1)]

    queries = []
    event.listen(engine, "before_cursor_execute", lambda *a: queries.append(a[2]))
    with Session(engine) as s:
        result = all_posts_with_tags(s)
    assert result["FastAPI in depth"] == ["python", "web"]
    assert len(queries) <= 2
    print("All checks passed!")
