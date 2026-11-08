# Module 22 · Interview questions (with answers)

[← Module 22](README.md) · [Quiz](QUIZ.md)

---

### 1. How does FastAPI validate input?

**Say:** You declare path, query, header and body parameters with type hints and Pydantic models. FastAPI parses and converts them and checks the constraints. Invalid input returns **422** with field-level errors before your code runs. The same models generate the OpenAPI docs.

---

### 2. What is dependency injection in FastAPI?

**Say:** Endpoints declare what they need with `Depends(...)`, for example a DB session, the current user or pagination parameters. FastAPI resolves them per request. Dependencies can depend on each other, and `yield` dependencies clean up afterwards. In tests, `app.dependency_overrides` swaps them for fakes.

---

### 3. 401 vs 403 vs 422?

**Say:** **401** means not authenticated (no valid credentials). **403** means authenticated but not allowed. **422** means the request was understood but the data is invalid.

---

### 4. Why separate input and output models?

**Say:** So clients can't set fields they shouldn't (`id`, `is_admin`) and you never leak fields like `password_hash`. `response_model=UserOut` filters the response.

---

### 5. How do you handle errors consistently?

**Say:** Raise domain exceptions in services (`OutOfStock`). Register `@app.exception_handler` functions that map them to status codes and a consistent JSON shape. A global handler logs unexpected errors with a request ID and returns a generic 500.

---

### 6. What is middleware? Give examples.

**Say:** Code that wraps **every** request and response: request IDs, timing and logging, CORS, GZip, security headers, authentication for whole route groups.

---

### 7. What is CORS?

**Say:** A **browser** security rule. JavaScript from origin A may read responses from API origin B only if B sends `Access-Control-Allow-Origin` that permits A. For non-simple requests, the browser first sends a **preflight** `OPTIONS` request. Configure exact origins. CORS doesn't protect against non-browser clients.

---

### 8. `def` vs `async def` endpoints?

**Say:** Use `async def` when everything inside is awaitable. Use `def` for blocking code: FastAPI runs it in a thread pool. Never call blocking I/O inside `async def`.

---

### 9. How do you manage configuration and startup?

**Say:** `pydantic-settings` `BaseSettings` reads typed config from environment variables (12-factor). The **lifespan** handler creates shared resources once at startup (DB pool, `httpx.AsyncClient`) and closes them at shutdown.

---

### 10. How do you version and paginate an API?

**Say:** Versioning: a URL prefix (`/v1/`) or a header, and you never break existing clients without a new version. Pagination: `limit` and `offset` with a maximum limit, or **cursor/keyset** pagination (`?after=<id>`) for large or changing tables. Return the total or a `next` link.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
