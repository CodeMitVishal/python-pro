"""Slides · Module 21 · HTTP, Flask & Jinja2"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 21 · HTTP, Flask &amp; Jinja2"
SLIDES = [
 cover("21", "HTTP, Flask &amp; Jinja2", "How the web really works, and your first server-rendered web app.",
       [("HTTP from scratch", "01_http_from_scratch.py"), ("Flask basics", "02_flask_basics.py"),
        ("Templates, forms &amp; sessions", "03_templates_forms_sessions.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "The web", "Frameworks hide HTTP, until something breaks",
     "A form submits twice, a cookie isn't sent, CORS blocks your frontend. Without knowing <b>HTTP</b> you can only guess.",
     "Every web framework turns <b>one HTTP request into one HTTP response</b>. Learn that message format once and every framework makes sense."),

 picture(M, "HTTP", "What happens when you open a page",
     "&#127760; Your browser looks up the server's address (<b>DNS</b>), opens a connection (<b>TCP + TLS</b> for https), "
     "sends a text <b>request</b>, and gets a text <b>response</b>. The framework only does the middle part.",
     [("DNS", "shop.de &#8594; 203.0.113.7"), ("TCP + TLS", "a secure connection"),
      ("request", "GET /cart HTTP/1.1 + headers + cookie"), ("response", "200 OK + headers + HTML/JSON")]),

 code_out(M, "HTTP from scratch", "A real HTTP request is just text", '''
request = (
    "GET /orders?page=2 HTTP/1.1\\r\\n"
    "Host: shop.de\\r\\n"
    "Cookie: session=abc123\\r\\n"
    "\\r\\n"                                  # blank line = end of headers
)
print(request)

response = "HTTP/1.1 200 OK\\r\\nContent-Type: application/json\\r\\n\\r\\n[]"
status_line, rest = response.split("\\r\\n", 1)
print("status:", status_line.split()[1])''',
     steps=["Line 1: <b>method, path, version</b>; then headers, a blank line, the body."]),

 code_out(M, "Flask basics", "Routes, parameters, JSON, status codes", '''
from flask import Flask, jsonify, request

app = Flask(__name__)
BOOKS = {1: {"id": 1, "title": "Fluent Python"}}

@app.get("/books/<int:book_id>")
def get_book(book_id):
    book = BOOKS.get(book_id)
    if book is None:
        return jsonify(error="not found"), 404
    return jsonify(book)

@app.post("/books")
def create_book():
    data = request.get_json()
    new = {"id": len(BOOKS) + 1, "title": data["title"]}
    BOOKS[new["id"]] = new
    return jsonify(new), 201

c = app.test_client()
print(c.get("/books/1").get_json())
print(c.get("/books/9").status_code)
print(c.post("/books", json={"title": "Python Pro"}).get_json())''',
     steps=["<b>&lt;int:book_id&gt;</b> converts and validates the path.", "Return <b>(body, status)</b>.",
            "<b>test_client()</b> calls the app without a server."]),

 picture(M, "Templates", "Server-side rendering with Jinja2",
     "&#127912; A template is an HTML page with <b>holes</b>. The view fills the holes with data; Jinja2 <b>escapes</b> it so user text "
     "can't inject scripts. A <b>base</b> layout is reused by every page.",
     [("view", "render_template(\"books.html\", books=books)"), ("books.html", "{% extends \"base.html\" %}"),
      ("{% for b in books %}", "loops and ifs"), ("{{ b.title }}", "auto-escaped output")]),

 mistake(M, "Forms", "The double-submit bug",
     '''
@app.post("/order")
def order():
    save_order(request.form)
    return render_template("thanks.html")
# user presses F5 -> the browser POSTs again''',
     "Refreshing a page that was the answer to a POST <b>repeats the POST</b>: a second order, a second payment.",
     '''
@app.post("/order")
def order():
    save_order(request.form)
    flash("Order placed!")
    return redirect(url_for("thanks"))   # 303
# refresh now repeats a harmless GET''',
     "<b>Post/Redirect/Get</b>: after a successful POST, redirect. Add CSRF tokens to forms (Flask-WTF)."),

 trace(M, "Cookies and sessions", "How a site remembers you", ["Piece", "What it does", "Watch out"],
       [["<b>Cookie</b>", "small data the browser sends back on every request", "set <span class=\"m\">HttpOnly</span>, <span class=\"m\">Secure</span>, <span class=\"m\">SameSite</span>"],
        ["<b>Flask session</b>", "a <b>signed</b> cookie (readable, not editable)", "never store secrets in it; set a strong SECRET_KEY"],
        ["<b>Server-side session</b>", "cookie holds only an ID; data in Redis/DB", "can be revoked; scales with a shared store"],
        ["<b>Token (JWT)</b>", "sent in the Authorization header by API clients", "Module 24"]],
       "HTTP is <b>stateless</b>: cookies and tokens are how state is added on top."),

 job(M, "Flask", "Where Flask fits at work", [
     ("Small services and internal tools", '''
@app.get("/health")
def health(): return {"status": "ok"}'''),
     ("Blueprints for bigger apps", '''
bp = Blueprint("orders", __name__)
app.register_blueprint(bp, url_prefix="/orders")'''),
     ("Production server", '''
gunicorn "app:create_app()" -w 4'''),
     ("Choose the tool", '''
Flask: small + flexible  | FastAPI: typed APIs
Django: batteries included (admin, ORM, auth)'''),
 ]),

 interview(M, "What happens when you type a URL and press Enter?",
     ["The browser parses the URL and checks its cache.",
      "<b>DNS</b> resolves the host name to an IP address.",
      "It opens a <b>TCP</b> connection and does the <b>TLS</b> handshake for https.",
      "It sends an <b>HTTP request</b> (method, path, headers, cookies).",
      "The server (load balancer &#8594; app server &#8594; framework &#8594; your view &#8594; DB) builds the <b>response</b>.",
      "The browser renders the HTML and fetches CSS, JS and images with more requests."],
     None,
     "\"What's the difference between a cookie and a session?\" (the cookie lives in the browser; a session is server-side state usually found via an ID stored in a cookie)."),

 interview(M, "Flask vs Django vs FastAPI?",
     ["<b>Flask</b>: a micro-framework. Minimal core, you choose the extensions. Great for small services.",
      "<b>Django</b>: batteries included: ORM, migrations, admin, auth, forms. Great for full web apps and CRUD-heavy products.",
      "<b>FastAPI</b>: async, type-hint driven, automatic validation and OpenAPI docs. Great for JSON APIs and microservices.",
      "All are WSGI/ASGI apps; the HTTP fundamentals are identical."],
     None,
     "\"What are WSGI and ASGI?\" (the interfaces between Python apps and servers: WSGI is synchronous (gunicorn), ASGI adds async and WebSockets (uvicorn))."),

 recap(M, "Module 21 in 5 lines",
     ["HTTP = text request (method, path, headers, body) &#8594; text response (status, headers, body).",
      "Flask: <b>@app.get/post</b>, path converters, <b>jsonify</b>, (body, status).",
      "Jinja2 templates: <b>extends</b>, loops, and <b>auto-escaping</b> against XSS.",
      "After a POST: <b>redirect</b> (Post/Redirect/Get); protect forms with CSRF tokens.",
      "Cookies carry state; set HttpOnly, Secure, SameSite."],
     "Run <b>02_flask_basics.py</b>, then add a <b>DELETE /books/&lt;id&gt;</b> route that returns 204."),
]
