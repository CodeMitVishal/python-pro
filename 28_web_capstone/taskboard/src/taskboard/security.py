"""Password hashing and JWT tokens (Module 24)."""
import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

import jwt

from taskboard.config import settings

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    _, salt_hex, digest_hex = stored.split("$")
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
    return hmac.compare_digest(digest.hex(), digest_hex)


def create_access_token(user_id: int) -> str:
    exp = datetime.now(UTC) + timedelta(minutes=settings.token_minutes)
    return jwt.encode({"sub": str(user_id), "exp": exp},
                      settings.jwt_secret.get_secret_value(), algorithm=ALGORITHM)


def read_user_id(token: str) -> int | None:
    try:
        claims = jwt.decode(token, settings.jwt_secret.get_secret_value(), algorithms=[ALGORITHM])
        return int(claims["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        return None
