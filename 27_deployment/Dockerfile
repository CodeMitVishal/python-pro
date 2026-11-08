# syntax=docker/dockerfile:1
# A production Dockerfile for the FastAPI service, built in two stages.
#   docker build -t hello-service:1.0.0 --build-arg APP_VERSION=1.0.0 .
#   docker run -p 8000:8000 -e APP_ENV=prod hello-service:1.0.0

# ---------- Stage 1: build the dependencies (has compilers, never shipped) ----------
FROM python:3.12-slim AS build
WORKDIR /build
COPY requirements.txt .
# Install into a separate folder so stage 2 can copy just the result
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2: the small runtime image ----------
FROM python:3.12-slim
ARG APP_VERSION=0.0.0-local
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_VERSION=${APP_VERSION}

# Never run as root: if the app is hacked, the attacker isn't root in the container
RUN useradd --create-home --uid 1000 appuser
WORKDIR /srv
COPY --from=build /install /usr/local
# Copy the code LAST: code changes often, so Docker reuses the cached dependency layers
COPY app ./app
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')"

# gunicorn manages several uvicorn worker processes (use all CPU cores, restart crashed workers)
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "-b", "0.0.0.0:8000"]
