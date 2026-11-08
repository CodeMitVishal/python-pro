# Module 24 · Authentication & security

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-24.pdf) · [Interview Q&A](INTERVIEW.md)

Log users in safely and defend your app: password hashing, JWTs, OAuth2 login with roles, and the OWASP basics.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Password hashing | [`01_password_hashing.py`](01_password_hashing.py) | why sha256 is wrong; salted scrypt; `secrets` |
| JWT tokens | [`02_jwt_tokens.py`](02_jwt_tokens.py) | what's inside, signatures, expiry, tampering |
| FastAPI login | [`03_fastapi_login.py`](03_fastapi_login.py) | OAuth2 password flow, current user, roles (401 vs 403) |
| Security checklist | [`04_web_security_checklist.py`](04_web_security_checklist.py) | XSS, path traversal, rate limiting, security headers |

```bash
pip install fastapi pyjwt python-multipart
```

```bash
python 24_auth_security/01_password_hashing.py
```

## Exercise: An auth toolkit

Hashing, JWT create/verify, and role-protected endpoints.

- Start here: [`exercises/ex24_auth_toolkit.py`](../exercises/ex24_auth_toolkit.py)
- Solution: [`solutions/ex24_auth_toolkit.py`](../solutions/ex24_auth_toolkit.py)

## Knowledge check

Preparing for interviews? Read the [Module 24 interview questions](INTERVIEW.md): short answers you can say out loud.


Test yourself with the [Module 24 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 25 · Django + DRF](../25_django/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
