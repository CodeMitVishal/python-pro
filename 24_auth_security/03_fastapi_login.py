"""Module 24 · Login with OAuth2 password flow + JWT in FastAPI

  pip install fastapi pyjwt python-multipart

  POST /token     form: username + password -> {"access_token": "...", "token_type": "bearer"}
  GET  /me        header: Authorization: Bearer <token>   -> the current user
  GET  /admin     same, but only for role "admin"          -> 403 for others

FastAPI's OAuth2PasswordBearer also adds the "Authorize" button to /docs.

Run it:  python 24_auth_security/03_fastapi_login.py
"""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET = secrets.token_urlsafe(64)            # real apps: from settings / Azure Key Vault
ALGORITHM = "HS256"
TOKEN_MINUTES = 15


def hash_password(pw: str) -> str:
    salt = secrets.token_bytes(16)
    return salt.hex() + "$" + hashlib.scrypt(pw.encode(), salt=salt, n=2**14, r=8, p=1).hex()


def verify_password(pw: str, stored: str) -> bool:
    salt, digest = stored.split("$")
    check = hashlib.scrypt(pw.encode(), salt=bytes.fromhex(salt), n=2**14, r=8, p=1).hex()
    return hmac.compare_digest(check, digest)


USERS = {
    "vishal": {"username": "vishal", "role": "admin", "hashed": hash_password("s3cret!pass")},
    "raj": {"username": "raj", "role": "customer", "hashed": hash_password("raj-pass-123")},
}

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="token")   # reads "Authorization: Bearer <token>"


@app.post("/token")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    user = USERS.get(form.username)
    # Same error for "no such user" and "wrong password": don't tell attackers which one
    if user is None or not verify_password(form.password, user["hashed"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "wrong username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    expires = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES)
    token = jwt.encode({"sub": user["username"], "role": user["role"], "exp": expires},
                       SECRET, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


def current_user(token: Annotated[str, Depends(oauth2)]) -> dict:
    try:
        claims = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:                  # bad signature, expired, garbage...
        raise HTTPException(401, "invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    user = USERS.get(claims["sub"])
    if user is None:
        raise HTTPException(401, "user no longer exists")
    return user


def require_role(role: str):
    def checker(user: Annotated[dict, Depends(current_user)]) -> dict:
        if user["role"] != role:
            raise HTTPException(403, f"needs role {role!r}")
        return user
    return checker                                 # a dependency FACTORY (Module 10 closures!)


@app.get("/me")
def me(user: Annotated[dict, Depends(current_user)]) -> dict:
    return {"username": user["username"], "role": user["role"]}   # never return the hash


@app.get("/admin")
def admin_area(user: Annotated[dict, Depends(require_role("admin"))]) -> dict:
    return {"secret_stats": 42, "viewer": user["username"]}


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    c = TestClient(app)
    print("wrong password:", c.post("/token", data={"username": "vishal", "password": "x"}).status_code)
    print("no token:      ", c.get("/me").status_code)
    print("garbage token: ", c.get("/me", headers={"Authorization": "Bearer abc.def.ghi"}).status_code)

    def login_as(name, pw):
        token = c.post("/token", data={"username": name, "password": pw}).json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    raj = login_as("raj", "raj-pass-123")
    vishal = login_as("vishal", "s3cret!pass")
    print("raj /me:       ", c.get("/me", headers=raj).json())
    print("raj /admin:    ", c.get("/admin", headers=raj).status_code, "<- authenticated, not authorised")
    print("vishal /admin: ", c.get("/admin", headers=vishal).json())
