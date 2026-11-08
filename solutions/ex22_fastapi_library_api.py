"""Solution · Exercise 22: A library API with FastAPI

Run it:  python solutions/ex22_fastapi_library_api.py
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


class BookIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str
    year: int = Field(ge=1450, le=2100)


def require_api_key(x_api_key: Annotated[str | None, Header()] = None) -> None:
    # The X-API-Key header arrives as the x_api_key parameter (dashes -> underscores)
    if x_api_key != "secret":               # real apps: compare with secrets.compare_digest
        raise HTTPException(401, "invalid API key")


router = APIRouter(prefix="/books", tags=["books"])


@router.get("")
def list_books(author: str | None = None,
               limit: Annotated[int, Query(ge=1, le=50)] = 10,
               offset: Annotated[int, Query(ge=0)] = 0) -> dict:
    items = [b for b in BOOKS if author is None or b["author"].lower() == author.lower()]
    return {"total": len(items), "items": items[offset: offset + limit]}


@router.post("", status_code=201, dependencies=[Depends(require_api_key)])
def create_book(book: BookIn) -> dict:
    new = {"id": max(b["id"] for b in BOOKS) + 1, **book.model_dump()}
    BOOKS.append(new)
    return new


@router.get("/{book_id}")
def get_book(book_id: int) -> dict:
    for b in BOOKS:
        if b["id"] == book_id:
            return b
    raise BookNotFound(book_id)


app = FastAPI()
app.include_router(router, prefix="/api/v1")


@app.exception_handler(BookNotFound)
async def book_not_found(request: Request, exc: BookNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"error": "book_not_found", "id": exc.book_id})


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    c = TestClient(app)
    r = c.get("/api/v1/books", params={"author": "MARTIN"})
    assert r.status_code == 200 and r.json()["total"] == 2
    assert len(c.get("/api/v1/books?limit=1&offset=1").json()["items"]) == 1
    assert c.get("/api/v1/books?limit=0").status_code == 422
    assert c.get("/api/v1/books/2").json()["title"] == "Clean Code"
    assert c.get("/api/v1/books/9").json() == {"error": "book_not_found", "id": 9}
    assert c.get("/api/v1/books/9").status_code == 404
    new = {"title": "Python Tricks", "author": "Bader", "year": 2017}
    assert c.post("/api/v1/books", json=new).status_code == 401
    assert c.post("/api/v1/books", json=new, headers={"X-API-Key": "nope"}).status_code == 401
    r = c.post("/api/v1/books", json=new, headers={"X-API-Key": "secret"})
    assert r.status_code == 201 and r.json()["id"] == 4
    assert c.post("/api/v1/books", json={**new, "year": 1200},
                  headers={"X-API-Key": "secret"}).status_code == 422
    print("All checks passed!")
