# Python Pro – Module 25 Knowledge Check
**Django essentials + Django REST Framework**

The answer key is at the bottom, and each answer says which file to revisit.

---

**1. What does "batteries included" mean for Django?**
- A) It's slow
- B) ORM, migrations, admin, templates, forms, auth, security and tests come built in
- C) It needs plugins for everything
- D) It's only for APIs

**2. What is a Django "app"?**
- A) A mobile app
- B) One feature area of a project (models, views, URLs, templates, tests)
- C) The settings file
- D) A server

**3. `makemigrations` vs `migrate`?**
- A) Same thing
- B) `makemigrations` writes migration files from model changes; `migrate` applies them to the database
- C) `migrate` creates models
- D) `makemigrations` deletes data

**4. Why `DecimalField` for prices?**
- A) Speed
- B) Floats can't represent money exactly (0.1 + 0.2 ≠ 0.3)
- C) It's required
- D) Smaller storage

**5. What does `related_name="books"` on `Book.author` give you?**
- A) A new table
- B) `author.books.all()` to reach an author's books
- C) A unique constraint
- D) An index

**6. What does `select_related("author")` do?**
- A) Filters authors
- B) Loads books and their authors in one JOIN query (no N+1)
- C) Sorts by author
- D) Caches the page

**7. What is the Django admin?**
- A) A server tool
- B) A ready-made back-office UI to manage your models
- C) A deployment tool
- D) A test runner

**8. What is a DRF serializer?**
- A) A database driver
- B) It converts model instances to JSON and validates incoming data, like pydantic
- C) A URL router
- D) A template

**9. What does a `ModelViewSet` provide?**
- A) Only GET
- B) list, create, retrieve, update and delete endpoints in one class
- C) HTML pages
- D) The admin

**10. With `IsAuthenticatedOrReadOnly`, what happens to a guest POST?**
- A) 201
- B) 403 (401 with token auth); guests can only read
- C) 500
- D) 404

**11. Where should `SECRET_KEY` and `DEBUG` come from in production?**
- A) Hard-coded in settings.py
- B) Environment variables (`DEBUG` must be False)
- C) The database
- D) URLs

**12. Django or FastAPI?**
- A) Always Django
- B) Django for full web apps with an admin, auth and HTML; FastAPI for lean, async, typed APIs and microservices
- C) Always FastAPI
- D) They're the same

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Revisit |
|---|--------|---------|
| 1 | B | `01_django_tour.py` |
| 2 | B | `bookstore_project/catalog/` |
| 3 | B | `catalog/models.py` |
| 4 | B | `catalog/models.py` |
| 5 | B | `catalog/models.py` |
| 6 | B | `catalog/views.py`, `01_django_tour.py` |
| 7 | B | `catalog/admin.py` |
| 8 | B | `catalog/serializers.py` |
| 9 | B | `catalog/api.py` |
| 10 | B | `config/settings.py`, `catalog/tests.py` |
| 11 | B | `config/settings.py` |
| 12 | B | Modules 22 & 25 |

</details>

---

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
