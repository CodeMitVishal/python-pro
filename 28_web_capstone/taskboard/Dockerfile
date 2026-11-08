# syntax=docker/dockerfile:1
# docker build -t taskboard:1.0.0 .
# docker run -p 8000:8000 -e TASKBOARD_JWT_SECRET=$(python -c "import secrets;print(secrets.token_urlsafe(64))") taskboard:1.0.0
FROM python:3.12-slim AS build
WORKDIR /build
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir --prefix=/install . "gunicorn>=22"

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 1000 appuser
COPY --from=build /install /usr/local
WORKDIR /home/appuser
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["gunicorn", "taskboard.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "-b", "0.0.0.0:8000"]
