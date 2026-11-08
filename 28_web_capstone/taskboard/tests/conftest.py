import os

os.environ["TASKBOARD_DATABASE_URL"] = "sqlite://"          # in-memory DB for tests (set before import)

from collections.abc import Callable, Iterator  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from taskboard.db import Base, engine  # noqa: E402
from taskboard.main import app  # noqa: E402


@pytest.fixture
def client() -> Iterator[TestClient]:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)                         # a clean database for every test
    with TestClient(app) as c:
        yield c


@pytest.fixture
def login(client: TestClient) -> Callable[[str], dict[str, str]]:
    """Sign up + log in a user, return the Authorization header."""
    def _login(email: str) -> dict[str, str]:
        client.post("/auth/signup", json={"email": email, "password": "long-password-1"})
        r = client.post("/auth/token", data={"username": email, "password": "long-password-1"})
        return {"Authorization": f"Bearer {r.json()['access_token']}"}
    return _login
