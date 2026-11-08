# Python Pro – Module 23 Knowledge Check
**SQLAlchemy 2.0 & Alembic**

The answer key is at the bottom, and each answer says which file to revisit.

---

**1. What does an ORM do?**
- A) Replaces the database
- B) Maps tables to classes and rows to objects, and writes the SQL for you
- C) Only creates tables
- D) Encrypts data

**2. What does `Mapped[str | None]` mean for a column?**
- A) The column is a list
- B) A string column that allows NULL
- C) A primary key
- D) An index

**3. What is the Session for?**
- A) A login
- B) A unit of work: it tracks changes and writes them in one transaction on `commit()`
- C) A connection string
- D) Caching

**4. How do you get a book by primary key?**
- A) `session.find(Book, 1)`
- B) `session.get(Book, 1)`
- C) `select(1)`
- D) `Book[1]`

**5. Is `select(Book).where(Book.title == user_input)` safe from SQL injection?**
- A) No
- B) Yes: values are sent as bound parameters
- C) Only on SQLite
- D) Only with `echo=True`

**6. What is the N+1 query problem?**
- A) An off-by-one bug
- B) 1 query for the list plus 1 per item when lazily loading relationships, which is very slow
- C) Too many tables
- D) Missing indexes

**7. Which loading option fixes N+1 for a one-to-many like `Author.books`?**
- A) `lazyload`
- B) `selectinload(Author.books)`
- C) `noload`
- D) `raiseload`

**8. How does a many-to-many relationship work in SQL?**
- A) A list column
- B) An association table with pairs of foreign keys
- C) JSON
- D) Two primary keys in one table

**9. In FastAPI, why use a `get_db()` dependency with `yield` and `finally: db.close()`?**
- A) Speed
- B) One session per request, always closed, even when errors happen
- C) It's required by SQLAlchemy
- D) To share one session across all users

**10. What should you do after an `IntegrityError` on commit?**
- A) Ignore it
- B) `session.rollback()`, then return a clean error (for example 409)
- C) Restart the app
- D) Delete the table

**11. Why use Alembic instead of `create_all()` in real projects?**
- A) It's faster
- B) It applies versioned schema changes (add a column, rename...) to existing databases without losing data
- C) `create_all()` doesn't exist
- D) Alembic is an ORM

**12. Which command applies all missing migrations?**
- A) `alembic init`
- B) `alembic upgrade head`
- C) `alembic downgrade -1`
- D) `alembic history`

**13. How does the database know which migrations already ran?**
- A) It guesses
- B) The `alembic_version` table stores the current revision
- C) From file dates
- D) From git

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Revisit |
|---|--------|---------|
| 1 | B | `01_orm_crud.py` |
| 2 | B | `models.py` |
| 3 | B | `01_orm_crud.py` |
| 4 | B | `01_orm_crud.py` |
| 5 | B | `01_orm_crud.py` |
| 6 | B (51 vs 2 queries in the demo) | `02_n_plus_1_and_loading.py` |
| 7 | B | `02_n_plus_1_and_loading.py` |
| 8 | B | `ex23_blog_orm.py` |
| 9 | B | `03_sqlalchemy_with_fastapi.py` |
| 10 | B | `03_sqlalchemy_with_fastapi.py` |
| 11 | B | `04_alembic_migrations.py` |
| 12 | B | `alembic.ini` |
| 13 | B | `04_alembic_migrations.py` |

</details>

---

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
