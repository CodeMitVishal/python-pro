"""Solution · Exercise 26: Live prices

Run it:  python solutions/ex26_live_prices.py
"""
import json

import fakeredis
from fastapi import FastAPI, HTTPException, Response, WebSocket, WebSocketDisconnect

app = FastAPI()
cache = fakeredis.FakeRedis(decode_responses=True)
DB = {1: {"id": 1, "name": "Laptop", "price": 899.0}, 2: {"id": 2, "name": "Mouse", "price": 19.9}}
DB_READS = {"count": 0}
LISTENERS: set[WebSocket] = set()


@app.get("/products/{product_id}")
def get_product(product_id: int, response: Response) -> dict:
    key = f"product:{product_id}"
    if (cached := cache.get(key)) is not None:
        response.headers["X-Cache"] = "HIT"
        return json.loads(cached)
    if product_id not in DB:
        raise HTTPException(404, "product not found")
    DB_READS["count"] += 1
    product = DB[product_id]
    cache.set(key, json.dumps(product), ex=30)
    response.headers["X-Cache"] = "MISS"
    return product


@app.put("/products/{product_id}")
async def update_price(product_id: int, price: float) -> dict:
    if product_id not in DB:
        raise HTTPException(404, "product not found")
    DB[product_id]["price"] = price                       # 1. the database
    cache.delete(f"product:{product_id}")                 # 2. invalidate
    message = json.dumps({"id": product_id, "price": price})
    for ws in list(LISTENERS):                             # 3. push to everyone listening
        try:
            await ws.send_text(message)
        except Exception:
            LISTENERS.discard(ws)                          # drop dead connections
    return DB[product_id]


@app.websocket("/ws/prices")
async def prices(ws: WebSocket):
    await ws.accept()
    LISTENERS.add(ws)
    try:
        while True:
            await ws.receive_text()                       # keep the connection open
    except WebSocketDisconnect:
        LISTENERS.discard(ws)


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    c = TestClient(app)
    r1, r2 = c.get("/products/1"), c.get("/products/1")
    assert r1.status_code == 200 and r1.json()["price"] == 899.0
    assert (r1.headers.get("X-Cache"), r2.headers.get("X-Cache")) == ("MISS", "HIT")
    assert DB_READS["count"] == 1
    assert 0 < cache.ttl("product:1") <= 30
    assert c.get("/products/9").status_code == 404

    with c.websocket_connect("/ws/prices") as ws:
        assert c.put("/products/1?price=799.0").status_code == 200
        assert json.loads(ws.receive_text()) == {"id": 1, "price": 799.0}
    r3 = c.get("/products/1")
    assert r3.headers["X-Cache"] == "MISS" and r3.json()["price"] == 799.0
    print("All checks passed!")
