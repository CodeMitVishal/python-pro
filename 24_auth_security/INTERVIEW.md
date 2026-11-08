# Module 24 · Interview questions (with answers)

[← Module 24](README.md) · [Quiz](QUIZ.md)

---

### 1. Authentication vs authorisation?

**Say:** **Authentication** answers "who are you?" (login, token); if it fails, the response is **401**. **Authorisation** answers "what may you do?" (roles, ownership); if it fails, the response is **403** (or 404 to hide that the object exists). Both must be enforced on the server.

---

### 2. How do you store passwords?

**Say:** Never in plain text or with a fast hash. Use a slow, salted, adaptive algorithm: **argon2id**, **scrypt** or **bcrypt**. A unique salt per user defeats rainbow tables. Compare in constant time, and rehash when you increase the cost.

---

### 3. Hashing vs encryption vs encoding?

**Say:** **Hashing** is one-way (passwords, integrity checks). **Encryption** is reversible with a key (data you need to read back). **Encoding** (base64) is just a format, with no security at all.

---

### 4. How does JWT work? Pros and cons?

**Say:** The server signs a token with claims (`sub`, `role`, `exp`). The client sends `Authorization: Bearer <token>`, and the server verifies the signature and expiry without a database lookup.
- **Pros**: stateless, works across services.
- **Cons**: hard to revoke, the payload is readable, and tokens stolen through XSS from localStorage can be reused.

Use short-lived access tokens with refresh tokens.

---

### 5. Sessions vs tokens?

**Say:** A **session** keeps state on the server and the cookie holds only an ID. It's easy to revoke, and it's the best fit for browser apps. **Tokens** are stateless and the best fit for APIs and mobile clients. In browsers, prefer HttpOnly cookies over localStorage.

---

### 6. What is OAuth2 / OpenID Connect?

**Say:** **OAuth2** is a framework for **delegated authorisation**: an app gets an access token to call an API on a user's behalf. **OIDC** adds **authentication** on top (an ID token about who the user is). It's used for "Login with Google / Microsoft Entra ID". The authorization code flow with PKCE is the standard for web and mobile apps.

---

### 7. What are XSS and CSRF?

**Say:** **XSS**: an attacker's script runs in other users' browsers. Prevent it with output escaping, a CSP header, and HttpOnly cookies. **CSRF**: another site makes a logged-in user's browser send a request. Prevent it with CSRF tokens, `SameSite` cookies, and by not using GET for state changes.

---

### 8. What is broken access control / IDOR?

**Say:** **IDOR** (Insecure Direct Object Reference) means changing an ID in the URL (`/orders/7` → `/orders/8`) shows someone else's data because the server checks only the login, not the **ownership**. It's the #1 risk in the OWASP Top 10. Check owner-or-role on every object access, and test it.

---

### 9. How do you protect a login endpoint?

**Say:** Rate-limit per IP and per account, use generic error messages ("invalid credentials"), apply a slow hash, offer 2FA, add lockout or CAPTCHA after repeated failures, log suspicious activity, and force HTTPS.

---

### 10. Where do secrets go?

**Say:** Never in git or in Docker images. They go in environment variables injected at runtime, or in a secrets manager (Azure Key Vault, AWS Secrets Manager). Rotate them, scan repos for leaked keys (gitleaks), and use least-privilege credentials.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
