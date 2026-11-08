"""Module 24 · Storing passwords safely

Rule: you never store a password, only a slow, salted HASH of it.

  plain text   -> one database leak = every account stolen
  md5 / sha256 -> FAST hashes: a GPU tries billions per second, rainbow tables crack
                  common passwords instantly, and equal passwords get equal hashes
  scrypt / argon2 / bcrypt -> deliberately SLOW + a random SALT per user

Here we use hashlib.scrypt (standard library). In production, argon2id via the
argon2-cffi or pwdlib packages is the current recommendation.

TEACHING NOTES
  Why it matters  When a database leaks, the password hashing decides whether users are safe.
  Picture it      A slow salted hash is a lock that takes a second to try: fine for one login,
                  hopeless for billions of guesses.
  Watch out       SHA-256 is fast, which is bad for passwords; use argon2, scrypt or bcrypt with
                  a salt.
  In real jobs    Django's and passlib's password hashers; secrets.token_urlsafe for reset
                  tokens.
  Interview       Q: How do you store passwords?
                  A: Slow, salted, adaptive hashes (argon2id/scrypt/bcrypt), constant-time
                     comparison, never plain text.

Run it:  python 24_auth_security/01_password_hashing.py
"""
import hashlib
import hmac
import secrets
import time

# --- 1. Why fast hashes are bad --------------------------------------------------------------
start = time.perf_counter()
for i in range(100_000):
    hashlib.sha256(f"guess{i}".encode()).hexdigest()
per_sec = 100_000 / (time.perf_counter() - start)
print(f"sha256: ~{per_sec:,.0f} guesses/second on ONE laptop core (GPUs: billions)")
print("same password, same sha256:",
      hashlib.sha256(b"summer2026").hexdigest() == hashlib.sha256(b"summer2026").hexdigest())


# --- 2. Salted, slow hashing with scrypt ---------------------------------------------------------
def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)                         # random, unique per user
    digest = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${salt.hex()}${digest.hex()}"           # store the salt WITH the hash


def verify_password(password: str, stored: str) -> bool:
    _, salt_hex, digest_hex = stored.split("$")
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
    return hmac.compare_digest(digest.hex(), digest_hex)   # constant-time comparison


h1, h2 = hash_password("summer2026"), hash_password("summer2026")
print("\nstored:", h1[:40] + "...")
print("same password, same scrypt hash:", h1 == h2, "<- different salts")
print("verify correct:", verify_password("summer2026", h1))
print("verify wrong:  ", verify_password("Summer2026", h1))

start = time.perf_counter()
verify_password("summer2026", h1)
print(f"one scrypt check: {(time.perf_counter() - start) * 1000:.0f} ms <- fine for a login, terrible for an attacker")

# --- 3. Random tokens: use `secrets`, never `random` ------------------------------------------------
print("\nreset token:", secrets.token_urlsafe(32))    # for password resets, API keys, session ids
# random.random() is predictable; secrets uses the OS's cryptographic randomness.
# hmac.compare_digest() avoids timing attacks: == stops at the first different character.
