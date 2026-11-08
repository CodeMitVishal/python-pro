# Python Pro – Module 26 Knowledge Check
**WebSockets, background tasks & caching**

The answer key is at the bottom, and each answer says which lesson file to revisit.

---

**1. Why use WebSockets instead of normal HTTP for a chat?**
- A) They're encrypted
- B) The connection stays open, so the server can push messages at any time
- C) They're faster to write
- D) HTTP can't send text

**2. How does a WebSocket connection start?**
- A) With FTP
- B) As an HTTP request that "upgrades" the connection
- C) With a raw socket only
- D) With email

**3. What exception tells you a client left?**
- A) `TimeoutError`
- B) `WebSocketDisconnect`
- C) `KeyError`
- D) `StopIteration`

**4. Why keep a set or dict of open connections?**
- A) Logging
- B) To broadcast a message to everyone connected
- C) Security
- D) It's required by FastAPI

**5. When does a FastAPI `BackgroundTasks` function run?**
- A) Before the endpoint
- B) After the response has been sent
- C) In another server
- D) Never in tests

**6. What does `202 Accepted` mean?**
- A) Done
- B) "Received; it's being processed", often with a job id to poll
- C) Not found
- D) Unauthorized

**7. Why use Celery, RQ or arq in production instead of in-process tasks?**
- A) Prettier code
- B) Separate workers, jobs that survive restarts, retries and scheduling
- C) No Redis needed
- D) They're faster for tiny tasks

**8. What is the cache-aside pattern?**
- A) Write to the cache only
- B) Read from the cache; on a miss, load from the DB and store with a TTL. On writes, update the DB, then delete the cache key
- C) Never expire data
- D) Cache everything forever

**9. Why delete the cache key after an update?**
- A) To save memory
- B) So nobody reads stale data
- C) Redis requires it
- D) To reset the TTL

**10. What does `ex=60` in `r.set(key, value, ex=60)` do?**
- A) Retries 60 times
- B) Expires the key after 60 seconds
- C) Limits the size
- D) Compresses the value

**11. Which data is a good fit for caching?**
- A) Data that changes every second and is rarely read
- B) Data that's read often and changes rarely
- C) Passwords
- D) Everything

**12. Why is Redis better than a Python dict as a cache when you run 4 server processes?**
- A) It's faster than a dict
- B) It's shared by all processes and servers, and survives app restarts
- C) Dicts can't store JSON
- D) It's free

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Revisit |
|---|--------|---------|
| 1 | B | `01_websockets_chat.py` |
| 2 | B | `01_websockets_chat.py` |
| 3 | B | `01_websockets_chat.py` |
| 4 | B | `01_websockets_chat.py` |
| 5 | B | `02_background_tasks.py` |
| 6 | B | `02_background_tasks.py` |
| 7 | B | `02_background_tasks.py` |
| 8 | B | `03_caching_with_redis.py` |
| 9 | B | `03_caching_with_redis.py` |
| 10 | B | `03_caching_with_redis.py` |
| 11 | B | `03_caching_with_redis.py` |
| 12 | B | `03_caching_with_redis.py` |

</details>

---

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
