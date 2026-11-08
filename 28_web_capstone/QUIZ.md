# Python Pro – Web Development Final Exam
**Modules 21–28**

Score 12+ out of 15 and you're ready for backend Python jobs. The answer key says which module to revisit.

---

**1.** Name the parts of an HTTP request and say what a 201, a 401, a 403 and a 422 mean.

**2.** Why redirect after a successful form POST?

**3.** What does Jinja2 auto-escaping protect against, and what turns it off?

**4.** Why have separate pydantic models for input and output?

**5.** How do tests replace the "current user" dependency in FastAPI?

**6.** What is the N+1 problem, and how do you fix it in SQLAlchemy?

**7.** Why use Alembic instead of `create_all()` in production?

**8.** Why scrypt/argon2 with a salt, instead of sha256, for passwords?

**9.** Is a JWT payload secret? What protects it?

**10.** In taskboard, why does editing another user's task return 403 and not 404 or 200?

**11.** When would you choose Django over FastAPI?

**12.** Describe the cache-aside pattern and when you invalidate.

**13.** Why push task changes over a WebSocket instead of having clients poll every second?

**14.** Name four things that make a Dockerfile production-ready.

**15.** What does the CI pipeline check before deploying, and why tag images with the commit SHA?

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Revisit |
|---|--------|---------|
| 1 | Request line, headers, blank line, body. 201 Created, 401 not authenticated, 403 not allowed, 422 invalid input | 21 |
| 2 | Refreshing the page must not resubmit the form (POST → redirect → GET) | 21 |
| 3 | XSS. `\|safe` / `Markup` turn it off; never use them on user input | 21, 24 |
| 4 | Validate what comes in; never leak fields like password hashes in what goes out | 22 |
| 5 | `app.dependency_overrides[current_user] = lambda: fake_user` | 22 |
| 6 | 1 query for the list + 1 per item. Fix with `selectinload` / `joinedload` | 23 |
| 7 | Versioned, reversible schema changes that keep existing data | 23 |
| 8 | Slow + salted: brute force is impractical and equal passwords hash differently | 24 |
| 9 | No, it's only base64. The signature (and a short `exp`) protects it | 24 |
| 10 | The user is authenticated but not authorised; ownership is checked on every write | 24, 28 |
| 11 | Full web apps that need an admin, auth, forms and server-rendered HTML; Django's batteries | 25 |
| 12 | Read: cache → miss → DB → store with TTL. Write: update the DB, then delete the key | 26 |
| 13 | Instant updates, far fewer requests, and the server pushes only when something changes | 26 |
| 14 | Slim pinned base, deps before code (caching), non-root user, no secrets, HEALTHCHECK, exec-form CMD | 27 |
| 15 | Lint, type check, tests; nothing deploys if they fail. The SHA shows exactly what runs and makes rollback easy | 27 |

</details>

---

🎓 **Finished the web track?** Deploy taskboard, share the link on LinkedIn, and tag me!

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
