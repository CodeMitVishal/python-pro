# Module 26 · Interview questions (with answers)

[← Module 26](README.md) · [Quiz](QUIZ.md)

---

### 1. WebSockets vs HTTP polling vs Server-Sent Events?

**Say:**
- **Polling** asks repeatedly. It's simple but wasteful and laggy.
- **SSE** is a one-way server→client stream over HTTP, good for live feeds.
- **WebSockets** keep a two-way connection open, good for chat, collaboration and games.

WebSockets need connection management and a shared broker (Redis pub/sub) to scale across servers.

---

### 2. When would you use a background job queue?

**Say:** For work that's slow, unreliable or not needed for the immediate response: emails, PDFs, image processing, partner API calls, imports. Return **202 Accepted** with a job ID, and let workers (Celery, RQ, Dramatiq) process jobs from a broker (Redis, RabbitMQ) with retries and backoff.

---

### 3. Why must tasks be idempotent?

**Say:** Queues guarantee **at-least-once** delivery: a worker can crash after doing the work but before acknowledging it, so the task runs again. Idempotent tasks (check whether the work is already done, use unique keys) make duplicates harmless.

---

### 4. Explain cache-aside.

**Say:** Read from the cache. On a miss, read from the DB and store the result with a **TTL**. On writes, update the DB and **invalidate** (delete) the cache key. It's simple and robust, and the TTL bounds staleness.

---

### 5. What is cache invalidation, and why is it hard?

**Say:** Keeping cached data consistent when the source changes. It's hard because data can change in many places, keys depend on many inputs (user, language, permissions), and races exist between read-through and invalidation. Use short TTLs, versioned keys, and delete on write.

---

### 6. What is a cache stampede?

**Say:** A popular key expires and thousands of requests miss at once and hit the DB together. Mitigate it with a lock so only one request rebuilds the value, early or background refresh, or jittered TTLs.

---

### 7. What else is Redis used for?

**Say:** Caching, sessions, rate limiting (`INCR` + `EXPIRE`), counters, leaderboards (sorted sets), queues and brokers, pub/sub for WebSockets, and distributed locks.

---

### 8. How would you implement rate limiting?

**Say:** Count requests per key (user or IP) per time window in Redis: `INCR rl:{key}:{window}` with `EXPIRE`, and answer **429** with `Retry-After` over the limit. For smoother limits, use a sliding window or token bucket. It's often done at the API gateway as well.

---

### 9. Where can you cache in a web system?

**Say:** In the browser (`Cache-Control`, `ETag`), at the CDN, at a reverse proxy, in app memory (`lru_cache`, per process), in a shared cache (Redis), and in the database's own caches. Cache as close to the user as correctness allows.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
