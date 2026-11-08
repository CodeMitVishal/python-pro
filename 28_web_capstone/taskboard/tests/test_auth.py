from fastapi.testclient import TestClient


def test_signup_login_me(client: TestClient) -> None:
    r = client.post("/auth/signup", json={"email": "Vishal@Example.com", "password": "long-password-1"})
    assert r.status_code == 201 and "password" not in str(r.json())
    token = client.post("/auth/token", data={"username": "vishal@example.com",
                                             "password": "long-password-1"}).json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).json()
    assert me["email"] == "vishal@example.com"


def test_duplicate_email_and_weak_password(client: TestClient) -> None:
    body = {"email": "a@b.de", "password": "long-password-1"}
    assert client.post("/auth/signup", json=body).status_code == 201
    assert client.post("/auth/signup", json=body).status_code == 409
    assert client.post("/auth/signup", json={"email": "c@d.de", "password": "short"}).status_code == 422


def test_wrong_password_and_bad_token(client: TestClient) -> None:
    client.post("/auth/signup", json={"email": "a@b.de", "password": "long-password-1"})
    assert client.post("/auth/token", data={"username": "a@b.de", "password": "nope"}).status_code == 401
    assert client.get("/auth/me", headers={"Authorization": "Bearer junk"}).status_code == 401
