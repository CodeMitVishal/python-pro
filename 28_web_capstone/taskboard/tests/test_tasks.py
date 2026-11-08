import json
from collections.abc import Callable

from fastapi.testclient import TestClient

Login = Callable[[str], dict[str, str]]


def test_crud_filter_and_pagination(client: TestClient, login: Login) -> None:
    me = login("vishal@example.com")
    for title in ["write tests", "record video", "deploy"]:
        assert client.post("/tasks", json={"title": title}, headers=me).status_code == 201
    assert client.patch("/tasks/2", json={"status": "done"}, headers=me).json()["status"] == "done"
    assert client.get("/tasks?status=done", headers=me).json()["total"] == 1
    page = client.get("/tasks?limit=2&offset=2", headers=me).json()
    assert page["total"] == 3 and [t["title"] for t in page["items"]] == ["deploy"]
    assert client.delete("/tasks/1", headers=me).status_code == 204
    assert client.get("/tasks", headers=me).json()["total"] == 2


def test_users_cannot_touch_each_others_tasks(client: TestClient, login: Login) -> None:
    vishal, raj = login("vishal@example.com"), login("raj@example.com")
    client.post("/tasks", json={"title": "secret plan"}, headers=vishal)
    assert client.get("/tasks", headers=raj).json()["total"] == 0          # not even listed
    assert client.patch("/tasks/1", json={"title": "hacked"}, headers=raj).status_code == 403
    assert client.delete("/tasks/1", headers=raj).status_code == 403
    assert client.get("/tasks").status_code == 401                         # no token at all


def test_validation(client: TestClient, login: Login) -> None:
    me = login("vishal@example.com")
    assert client.post("/tasks", json={"title": ""}, headers=me).status_code == 422
    client.post("/tasks", json={"title": "x"}, headers=me)
    assert client.patch("/tasks/1", json={"status": "archived"}, headers=me).status_code == 422
    assert client.patch("/tasks/99", json={"status": "done"}, headers=me).status_code == 404


def test_live_updates_over_websocket(client: TestClient, login: Login) -> None:
    me = login("vishal@example.com")
    with client.websocket_connect("/ws") as ws:
        client.post("/tasks", json={"title": "go live"}, headers=me)
        event = json.loads(ws.receive_text())
        assert event["event"] == "task_created" and event["title"] == "go live"
