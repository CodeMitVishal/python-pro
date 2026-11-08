# Module 28 · Interview questions (with answers)

These are the "tell me about your project" and system design questions. Use taskboard as your example.

[← Module 28](README.md) · [Final exam](QUIZ.md)

---

### 1. Walk me through a project you built.

**Say (STAR-style):**
- **Situation and goal**: a task API with accounts, permissions and live updates.
- **Stack**: FastAPI, SQLAlchemy, JWT, WebSockets, Docker, GitHub Actions.
- **Architecture**: routers → services → models; security in dependencies.
- **A hard problem and how you solved it**: N+1 queries, fixed with `selectinload` and a query-count test.
- **Results and next steps**: tests and strict typing in CI; Postgres and Azure deployment next.

---

### 2. How did you design authorisation?

**Say:** Authentication via JWT in a `current_user` dependency. Authorisation in one place: owner-or-admin checks before any read or write of a task. The API returns 404 instead of 403 so it doesn't reveal other users' IDs. Every rule has tests for allowed and denied cases.

---

### 3. How would you scale it to 1 million users?

**Say:**
- Stateless API replicas behind a load balancer, with autoscaling.
- Postgres with the right indexes, connection pooling, and read replicas.
- A Redis cache for hot reads.
- Redis pub/sub so WebSocket servers share events.
- Background workers for notifications.
- Rate limiting, and a CDN for static assets.
- Monitoring with SLO alerts.

Measure before optimising.

---

### 4. How do you make sure your API keeps working?

**Say:** A test pyramid (unit tests for permissions and services, API tests with `TestClient`, a few end-to-end tests), type checking and linting in CI, branch protection, staging deploys with smoke tests, monitoring and alerts in production, and a quick rollback.

---

### 5. Design a URL shortener (a classic system design warm-up).

**Say:**
- `POST /links` creates a short code (base62 of an ID, or random with a uniqueness check) and stores code → URL in a DB with an index on the code.
- `GET /{code}` looks it up (Redis cache first) and returns a **301/302** redirect.
- Click counts go through a queue or async increments.
- Add rate limiting, expiry and abuse checks.
- Scale reads with the cache and read replicas.

---

### 6. What would you improve in your project?

**Say:** Pick concrete items: Alembic migrations instead of `create_all`, Postgres with proper indexes, refresh tokens, login rate limits, per-user WebSocket channels, OpenTelemetry tracing, and an Azure deployment with CI/CD. Interviewers like candidates who can see their own project's limits.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
