"""Solution · Exercise 24: Build a small auth toolkit

Run it:  python solutions/ex24_auth_toolkit.py
"""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

SECRET = secrets.token_urlsafe(64)


class AuthError(Exception):
    pass


def _scrypt(pw: str, salt: bytes) -> str:
    return hashlib.scrypt(pw.encode(), salt=salt, n=2**14, r=8, p=1).hex()


def hash_password(pw):
    salt = secrets.token_bytes(16)
    return f"{salt.hex()}${_scrypt(pw, salt)}"


def verify_password(pw, stored):
    salt_hex, digest = stored.split("$")
    return hmac.compare_digest(_scrypt(pw, bytes.fromhex(salt_hex)), digest)


def create_token(username, role, minutes=15):
    exp = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    return jwt.encode({"sub": username, "role": role, "exp": exp}, SECRET, algorithm="HS256")


def read_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError as e:          # parent of expired, bad signature, decode errors
        raise AuthError("invalid token") from e


app = FastAPI()
USERS = {}


class LoginIn(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(body: LoginIn) -> dict:
    user = USERS.get(body.username)
    if user is None or not verify_password(body.password, user["hashed"]):
        raise HTTPException(401, "wrong username or password")
    return {"token": create_token(body.username, user["role"])}


def current_claims(authorization: Annotated[str | None, Header()] = None) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing token")
    try:
        return read_token(authorization.removeprefix("Bearer "))
    except AuthError:
        raise HTTPException(401, "invalid token")


def admin_only(claims: Annotated[dict, Depends(current_claims)]) -> dict:
    if claims["role"] != "admin":
        raise HTTPException(403, "admins only")
    return claims


@app.get("/orders")
def orders(claims: Annotated[dict, Depends(current_claims)]) -> list[str]:
    return ["order-1", "order-2"]


@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int, claims: Annotated[dict, Depends(admin_only)]) -> None:
    pass


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    h = hash_password("pa55word!")
    assert h and h != hash_password("pa55word!")
    assert verify_password("pa55word!", h) and not verify_password("Pa55word!", h)

    t = create_token("vishal", "admin")
    assert read_token(t)["sub"] == "vishal" and read_token(t)["role"] == "admin"
    for bad in [t[:-2] + "xx", "garbage", create_token("raj", "user", minutes=-1)]:
        try:
            read_token(bad)
            raise AssertionError("accepted an invalid token")
        except AuthError:
            pass

    USERS.update({"vishal": {"role": "admin", "hashed": hash_password("admin-pass")},
                  "raj": {"role": "user", "hashed": hash_password("raj-pass")}})
    c = TestClient(app)
    assert c.post("/login", json={"username": "raj", "password": "nope"}).status_code == 401
    raj = {"Authorization": "Bearer " + c.post("/login", json={"username": "raj", "password": "raj-pass"}).json()["token"]}
    adm = {"Authorization": "Bearer " + c.post("/login", json={"username": "vishal", "password": "admin-pass"}).json()["token"]}
    assert c.get("/orders").status_code == 401
    assert c.get("/orders", headers=raj).json() == ["order-1", "order-2"]
    assert c.delete("/orders/1", headers=raj).status_code == 403
    assert c.delete("/orders/1", headers=adm).status_code == 204
    print("All checks passed!")
