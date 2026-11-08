# Module 23 · SQLAlchemy 2.0 & Alembic

[← Back to the course](../README.md) · [Slides](../slides/python-pro-slides.pdf)

Work with real databases through an ORM: typed models, relationships, the N+1 problem, sessions in FastAPI, and versioned schema migrations.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Models | [`models.py`](models.py) | Author 1---< Book with `Mapped[...]` |
| ORM CRUD | [`01_orm_crud.py`](01_orm_crud.py) | Session, select(), joins, group by, update, delete |
| N+1 & loading | [`02_n_plus_1_and_loading.py`](02_n_plus_1_and_loading.py) | 51 queries → 2 with `selectinload` |
| SQLAlchemy + FastAPI | [`03_sqlalchemy_with_fastapi.py`](03_sqlalchemy_with_fastapi.py) | session per request, IntegrityError → 409 |
| Alembic migrations | [`04_alembic_migrations.py`](04_alembic_migrations.py) | upgrade, downgrade, data survives |

```bash
pip install sqlalchemy alembic
```

```bash
python 23_sqlalchemy_alembic/01_orm_crud.py
```

## Exercise: A blog database

Users, posts and tags (many-to-many), queries, and no N+1.

- Start here: [`exercises/ex23_blog_orm.py`](../exercises/ex23_blog_orm.py)
- Solution: [`solutions/ex23_blog_orm.py`](../solutions/ex23_blog_orm.py)

## Knowledge check

Test yourself with the [Module 23 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 24 · Authentication & security](../24_auth_security/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
