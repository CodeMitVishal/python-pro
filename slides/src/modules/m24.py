"""Slides · Module 24 · Authentication & security"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 24 · Authentication &amp; security"
SLIDES = [
 cover("24", "Authentication &amp; security", "Store passwords safely, issue tokens, check permissions, and stop the classic web attacks.",
       [("Password hashing", "01_password_hashing.py"), ("JWT tokens", "02_jwt_tokens.py"),
        ("FastAPI login", "03_fastapi_login.py"), ("Security checklist", "04_web_security_checklist.py"),
        ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Security", "One leak can end a company",
     "A database dump leaks. If passwords were stored as plain text or a fast hash, attackers log in as your users, "
     "and on every other site where they reused the password.",
     "Hash passwords <b>slowly with a salt</b>, give clients <b>short-lived tokens</b>, check <b>permissions</b> on every request, and validate all input."),

 trace(M, "Auth basics", "Authentication vs authorisation", ["", "Question", "Failure", "Example"],
       [["<b>Authentication</b> (authN)", "<b>Who</b> are you?", "<b>401</b> Unauthorized", "password, token, OAuth login"],
        ["<b>Authorisation</b> (authZ)", "What may you <b>do</b>?", "<b>403</b> Forbidden", "roles, owner-only, admin-only"]],
       "Check authorisation on the <b>server</b> for every request. Hiding a button in the UI is not security."),

 mistake(M, "Password hashing", "Storing passwords the wrong way",
     '''
users[email] = password                    # plain text!
users[email] = hashlib.sha256(
    password.encode()).hexdigest()         # fast, unsalted''',
     "SHA-256 is built to be <b>fast</b>: a GPU tries billions per second. Without a salt, equal passwords have equal hashes (rainbow tables).",
     '''
salt = secrets.token_bytes(16)             # unique per user
key = hashlib.scrypt(password.encode(), salt=salt,
                     n=2**14, r=8, p=1)    # deliberately SLOW
store(email, salt, key)
# or: argon2-cffi / passlib / Django's hashers''',
     "Use a <b>slow, salted</b> password hash: <b>argon2</b>, <b>scrypt</b> or <b>bcrypt</b>. Compare with <b>hmac.compare_digest</b>."),

 code_out(M, "Password hashing", "Hash and verify with scrypt", '''
import hashlib, hmac, secrets

def hash_password(pw: str) -> str:
    salt = secrets.token_bytes(16)
    key = hashlib.scrypt(pw.encode(), salt=salt, n=2**14, r=8, p=1)
    return salt.hex() + "$" + key.hex()

def verify(pw: str, stored: str) -> bool:
    salt_hex, key_hex = stored.split("$")
    key = hashlib.scrypt(pw.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
    return hmac.compare_digest(key.hex(), key_hex)    # constant time

a, b = hash_password("hunter2"), hash_password("hunter2")
print(a[:40] + "...")
print("same password, different hashes:", a != b)
print(verify("hunter2", a), verify("Hunter2", a))''',
     steps=["The <b>salt</b> makes every hash unique.", "<b>compare_digest</b> avoids timing attacks.",
            "<b>secrets</b> (not random) for anything security-related."]),

 picture(M, "JWT", "What's inside a JWT",
     "&#127915; A JWT is a <b>signed ticket</b>: anyone can <b>read</b> it, but only the server (with the secret key) can <b>create</b> a valid one. "
     "Change one character and the signature no longer matches.",
     [("header", "{\"alg\": \"HS256\"}"), ("payload", "{\"sub\": \"42\", \"role\": \"admin\", \"exp\": ...}"),
      ("signature", "HMAC(header.payload, SECRET)"), ("server", "verifies the signature + exp on every request")],
     "Never put secrets in the payload: it's only base64, not encrypted."),

 code_out(M, "JWT", "Issue, verify, expire, tamper", '''
import base64, json, time
import jwt                                  # pip install pyjwt

SECRET = "change-me-to-a-long-random-value"
token = jwt.encode({"sub": "42", "role": "user", "exp": int(time.time()) + 900},
                   SECRET, algorithm="HS256")
print(token[:36] + "...")
print(jwt.decode(token, SECRET, algorithms=["HS256"])["role"])

head, payload, sig = token.split(".")
data = json.loads(base64.urlsafe_b64decode(payload + "=="))
data["role"] = "admin"                       # attacker edits the payload
forged = ".".join([head, base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip("="), sig])
try:
    jwt.decode(forged, SECRET, algorithms=["HS256"])
except jwt.InvalidSignatureError:
    print("forged token rejected")

old = jwt.encode({"sub": "42", "exp": int(time.time()) - 1}, SECRET, algorithm="HS256")
try:
    jwt.decode(old, SECRET, algorithms=["HS256"])
except jwt.ExpiredSignatureError:
    print("expired token rejected")''',
     steps=["Short <b>exp</b> (15 min) + a refresh token.", "Always pass <b>algorithms=[...]</b> when decoding.",
            "Logout/revocation needs extra work (a deny-list or short expiry)."]),

 trace(M, "Sessions vs tokens", "Session cookies or JWTs?", ["", "Session cookie", "JWT (Bearer token)"],
       [["State lives", "on the server (DB/Redis)", "in the token (stateless)"],
        ["Revoke / logout", "easy: delete the session", "hard: wait for expiry or keep a deny-list"],
        ["Best for", "browser web apps (Django)", "APIs, mobile apps, service-to-service"],
        ["Main risk", "CSRF (use SameSite + CSRF tokens)", "XSS stealing a token from localStorage"]],
       "For browser apps, prefer <b>HttpOnly</b> cookies; for APIs, short-lived bearer tokens. OAuth2/OIDC (Google, Entra ID) for third-party login."),

 trace(M, "OWASP", "The attacks every web developer must know", ["Attack", "What happens", "Defence"],
       [["<b>SQL injection</b>", "input changes the SQL", "parameterised queries / ORM"],
        ["<b>XSS</b>", "attacker's &lt;script&gt; runs in other users' browsers", "auto-escaping templates, CSP header"],
        ["<b>CSRF</b>", "another site makes your logged-in browser POST", "CSRF tokens, SameSite cookies"],
        ["<b>Broken access control</b>", "user reads /orders/7 that isn't theirs", "check ownership on every request"],
        ["<b>Path traversal</b>", "../../etc/passwd", "resolve the path, check it stays inside the folder"],
        ["<b>Brute force</b>", "millions of login attempts", "rate limiting, lockouts, 2FA"]]),

 mistake(M, "Access control", "Checking login but not ownership",
     '''
@app.get("/orders/{order_id}")
def get_order(order_id: int, user=Depends(current_user)):
    return db.get(Order, order_id)
# any logged-in user can read ANY order (IDOR)''',
     "Being <b>logged in</b> isn't permission. Changing the number in the URL shows other customers' orders: the #1 OWASP risk.",
     '''
@app.get("/orders/{order_id}")
def get_order(order_id: int, user=Depends(current_user)):
    order = db.get(Order, order_id)
    if order is None or (order.user_id != user.id
                         and not user.is_admin):
        raise HTTPException(404)          # don't reveal it exists
    return order''',
     "Check <b>ownership or role</b> on the server for every object."),

 job(M, "Security", "Security habits at work", [
     ("Secrets never in git", '''
DATABASE_URL, JWT_SECRET -> env vars / Key Vault
git-secrets / gitleaks in CI'''),
     ("Security headers", '''
Strict-Transport-Security, Content-Security-Policy,
X-Content-Type-Options: nosniff'''),
     ("Dependency scanning", '''
pip-audit · Dependabot · bandit'''),
     ("Login via your company IdP", '''
OAuth2 / OpenID Connect (Entra ID, Google)
instead of storing passwords yourself'''),
 ]),

 interview(M, "How do you store passwords securely?",
     ["Never store the password or a fast hash (MD5, SHA-256).",
      "Use a <b>slow, salted, adaptive</b> hash: <b>argon2id</b>, <b>scrypt</b> or <b>bcrypt</b> (frameworks have this built in).",
      "A unique random <b>salt</b> per user defeats rainbow tables; the work factor slows brute force.",
      "Verify with a constant-time comparison; rehash when you raise the cost.",
      "Add rate limiting, 2FA and breached-password checks."],
     None,
     "\"Hashing vs encryption?\" (hashing is one-way, for verifying; encryption is reversible with a key, for data you need to read back)."),

 interview(M, "How does JWT authentication work? What are its downsides?",
     ["On login the server issues a <b>signed</b> token with claims (sub, role, exp).",
      "The client sends it as <b>Authorization: Bearer &lt;token&gt;</b>; the server verifies the signature and expiry on every request: no session lookup.",
      "Downsides: hard to <b>revoke</b> before expiry, payload is <b>readable</b>, tokens in localStorage are exposed to XSS.",
      "Mitigate: short-lived access tokens + refresh tokens, HttpOnly cookies for browsers, rotate keys."],
     None,
     "\"What are XSS and CSRF and how do you prevent them?\" (XSS: escape output + CSP; CSRF: CSRF tokens + SameSite cookies)."),

 recap(M, "Module 24 in 6 lines",
     ["authN = who (401), authZ = what (403); check on the server.",
      "Passwords: <b>argon2/scrypt/bcrypt</b> + salt; never SHA-256.",
      "JWT = signed, readable, short-lived; verify signature and exp.",
      "Sessions for browsers, tokens for APIs; OAuth2/OIDC for SSO.",
      "OWASP: injection, XSS, CSRF, broken access control, path traversal.",
      "Secrets in env/vault, security headers, rate limits, dependency scans."],
     "Run <b>03_fastapi_login.py</b>, then add an <b>owner-only</b> check to an endpoint and a test that gets 404 for someone else's order."),
]
