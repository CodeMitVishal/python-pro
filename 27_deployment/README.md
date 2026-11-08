# Module 27 · Docker, CI/CD & deploying to Azure

[← Back to the course](../README.md) · [Slides](../slides/python-pro-slides.pdf)

Ship it: a 12-factor service, a production Dockerfile, docker compose, a GitHub Actions pipeline, and Azure Container Apps.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Production-ready tour | [`01_production_ready_tour.py`](01_production_ready_tour.py) | env config, JSON logs, health probes, tests |
| The service | [`app/main.py`](app/main.py) | settings, structured logging, /health/live and /health/ready |
| Dockerfile | [`Dockerfile`](Dockerfile) | multi-stage, non-root, layer caching, HEALTHCHECK, gunicorn |
| docker compose | [`docker-compose.yml`](docker-compose.yml) | API + PostgreSQL + Redis |
| CI/CD pipeline | [`github-actions/ci-cd.yml`](github-actions/ci-cd.yml) | lint → mypy → test → build → deploy with OIDC |
| Azure | [`azure/deploy.sh`](azure/deploy.sh) | ACR + Container Apps with the az CLI |

```bash
pip install fastapi uvicorn pydantic-settings
```

```bash
python 27_deployment/01_production_ready_tour.py
```

## Exercise: Fix a bad Dockerfile

Turn a working-but-dangerous Dockerfile into a production one (9 checks).

- Start here: [`exercises/ex27_fix_the_dockerfile.py`](../exercises/ex27_fix_the_dockerfile.py)
- Solution: [`solutions/ex27_Dockerfile`](../solutions/ex27_Dockerfile)

## Knowledge check

Test yourself with the [Module 27 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 28 · Web capstone](../28_web_capstone/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
