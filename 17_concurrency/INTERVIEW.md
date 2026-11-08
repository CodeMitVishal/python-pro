# Module 17 · Interview questions (with answers)

Short answers you can say out loud, with code and the usual follow-up.

[← Module 17](README.md) · [Quiz](QUIZ.md)

---

### 1. What is the GIL?

**Say:** The **Global Interpreter Lock** in CPython lets only **one thread execute Python bytecode at a time**. It makes reference counting safe and simple. The downside is that threads can't speed up **pure-Python CPU work** on several cores. It is released during blocking I/O and by many C extensions (NumPy), so threads still help with I/O. Python 3.13+ has an experimental free-threaded build.

---

### 2. Threads vs processes vs asyncio: when do you use which?

**Say:**
- **I/O-bound** with a moderate number of tasks, or blocking libraries: **threads** (`ThreadPoolExecutor`).
- **I/O-bound** with thousands of connections and async libraries: **asyncio**.
- **CPU-bound**: **processes** (`ProcessPoolExecutor`, multiprocessing) or vectorised C code (NumPy).

---

### 3. Concurrency vs parallelism?

**Say:** **Concurrency** means dealing with many tasks at once by interleaving them (one cook, several pots). **Parallelism** means literally doing several things at the same instant on several cores (several cooks). asyncio is concurrent; multiprocessing is parallel.

---

### 4. What is a race condition? How do you prevent it?

**Say:** Two threads access shared data and at least one writes, so the result depends on timing. For example, `count += 1` is read-modify-write and can lose updates. Prevent it with a `threading.Lock`, with thread-safe structures like `queue.Queue`, or by not sharing state (each worker returns results and you combine them).

---

### 5. What is a deadlock?

**Say:** Two (or more) threads each hold a lock and wait for the other's lock forever. Avoid it by acquiring locks in a **fixed order**, holding them briefly, using timeouts, or using higher-level tools (queues, executors).

---

### 6. How does async/await work?

**Say:** `async def` defines a coroutine. `await` suspends it at a point where it would wait (network, sleep) and hands control back to the **event loop**, which resumes whichever coroutine is ready. It's single-threaded and cooperative, so switches happen only at `await`.

---

### 7. What happens if you call a blocking function inside `async def`?

**Say:** It blocks the **entire event loop**: every other request and task freezes until it returns. Use async libraries (httpx, asyncpg), or offload the call with `await asyncio.to_thread(func)` or `loop.run_in_executor`.

---

### 8. `asyncio.gather` vs `TaskGroup`?

**Say:** Both run coroutines concurrently. `TaskGroup` (3.11+) is **structured concurrency**: if one task fails, the others are cancelled and the errors are raised together as an `ExceptionGroup`. `gather` by default keeps the others running, which can leak work. I prefer `TaskGroup`.

---

### 9. In FastAPI, when do you use `def` vs `async def` endpoints?

**Say:** Use `async def` when everything inside is awaitable (async DB driver, httpx). Use plain `def` when you call blocking libraries (requests, a sync ORM). FastAPI then runs the function in a thread pool so it doesn't block the loop.

---

### 10. How would you limit concurrency, e.g. at most 10 requests at once?

**Say:** In asyncio, use an `asyncio.Semaphore(10)` around the request. With threads, set `max_workers=10`. This protects the partner API and your own resources and respects rate limits.

```python
sem = asyncio.Semaphore(10)
async def fetch(url):
    async with sem:
        return await client.get(url)
```

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
