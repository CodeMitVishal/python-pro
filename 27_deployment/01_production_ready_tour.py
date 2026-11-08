"""Module 27 · From "works on my laptop" to running in the cloud

The path of every production web app:

  code + tests ──► CI pipeline ──► container image ──► registry ──► cloud platform
  (Modules 8-26)   (GitHub Actions)  (Dockerfile)       (Azure ACR)   (Azure Container Apps)

Files in this module:
  app/main.py                 a 12-factor FastAPI service (env config, JSON logs, health probes)
  tests/test_app.py           the tests CI runs on every push
  Dockerfile + .dockerignore  a small, secure, multi-stage image (non-root, cached layers)
  docker-compose.yml          API + PostgreSQL + Redis locally, with one command
  github-actions/ci-cd.yml    lint -> type check -> test -> build -> deploy to Azure
  azure/deploy.sh             one-time Azure Container Apps setup with the az CLI

This script runs the app the way a platform sees it: config from env vars,
probes, JSON logs, and the pytest suite.

TEACHING NOTES
  Why it matters  'Works on my machine' isn't done; production needs config, logs, health checks
                  and repeatable deploys.
  Picture it      A container is a shipping container: the same box runs on any ship (laptop,
                  CI, Azure).
  Watch out       Secrets in env vars or a vault, never in the image or git; logs to stdout, not
                  files.
  In real jobs    Docker images built in CI, deployed to Azure Container Apps with health
                  probes.
  Interview       Q: What is the 12-factor app?
                  A: Config in env, stateless processes, logs to stdout, backing services by
                     URL, same build everywhere.

Run it:  python 27_deployment/01_production_ready_tour.py
"""
import os
import subprocess
import sys
import warnings
from pathlib import Path

here = Path(__file__).parent
sys.path.insert(0, str(here))

# --- 1. Config comes from the environment (set by Docker / Azure / CI) ------------------------
os.environ.update(APP_ENV="prod", APP_VERSION="1.4.2", APP_LOG_LEVEL="INFO")

warnings.filterwarnings("ignore", message=".*httpx.*")
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app, settings  # noqa: E402

print(f"config from env: env={settings.env} version={settings.version}\n")

# --- 2. Probes + JSON logs (one line per request, ready for Azure Monitor / Log Analytics) ----
client = TestClient(app)
print("liveness: ", client.get("/health/live").json())
print("readiness:", client.get("/health/ready").json())
print("api:      ", client.get("/api/hello/Azure").json())

# --- 3. The same tests CI runs before anything is deployed --------------------------------
print("\n$ pytest 27_deployment/tests -q")
result = subprocess.run([sys.executable, "-m", "pytest", "-q", str(here / "tests")],
                        capture_output=True, text=True, cwd=here)
print(result.stdout.strip().splitlines()[-1])

print("""
Next steps (need Docker / the Azure CLI):
  docker build -t hello-service:1.0.0 27_deployment
  docker run -p 8000:8000 -e APP_ENV=prod hello-service:1.0.0
  docker compose -f 27_deployment/docker-compose.yml up --build
  bash 27_deployment/azure/deploy.sh          (creates Azure resources!)""")
