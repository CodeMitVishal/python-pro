# System design basics for Python web developers

Mid-level and senior interviews often include a 45-minute "design a system" round. You don't need to know everything. You need a **structured approach** and the **building blocks** below.

[← Interview prep](README.md)

---

## The approach (say this out loud)

1. **Clarify requirements.** Functional ("users shorten URLs") and non-functional (how many users, reads vs writes, latency, availability).
2. **Estimate the scale.** Requests per second, data size per year. Round numbers are fine.
3. **Define the API.** `POST /links`, `GET /{code}`.
4. **Design the data model.** Tables, keys, indexes.
5. **Draw the high-level design.** Client → load balancer → API servers → cache → database → workers.
6. **Deep-dive the bottlenecks.** Caching, scaling the DB, queues, failure cases.
7. **Discuss the trade-offs.** Consistency vs availability, cost, complexity.

## The building blocks

| Block | What it does | Python/web example |
|---|---|---|
| **Load balancer** | spreads traffic over stateless app servers | Azure Front Door, nginx |
| **Stateless API servers** | scale horizontally; no local sessions/files | FastAPI/Django in containers |
| **Cache** | serves hot reads in < 1 ms | Redis cache-aside with TTL |
| **Relational DB** | source of truth, transactions | Postgres + indexes |
| **Read replicas** | scale reads | route GETs to replicas |
| **Sharding / partitioning** | scale writes and data size | by user_id / tenant |
| **Message queue + workers** | slow/async work, smoothing spikes | Celery + Redis/RabbitMQ |
| **Object storage + CDN** | files, images, static assets | Azure Blob + CDN |
| **Search** | full-text search | Postgres FTS, Elasticsearch |
| **Observability** | logs, metrics, traces, alerts | OpenTelemetry, App Insights |

## Key concepts to name

- **Horizontal vs vertical scaling**: more machines vs a bigger machine.
- **CAP theorem**: during a network partition, choose consistency or availability.
- **Caching strategies**: cache-aside, write-through, TTLs, invalidation, stampedes.
- **Idempotency keys**: safe retries for payments and webhooks.
- **Rate limiting**: protect the system (token bucket in Redis).
- **Back pressure and queues**: absorb spikes instead of crashing.
- **Database indexes and N+1**: the most common real-world bottleneck.

---

## Practice questions (with a starting design)

### Design a URL shortener
API: `POST /links {url}` → `{code}`, and `GET /{code}` → 301/302. Store `code → url` in Postgres with a unique index, and generate the code as base62 of an ID. Reads massively outnumber writes, so cache codes in Redis and use read replicas. Count clicks asynchronously via a queue.

### Design a notification service (email / SMS / push)
The API accepts events → a queue → workers per channel. Store templates and user preferences. Add retries with backoff and a dead-letter queue, idempotency keys so users don't get duplicates, and rate limits per user and per provider.

### Design a rate limiter
Count requests per key in Redis (`INCR` + `EXPIRE`, a sliding window or a token bucket). Enforce it at the gateway or in middleware and return 429 with `Retry-After`. Decide whether to fail open or fail closed when Redis is down.

### Design a chat app
WebSocket servers keep connections open. Redis pub/sub (or Kafka) fans messages out across servers. Messages are stored in a DB partitioned by conversation and paginated by a time cursor. Presence uses Redis with TTL heartbeats.

### Design an e-commerce checkout
Validate the cart → reserve stock (atomic conditional UPDATE) → create the order (transaction) → charge the payment provider with an **idempotency key** → confirm via webhook → send emails from a queue. On payment failure, release the stock.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
