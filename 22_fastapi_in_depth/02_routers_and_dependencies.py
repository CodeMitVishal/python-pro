"""Module 22 · Routers and dependencies: structure a real API

APIRouter   -> split endpoints into files/groups, each with a prefix and tags
Depends()   -> FastAPI calls a function for you and passes the result in:
               database sessions, the current user, pagination, settings...
               Dependencies can depend on other dependencies, and tests can
               REPLACE any of them with app.dependency_overrides.

Run it:  python 22_fastapi_in_depth/02_routers_and_dependencies.py
"""
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Path, Query
from pydantic import BaseModel

# --- A fake "database" ---------------------------------------------------------------------
PRODUCTS = [{"id": i, "name": f"Product {i}", "price": 10.0 * i} for i in range(1, 26)]
USERS = {"token-vishal": {"name": "vishal", "role": "admin"},
         "token-raj": {"name": "raj", "role": "customer"}}


# --- Dependencies: small reusable functions --------------------------------------------------
class Page(BaseModel):
    limit: int
    offset: int


def pagination(limit: Annotated[int, Query(ge=1, le=100)] = 10,
               offset: Annotated[int, Query(ge=0)] = 0) -> Page:
    return Page(limit=limit, offset=offset)            # validated query params, reused everywhere


def current_user(authorization: Annotated[str | None, Header()] = None) -> dict:
    token = (authorization or "").removeprefix("Bearer ")
    user = USERS.get(token)
    if user is None:
        raise HTTPException(401, "not logged in", headers={"WWW-Authenticate": "Bearer"})
    return user


def admin_user(user: Annotated[dict, Depends(current_user)]) -> dict:   # a dependency of a dependency
    if user["role"] != "admin":
        raise HTTPException(403, "admins only")
    return user


PageDep = Annotated[Page, Depends(pagination)]
UserDep = Annotated[dict, Depends(current_user)]
AdminDep = Annotated[dict, Depends(admin_user)]

# --- A router: one group of endpoints ---------------------------------------------------------
products = APIRouter(prefix="/products", tags=["products"])


@products.get("")
def list_products(page: PageDep, max_price: float | None = None) -> dict:
    items = [p for p in PRODUCTS if max_price is None or p["price"] <= max_price]
    return {"total": len(items), "items": items[page.offset: page.offset + page.limit]}


@products.get("/{product_id}")
def get_product(product_id: Annotated[int, Path(ge=1)], user: UserDep) -> dict:
    for p in PRODUCTS:
        if p["id"] == product_id:
            return {**p, "viewed_by": user["name"]}
    raise HTTPException(404, "product not found")


@products.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, admin: AdminDep) -> None:
    PRODUCTS[:] = [p for p in PRODUCTS if p["id"] != product_id]


app = FastAPI(title="Shop API")
app.include_router(products, prefix="/api/v1")          # versioned URLs: /api/v1/products


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    c = TestClient(app)
    vishal, raj = {"Authorization": "Bearer token-vishal"}, {"Authorization": "Bearer token-raj"}
    r = c.get("/api/v1/products", params={"limit": 3, "offset": 5})
    print("page:      ", r.status_code, [p["id"] for p in r.json()["items"]], "of", r.json()["total"])
    print("bad limit: ", c.get("/api/v1/products?limit=500").status_code)            # 422
    print("filter:    ", c.get("/api/v1/products?max_price=30").json()["total"])      # 3
    print("no token:  ", c.get("/api/v1/products/1").status_code)                     # 401
    print("with token:", c.get("/api/v1/products/1", headers=raj).json()["viewed_by"])
    print("raj delete:", c.delete("/api/v1/products/1", headers=raj).status_code)     # 403
    print("admin del: ", c.delete("/api/v1/products/1", headers=vishal).status_code)  # 204

    # Tests can swap a dependency for a fake:
    app.dependency_overrides[current_user] = lambda: {"name": "test-bot", "role": "admin"}
    print("override:  ", c.get("/api/v1/products/2").json()["viewed_by"])             # test-bot
    app.dependency_overrides.clear()
