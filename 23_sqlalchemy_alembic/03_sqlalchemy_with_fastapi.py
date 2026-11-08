"""Module 23 · SQLAlchemy inside FastAPI: one session per request

The pattern every production FastAPI + SQL app uses:
  - a dependency opens a Session for each request and always closes it
  - endpoints commit their own changes
  - database errors (like a UNIQUE violation) become clean HTTP errors
  - pydantic models (from_attributes=True) turn ORM objects into JSON

Run it:  python 23_sqlalchemy_alembic/03_sqlalchemy_with_fastapi.py
"""
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from models import Author, Base

# StaticPool: one shared in-memory DB for the demo. Real apps: "postgresql+psycopg://..."
engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db                     # the endpoint runs here
    finally:
        db.close()                   # always returned to the pool, even on errors


DB = Annotated[Session, Depends(get_db)]


class AuthorIn(BaseModel):
    name: str
    country: str | None = None


class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)   # read attributes from ORM objects
    id: int
    name: str
    country: str | None


app = FastAPI()


@app.post("/authors", status_code=201)
def create_author(data: AuthorIn, db: DB) -> AuthorOut:
    author = Author(**data.model_dump())
    db.add(author)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()                # leave the session usable
        raise HTTPException(409, f"author {data.name!r} already exists")
    db.refresh(author)               # load the generated id
    return AuthorOut.model_validate(author)


@app.get("/authors")
def list_authors(db: DB) -> list[AuthorOut]:
    return [AuthorOut.model_validate(a) for a in db.scalars(select(Author).order_by(Author.name))]


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")
    from fastapi.testclient import TestClient

    c = TestClient(app)
    print(c.post("/authors", json={"name": "Vishal Singh", "country": "IN"}).json())
    print(c.post("/authors", json={"name": "Vishal Singh"}).status_code, "<- duplicate -> 409")
    print(c.post("/authors", json={"name": "Raj"}).status_code)
    print(c.get("/authors").json())
