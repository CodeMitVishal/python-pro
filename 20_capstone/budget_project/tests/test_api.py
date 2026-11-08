from fastapi.testclient import TestClient

from budget.api import app, get_service
from budget.service import BudgetService


def make_client(service: BudgetService) -> TestClient:
    app.dependency_overrides[get_service] = lambda: service   # use the test's fresh service
    return TestClient(app)


def test_create_and_summarise(service: BudgetService) -> None:
    client = make_client(service)
    r = client.post("/expenses", json={"amount": 120, "category": "food",
                                       "spent_on": "2026-11-03"})
    assert r.status_code == 201
    assert r.json()["id"] == 1
    summary = client.get("/summary/2026/11").json()
    assert summary == {"total": 120.0, "by_category": {"food": 120.0}, "over_budget": ["food"]}


def test_validation_errors(service: BudgetService) -> None:
    client = make_client(service)
    assert client.post("/expenses", json={"amount": -1, "category": "food"}).status_code == 422
    assert client.post("/expenses", json={"amount": 5, "category": "pizza"}).status_code == 400


def test_delete(service: BudgetService) -> None:
    client = make_client(service)
    client.post("/expenses", json={"amount": 9, "category": "fun"})
    assert client.delete("/expenses/1").status_code == 204
    assert client.delete("/expenses/1").status_code == 404
