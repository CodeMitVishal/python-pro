# Module 25 · Interview questions (with answers)

[← Module 25](README.md) · [Quiz](QUIZ.md)

---

### 1. Explain Django's architecture (MVT).

**Say:** **Model** (ORM classes mapped to tables), **View** (Python function or class that handles the request) and **Template** (HTML with placeholders). The URL dispatcher routes requests to views, and middleware wraps every request. With DRF, serializers replace templates for JSON.

---

### 2. Describe the request/response cycle.

**Say:** The WSGI/ASGI server passes the request to Django. Middleware runs on the way in (security, session, auth, CSRF). The URL resolver picks the view. The view uses models and returns a response (template or serializer). Middleware runs on the way out.

---

### 3. `select_related` vs `prefetch_related`?

**Say:** Both prevent N+1 queries.
- `select_related` follows **ForeignKey/OneToOne** with a SQL **JOIN**: one query.
- `prefetch_related` handles **reverse FK and ManyToMany** with a separate `IN` query, joined in Python.

Verify with `assertNumQueries` or the debug toolbar.

---

### 4. Are QuerySets lazy?

**Say:** Yes. `filter()`, `exclude()` and `order_by()` only build the query. The database is hit when the QuerySet is **evaluated**: iteration, `list()`, `len()`, slicing with a step, `bool()`, or `repr` in the shell. Results are cached on that QuerySet.

---

### 5. What are `F()` and `Q()` expressions?

**Say:** `F("stock") - 1` refers to a column **in the database**, which gives atomic updates without race conditions. `Q(a=1) | Q(b=2)` builds OR and NOT conditions.

---

### 6. What are signals? When would you avoid them?

**Say:** Hooks such as `post_save` and `pre_delete` that run when model events happen. They're good for decoupled side effects in reusable apps. Avoid them for core business logic: they hide what happens and are skipped by `bulk_create` and `update()`. Prefer explicit service functions.

---

### 7. What is middleware in Django? Give an example.

**Say:** A layer that processes every request and response: `SecurityMiddleware`, `SessionMiddleware`, `AuthenticationMiddleware`, `CsrfViewMiddleware`. Custom examples include adding a request ID, timing, or tenant detection.

---

### 8. How do migrations work?

**Say:** `makemigrations` compares models with the last migration state and writes a migration file. `migrate` applies the pending migrations and records them in `django_migrations`. Commit migrations to git and run `migrate` during deploys. Use data migrations (`RunPython`) for backfills.

---

### 9. DRF: serializer vs ViewSet vs router?

**Say:** A **Serializer** validates input and converts models to and from JSON. A **ViewSet** bundles the list/create/retrieve/update/destroy actions. A **Router** generates the URL patterns. Permissions (`IsAuthenticated`, custom `has_object_permission`), pagination and filtering plug in through settings.

---

### 10. How do you make a Django app production-ready?

**Say:** `DEBUG=False`, the secret key and DB URL from env, `ALLOWED_HOSTS`, HTTPS with secure cookies and HSTS, `collectstatic` (WhiteNoise or a CDN), Postgres, gunicorn/uvicorn workers, caching (Redis), logging, error tracking, and `manage.py check --deploy` in CI.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
