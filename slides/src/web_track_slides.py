"""Slide data for the bonus advanced lessons and the web development track (Modules 21-28).
Imported by build_module_slides.py, which passes in its layout functions."""


def web_slides(title, code, table, cards, exercise):
    S = []
    M = "Bonus lessons · Modules 8-19"
    S += [
     code(M, "Bonus · Module 8 · Pattern matching", "match / case: match the SHAPE of data", '''
match event:
    case {"type": "order", "items": [first, *rest]}:
        return f"order: {first} (+{len(rest)} more)"
    case {"type": "refund", "amount": float(a)} if a > 0:
        return f"refund {a:.2f}"
    case Point(x=0, y=0):
        return "the origin"
    case _:
        return "something else"''', ["Match <b>literals</b>, <b>sequences</b>, <b>dicts</b> (extra keys ignored) and <b>classes</b>.",
                                   "<span class=\"m\">if ...</span> after a pattern is a <b>guard</b>.",
                                   "A bare name <b>captures</b>; compare constants with <span class=\"m\">Color.RED</span>."],
          tip="Also new in Module 8: <b>08_regex.py</b>, named groups, <span class=\"m\">re.sub</span>, validation"),
     table(M, "Bonus · Module 9 · Enums, heapq, bisect", "The right tool for constants, priorities and sorted data",
           ["Tool", "Use it for", "Example"],
           [["<b>StrEnum</b>", "fixed string options (JSON/DB friendly)", "<span class=\"m\">OrderStatus.PAID == \"paid\"</span>"],
            ["<b>IntEnum / Flag</b>", "sortable levels / combinable permissions", "<span class=\"m\">READ | WRITE</span>"],
            ["<b>heapq</b>", "priority queue, top-k", "<span class=\"m\">heappop(jobs)</span> → most urgent"],
            ["<b>heapq.nlargest</b>", "top 3 of 1M without a full sort", "O(n log k)"],
            ["<b>bisect</b>", "search/insert in sorted lists", "<span class=\"m\">insort(timeline, 30)</span>"]],
           tip="Typos in plain strings fail silently. <b>Enum typos fail loudly.</b>"),
     table(M, "Bonus · Modules 11-13", "Deeper language features", ["Lesson", "Key idea"],
           [["<b>gen.send(value)</b>", "two-way generators: <span class=\"m\">value = yield result</span>"],
            ["<b>async generators</b>", "<span class=\"m\">async for item in all_items()</span>: stream API pages"],
            ["<b>descriptors</b>", "<span class=\"m\">__get__/__set__/__set_name__</span>: how <span class=\"m\">@property</span> works"],
            ["<b>__new__</b> / <b>__init_subclass__</b>", "control creation; auto-register plugins"],
            ["<b>metaclasses</b>", "the class of a class: framework territory"],
            ["<b>ExitStack</b>", "a variable number of context managers, all cleaned up"],
            ["<b>ExceptionGroup + except*</b>", "report and handle several errors at once"]]),
     table(M, "Bonus · Modules 14-19", "Pro tooling and performance", ["Lesson", "Key idea"],
           [["<b>PyPI, uv, pre-commit</b>", "<span class=\"m\">python -m build</span> · <span class=\"m\">uv add</span> · checks on every commit"],
            ["<b>Generic[T], ParamSpec, @overload</b>", "typed containers and decorators that keep signatures"],
            ["<b>hypothesis + coverage</b>", "properties tested on hundreds of generated inputs; <span class=\"m\">--cov</span>"],
            ["<b>TaskGroup + Queue</b>", "structured concurrency, backpressure, <span class=\"m\">httpx.AsyncClient</span>"],
            ["<b>dates &amp; zoneinfo</b>", "store UTC, show local; DST makes a day 23 hours"],
            ["<b>pickle vs JSON</b>", "loading an untrusted pickle can run code"],
            ["<b>dis, weakref, NumPy</b>", "bytecode, weak caches, 28× faster vectorised maths"]]),
    ]

    # ---------------------------------------------------------------- Module 21
    S.append(table("Web development track", "Web development track", "From HTTP basics to a deployed, secure API",
                   ["#", "Module", "You'll be able to…"],
                   [["<b>21</b>", "<b>HTTP, Flask &amp; Jinja2</b>", "understand HTTP; build server-rendered pages"],
                    ["<b>22</b>", "<b>FastAPI in depth</b>", "design production APIs with validation and DI"],
                    ["<b>23</b>", "<b>SQLAlchemy 2.0 &amp; Alembic</b>", "use an ORM, avoid N+1, migrate schemas"],
                    ["<b>24</b>", "<b>Authentication &amp; security</b>", "hash passwords, issue JWTs, stop OWASP bugs"],
                    ["<b>25</b>", "<b>Django + DRF</b>", "build Django apps with an admin and REST API"],
                    ["<b>26</b>", "<b>WebSockets, tasks &amp; caching</b>", "push live updates, run jobs, cache with Redis"],
                    ["<b>27</b>", "<b>Docker, CI/CD &amp; Azure</b>", "containerise, test in CI, deploy to Azure"],
                    ["<b>28</b>", "<b>Web capstone: taskboard</b>", "ship a secure, tested, real-time API"]]))

    M = "Module 21 · HTTP, Flask &amp; Jinja2"
    S += [
     title("21", "HTTP, Flask &amp; Jinja2", "How the web really works, then server-rendered pages with Flask.",
           [("HTTP from scratch", "01_http_from_scratch.py"), ("Flask basics", "02_flask_basics.py"),
            ("Templates, forms &amp; sessions", "03_templates_forms_sessions.py"), ("Exercise: guestbook", "ex21_flask_guestbook.py")]),
     code(M, "Lesson · HTTP", "HTTP is just text", '''
GET /hello?name=Vishal HTTP/1.1      <- request line
Host: localhost:8765                 <- headers
Accept: application/json
                                     <- blank line ends the headers
HTTP/1.0 200 OK                      <- status line
Content-Type: application/json
Set-Cookie: visits=1

{"message": "Hello, Vishal!"}        <- body''',
          ["<b>2xx</b> success · <b>3xx</b> redirect · <b>4xx</b> your fault · <b>5xx</b> server fault",
           "<b>201</b> created · <b>204</b> no content · <b>401</b> who are you? · <b>403</b> not allowed · <b>422</b> invalid",
           "<b>Cookies</b>: the server asks the browser to remember a value and send it back."]),
     code(M, "Lesson · Flask", "URLs → functions", '''
@app.get("/books/<int:book_id>")
def get_book(book_id):
    book = BOOKS.get(book_id)
    if book is None:
        abort(404, description="not found")
    return book                       # dict -> JSON

@app.post("/books")
def create_book():
    data = request.get_json(silent=True) or {}
    if not data.get("title"):
        return {"error": "title is required"}, 400
    return new_book, 201''',
          ["<span class=\"m\">request.args</span> query · <span class=\"m\">request.form</span> forms · <span class=\"m\">request.get_json()</span> JSON",
           "<span class=\"m\">app.test_client()</span> tests without a server."]),
     code(M, "Lesson · Jinja2, forms &amp; sessions", "Server-rendered pages, safely", '''
{% extends "base.html" %}
{% block content %}
  {% for book in books %}
    <li>{{ book.title|title }}: {{ "%.2f"|format(book.price) }}</li>
  {% endfor %}
  <p>{{ review }}</p>     {# <script> becomes &lt;script&gt; #}
{% endblock %}

# POST -> redirect -> GET
flash("Added!"); return redirect(url_for("shop"))''',
          ["<b>Auto-escaping</b> blocks XSS. Never <span class=\"m\">|safe</span> user input.",
           "Redirect after POST: a refresh doesn't resubmit.",
           "<b>session</b> = a signed cookie; <span class=\"m\">secret_key</span> from an env var."]),
     exercise(21, "A Flask guestbook", ["GET / renders entries, newest first", "POST /sign validates + flashes + redirects",
                                         "Escape user messages (no |safe)", "GET /api/entries?name= returns JSON"],
              "ex21_flask_guestbook.py", '''POST /sign  -> 302 /
"Thanks for signing!"
GET /api/entries?name=RAJ
[{"name": "Raj", ...}]'''),
    ]

    # ---------------------------------------------------------------- Module 22
    M = "Module 22 · FastAPI in depth"
    S += [
     title("22", "FastAPI in depth", "Production API design: validation, dependencies, errors, middleware, settings.",
           [("pydantic models", "01_pydantic_models.py"), ("Routers &amp; dependencies", "02_routers_and_dependencies.py"),
            ("Errors, middleware &amp; CORS", "03_errors_middleware_cors.py"), ("Settings, lifespan &amp; async", "04_settings_lifespan_async.py"),
            ("Exercise: library API", "ex22_fastapi_library_api.py")]),
     code(M, "Lesson · pydantic", "Validate at the edges", '''
class UserIn(BaseModel):
    username: str = Field(min_length=3, pattern=r"^[a-z0-9_]+$")
    password: str = Field(min_length=8)
    age: int = Field(ge=13, le=120)
    address: Address                    # nested

    @field_validator("tags")
    @classmethod
    def clean(cls, tags): return sorted({t.lower() for t in tags})

class UserOut(BaseModel):               # no password field!
    username: str''',
          ["Strings like <span class=\"m\">\"30\"</span> become the right types.",
           "Every error comes with its location: <span class=\"m\">address.country</span>.",
           "Separate <b>In</b> and <b>Out</b> models: secrets never leak."]),
     code(M, "Lesson · Dependencies", "Depends(): reusable, testable building blocks", '''
def current_user(authorization: Annotated[str | None, Header()] = None):
    user = USERS.get((authorization or "").removeprefix("Bearer "))
    if user is None: raise HTTPException(401, "not logged in")
    return user

def admin_user(user = Depends(current_user)):      # chains
    if user["role"] != "admin": raise HTTPException(403)
    return user

@products.delete("/{id}", status_code=204)
def delete(id: int, admin: AdminDep): ...

app.dependency_overrides[current_user] = fake_user  # tests''',
          ["<b>APIRouter</b>: group endpoints, with a prefix such as <span class=\"m\">/api/v1</span>.",
           "Pagination, DB sessions, settings, and the current user are all dependencies."]),
     table(M, "Lesson · Production plumbing", "Errors, middleware, CORS, settings", ["Feature", "What it gives you"],
           [["<b>@app.exception_handler</b>", "domain errors → clean JSON (409); no tracebacks leaked"],
            ["<b>middleware</b>", "request IDs, timing headers, access logs on every request"],
            ["<b>CORSMiddleware</b>", "only your frontends may call the API from a browser"],
            ["<b>pydantic-settings</b>", "env vars → typed config; <span class=\"m\">SecretStr</span> hides secrets"],
            ["<b>lifespan</b>", "open shared clients/pools at startup, close at shutdown"],
            ["<b>async def</b>", "for awaited I/O (httpx, async DB); plain <span class=\"m\">def</span> for blocking code"]]),
     exercise(22, "A library API", ["APIRouter at /api/v1/books", "author filter + limit/offset validation",
                                     "X-API-Key dependency on POST (401)", "BookNotFound → custom 404 JSON"],
              "ex22_fastapi_library_api.py", '''GET /api/v1/books?author=martin
{"total": 2, "items": [...]}
GET /api/v1/books/9
404 {"error": "book_not_found", "id": 9}'''),
    ]

    # ---------------------------------------------------------------- Module 23
    M = "Module 23 · SQLAlchemy &amp; Alembic"
    S += [
     title("23", "SQLAlchemy 2.0 &amp; Alembic", "Databases through an ORM, without N+1, with versioned migrations.",
           [("Models", "models.py"), ("ORM CRUD", "01_orm_crud.py"), ("N+1 &amp; loading", "02_n_plus_1_and_loading.py"),
            ("SQLAlchemy + FastAPI", "03_sqlalchemy_with_fastapi.py"), ("Alembic", "04_alembic_migrations.py"),
            ("Exercise: blog ORM", "ex23_blog_orm.py")]),
     code(M, "Lesson · The ORM", "Tables as typed classes", '''
class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[Author] = relationship(back_populates="books")

with Session(engine) as session:
    cheap = session.scalars(select(Book).where(Book.price < 40)).all()
    book.price = 29.0          # just change it...
    session.commit()           # ...one transaction''',
          ["The same code runs on SQLite, PostgreSQL and <b>Azure SQL</b>.",
           "Values are bound parameters: <b>no SQL injection</b>."]),
     table(M, "Lesson · N+1 and migrations", "The two things that bite in production", ["Problem", "Fix", "Measured"],
           [["lazy loading in a loop", "<span class=\"m\">selectinload(Author.books)</span>", "51 → <b>2</b> queries"],
            ["many-to-one in a loop", "<span class=\"m\">joinedload(Book.author)</span>", "<b>1</b> query"],
            ["schema changes on live DBs", "<b>Alembic</b> migrations", "data survives"],
            ["", "<span class=\"m\">alembic upgrade head</span>", "apply missing steps"],
            ["", "<span class=\"m\">alembic downgrade -1</span>", "undo the last step"]],
           src='''def get_db():
    db = SessionLocal()
    try:
        yield db          # one session per request
    finally:
        db.close()''', width=600),
     exercise(23, "A blog database", ["User, Post, Tag + a many-to-many table", "publish(): reuse existing tags",
                                       "posts_with_tag, top_authors (GROUP BY)", "all posts with tags in ≤ 2 queries"],
              "ex23_blog_orm.py", '''top_authors(s)
# [("vishal", 2), ("raj", 1)]
queries: 2   # not N+1'''),
    ]

    # ---------------------------------------------------------------- Module 24
    M = "Module 24 · Authentication &amp; security"
    S += [
     title("24", "Authentication &amp; security", "Store passwords right, issue tokens, and stop the OWASP classics.",
           [("Password hashing", "01_password_hashing.py"), ("JWT tokens", "02_jwt_tokens.py"),
            ("FastAPI login", "03_fastapi_login.py"), ("Security checklist", "04_web_security_checklist.py"),
            ("Exercise: auth toolkit", "ex24_auth_toolkit.py")]),
     code(M, "Lesson · Passwords", "Slow + salted, never sha256", '''
def hash_password(pw):
    salt = secrets.token_bytes(16)            # unique per user
    digest = hashlib.scrypt(pw.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${salt.hex()}${digest.hex()}"

def verify_password(pw, stored):
    _, salt, digest = stored.split("$")
    check = hashlib.scrypt(pw.encode(), salt=bytes.fromhex(salt), n=2**14, r=8, p=1)
    return hmac.compare_digest(check.hex(), digest)  # constant time''',
          ["sha256: ~1,000,000 guesses/s on one core. scrypt: <b>50 ms</b> each.",
           "In production: <b>argon2id</b> (argon2-cffi / pwdlib).",
           "Tokens and reset links: <span class=\"m\">secrets</span>, never <span class=\"m\">random</span>."]),
     code(M, "Lesson · JWT + login", "Signed, not secret", '''
token = jwt.encode({"sub": "vishal", "role": "admin",
                    "exp": now + timedelta(minutes=15)},
                   SECRET, algorithm="HS256")

claims = jwt.decode(token, SECRET, algorithms=["HS256"])  # pin it!

@app.get("/admin")
def admin(user = Depends(require_role("admin"))): ...
#  no / bad token -> 401   wrong role -> 403''',
          ["The payload is <b>base64</b>: anyone can read it. Put no secrets in it.",
           "Tampering → <span class=\"m\">InvalidSignatureError</span>; expired → rejected.",
           "Same message for wrong user and wrong password."]),
     table(M, "Lesson · OWASP basics", "A checklist you can run", ["Threat", "Defence"],
           [["SQL injection", "parameters / ORM"], ["XSS", "escape output + Content-Security-Policy"],
            ["Broken access control", "check ownership on <b>every</b> request (401 vs 403)"],
            ["Path traversal", "<span class=\"m\">resolve()</span> + <span class=\"m\">is_relative_to(UPLOADS)</span>"],
            ["Brute force", "rate limiting → <b>429</b> + Retry-After"],
            ["CSRF", "SameSite cookies + CSRF tokens (Bearer headers aren't auto-sent)"],
            ["Leaked secrets / vulnerable deps", "env vars / Key Vault · <span class=\"m\">pip-audit</span>"]]),
     exercise(24, "An auth toolkit", ["scrypt hash + verify", "create/read JWT; AuthError on any bad token",
                                       "POST /login, GET /orders (401)", "DELETE /orders/{id}: admins only (403)"],
              "ex24_auth_toolkit.py", '''read_token(expired)  # AuthError
DELETE /orders/1 as raj    -> 403
DELETE /orders/1 as admin  -> 204'''),
    ]

    # ---------------------------------------------------------------- Module 25
    M = "Module 25 · Django + DRF"
    S += [
     title("25", "Django + DRF", "Batteries included: ORM, admin, templates, auth, and a REST API.",
           [("Guided tour", "01_django_tour.py"), ("The project", "bookstore_project/"), ("The API", "catalog/api.py"),
            ("Tests", "catalog/tests.py"), ("Exercise: reviews", "ex25_test_reviews.py")]),
     code(M, "Lesson · Django", "Model → migration → admin → view → template", '''
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               related_name="books")
    price = models.DecimalField(max_digits=7, decimal_places=2)

$ python manage.py makemigrations && python manage.py migrate
$ python manage.py createsuperuser && python manage.py runserver

Book.objects.filter(price__lt=35).select_related("author")''',
          ["<b>admin.py</b>: a full back office with search and filters, for free.",
           "<b>DecimalField</b> for money, never float.",
           "Settings from <b>env vars</b>; <span class=\"m\">DEBUG</span> off in production."]),
     code(M, "Lesson · Django REST Framework", "Serializers + ViewSets + a router", '''
class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    class Meta:
        model = Book
        fields = ["id", "title", "author", "author_name", "price"]
    def validate_price(self, value):
        if value <= 0: raise serializers.ValidationError("price must be positive")
        return value

class BookViewSet(viewsets.ModelViewSet): ...     # list/create/retrieve/update/delete
router.register("books", BookViewSet, basename="book")''',
          ["<b>IsAuthenticatedOrReadOnly</b>: guests read, users write.",
           "Django when you need admin + auth + HTML; FastAPI for lean async APIs."], size=22, width=980),
     exercise(25, "Book reviews", ["Review model (1-5) + migration", "admin + ReviewSerializer validation",
                                    "avg_rating on books (Avg annotate)", "/api/reviews/?book=<id>"],
              "ex25_test_reviews.py", '''$ python manage.py test
Ran 8 tests ... OK''', sol="ex25_django_reviews/"),
    ]

    # ---------------------------------------------------------------- Module 26
    M = "Module 26 · Real-time, tasks &amp; caching"
    S += [
     title("26", "WebSockets, tasks &amp; caching", "Push live updates, move slow work out of the request, cache with Redis.",
           [("WebSocket chat", "01_websockets_chat.py"), ("Background tasks", "02_background_tasks.py"),
            ("Caching with Redis", "03_caching_with_redis.py"), ("Exercise: live prices", "ex26_live_prices.py")]),
     code(M, "Lesson · WebSockets", "The server can push", '''
@app.websocket("/ws/{name}")
async def chat(ws: WebSocket, name: str):
    await room.join(ws, name)            # accept + remember
    try:
        while True:
            text = await ws.receive_text()
            await room.broadcast(f"{name}: {text}")
    except WebSocketDisconnect:
        await room.leave(ws)''',
          ["Starts as HTTP, <b>upgrades</b>, then stays open both ways.",
           "Chat, notifications, dashboards, live prices."]),
     table(M, "Lesson · Background work &amp; caching", "Answer fast, do the slow part later", ["Tool", "Use"],
           [["<b>BackgroundTasks</b>", "small jobs after the response (welcome email)"],
            ["<b>queue + worker</b>", "<b>202</b> + job id, then the client polls <span class=\"m\">/jobs/{id}</span>"],
            ["<b>Celery / RQ / arq</b>", "separate workers, retries, schedules, survive restarts"],
            ["<b>Redis cache-aside</b>", "read → miss → DB → <span class=\"m\">set(key, ex=60)</span>; write → <span class=\"m\">delete(key)</span>"],
            ["<b>Redis extras</b>", "counters (<span class=\"m\">incr</span>), leaderboards (<span class=\"m\">zadd</span>), rate limits"]],
           src='''1st read:  899.0 EUR in 224.5 ms
2nd read:  899.0 EUR in   0.1 ms
after update: 799.0 EUR  <- fresh''', width=560),
     exercise(26, "Live prices", ["GET /products/{id}: cache-aside, X-Cache HIT/MISS", "30 s TTL, 404 when missing",
                                   "PUT: update DB + delete cache key", "push {id, price} to every /ws/prices client"],
              "ex26_live_prices.py", '''X-Cache: MISS -> HIT
PUT /products/1?price=799.0
ws <- {"id": 1, "price": 799.0}'''),
    ]

    # ---------------------------------------------------------------- Module 27
    M = "Module 27 · Docker, CI/CD &amp; Azure"
    S += [
     title("27", "Docker, CI/CD &amp; Azure", "From laptop to cloud: containers, pipelines, Azure Container Apps.",
           [("Production-ready tour", "01_production_ready_tour.py"), ("Dockerfile", "Dockerfile"),
            ("docker compose", "docker-compose.yml"), ("CI/CD pipeline", "github-actions/ci-cd.yml"),
            ("Azure deploy", "azure/deploy.sh"), ("Exercise: fix a Dockerfile", "ex27_fix_the_dockerfile.py")]),
     code(M, "Lesson · Dockerfile", "Small, cached, non-root", '''
FROM python:3.12-slim AS build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install \
        -r requirements.txt

FROM python:3.12-slim
RUN useradd --create-home --uid 1000 appuser
COPY --from=build /install /usr/local
COPY app ./app                 # code LAST: cached layers
USER appuser
HEALTHCHECK CMD python -c "...urlopen('.../health/live')"
CMD ["gunicorn", "app.main:app", "-k",
     "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]''',
          ["<b>12-factor</b>: config from env, logs to stdout as JSON, health probes.",
           "<b>Liveness</b> = restart me · <b>Readiness</b> = send me traffic."], size=22, width=1000),
     code(M, "Lesson · CI/CD to Azure", "Nothing ships unless the tests pass", '''
jobs:
  test:                         # every push + PR
    steps: [checkout, setup-python, ruff, mypy, pytest]
  deploy:
    needs: test                 # only if green
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: azure/login@v2    # OIDC: no stored passwords
      - run: az acr build --image hello-service:${{ github.sha }} ...
      - run: az containerapp update --image ...:${{ github.sha }}''',
          ["Tag images with the <b>commit SHA</b>: you know what runs, and rollback is easy.",
           "Container Apps: HTTPS, <b>scale to zero</b>, secrets via <span class=\"m\">secretref:</span>.",
           "<span class=\"m\">docker compose up</span>: API + Postgres + Redis locally."], size=22, width=980),
     exercise(27, "Fix a bad Dockerfile", ["slim pinned base, no latest", "deps before code, --no-cache-dir",
                                            "non-root USER, no baked secrets", "HEALTHCHECK, exec-form CMD, no --reload"],
              "ex27_fix_the_dockerfile.py", '''Reviewed ex27_Dockerfile.bad: 0/9
Reviewed ex27_Dockerfile:     9/9
All checks passed!''', sol="ex27_Dockerfile"),
    ]

    # ---------------------------------------------------------------- Module 28
    M = "Module 28 · Web capstone"
    S += [
     title("28", "Web capstone: taskboard", "Auth, SQL, permissions, live updates, tests, Docker: all in one API.",
           [("The project", "taskboard/"), ("Architecture", "taskboard/README.md"), ("Tests", "taskboard/tests/"),
            ("Challenges", "ex28_web_capstone_challenges.md"), ("Final exam", "28_web_capstone/QUIZ.md")]),
     table(M, "Capstone · Architecture", "Every web module in one service", ["File", "Job", "Module"],
           [["<b>config.py</b>", "TASKBOARD_* env vars", "22, 27"], ["<b>db.py · models.py</b>", "engine, session per request, User 1---&lt; Task", "23"],
            ["<b>schemas.py</b>", "pydantic in/out, validation", "22"], ["<b>security.py · deps.py</b>", "scrypt, JWT, current_user (401)", "24"],
            ["<b>routers/tasks.py</b>", "CRUD, owner-or-admin (403), pagination", "22-24"],
            ["<b>realtime.py</b>", "WebSocket push on every change", "26"], ["<b>Dockerfile</b>", "multi-stage, non-root, health check", "27"]],
           src='''$ pytest      7 passed
$ mypy        Success (strict)
$ ruff check  All checks passed!''', width=520),
     exercise(28, "Web capstone challenges", ["⭐ due dates + an admin view", "⭐⭐ Alembic · login rate limit · Redis counts",
                                               "⭐⭐⭐ projects with members, no N+1", "⭐⭐⭐ per-user WebSocket · deploy to Azure"],
              "ex28_web_capstone_challenges.md", '''# for EVERY challenge:
# 1. write the test first
# 2. make it pass
# 3. keep pytest, mypy, ruff green''', sol=False),
    ]
    return S
