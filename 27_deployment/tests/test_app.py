"""Tests that CI runs before any image is built or deployed."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_liveness():
    assert client.get("/health/live").json() == {"status": "ok"}


def test_readiness_reports_version():
    body = client.get("/health/ready").json()
    assert body["status"] == "ready" and "version" in body


def test_hello():
    assert client.get("/api/hello/Vishal").json()["message"] == "Hello, Vishal!"
