# Module 27 · Interview questions (with answers)

[← Module 27](README.md) · [Quiz](QUIZ.md)

---

### 1. Image vs container?

**Say:** An **image** is a read-only template: layers containing the OS base, Python, dependencies and your code. A **container** is a running instance of an image with its own writable layer. You build once and run the same image everywhere.

---

### 2. How do you write a good Dockerfile for Python?

**Say:**
- A pinned slim base (`python:3.12-slim`).
- Copy `requirements.txt` and install **before** copying the code (layer caching), with `--no-cache-dir`.
- A multi-stage build if you compile anything.
- A non-root `USER` and a `HEALTHCHECK`.
- An exec-form `CMD` with gunicorn/uvicorn.
- No secrets baked in, and a `.dockerignore`.

---

### 3. What is the 12-factor app?

**Say:** A set of principles for cloud-friendly apps:
- Config in the environment.
- Dependencies declared and isolated.
- Stateless processes.
- Logs as event streams to stdout.
- Backing services (DB, cache) attached by URL.
- Dev/prod parity.
- Fast startup and graceful shutdown.
- Admin tasks as one-off processes.

---

### 4. What is CI/CD?

**Say:** **CI** (Continuous Integration) automatically builds, lints and tests every change, typically on each pull request. **CD** (Continuous Delivery/Deployment) automatically packages and deploys every green build of main to staging and production, with approvals if needed.

---

### 5. What does your pipeline contain?

**Say:** Checkout → install → `ruff` → `mypy` → `pytest` with coverage (plus a Postgres service) → security scan (pip-audit, image scan) → build the image tagged with the commit SHA → push to a registry → deploy to staging → smoke tests → production. Cloud login uses OIDC, so no stored secrets.

---

### 6. Liveness vs readiness probes?

**Say:** **Liveness**: is the process healthy? If not, restart it. **Readiness**: can it serve traffic right now (DB reachable, warmed up)? If not, take it out of the load balancer without restarting it.

---

### 7. How do you deploy without downtime?

**Say:** Rolling or blue-green deployments with readiness probes, backwards-compatible DB migrations (expand/contract), graceful shutdown on SIGTERM, and feature flags. Keep the previous revision for a quick rollback.

---

### 8. How do you scale a Python web service?

**Say:** Run stateless replicas behind a load balancer, with several workers per container (gunicorn), autoscaling on CPU or requests, a shared cache (Redis), DB connection pooling, read replicas, background workers for slow jobs, and a CDN for static files. Measure first.

---

### 9. How do you monitor a service in production?

**Say:** Structured logs, metrics (latency, error rate, throughput, saturation), distributed traces (OpenTelemetry → App Insights / Grafana), error tracking (Sentry), and alerts on SLOs, plus dashboards per service.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
