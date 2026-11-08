"""Module 21 · Server-rendered pages: Jinja2 templates, forms and sessions

  templates/base.html  -> the shared layout       ({% block %})
  templates/shop.html  -> one page that extends it ({% extends %}, loops, filters)
  static/style.css     -> files served as-is

Forms follow the POST -> REDIRECT -> GET pattern: after a successful POST we
redirect, so refreshing the page doesn't submit the form twice.

The SESSION is a signed cookie: the browser stores it, but can't change it
without the secret key.

Run the self-test:   python 21_web_flask/03_templates_forms_sessions.py
Run a real server:   flask --app 21_web_flask/03_templates_forms_sessions.py run --debug
"""
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"     # in production: from an environment variable!

BOOKS = [{"title": "fluent python", "price": 39.9}, {"title": "python tricks", "price": 19.5}]


@app.get("/")
def shop():
    session["visits"] = session.get("visits", 0) + 1          # remembered per browser
    return render_template(
        "shop.html",
        books=BOOKS,
        user=session.get("user"),
        review="<script>alert('hacked')</script> Great book!",   # untrusted input
    )


@app.post("/books")
def add_book():
    title = request.form.get("title", "").strip()             # form fields, not JSON
    try:
        price = float(request.form.get("price", ""))
    except ValueError:
        price = None
    if not title or price is None or price <= 0:
        flash("Please enter a title and a positive price.")
        return redirect(url_for("shop"))                         # 302 -> back to the page
    BOOKS.append({"title": title, "price": price})
    flash(f"Added {title!r}.")
    return redirect(url_for("shop"))


@app.get("/login/<name>")
def login(name):
    session["user"] = name                                      # signed, so it can't be forged
    return redirect(url_for("shop"))


if __name__ == "__main__":
    client = app.test_client()                                  # keeps cookies between requests

    html = client.get("/").get_data(as_text=True)
    print("title tag:   ", html[html.index("<title>"):html.index("</title>") + 8])
    print("XSS escaped: ", "&lt;script&gt;" in html and "<script>alert" not in html)

    r = client.post("/books", data={"title": "clean code", "price": "abc"})
    print("bad form ->  ", r.status_code, "redirect to", r.headers["Location"])
    page = client.get("/").get_data(as_text=True)
    print("flash shown: ", "positive price" in page)

    client.post("/books", data={"title": "clean code", "price": "29.99"})
    page = client.get("/").get_data(as_text=True)
    print("book listed: ", "Clean Code: 29.99 EUR" in page)

    client.get("/login/Vishal")
    page = client.get("/").get_data(as_text=True)
    print("logged in:   ", "Hello, Vishal!" in page)
    with client.session_transaction() as s:
        print("visits:      ", s["visits"])
