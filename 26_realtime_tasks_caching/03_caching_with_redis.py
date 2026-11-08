"""Module 26 · Caching with Redis: the cache-aside pattern

Redis is an in-memory key-value store: microseconds to read, shared by all your
server processes, with automatic expiry (TTL). Used for caches, sessions, rate
limits, queues and leaderboards.

CACHE-ASIDE:
  read:   look in the cache -> HIT: return it
                            -> MISS: load from the DB, store in the cache with a TTL
  write:  update the DB, then DELETE the cache key (so nobody reads stale data)

This demo uses `fakeredis`: the same API as the real `redis` client, but in
memory, so no server is needed. In production:
    r = redis.Redis.from_url(os.environ["REDIS_URL"])     # e.g. Azure Cache for Redis

Run it:  pip install fakeredis
         python 26_realtime_tasks_caching/03_caching_with_redis.py
"""
import json
import time

import fakeredis

r = fakeredis.FakeRedis(decode_responses=True)
DB = {1: {"id": 1, "name": "Laptop", "price": 899.0}}
stats = {"hits": 0, "misses": 0, "db_reads": 0}


def slow_db_get(product_id: int) -> dict:
    stats["db_reads"] += 1
    time.sleep(0.2)                                  # pretend: a slow query
    return dict(DB[product_id])


def get_product(product_id: int) -> dict:
    key = f"product:{product_id}"
    cached = r.get(key)
    if cached is not None:                           # HIT
        stats["hits"] += 1
        return json.loads(cached)
    stats["misses"] += 1                             # MISS
    product = slow_db_get(product_id)
    r.set(key, json.dumps(product), ex=60)           # expires after 60 seconds
    return product


def update_price(product_id: int, price: float) -> None:
    DB[product_id]["price"] = price                  # 1. write to the database
    r.delete(f"product:{product_id}")                # 2. invalidate the cache


for label in ["1st read", "2nd read", "3rd read"]:
    start = time.perf_counter()
    p = get_product(1)
    print(f"{label}: {p['price']:>6} EUR in {(time.perf_counter() - start) * 1000:6.1f} ms")

update_price(1, 799.0)
print("after update:", get_product(1)["price"], "EUR  <- fresh, not stale")
print("stats:", stats, "| TTL left:", r.ttl("product:1"), "s")

# --- Other everyday Redis tools ------------------------------------------------------------
r.incr("page_views:home")                            # atomic counters
r.incr("page_views:home")
print("page views:", r.get("page_views:home"))

r.zadd("leaderboard", {"vishal": 120, "raj": 95, "li": 140})   # sorted sets
print("top 2:", r.zrevrange("leaderboard", 0, 1, withscores=True))

# The two hard problems: cache invalidation (when is data stale?) and choosing TTLs.
# Cache data that is READ often and CHANGES rarely. Never cache per-user secrets
# under shared keys.
