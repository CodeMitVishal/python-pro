"""Solution · Exercise 21: A Flask guestbook

Run it:  python solutions/ex21_flask_guestbook.py
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


@app.get("/")
def index():
    return render_template_string(PAGE, entries=list(reversed(ENTRIES)))   # newest first


@app.post("/sign")
def sign():
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()
    if not name or not message:
        flash("Name and message are both required.")
    elif len(message) > 200:
        flash("Messages can be at most 200 characters.")
    else:
        ENTRIES.append({"name": name, "message": message})
        flash("Thanks for signing!")
    return redirect(url_for("index"))          # POST -> redirect -> GET, valid or not


@app.get("/api/entries")
def api_entries():
    wanted = request.args.get("name", "").lower()
    entries = [e for e in reversed(ENTRIES) if not wanted or e["name"].lower() == wanted]
    return entries                             # Flask turns a list into JSON


if __name__ == "__main__":
    c = app.test_client()
    assert c.get("/").status_code == 200
    r = c.post("/sign", data={"name": "Vishal", "message": "Great course!"})
    assert r.status_code == 302 and r.headers["Location"] == "/"
    c.post("/sign", data={"name": "Raj", "message": "<script>alert(1)</script>Hi"})
    page = c.get("/").get_data(as_text=True)
    assert "Thanks for signing!" in page
    assert "&lt;script&gt;" in page and "<script>alert" not in page
    assert page.index("Raj") < page.index("Vishal")
    assert c.post("/sign", data={"name": "", "message": "x"}).status_code == 302
    assert c.post("/sign", data={"name": "Li", "message": "x" * 201}).status_code == 302
    assert "Guestbook (2)" in c.get("/").get_data(as_text=True)
    assert c.get("/api/entries").get_json()[0]["name"] == "Raj"
    assert [e["name"] for e in c.get("/api/entries?name=RAJ").get_json()] == ["Raj"]
    print("All checks passed!")
