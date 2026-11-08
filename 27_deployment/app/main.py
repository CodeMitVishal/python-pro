"""A small, production-ready FastAPI service: the thing we put in a container.

Production habits shown here (the "12-factor app" ideas):
  - ALL config from environment variables (pydantic-settings), no secrets in code
  - logs go to stdout as one JSON object per line (the platform collects them)
  - /health/live and /health/ready endpoints for the orchestrator's probes
  - the app version is visible, so you know what's deployed
"""
import json
import logging
import sys
import time
from datetime import UTC, datetime

from fastapi import FastAPI, Request
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")
    env: str = "dev"                         # APP_ENV=prod
    version: str = "0.0.0-local"             # APP_VERSION=1.4.2 (set by CI from the git tag/sha)
    log_level: str = "INFO"
    database_url: str = "sqlite:///./local.db"   # APP_DATABASE_URL=postgresql+psycopg://...


settings = Settings()


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry = {"time": datetime.now(UTC).isoformat(timespec="seconds"),
                 "level": record.levelname, "logger": record.name, "msg": record.getMessage()}
        entry.update(getattr(record, "extra_fields", {}))
        return json.dumps(entry)


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=settings.log_level, handlers=[handler], force=True)
logging.getLogger("httpx").setLevel(logging.WARNING)   # quiet the test client
log = logging.getLogger("app")

app = FastAPI(title="Hello Service", version=settings.version)


@app.middleware("http")
async def access_log(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    log.info("request", extra={"extra_fields": {
        "method": request.method, "path": request.url.path, "status": response.status_code,
        "ms": round((time.perf_counter() - start) * 1000, 1)}})
    return response


@app.get("/health/live")
def live() -> dict:
    """Liveness: is the process alive? If this fails, the platform restarts the container."""
    return {"status": "ok"}


@app.get("/health/ready")
def ready() -> dict:
    """Readiness: can we serve traffic (DB reachable, config loaded)? If not, no traffic is sent."""
    return {"status": "ready", "env": settings.env, "version": settings.version}


@app.get("/api/hello/{name}")
def hello(name: str) -> dict:
    return {"message": f"Hello, {name}!", "served_by_version": settings.version}
