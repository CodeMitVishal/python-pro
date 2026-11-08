"""Module 21 · Flask basics: routes, URL parameters, JSON and errors

  pip install flask

Flask maps URLs to Python functions. It's small, explicit and everywhere,
which makes it the best framework to SEE how a web app works.

TEACHING NOTES
  Why it matters  Small services and internal tools need a web app in minutes, not days.
  Picture it      A route is a doorbell: a URL rings, and the function behind that door answers.
  Watch out       Return the right status code (201, 404), not 200 with an error message in the
                  body.
  In real jobs    Health checks, webhooks, internal dashboards, small JSON APIs.
  Interview       Q: Flask vs Django vs FastAPI?
                  A: Flask: minimal and flexible. Django: batteries included. FastAPI: typed,
                     async APIs with auto docs.

Run the self-test:   python 21_web_flask/02_flask_basics.py
Run a real server:   flask --app 21_web_flask/02_flask_basics.py run --debug
                     then open http://127.0.0.1:5000/books
"""
from flask import Flask, abort, jsonify, request

app = Flask(__name__)

BOOKS = {
    1: {"id": 1, "title": "Fluent Python", "year": 2022},
    2: {"id": 2, "title": "Clean Code", "year": 2008},
}


@app.get("/")                                    # GET /
def home():
    return "<h1>Book API</h1><p>Try <a href='/books'>/books</a></p>"   # a str becomes HTML


@app.get("/books")                               # GET /books?after=2010
def list_books():
    after = request.args.get("after", type=int)   # query string, converted to int
    books = [b for b in BOOKS.values() if after is None or b["year"] > after]
    return jsonify(books)                        # a list -> JSON response


@app.get("/books/<int:book_id>")                 # path parameter, converted to int
def get_book(book_id):
    book = BOOKS.get(book_id)
    if book is None:
        abort(404, description=f"book {book_id} not found")
    return book                                  # a dict is turned into JSON automatically


@app.post("/books")                              # POST /books  with a JSON body
def create_book():
    data = request.get_json(silent=True) or {}
    if not data.get("title"):
        return {"error": "title is required"}, 400    # (body, status code)
    book_id = max(BOOKS) + 1
    BOOKS[book_id] = {"id": book_id, "title": data["title"], "year": data.get("year")}
    return BOOKS[book_id], 201, {"Location": f"/books/{book_id}"}   # body, status, headers


@app.errorhandler(404)                           # one place to format every 404 as JSON
def not_found(err):
    return {"error": err.description}, 404


if __name__ == "__main__":
    # test_client() sends requests straight to the app: no server, no network
    client = app.test_client()
    for method, url, body in [
        ("GET", "/books", None),
        ("GET", "/books?after=2010", None),
        ("GET", "/books/2", None),
        ("GET", "/books/99", None),
        ("POST", "/books", {"title": "Python Tricks", "year": 2017}),
        ("POST", "/books", {}),
    ]:
        resp = client.open(url, method=method, json=body)
        print(f"{method:<4} {url:<18} -> {resp.status_code} {resp.get_data(as_text=True).strip()}")
