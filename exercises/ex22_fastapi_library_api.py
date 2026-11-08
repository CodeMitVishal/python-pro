"""Exercise 22 · A library API with FastAPI

Build a books API under the prefix /api/v1/books (use an APIRouter):

  GET    /api/v1/books?author=...&limit=..&offset=..
         -> {"total": N, "items": [...]}; limit 1-50 (default 10), offset >= 0
            author filter is case-insensitive
  POST   /api/v1/books            (header X-API-Key: secret)
         body: {"title": str (1-100 chars), "author": str, "year": int (1450-2100)}
         -> 201 with the created book, including a new "id"
         -> 401 if the X-API-Key header is missing or wrong (use a dependency)
  GET    /api/v1/books/{id}       -> the book, or 404 {"error": "book_not_found", "id": id}
                                     raise BookNotFound and handle it with an exception handler

Run it to check your work:
    pip install fastapi httpx
    python exercises/ex22_fastapi_library_api.py

Stuck? Compare with solutions/ex22_fastapi_library_api.py
"""
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

BOOKS: list[dict] = [
    {"id": 1, "title": "Fluent Python", "author": "Ramalho", "year": 2022},
    {"id": 2, "title": "Clean Code", "author": "Martin", "year": 2008},
    {"id": 3, "title": "Clean Architecture", "author": "Martin", "year": 2017},
]


class BookNotFound(Exception):
    def __init__(self, book_id: int):
        self.book_id = book_id


app = FastAPI()

# TODO: BookIn model, an API-key dependency, the router with 3 endpoints,
#       include it with prefix /api/v1, and an exception handler for BookNotFound


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    c = TestClient(app)
    r = c.get("/api/v1/books", params={"author": "MARTIN"})
    assert r.status_code == 200 and r.json()["total"] == 2, r.text
    assert len(c.get("/api/v1/books?limit=1&offset=1").json()["items"]) == 1
    assert c.get("/api/v1/books?limit=0").status_code == 422
    assert c.get("/api/v1/books/2").json()["title"] == "Clean Code"
    assert c.get("/api/v1/books/9").json() == {"error": "book_not_found", "id": 9}
    assert c.get("/api/v1/books/9").status_code == 404
    new = {"title": "Python Tricks", "author": "Bader", "year": 2017}
    assert c.post("/api/v1/books", json=new).status_code == 401
    assert c.post("/api/v1/books", json=new, headers={"X-API-Key": "nope"}).status_code == 401
    r = c.post("/api/v1/books", json=new, headers={"X-API-Key": "secret"})
    assert r.status_code == 201 and r.json()["id"] == 4, r.text
    assert c.post("/api/v1/books", json={**new, "year": 1200},
                  headers={"X-API-Key": "secret"}).status_code == 422
    print("All checks passed!")
