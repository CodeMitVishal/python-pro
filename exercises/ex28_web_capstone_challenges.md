# Exercise 28 · Web capstone challenges

Extend [`28_web_capstone/taskboard`](../28_web_capstone/taskboard). For every challenge:
**write the test first**, make it pass, and keep `pytest`, `mypy` and `ruff check .` green.

### ⭐ Level 1
1. **Due dates**: add `due: date | None` to tasks, plus `GET /tasks?overdue=true`. *(22, 23)*
2. **Admin view**: `GET /admin/tasks` lists everyone's tasks, admins only (403 otherwise). *(24)*

### ⭐⭐ Level 2
3. **Alembic**: replace `create_all()` with Alembic migrations, and add a migration for `due`. *(23)*
4. **Rate-limit login**: 5 attempts per minute per IP → 429 with `Retry-After`. *(24)*
5. **Cache the task count** per user in Redis (fakeredis in tests); invalidate on create/delete. *(26)*

### ⭐⭐⭐ Level 3
6. **Projects + members**: `Project` has many tasks and many members (many-to-many). Only members
   can see a project's tasks. Avoid N+1 queries when listing projects with their tasks. *(23)*
7. **Per-user WebSocket**: `/ws?token=...` only receives events for that user's tasks. *(24, 26)*
8. **Ship it**: a GitHub Actions workflow (lint → mypy → test → build) and a deployment to
   Azure Container Apps with PostgreSQL. Put the URL in your README. *(27)*

Done? Open a **Pull Request** with your solution in `submissions/<your-github-name>/`. 🚀
