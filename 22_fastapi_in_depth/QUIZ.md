# Python Pro – Module 22 Knowledge Check
**FastAPI in depth**

The answer key is at the bottom, and each answer says which lesson file to revisit.

---

**1. Why validate with pydantic at the edges of your app?**
- A) Speed
- B) Everything from outside is untrusted; pydantic converts it to typed objects or explains exactly what's wrong
- C) FastAPI can't run without it
- D) To encrypt data

**2. Which constraint means "13 ≤ age ≤ 120"?**
- A) `Field(min=13, max=120)`
- B) `Field(ge=13, le=120)`
- C) `Field(13, 120)`
- D) `int[13:120]`

**3. Why have separate `UserIn` and `UserOut` models?**
- A) Speed
- B) So secrets like passwords never appear in responses
- C) It's required
- D) For versioning

**4. What does `@field_validator` let you do?**
- A) Rename fields
- B) Clean or check one field's value with your own code
- C) Make a field optional
- D) Sort models

**5. What is an `APIRouter` for?**
- A) Load balancing
- B) Grouping endpoints with a shared prefix and tags, often one file per resource
- C) Routing network packets
- D) Caching

**6. What does `Depends(current_user)` do?**
- A) Imports a module
- B) FastAPI calls `current_user` for each request and passes the result in
- C) Creates a user
- D) Caches the user forever

**7. How do tests replace a dependency with a fake?**
- A) Edit the code
- B) `app.dependency_overrides[real_dep] = fake`
- C) Monkeypatch `FastAPI`
- D) They can't

**8. Not logged in vs logged in but not allowed: which status codes?**
- A) 403 / 401
- B) 401 / 403
- C) 404 / 500
- D) 400 / 400

**9. Why register an `@app.exception_handler(Exception)` that returns a generic 500?**
- A) Speed
- B) So tracebacks and secrets never leak to clients
- C) It's required
- D) To retry requests

**10. What is middleware?**
- A) A database layer
- B) Code that runs around every request (timing, request IDs, logging)
- C) A frontend framework
- D) A type of router

**11. What does CORS control?**
- A) Server-to-server calls
- B) Which other website origins may call your API from a browser
- C) Database access
- D) Rate limits

**12. Why `api_key: SecretStr` in pydantic-settings?**
- A) Encryption at rest
- B) The value is hidden when printed or logged (`**********`)
- C) It's faster
- D) It's required

**13. When should an endpoint be `async def`?**
- A) Always
- B) When it awaits async I/O (async HTTP clients, async DB drivers); blocking code should use plain `def`
- C) Never
- D) Only for GET

**14. What is the `lifespan` function for?**
- A) Request timeouts
- B) Code that runs once at startup (create shared clients/pools) and once at shutdown (close them)
- C) Session cookies
- D) Logging levels

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Revisit |
|---|--------|---------|
| 1 | B | `01_pydantic_models.py` |
| 2 | B | `01_pydantic_models.py` |
| 3 | B | `01_pydantic_models.py` |
| 4 | B | `01_pydantic_models.py` |
| 5 | B | `02_routers_and_dependencies.py` |
| 6 | B | `02_routers_and_dependencies.py` |
| 7 | B | `02_routers_and_dependencies.py` |
| 8 | B | `02_routers_and_dependencies.py` |
| 9 | B | `03_errors_middleware_cors.py` |
| 10 | B | `03_errors_middleware_cors.py` |
| 11 | B | `03_errors_middleware_cors.py` |
| 12 | B | `04_settings_lifespan_async.py` |
| 13 | B | `04_settings_lifespan_async.py` |
| 14 | B | `04_settings_lifespan_async.py` |

</details>

---

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
