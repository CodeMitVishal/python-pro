# taskboard: the Python Pro web capstone

A team task board API: users sign up and log in, manage their own tasks, and
every change is pushed live over a WebSocket. Built like a production service.

## Architecture

```
src/taskboard/
├── main.py          app wiring: routers, CORS, lifespan, /health, /ws      (22, 26, 27)
├── config.py        settings from TASKBOARD_* env vars                     (22, 27)
├── db.py            engine + one session per request                       (23)
├── models.py        User 1---< Task  (SQLAlchemy 2.0)                       (23)
├── schemas.py       pydantic in/out models, validation                     (22)
├── security.py      scrypt password hashes + JWT tokens                    (24)
├── deps.py          current_user dependency (401 for bad tokens)           (22, 24)
├── realtime.py      WebSocket notifier: push every change                  (26)
└── routers/
    ├── auth.py      POST /auth/signup  POST /auth/token  GET /auth/me
    └── tasks.py     GET/POST /tasks  PATCH/DELETE /tasks/{id}  (owner or admin only: 403)
tests/               7 tests: auth, CRUD, permissions, validation, WebSocket  (16)
Dockerfile           multi-stage, non-root, health check, gunicorn          (27)
```

## Run it

```bash
cd 28_web_capstone/taskboard
```

```bash
pip install -e ".[dev]"
```

```bash
uvicorn taskboard.main:app --reload
```

Open http://127.0.0.1:8000/docs, sign up, click **Authorize**, and try every endpoint.

## Quality gates (CI runs these)

```bash
pytest
```

```bash
mypy
```

```bash
ruff check .
```

## Deploy it

Same steps as Module 27: build the Dockerfile with `az acr build`, run it on
Azure Container Apps, and set `TASKBOARD_DATABASE_URL` (Azure Database for
PostgreSQL) and `TASKBOARD_JWT_SECRET` as **secrets**.

## Your turn

The challenges are in [`exercises/ex28_web_capstone_challenges.md`](../../exercises/ex28_web_capstone_challenges.md).
