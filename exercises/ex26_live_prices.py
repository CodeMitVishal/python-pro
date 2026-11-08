"""Exercise 26 · Live prices: caching + WebSocket notifications

Build a small price service:

  GET  /products/{id}        -> the product as JSON
                                cache-aside with Redis (fakeredis): key "product:{id}", TTL 30 s
                                response header X-Cache: "MISS" (from the DB) or "HIT"
                                404 if the product doesn't exist
  PUT  /products/{id}?price=799.0
                             -> update DB, DELETE the cache key, then push
                                {"id": 1, "price": 799.0} to EVERY client connected to /ws/prices
  WS   /ws/prices            -> clients connect here and just listen

Run it to check your work:
    pip install fastapi fakeredis httpx
    python exercises/ex26_live_prices.py

Stuck? Compare with solutions/ex26_live_prices.py
"""
import json

import fakeredis
from fastapi import FastAPI, HTTPException, Response, WebSocket, WebSocketDisconnect

app = FastAPI()
cache = fakeredis.FakeRedis(decode_responses=True)
DB = {1: {"id": 1, "name": "Laptop", "price": 899.0}, 2: {"id": 2, "name": "Mouse", "price": 19.9}}
DB_READS = {"count": 0}            # increase this every time you read from DB

# TODO: the three endpoints (and a way to remember the connected WebSockets)


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    c = TestClient(app)
    r1, r2 = c.get("/products/1"), c.get("/products/1")
    assert r1.status_code == 200 and r1.json()["price"] == 899.0, r1.text
    assert (r1.headers.get("X-Cache"), r2.headers.get("X-Cache")) == ("MISS", "HIT")
    assert DB_READS["count"] == 1, "the 2nd read must come from the cache"
    assert 0 < cache.ttl("product:1") <= 30, "set a 30 s TTL"
    assert c.get("/products/9").status_code == 404

    with c.websocket_connect("/ws/prices") as ws:
        assert c.put("/products/1?price=799.0").status_code == 200
        assert json.loads(ws.receive_text()) == {"id": 1, "price": 799.0}
    r3 = c.get("/products/1")
    assert r3.headers["X-Cache"] == "MISS" and r3.json()["price"] == 799.0, "invalidate on update"
    print("All checks passed!")
