"""Exercise 21 · A Flask guestbook (HTML pages + a JSON API)

Build a guestbook with these routes:

  GET  /              -> an HTML page listing every entry (newest first), using the
                         PAGE template below with render_template_string
  POST /sign          -> form fields `name` and `message`
                         - both required, message max 200 characters
                         - invalid: flash an error, redirect to /
                         - valid: save it, flash "Thanks for signing!", redirect to /
  GET  /api/entries   -> the entries as JSON: [{"name": ..., "message": ...}, ...]
  GET  /api/entries?name=raj -> only entries by that name (case-insensitive)

Messages are untrusted: a <script> in a message must NOT run (Jinja escaping
does this for you, as long as you don't use |safe).

Run it to check your work:
    pip install flask
    python exercises/ex21_flask_guestbook.py

Stuck? Compare with solutions/ex21_flask_guestbook.py
"""
from flask import Flask, flash, redirect, render_template_string, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only"
ENTRIES: list[dict] = []

PAGE = """
<h1>Guestbook ({{ entries|length }})</h1>
{% for m in get_flashed_messages() %}<p class="flash">{{ m }}</p>{% endfor %}
<ul>{% for e in entries %}<li><b>{{ e.name }}</b>: {{ e.message }}</li>{% endfor %}</ul>
<form method="post" action="/sign"><input name="name"><input name="message"><button>Sign</button></form>
"""

# TODO: the four routes


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    c = app.test_client()
    assert c.get("/").status_code == 200, "GET / must show the page"
    r = c.post("/sign", data={"name": "Vishal", "message": "Great course!"})
    assert r.status_code == 302 and r.headers["Location"] == "/", "redirect to / after POST"
    c.post("/sign", data={"name": "Raj", "message": "<script>alert(1)</script>Hi"})
    page = c.get("/").get_data(as_text=True)
    assert "Thanks for signing!" in page, "flash a thank-you message"
    assert "&lt;script&gt;" in page and "<script>alert" not in page, "escape user input"
    assert page.index("Raj") < page.index("Vishal"), "newest entry first"
    assert c.post("/sign", data={"name": "", "message": "x"}).status_code == 302
    assert c.post("/sign", data={"name": "Li", "message": "x" * 201}).status_code == 302
    assert "Guestbook (2)" in c.get("/").get_data(as_text=True), "invalid entries must not be saved"
    assert c.get("/api/entries").get_json()[0]["name"] == "Raj"
    assert [e["name"] for e in c.get("/api/entries?name=RAJ").get_json()] == ["Raj"]
    print("All checks passed!")
