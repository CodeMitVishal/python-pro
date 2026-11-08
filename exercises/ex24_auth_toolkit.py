"""Exercise 24 · Build a small auth toolkit

  1. hash_password(pw) / verify_password(pw, stored)
       - salted scrypt (hashlib.scrypt), salt stored with the hash
       - verify uses hmac.compare_digest
  2. create_token(username, role, minutes=15) / read_token(token)
       - HS256 JWT with claims sub, role, exp
       - read_token returns the claims, or raises AuthError for ANY invalid token
         (bad signature, expired, garbage)
  3. A FastAPI app:
       POST /login   JSON {"username", "password"} -> {"token": ...} or 401
       GET  /orders  Authorization: Bearer <token> -> ["order-1", "order-2"]   (any logged-in user)
       DELETE /orders/{id}  -> 204 for role "admin", 403 for others, 401 without a token

Run it to check your work:
    pip install fastapi pyjwt httpx
    python exercises/ex24_auth_toolkit.py

Stuck? Compare with solutions/ex24_auth_toolkit.py
"""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

SECRET = secrets.token_urlsafe(64)


class AuthError(Exception):
    pass


def hash_password(pw):
    """TODO 1"""


def verify_password(pw, stored):
    """TODO 1"""


def create_token(username, role, minutes=15):
    """TODO 2"""


def read_token(token):
    """TODO 2"""


app = FastAPI()
USERS = {}            # filled in by the checks: {"name": {"role": ..., "hashed": ...}}

# TODO 3: the endpoints and the dependencies they need


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    h = hash_password("pa55word!")
    assert h and h != hash_password("pa55word!"), "use a random salt"
    assert verify_password("pa55word!", h) and not verify_password("Pa55word!", h)

    t = create_token("vishal", "admin")
    assert read_token(t)["sub"] == "vishal" and read_token(t)["role"] == "admin"
    for bad in [t[:-2] + "xx", "garbage", create_token("raj", "user", minutes=-1)]:
        try:
            read_token(bad)
            raise AssertionError(f"read_token accepted an invalid token: {bad[:20]}")
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
