"""Slides · Module 27 · Docker, CI/CD & Azure"""
from teach_kit import snippet, code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 27 · Docker, CI/CD &amp; Azure"
SLIDES = [
 cover("27", "Docker, CI/CD &amp; Azure", "From \"works on my laptop\" to a tested, containerised service running in the cloud.",
       [("Production-ready tour", "01_production_ready_tour.py"), ("The service", "app/main.py"), ("Dockerfile", "Dockerfile"),
        ("docker compose", "docker-compose.yml"), ("CI/CD pipeline", "github-actions/ci-cd.yml"), ("Azure deploy", "azure/deploy.sh"),
        ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Deployment", "\"It works on my machine\"",
     "Your API runs on your laptop. On the server: a different Python, a missing library, no database, secrets in a file nobody has, "
     "and deploying means SSH and crossed fingers.",
     "<b>Containers</b> package the app with everything it needs. <b>CI/CD</b> tests and ships every change automatically."),

 trace(M, "12-factor", "What \"production-ready\" means", ["Principle", "In practice"],
       [["<b>Config in the environment</b>", "<span class=\"m\">DATABASE_URL</span>, secrets from env vars / Key Vault, never in git"],
        ["<b>Logs to stdout</b>", "JSON lines; the platform collects them"],
        ["<b>Stateless processes</b>", "no files or sessions on local disk; use DB, Redis, blob storage"],
        ["<b>Health checks</b>", "<span class=\"m\">/health/live</span> (restart me) and <span class=\"m\">/health/ready</span> (send me traffic)"],
        ["<b>Same build everywhere</b>", "one image promoted from test to production"],
        ["<b>Graceful shutdown</b>", "finish requests on SIGTERM"]]),

 picture(M, "Docker", "Image vs container",
     "&#128230; An <b>image</b> is a frozen recipe-plus-ingredients (OS layer, Python, your code). A <b>container</b> is a running copy of it. "
     "Build once, run the same image on your laptop, in CI and in Azure.",
     [("Dockerfile", "the instructions"), ("docker build", "&#8594; image (layers, cached)"),
      ("docker run / compose", "&#8594; container(s)"), ("registry (ACR)", "where images live for deploys")]),

 mistake(M, "Dockerfile", "The slow, unsafe Dockerfile",
     '''
FROM python:latest
COPY . .                       # code first
RUN pip install -r requirements.txt
ENV SECRET_KEY=abc123          # baked-in secret
CMD uvicorn app.main:app --reload''',
     "<b>latest</b> changes silently; any code change re-installs every library; secrets end up in the image; runs as <b>root</b> with the dev reloader.",
     '''
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app                 # code LAST: layers cache
RUN useradd -m appuser
USER appuser
HEALTHCHECK CMD ["python", "healthcheck.py"]  # no curl in slim
CMD ["gunicorn", "app.main:app", "-b", "0.0.0.0:8000",
     "-k", "uvicorn.workers.UvicornWorker"]''',
     "Pinned slim base, deps before code, non-root, health check, secrets at <b>runtime</b> via env."),

 snippet(M, "docker compose", "The whole stack with one command", '''
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: postgresql://app:app@db:5432/app
      REDIS_URL: redis://cache:6379/0
    depends_on: [db, cache]
  db:
    image: postgres:16
    environment: {POSTGRES_USER: app, POSTGRES_PASSWORD: app}
    volumes: ["pgdata:/var/lib/postgresql/data"]
  cache:
    image: redis:7
volumes:
  pgdata:''',
     steps=["<b>docker compose up</b>: API + Postgres + Redis.", "Services find each other by <b>name</b> (db, cache).",
            "A <b>volume</b> keeps the DB data."]),

 picture(M, "CI/CD", "Nothing ships unless the tests pass",
     "&#128678; Every push runs the pipeline. A red step stops the line. Only green builds on <b>main</b> are deployed, tagged with the "
     "<b>commit SHA</b> so you always know what's running and can roll back.",
     [("push / PR", "GitHub Actions starts"), ("lint + type check", "ruff · mypy"), ("tests", "pytest (+ a Postgres service)"),
      ("build image", "tag :&lt;git sha&gt;, push to ACR"), ("deploy", "Container Apps, only on main")]),

 snippet(M, "CI/CD", "A GitHub Actions pipeline", '''
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install -r requirements.txt
      - run: ruff check . && mypy app
      - run: pytest -q
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: azure/login@v2          # OIDC, no stored password
      - run: az acr build -t api:${{ github.sha }} .
      - run: az containerapp update --image ...:${{ github.sha }}''',
     steps=["<b>needs: test</b>: deploy only after green tests.", "<b>OIDC</b> login: no long-lived cloud secrets in GitHub.",
            "Tag with the <b>SHA</b> for traceability and rollback."]),

 job(M, "Deployment", "Running services in the cloud", [
     ("Azure Container Apps", '''
HTTPS, autoscaling (to zero),
revisions for rollback, secretref: for secrets'''),
     ("Observability", '''
structured logs + metrics + traces
(App Insights / OpenTelemetry)'''),
     ("Zero-downtime deploys", '''
rolling updates + readiness probes
+ backwards-compatible migrations'''),
     ("Scale", '''
stateless replicas behind a load balancer
DB connection pooling, Redis shared cache'''),
 ]),

 interview(M, "How do you deploy a Python web app to production?",
     ["Make it <b>12-factor</b>: config/secrets from env, logs to stdout, stateless, health endpoints.",
      "Package it in a <b>Docker image</b>: slim pinned base, deps before code, non-root, production server (gunicorn/uvicorn workers).",
      "<b>CI</b> runs lint, types and tests on every PR; <b>CD</b> builds the image, tags it with the SHA, pushes to a registry and deploys.",
      "Run migrations as a release step; use rolling deploys with readiness probes.",
      "Monitor: logs, metrics, alerts, error tracking; keep a rollback path."],
     None,
     "\"Image vs container? What's a layer cache?\" (image = template, container = running instance; each Dockerfile step is a cached layer, so copy requirements before code)."),

 interview(M, "What is CI/CD? What goes in a pipeline?",
     ["<b>Continuous Integration</b>: every change is merged often and automatically built and tested.",
      "<b>Continuous Delivery/Deployment</b>: every green build can be (or is) released automatically.",
      "Typical stages: checkout &#8594; install &#8594; lint/format &#8594; type check &#8594; tests (+ coverage) &#8594; security scan &#8594; build image &#8594; deploy to staging &#8594; production.",
      "Branch protection: PRs need green checks and a review."],
     None,
     "\"Liveness vs readiness probe?\" (liveness: is the process alive, else restart it; readiness: can it take traffic now, e.g. DB reachable)."),

 recap(M, "Module 27 in 5 lines",
     ["12-factor: env config, stdout logs, stateless, health checks.",
      "Dockerfile: pinned slim base, deps first, non-root, HEALTHCHECK, gunicorn.",
      "<b>docker compose</b> for the local stack.",
      "CI: ruff, mypy, pytest on every PR; CD only from green main, tagged with the SHA.",
      "Azure Container Apps: HTTPS, autoscale, revisions, secrets."],
     "Do <b>exercises/ex27_fix_the_dockerfile.py</b>: turn a dangerous Dockerfile into a production one."),
]
