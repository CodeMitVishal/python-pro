"""Module 24 · JSON Web Tokens (JWT): what's inside, and what's not

  pip install pyjwt

A JWT is three base64url parts:   HEADER . PAYLOAD . SIGNATURE
  - the payload is only ENCODED, not encrypted: anyone can read it
    -> never put secrets (passwords, card numbers) in a JWT
  - the signature proves the server created it and nobody changed it
  - `exp` makes it expire; short lifetimes limit the damage of a stolen token

SESSIONS vs JWT:
  server session (cookie with a random id) -> easy to revoke, needs server storage
  JWT (self-contained)                     -> no lookup per request, hard to revoke early
                                              -> keep them short-lived (minutes)

TEACHING NOTES
  Why it matters  APIs and mobile apps need stateless authentication; JWTs are the common
                  answer.
  Picture it      A JWT is a signed ticket: anyone can read it, only the server can create a
                  valid one.
  Watch out       Never put secrets in the payload; always check exp and pass algorithms=[...]
                  when decoding.
  In real jobs    Bearer tokens for APIs, short-lived access tokens plus refresh tokens.
  Interview       Q: How does JWT authentication work?
                  A: The server signs claims; the client sends Bearer <token>; the server
                     verifies signature and expiry.

Run it:  python 24_auth_security/02_jwt_tokens.py
"""
import base64
import json
import time
from datetime import datetime, timedelta, timezone

import jwt

SECRET = "change-me-use-a-long-random-value-from-env"   # e.g. secrets.token_urlsafe(64)

# --- 1. Create a token ---------------------------------------------------------------------------
now = datetime.now(timezone.utc)
token = jwt.encode(
    {"sub": "vishal", "role": "admin", "iat": now, "exp": now + timedelta(minutes=15)},
    SECRET, algorithm="HS256")
header, payload, signature = token.split(".")
print("token:", token[:50] + "...")

# --- 2. Anyone can READ the payload: it's just base64 ----------------------------------------------
padded = payload + "=" * (-len(payload) % 4)
print("decoded without the key:", json.loads(base64.urlsafe_b64decode(padded)))

# --- 3. Verify: signature + expiry ---------------------------------------------------------------
claims = jwt.decode(token, SECRET, algorithms=["HS256"])     # always pin the algorithm!
print("verified:", claims["sub"], claims["role"])

# --- 4. Tampering is detected ----------------------------------------------------------------------
fake_payload = base64.urlsafe_b64encode(
    json.dumps({"sub": "vishal", "role": "superadmin", "exp": claims["exp"]}).encode()
).decode().rstrip("=")
forged = f"{header}.{fake_payload}.{signature}"
try:
    jwt.decode(forged, SECRET, algorithms=["HS256"])
except jwt.InvalidSignatureError:
    print("forged token: rejected (signature doesn't match)")

# --- 5. Expired tokens are rejected ------------------------------------------------------------------
short = jwt.encode({"sub": "raj", "exp": datetime.now(timezone.utc) + timedelta(seconds=1)},
                   SECRET, algorithm="HS256")
time.sleep(1.5)
try:
    jwt.decode(short, SECRET, algorithms=["HS256"])
except jwt.ExpiredSignatureError:
    print("expired token: rejected")

# --- 6. Wrong key ---------------------------------------------------------------------------------------
try:
    jwt.decode(token, "a-different-but-equally-long-secret-key", algorithms=["HS256"])
except jwt.InvalidTokenError as e:
    print("wrong key:", type(e).__name__)
