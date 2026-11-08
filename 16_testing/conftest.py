"""conftest.py: pytest loads this automatically. Fixtures defined here are
available to every test file in this folder, without importing anything."""
import pytest


@pytest.fixture
def sample_cart():
    """A fresh cart for every test that asks for it (tests can't affect each other)."""
    return {"book": (12.5, 2), "pen": (1.2, 3)}
