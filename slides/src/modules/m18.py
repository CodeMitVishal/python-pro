"""Slides · Module 18 · Data, APIs & databases"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 18 · Data, APIs &amp; databases"
SLIDES = [
 cover("18", "Data, APIs &amp; databases", "Read files, call web APIs, store data in SQL, and serve your own REST API.",
       [("Files, CSV &amp; JSON", "01_files_csv_json.py"), ("Calling web APIs", "02_http_requests.py"),
        ("SQL with sqlite3", "03_sqlite.py"), ("Your own REST API", "04_fastapi_app.py"),
        ("Dates &amp; time zones", "05_dates_and_timezones.py"), ("pickle vs JSON", "06_pickle_vs_json.py"),
        ("Text &amp; bytes", "07_text_and_bytes.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Data", "Every backend job is moving data around",
     "A typical ticket: <b>\"Import the partner's CSV every night, enrich it from their API, save it in our database, and expose it to the frontend.\"</b>",
     "Four skills cover it: <b>files</b> (CSV/JSON), <b>HTTP clients</b>, <b>SQL</b>, and a <b>REST API</b>. This module does all four."),

 code_out(M, "Files", "CSV and JSON the professional way", '''
import csv, json
from pathlib import Path

orders = [{"id": 1, "item": "lamp", "price": 49.0},
          {"id": 2, "item": "cable", "price": 9.5}]

path = Path("orders.csv")
with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "item", "price"])
    writer.writeheader()
    writer.writerows(orders)

with path.open(encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print(rows[0])                          # CSV gives you STRINGS
print(json.dumps(orders[0], indent=None))
print(sum(float(r["price"]) for r in rows))''',
     steps=["<b>pathlib.Path</b> instead of string paths.", "Always pass <b>encoding=\"utf-8\"</b> (and <b>newline=\"\"</b> for CSV).",
            "CSV values are strings: convert them yourself."]),

 picture(M, "HTTP", "What happens when you call an API",
     "&#128238; HTTP is like sending a <b>letter with a form</b>: a method (what to do), an address (URL), headers (envelope info) "
     "and maybe a body. The reply has a <b>status code</b> and a body, usually JSON.",
     [("request", "GET /orders/7  Authorization: Bearer ..."), ("server", "checks, reads the DB"),
      ("response", "200 OK  {\"id\": 7, \"total\": 49.0}"), ("your code", "check status, parse JSON")]),

 trace(M, "HTTP", "Methods and status codes to know by heart", ["Method", "Means", "Status code", "Means"],
       [["<b>GET</b>", "read (safe, no changes)", "<b>200</b> OK / <b>201</b> Created", "it worked / new resource"],
        ["<b>POST</b>", "create", "<b>204</b> No Content", "worked, nothing to return"],
        ["<b>PUT</b>", "replace (idempotent)", "<b>400</b> / <b>422</b>", "bad input / validation failed"],
        ["<b>PATCH</b>", "change some fields", "<b>401</b> / <b>403</b>", "not logged in / not allowed"],
        ["<b>DELETE</b>", "remove (idempotent)", "<b>404</b> / <b>409</b>", "not found / conflict"],
        ["", "", "<b>429</b> / <b>500</b> / <b>503</b>", "rate limited / our bug / overloaded"]],
       "<b>Idempotent</b> = doing it twice has the same effect as once. Retries are safe only for idempotent calls."),

 mistake(M, "HTTP clients", "The fragile API call",
     '''
import requests
r = requests.get(url)          # waits forever
data = r.json()                # even on a 500''',
     "No timeout: one slow partner freezes your worker. No status check: you parse an error page as data.",
     '''
r = requests.get(url, params={"page": 2},
                 timeout=(3, 10))     # connect, read
r.raise_for_status()                  # 4xx/5xx -> error
data = r.json()''',
     "Always: a <b>timeout</b>, <b>raise_for_status()</b>, a <b>Session</b> for many calls, and retries with backoff."),

 code_out(M, "SQL", "SQL with sqlite3: tables, joins, totals", '''
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE users  (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INT, total REAL);
INSERT INTO users  VALUES (1, 'vishal'), (2, 'li'), (3, 'sam');
INSERT INTO orders VALUES (1, 1, 49), (2, 1, 20), (3, 2, 9.5);
""")
rows = db.execute("""
    SELECT u.name, COUNT(o.id) AS n, COALESCE(SUM(o.total), 0)
    FROM users u LEFT JOIN orders o ON o.user_id = u.id
    GROUP BY u.id ORDER BY 3 DESC
""").fetchall()
for r in rows:
    print(r)''',
     steps=["<b>JOIN</b> connects tables by a key.", "<b>LEFT JOIN</b> keeps users without orders (sam).",
            "<b>GROUP BY</b> + COUNT/SUM = one row per user."]),

 mistake(M, "SQL", "SQL injection",
     '''
name = request.args["name"]
db.execute(f"SELECT * FROM users "
           f"WHERE name = '{name}'")
# name = "x' OR '1'='1"  -> every user!''',
     "User input becomes part of the SQL. An attacker can read or delete <b>everything</b>. Still in the OWASP Top 10.",
     '''
db.execute("SELECT * FROM users WHERE name = ?",
           (name,))        # a PARAMETER

# ORMs do this for you:
User.objects.filter(name=name)''',
     "Never build SQL with f-strings. Use <b>placeholders</b> (<b>?</b> or <b>%s</b>) or an ORM."),

 code_out(M, "SQL", "Transactions: all or nothing", '''
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE acc (name TEXT, bal INT CHECK (bal >= 0))")
db.executemany("INSERT INTO acc VALUES (?, ?)", [("vishal", 100), ("li", 0)])
db.commit()

def transfer(src, dst, amount):
    try:
        with db:                                  # commit or rollback
            db.execute("UPDATE acc SET bal = bal + ? WHERE name = ?", (amount, dst))
            db.execute("UPDATE acc SET bal = bal - ? WHERE name = ?", (amount, src))
    except sqlite3.IntegrityError:
        print(f"transfer of {amount} failed, rolled back")

transfer("vishal", "li", 30)
transfer("vishal", "li", 500)
print(db.execute("SELECT * FROM acc").fetchall())''',
     steps=["<b>with db:</b> commits on success and rolls back on error.", "The failed transfer left <b>no</b> half-done change.",
            "This is the <b>A</b> in ACID: atomicity."]),

 code_out(M, "REST API", "Your own API with FastAPI", '''
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()
NOTES: dict[int, dict] = {}

class NoteIn(BaseModel):
    text: str

@app.post("/notes", status_code=201)
def create(note: NoteIn):
    nid = len(NOTES) + 1
    NOTES[nid] = {"id": nid, "text": note.text}
    return NOTES[nid]

@app.get("/notes/{nid}")
def read(nid: int):
    if nid not in NOTES:
        raise HTTPException(404, "note not found")
    return NOTES[nid]

c = TestClient(app)
print(c.post("/notes", json={"text": "buy milk"}).json())
print(c.get("/notes/9").status_code, c.get("/notes/9").json())
print(c.post("/notes", json={}).status_code)''',
     steps=["Type hints = validation + docs at <b>/docs</b>.", "Errors become proper status codes (404, 422).",
            "Modules 21-28 go much deeper."]),

 mistake(M, "Dates and time zones", "Naive datetimes",
     '''
from datetime import datetime
created = datetime.now()     # local, no zone
# server in Frankfurt, user in Mumbai,
# DST change in October... which hour?''',
     "A naive datetime has <b>no time zone</b>. Comparing or storing them across servers and DST changes gives wrong hours.",
     '''
from datetime import datetime, UTC
from zoneinfo import ZoneInfo
created = datetime.now(UTC)          # store UTC
local = created.astimezone(ZoneInfo("Asia/Kolkata"))
print(local.isoformat())             # show local''',
     "Rule: <b>store and compute in UTC</b>, convert to the user's zone only for display. Send ISO 8601 strings."),

 trace(M, "Serialisation", "pickle vs JSON, text vs bytes", ["", "Use it for", "Watch out"],
       [["<b>JSON</b>", "APIs, config, anything shared", "only dicts, lists, str, numbers, bool, None"],
        ["<b>pickle</b>", "Python-only caches, ML models you made", "<b>loading untrusted pickle runs code</b>: never"],
        ["<b>str</b>", "text (Unicode characters)", "<span class=\"m\">.encode(\"utf-8\")</span> &#8594; bytes"],
        ["<b>bytes</b>", "files, network, images", "<span class=\"m\">.decode(\"utf-8\")</span> &#8594; str; wrong codec = mojibake"]]),

 interview(M, "What is REST? What makes an API RESTful?",
     ["<b>Resources</b> with URLs (<b>/orders/7</b>), manipulated with HTTP <b>methods</b> (GET, POST, PUT, PATCH, DELETE).",
      "<b>Stateless</b>: every request carries what's needed (e.g. a token); the server keeps no session per client.",
      "Correct <b>status codes</b>, JSON representations, and cacheable GETs.",
      "Good practice: plural nouns, filtering with query params, pagination, versioning (<b>/v1/</b>)."],
     None,
     "\"PUT vs PATCH? Which methods are idempotent?\" (PUT replaces, PATCH changes some fields; GET, PUT and DELETE are idempotent, POST is not)."),

 interview(M, "How do you prevent SQL injection? What is a transaction?",
     ["Never concatenate user input into SQL. Use <b>parameterised queries</b> or an <b>ORM</b>.",
      "Also: least-privilege DB users and input validation at the edges.",
      "A <b>transaction</b> groups statements so they all succeed or all roll back.",
      "<b>ACID</b>: Atomic, Consistent, Isolated, Durable."],
     '''
cur.execute(
    "SELECT * FROM users WHERE email = %s",
    (email,))''',
     "\"INNER vs LEFT JOIN? What does GROUP BY do? What is an index?\" (see Module 23 and the Top 100 page)."),

 recap(M, "Module 18 in 6 lines",
     ["<b>pathlib</b>, <b>csv.DictReader/Writer</b>, <b>json</b>, always <b>encoding=\"utf-8\"</b>.",
      "HTTP clients: <b>timeout</b>, <b>raise_for_status()</b>, retries for idempotent calls.",
      "Know methods, status codes and <b>idempotency</b>.",
      "SQL: JOIN, GROUP BY, <b>parameters</b> (no injection), <b>transactions</b>.",
      "Store time in <b>UTC</b>, display in the user's zone.",
      "Never unpickle untrusted data; bytes &#8596; str with <b>utf-8</b>."],
     "Do <b>exercises/ex18_notes_repository.py</b>: a SQLite repository with safe queries."),
]
