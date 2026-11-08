"""Slides · Module 26 · WebSockets, background tasks & caching"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 26 · Real-time, tasks &amp; caching"
SLIDES = [
 cover("26", "WebSockets, background tasks &amp; caching", "Push live updates, move slow work off the request, and make hot data instant with Redis.",
       [("WebSocket chat", "01_websockets_chat.py"), ("Background tasks", "02_background_tasks.py"),
        ("Caching with Redis", "03_caching_with_redis.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Three performance tools", "Three problems, three tools",
     "1) The dashboard should update <b>without refreshing</b>. 2) Sign-up takes 6 s because it <b>sends emails</b> in the request. "
     "3) The product page runs the <b>same expensive query</b> 1,000 times a minute.",
     "1) <b>WebSockets</b> push updates. 2) <b>Background jobs</b> do slow work later. 3) A <b>cache</b> remembers hot results."),

 picture(M, "WebSockets", "HTTP vs WebSocket",
     "&#128222; HTTP is like <b>sending letters</b>: the client asks, the server answers, done. A WebSocket is a <b>phone call</b>: "
     "the line stays open and <b>both</b> sides can talk at any time.",
     [("HTTP request", "GET /ws  Upgrade: websocket"), ("101 Switching Protocols", "the connection stays open"),
      ("server &#8594; client", "push: \"order 7 shipped\""), ("client &#8594; server", "send: \"typing...\"")],
     "Use it for chat, live dashboards, notifications, multiplayer. Alternatives: polling, Server-Sent Events."),

 code_out(M, "WebSockets", "A broadcast chat room in FastAPI", '''
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.testclient import TestClient

app = FastAPI()
clients: set[WebSocket] = set()

@app.websocket("/ws/chat")
async def chat(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            msg = await ws.receive_text()
            for c in list(clients):            # broadcast to everyone
                await c.send_text(f"someone: {msg}")
    except WebSocketDisconnect:
        clients.discard(ws)

with TestClient(app).websocket_connect("/ws/chat") as ws:
    ws.send_text("hello room")
    print(ws.receive_text())''',
     steps=["Accept, then <b>loop</b>: receive and broadcast.", "Remove clients when they disconnect.",
            "Several servers? Share messages via <b>Redis pub/sub</b>."]),

 picture(M, "Background tasks", "Answer fast, work later",
     "&#127860; A restaurant waiter doesn't cook: he takes the order, gives you a <b>ticket number</b>, and the kitchen works on it. "
     "Your API returns <b>202 Accepted</b> + a job ID; a <b>worker</b> does the slow part.",
     [("POST /reports", "202 Accepted {job_id: 42}"), ("queue (Redis)", "job 42 waits"),
      ("worker (Celery / RQ)", "builds the PDF"), ("GET /jobs/42", "pending &#8594; done + link")]),

 code_out(M, "Background tasks", "202 + polling with a simple job queue", '''
import queue, threading, time, uuid
from fastapi import FastAPI
from fastapi.testclient import TestClient

app, jobs, q = FastAPI(), {}, queue.Queue()

def worker():
    while True:
        job_id = q.get()
        time.sleep(0.2)                         # the slow part
        jobs[job_id] = {"status": "done", "url": f"/files/{job_id}.pdf"}
threading.Thread(target=worker, daemon=True).start()
@app.post("/reports", status_code=202)
def create_report():
    job_id = uuid.uuid4().hex[:6]
    jobs[job_id] = {"status": "pending"}
    q.put(job_id)
    return {"job_id": job_id}
@app.get("/jobs/{job_id}")
def job_status(job_id: str): return jobs[job_id]
c = TestClient(app)
jid = c.post("/reports").json()["job_id"]
print(c.get(f"/jobs/{jid}").json()["status"])
time.sleep(0.4)
print(c.get(f"/jobs/{jid}").json()["status"])''',
     steps=["In production the queue is <b>Redis/RabbitMQ</b> and the worker is <b>Celery</b> or RQ.",
            "Small fire-and-forget jobs: FastAPI <b>BackgroundTasks</b>.", "Jobs must be <b>idempotent</b>: they may run twice."]),

 picture(M, "Caching", "Cache-aside: the most common pattern",
     "&#9889; Check the fast cache first. On a <b>miss</b>, load from the slow DB and store the result with a <b>TTL</b> (expiry). "
     "When the data changes, <b>invalidate</b> the key.",
     [("get(\"product:7\")", "hit? return it (&lt; 1 ms)"), ("miss", "query the DB (50 ms)"),
      ("set(key, value, ex=300)", "store for 5 minutes"), ("on update", "delete(\"product:7\")")]),

 code_out(M, "Caching", "Cache-aside with Redis (fakeredis here)", '''
import json, time
import fakeredis                       # same API as redis.Redis

r = fakeredis.FakeRedis()

def load_product_from_db(pid):
    time.sleep(0.05)                   # a slow query
    return {"id": pid, "name": "Lamp", "price": 49.0}

def get_product(pid):
    key = f"product:{pid}"
    if (cached := r.get(key)) is not None:
        return json.loads(cached), "hit"
    product = load_product_from_db(pid)
    r.set(key, json.dumps(product), ex=300)        # TTL 5 minutes
    return product, "miss"

for _ in range(3):
    t = time.perf_counter()
    _, how = get_product(7)
    print(f"{how:4} {(time.perf_counter() - t) * 1000:5.1f} ms")

r.delete("product:7")                  # after an update
print(get_product(7)[1], "after invalidation")
r.incr("views:7"); r.incr("views:7"); print("views:", int(r.get("views:7")))''',
     steps=["<b>TTL</b> limits how stale data can get.", "Invalidate on writes; \"there are only two hard things...\"",
            "Redis also does counters, rate limits, leaderboards, sessions."]),

 mistake(M, "Caching", "Caching per-user data under a shared key",
     '''
key = "dashboard"            # same for everyone!
if cached := r.get(key):
    return cached            # user B sees user A's data''',
     "A cache key that ignores the <b>user</b> (or language, permissions) leaks private data between users.",
     '''
key = f"dashboard:user:{user.id}:v2"
if cached := r.get(key):
    return cached''',
     "Put <b>everything the result depends on</b> in the key; add a version suffix to invalidate all at once."),

 job(M, "Real-time, tasks, caching", "In production systems", [
     ("Celery task", '''
@shared_task(bind=True, max_retries=3)
def send_invoice(self, order_id): ...'''),
     ("Rate limiting with Redis", '''
n = r.incr(f"rl:{ip}:{minute}")
r.expire(...); if n > 100: raise 429'''),
     ("HTTP caching", '''
Cache-Control: public, max-age=60
ETag + 304 Not Modified'''),
     ("Scheduled jobs", '''
celery beat / cron: nightly reports,
cleanup of expired tokens'''),
 ]),

 interview(M, "How would you design caching for a slow endpoint?",
     ["Measure first: which query or call is slow and how often is it hit?",
      "Use <b>cache-aside</b> with Redis: get &#8594; on miss load and set with a <b>TTL</b>.",
      "Design the <b>key</b> from everything the result depends on (ids, user, language, version).",
      "<b>Invalidate</b> on writes (delete the key) or accept staleness up to the TTL.",
      "Watch for <b>stampedes</b> (many misses at once): locks, early refresh, jittered TTLs."],
     None,
     "\"Where can you cache?\" (browser/CDN via HTTP headers, reverse proxy, app memory (lru_cache), Redis, DB query cache)."),

 interview(M, "When do you use background jobs? WebSockets vs polling?",
     ["Background jobs: anything <b>slow or unreliable</b> that the user doesn't need to wait for: emails, PDFs, image processing, calls to partner APIs.",
      "Return <b>202</b> + a job ID; workers (<b>Celery</b>/RQ) retry with backoff; tasks must be <b>idempotent</b>.",
      "<b>Polling</b> is simple but wasteful and laggy; <b>WebSockets</b> give instant two-way updates but need connection management and scaling (Redis pub/sub).",
      "<b>Server-Sent Events</b> fit one-way live feeds."],
     None,
     "\"What happens if a worker crashes mid-task?\" (with acks_late the message is redelivered, so the task runs again: that's why it must be idempotent)."),

 recap(M, "Module 26 in 5 lines",
     ["WebSockets: an open, two-way connection; broadcast to rooms; Redis pub/sub to scale.",
      "Slow work &#8594; queue + worker; return <b>202</b> and let the client poll or get pushed.",
      "Jobs retry, so make them <b>idempotent</b>.",
      "Cache-aside + <b>TTL</b> + invalidation; keys include everything the result depends on.",
      "Redis: cache, counters, rate limits, queues, sessions."],
     "Run <b>03_caching_with_redis.py</b>, then add a cached <b>GET /products/{id}</b> that invalidates on PATCH."),
]
