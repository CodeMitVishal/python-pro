# Python Pro – Module 24 Knowledge Check
**Authentication & security**

The answer key is at the bottom, and each answer says which lesson file to revisit.

---

**1. Why is `sha256(password)` a bad way to store passwords?**
- A) It's too slow
- B) It's fast (billions of guesses per second) and unsalted (equal passwords give equal hashes)
- C) It can't be reversed
- D) It's too long

**2. What does a salt do?**
- A) Encrypts the hash
- B) Makes each hash unique, so equal passwords look different and precomputed tables are useless
- C) Speeds up hashing
- D) Shortens the hash

**3. Which is a good password-hashing algorithm?**
- A) md5
- B) sha1
- C) argon2id / scrypt / bcrypt
- D) base64

**4. Why `hmac.compare_digest` instead of `==`?**
- A) It's shorter
- B) It takes constant time, so attackers can't learn from response timing
- C) It hashes the input
- D) `==` doesn't work on strings

**5. Which module generates tokens for password resets?**
- A) `random`
- B) `secrets`
- C) `uuid1`
- D) `time`

**6. Is a JWT payload secret?**
- A) Yes, it's encrypted
- B) No: it's only base64-encoded; the signature proves it wasn't changed
- C) Only the header is readable
- D) It depends on the browser

**7. Why give access tokens a short `exp`?**
- A) Speed
- B) A stolen JWT can't easily be revoked, so short lifetimes limit the damage
- C) Smaller tokens
- D) It's required

**8. Why pass `algorithms=["HS256"]` to `jwt.decode`?**
- A) Speed
- B) Pinning the algorithm stops attacks that switch it (for example `"none"`)
- C) It's optional decoration
- D) For logging

**9. Login fails. Why return the same message for "unknown user" and "wrong password"?**
- A) Simpler code
- B) It doesn't reveal which usernames exist
- C) It's required by HTTP
- D) For speed

**10. 401 vs 403?**
- A) Same thing
- B) 401 = not authenticated (who are you?); 403 = authenticated but not allowed
- C) 401 = server error
- D) 403 = not found

**11. What prevents XSS?**
- A) HTTPS
- B) Escaping user-controlled output (templates do it), plus a Content-Security-Policy
- C) Hashing
- D) Rate limiting

**12. What is path traversal, and how do you stop it?**
- A) A routing feature
- B) Input like `../../etc/passwd` escaping a folder; resolve the path and check it stays inside
- C) A redirect
- D) A CORS rule

**13. What does rate limiting return, and why have it?**
- A) 500; for logging
- B) 429 Too Many Requests; it slows down brute-force attacks
- C) 404; to hide endpoints
- D) 301; to redirect

**14. Which tool checks your dependencies for known vulnerabilities?**
- A) `pip list`
- B) `pip-audit`
- C) `mypy`
- D) `pytest`

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Revisit |
|---|--------|---------|
| 1 | B | `01_password_hashing.py` |
| 2 | B | `01_password_hashing.py` |
| 3 | C | `01_password_hashing.py` |
| 4 | B | `01_password_hashing.py` |
| 5 | B | `01_password_hashing.py` |
| 6 | B | `02_jwt_tokens.py` |
| 7 | B | `02_jwt_tokens.py` |
| 8 | B | `02_jwt_tokens.py` |
| 9 | B | `03_fastapi_login.py` |
| 10 | B | `03_fastapi_login.py` |
| 11 | B | `04_web_security_checklist.py` |
| 12 | B | `04_web_security_checklist.py` |
| 13 | B | `04_web_security_checklist.py` |
| 14 | B | `04_web_security_checklist.py` |

</details>

---

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
