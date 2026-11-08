# Module 18 · Interview questions (with answers)

Short answers you can say out loud, with code and the usual follow-up.

[← Module 18](README.md) · [Quiz](QUIZ.md)

---

### 1. What is REST?

**Say:** An architectural style for HTTP APIs:
- **Resources** are identified by URLs (`/orders/7`).
- Standard **methods** act on them (GET read, POST create, PUT replace, PATCH update, DELETE remove).
- It's **stateless**: each request carries its own auth.
- **Status codes** carry meaning, and representations are usually JSON.

---

### 2. PUT vs PATCH vs POST? What is idempotency?

**Say:** POST creates (not idempotent: twice creates two). PUT replaces the whole resource and PATCH changes some fields. **Idempotent** means repeating the request has the same effect as doing it once: GET, PUT and DELETE are; POST isn't. For safe retries of POST (payments), clients send an **Idempotency-Key** header.

---

### 3. Explain the common HTTP status codes.

**Say:**
- **200** OK, **201** Created, **204** No Content.
- **301/302** redirects.
- **400** Bad Request, **401** Unauthenticated, **403** Forbidden, **404** Not Found, **409** Conflict, **422** Validation error, **429** Too Many Requests.
- **500** server bug, **502/503/504** upstream or overload problems.

---

### 4. How do you call an external API robustly?

**Say:**
- Always set a **timeout**.
- Check the status (`raise_for_status()`).
- **Retry** idempotent calls with exponential backoff and jitter on 429/5xx and timeouts.
- Reuse a `Session` (connection pooling).
- Log failures with context.
- Use a circuit breaker for flaky dependencies.

---

### 5. What is SQL injection, and how do you prevent it?

**Say:** User input is concatenated into SQL and changes its meaning (`' OR '1'='1`). Prevent it with **parameterised queries** (`cursor.execute("... WHERE email = %s", (email,))`) or an ORM. Never use f-strings for SQL. Least-privilege DB accounts limit the damage.

---

### 6. INNER JOIN vs LEFT JOIN?

**Say:** An **INNER JOIN** returns only rows that match in both tables. A **LEFT JOIN** returns **all** rows of the left table, with NULLs where there's no match. Example: every user with their order count, including users with no orders, needs a LEFT JOIN.

---

### 7. What does GROUP BY do? WHERE vs HAVING?

**Say:** `GROUP BY` collapses rows into groups so you can aggregate them (COUNT, SUM, AVG). `WHERE` filters **rows before** grouping; `HAVING` filters **groups after** aggregation (`HAVING COUNT(*) > 5`).

---

### 8. What is a transaction? What is ACID?

**Say:** A transaction is a unit of work that fully commits or fully rolls back.
- **Atomicity**: all or nothing.
- **Consistency**: constraints hold.
- **Isolation**: concurrent transactions don't see each other's half-done work.
- **Durability**: once committed, the data survives a crash.

**Follow-up:** *"What are isolation levels?"* READ UNCOMMITTED, READ COMMITTED (Postgres default), REPEATABLE READ and SERIALIZABLE. Higher levels prevent more anomalies (dirty reads, non-repeatable reads, phantoms) but reduce concurrency.

---

### 9. How do you handle time zones in a backend?

**Say:** Store and compute in **UTC** with timezone-aware datetimes (`datetime.now(UTC)`). Convert to the user's zone (`zoneinfo.ZoneInfo`) only for display. Exchange ISO 8601 strings with an offset. Never use naive datetimes across servers; DST changes will bite you.

---

### 10. Why is `pickle` dangerous?

**Say:** Unpickling can execute arbitrary code, so loading a pickle from an untrusted source is remote code execution. Use JSON (or MessagePack, protobuf) for data that crosses trust boundaries.

---

### 11. `str` vs `bytes`? What is UTF-8?

**Say:** `str` is Unicode **text**; `bytes` is raw **data**. Convert between them with `.encode()` and `.decode()` and an explicit codec. **UTF-8** encodes any Unicode character in 1–4 bytes and is the standard for files and the web. Decoding with the wrong codec gives mojibake (`MÃ¼nchen`).

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
