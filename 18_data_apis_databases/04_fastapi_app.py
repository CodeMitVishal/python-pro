"""Module 18 · Build your own REST API with FastAPI + SQLite

  pip install fastapi uvicorn httpx

FastAPI turns type-hinted Python functions into a web API, with automatic
validation (pydantic) and interactive docs at /docs.

  GET    /todos          list all todos
  POST   /todos          create one         (JSON body: {"title": "..."})
  GET    /todos/{id}     read one           (404 if missing)
  PATCH  /todos/{id}     mark done
  DELETE /todos/{id}     delete one

Run the self-test:   python 18_data_apis_databases/04_fastapi_app.py
Run a real server:   cd 18_data_apis_databases
                     uvicorn 04_fastapi_app:app --reload
                     then open http://127.0.0.1:8000/docs in your browser
"""
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Todo API", version="1.0")
db = sqlite3.connect(":memory:", check_same_thread=False)   # a file name keeps data between runs
db.row_factory = sqlite3.Row
db.execute("CREATE TABLE todos (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER DEFAULT 0)")


class TodoIn(BaseModel):                     # what clients SEND (validated automatically)
    title: str = Field(min_length=1, max_length=100)


class Todo(BaseModel):                       # what we SEND BACK
    id: int
    title: str
    done: bool


def to_todo(row: sqlite3.Row) -> Todo:
    return Todo(id=row["id"], title=row["title"], done=bool(row["done"]))


def get_row(todo_id: int) -> sqlite3.Row:
    row = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="todo not found")
    return row


@app.get("/todos")
def list_todos() -> list[Todo]:
    return [to_todo(r) for r in db.execute("SELECT * FROM todos ORDER BY id")]


@app.post("/todos", status_code=201)         # 201 Created
def create_todo(todo: TodoIn) -> Todo:
    with db:
        cur = db.execute("INSERT INTO todos (title) VALUES (?)", (todo.title,))
    return to_todo(get_row(cur.lastrowid))


@app.get("/todos/{todo_id}")
def read_todo(todo_id: int) -> Todo:         # the {todo_id} in the URL is converted to int
    return to_todo(get_row(todo_id))


@app.patch("/todos/{todo_id}")
def complete_todo(todo_id: int) -> Todo:
    get_row(todo_id)
    with db:
        db.execute("UPDATE todos SET done = 1 WHERE id = ?", (todo_id,))
    return to_todo(get_row(todo_id))


@app.delete("/todos/{todo_id}", status_code=204)   # 204 No Content
def delete_todo(todo_id: int) -> None:
    get_row(todo_id)
    with db:
        db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))


if __name__ == "__main__":
    # TestClient calls the API in-process: no server, no network. Perfect for tests.
    import warnings
    warnings.filterwarnings("ignore", message=".*httpx.*")   # quiet a library notice
    from fastapi.testclient import TestClient

    client = TestClient(app)
    for method, url, body in [
        ("POST", "/todos", {"title": "Record Module 18"}),
        ("POST", "/todos", {"title": "Edit the video"}),
        ("POST", "/todos", {"title": ""}),          # invalid: too short -> 422
        ("PATCH", "/todos/1", None),
        ("GET", "/todos/99", None),                 # missing -> 404
        ("DELETE", "/todos/2", None),
        ("GET", "/todos", None),
    ]:
        r = client.request(method, url, json=body)
        shown = r.text if len(r.text) < 90 else r.text[:87] + "..."
        print(f"{method:<6} {url:<10} -> {r.status_code}  {shown}")
