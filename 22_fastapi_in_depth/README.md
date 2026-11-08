# Module 22 · FastAPI in depth

[← Back to the course](../README.md) · [Slides](../slides/python-pro-slides.pdf)

Build APIs the way production teams do: pydantic validation, routers, dependency injection, auth dependencies, error handlers, middleware, CORS, settings and async.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| pydantic models | [`01_pydantic_models.py`](01_pydantic_models.py) | Field constraints, validators, in/out models |
| Routers & dependencies | [`02_routers_and_dependencies.py`](02_routers_and_dependencies.py) | APIRouter, Depends chains, pagination, 401/403, overrides |
| Errors, middleware & CORS | [`03_errors_middleware_cors.py`](03_errors_middleware_cors.py) | exception handlers, request IDs, CORS |
| Settings, lifespan & async | [`04_settings_lifespan_async.py`](04_settings_lifespan_async.py) | pydantic-settings, startup/shutdown, httpx.AsyncClient |

```bash
pip install fastapi httpx pydantic-settings
```

```bash
python 22_fastapi_in_depth/02_routers_and_dependencies.py
```

## Exercise: A library API

Router, API-key dependency, pagination, validation and a custom 404 handler.

- Start here: [`exercises/ex22_fastapi_library_api.py`](../exercises/ex22_fastapi_library_api.py)
- Solution: [`solutions/ex22_fastapi_library_api.py`](../solutions/ex22_fastapi_library_api.py)

## Knowledge check

Test yourself with the [Module 22 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 23 · SQLAlchemy 2.0 & Alembic](../23_sqlalchemy_alembic/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
