"""Module 22 · Errors, middleware and CORS

EXCEPTION HANDLERS -> turn your own exceptions into clean HTTP responses, in one place
MIDDLEWARE         -> code that runs around EVERY request: timing, request IDs, logging
CORS               -> lets a website on another origin (e.g. a React app on :3000)
                      call your API from the browser

TEACHING NOTES
  Why it matters  Inconsistent error responses and missing request IDs make APIs painful to use
                  and debug.
  Picture it      Middleware is a security gate every request walks through, in and out.
  Watch out       CORS allow_origins=['*'] with credentials is unsafe and doesn't even work;
                  list exact origins.
  In real jobs    Global exception handlers, request ID and timing middleware, CORS for the
                  frontend.
  Interview       Q: What is CORS?
                  A: A browser rule: a page may read responses from another origin only if that
                     API allows it via CORS headers.

Run it:  python 22_fastapi_in_depth/03_errors_middleware_cors.py
"""
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()


# --- 1. Domain errors -> HTTP responses -------------------------------------------------------
class OutOfStock(Exception):
    def __init__(self, item: str, left: int):
        self.item, self.left = item, left


@app.exception_handler(OutOfStock)
async def out_of_stock_handler(request: Request, exc: OutOfStock) -> JSONResponse:
    return JSONResponse(status_code=409,                  # 409 Conflict
                        content={"error": "out_of_stock", "item": exc.item, "left": exc.left})


@app.exception_handler(Exception)                        # last resort: never leak a traceback
async def unexpected(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"error": "internal_error",
                                                  "request_id": request.state.request_id})


@app.post("/orders/{item}")
def order(item: str, qty: int = 1):
    if item == "laptop" and qty > 2:
        raise OutOfStock(item, left=2)                    # business code stays HTTP-free
    if item == "bug":
        raise RuntimeError("database password=hunter2")   # must NOT reach the client
    return {"ordered": qty, "item": item}


# --- 2. Middleware: runs before and after every request -----------------------------------------
@app.middleware("http")
async def add_request_id_and_timing(request: Request, call_next):
    request.state.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
    start = time.perf_counter()
    response = await call_next(request)                   # the actual endpoint runs here
    response.headers["X-Request-ID"] = request.state.request_id
    response.headers["X-Process-Time-ms"] = f"{(time.perf_counter() - start) * 1000:.1f}"
    return response


# --- 3. CORS: which other websites may call this API from a browser --------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://codemitvishal.dev"],   # never "*" with cookies
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
)


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    c = TestClient(app, raise_server_exceptions=False)
    r = c.post("/orders/laptop?qty=5")
    print("domain error:", r.status_code, r.json())
    r = c.post("/orders/bug", headers={"X-Request-ID": "abc123"})
    print("crash:       ", r.status_code, r.json(), "<- no password leaked")
    r = c.post("/orders/pen?qty=3")
    print("ok:          ", r.status_code, r.json(), "| id:", r.headers["X-Request-ID"],
          "| time header:", "X-Process-Time-ms" in r.headers)

    preflight = c.options("/orders/pen", headers={"Origin": "http://localhost:3000",
                                                   "Access-Control-Request-Method": "POST"})
    print("CORS allowed:", preflight.headers.get("access-control-allow-origin"))
    evil = c.options("/orders/pen", headers={"Origin": "https://evil.example",
                                             "Access-Control-Request-Method": "POST"})
    print("CORS blocked:", evil.status_code, evil.headers.get("access-control-allow-origin"))
