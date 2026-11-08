"""Slides · Module 22 · FastAPI in depth"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 22 · FastAPI in depth"
SLIDES = [
 cover("22", "FastAPI in depth", "Design production APIs: validation, dependency injection, errors, middleware, settings and async.",
       [("Pydantic models", "01_pydantic_models.py"), ("Routers &amp; dependencies", "02_routers_and_dependencies.py"),
        ("Errors, middleware &amp; CORS", "03_errors_middleware_cors.py"), ("Settings, lifespan &amp; async", "04_settings_lifespan_async.py"),
        ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Validation", "Never trust the client",
     "A mobile app sends <b>{\"qty\": \"-5\", \"email\": \"lol\"}</b>. Without validation you store garbage, or a negative order refunds money.",
     "Describe the data once with <b>Pydantic</b>. FastAPI validates every request, converts types, and answers <b>422</b> with clear errors."),

 code_out(M, "Pydantic", "Models that validate and convert", '''
from pydantic import BaseModel, Field, ValidationError, field_validator

class OrderIn(BaseModel):
    email: str = Field(pattern=r".+@.+\\..+")
    item: str = Field(min_length=1, max_length=50)
    qty: int = Field(gt=0, le=100)

    @field_validator("item")
    @classmethod
    def clean(cls, v): return v.strip().lower()

print(OrderIn(email="v@ex.com", item="  Lamp ", qty="3"))   # "3" -> 3

try:
    OrderIn(email="lol", item="", qty=-5)
except ValidationError as e:
    for err in e.errors():
        print(err["loc"][0], "->", err["msg"])''',
     steps=["Types are <b>converted</b> (\"3\" &#8594; 3) and constraints checked.", "All errors at once, with the field name.",
            "Separate models for <b>input</b> and <b>output</b> (never return password hashes)."]),

 picture(M, "Dependency injection", "Depends(): FastAPI hands you what you need",
     "&#128268; Instead of each endpoint creating its own DB session or checking the token, it <b>declares</b> what it needs. "
     "FastAPI builds it, passes it in, and cleans up afterwards. Tests can <b>swap</b> any dependency.",
     [("request arrives", "GET /orders"), ("get_db()", "open a session (yield)"),
      ("current_user(token)", "decode the token, load the user"), ("endpoint runs", "orders for that user"),
      ("cleanup", "session closed")]),

 code_out(M, "Dependency injection", "Chained dependencies + override in tests", '''
from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()
USERS = {"t-vishal": {"name": "vishal", "role": "admin"}}

def current_user(authorization: Annotated[str | None, Header()] = None):
    user = USERS.get((authorization or "").removeprefix("Bearer "))
    if not user:
        raise HTTPException(401, "not logged in")
    return user

def admin(user: Annotated[dict, Depends(current_user)]):
    if user["role"] != "admin":
        raise HTTPException(403, "admins only")
    return user

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, user: Annotated[dict, Depends(admin)]): ...

c = TestClient(app)
print(c.delete("/books/1").status_code)
print(c.delete("/books/1", headers={"Authorization": "Bearer t-vishal"}).status_code)''',
     steps=["<b>admin</b> depends on <b>current_user</b>: a chain.", "<b>401</b> = who are you? <b>403</b> = I know you, but no.",
            "Tests swap any of them with <b>dependency_overrides</b>."]),

 trace(M, "Project structure", "A FastAPI project that scales", ["File", "Job"],
       [["<span class=\"m\">main.py</span>", "create the app, include routers, middleware, lifespan"],
        ["<span class=\"m\">routers/orders.py</span>", "<span class=\"m\">APIRouter(prefix=\"/orders\", tags=[\"orders\"])</span>: thin endpoints"],
        ["<span class=\"m\">schemas.py</span>", "Pydantic in/out models"],
        ["<span class=\"m\">services/</span>", "business rules, no HTTP code"],
        ["<span class=\"m\">deps.py</span>", "get_db, current_user, pagination params"],
        ["<span class=\"m\">config.py</span>", "<span class=\"m\">Settings(BaseSettings)</span> from environment variables"]],
       "Endpoints stay thin: validate &#8594; call a service &#8594; return a schema."),

 code_out(M, "Errors and middleware", "One place for errors, one for every request", '''
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

app = FastAPI()

class OutOfStock(Exception):
    def __init__(self, item): self.item = item

@app.exception_handler(OutOfStock)
def out_of_stock(request: Request, exc: OutOfStock):
    return JSONResponse({"detail": f"{exc.item} is sold out"}, status_code=409)

@app.middleware("http")
async def request_id(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())[:8]
    return response

@app.post("/orders")
def order(): raise OutOfStock("lamp")

r = TestClient(app).post("/orders")
print(r.status_code, r.json(), "has id:", "x-request-id" in r.headers)''',
     steps=["Domain errors &#8594; HTTP codes in <b>one</b> place.", "Middleware wraps <b>every</b> request: IDs, timing, logging.",
            "CORS is middleware too: <b>CORSMiddleware(allow_origins=[...])</b>."]),

 mistake(M, "CORS", "\"Fixing\" CORS with a wildcard",
     '''
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,     # with cookies!
    allow_methods=["*"])''',
     "Any website could call your API from a victim's browser. (Browsers reject * with credentials anyway, so it also doesn't work.)",
     '''
app.add_middleware(CORSMiddleware,
    allow_origins=["https://app.shop.de"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Authorization", "Content-Type"])''',
     "CORS is a <b>browser</b> rule. List the exact frontend origins. It doesn't protect against curl or other servers."),

 code_out(M, "Settings and lifespan", "Config from the environment, startup and shutdown", '''
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///dev.db"
    debug: bool = False

os.environ["DEBUG"] = "true"           # e.g. set by Docker / Azure
settings = Settings()
print(settings)

@asynccontextmanager
async def lifespan(app):
    print("startup: open DB pool, HTTP client")
    yield
    print("shutdown: close them")

app = FastAPI(lifespan=lifespan)
with TestClient(app):
    print("serving requests...")''',
     steps=["<b>12-factor</b>: config in env vars, never in code.", "<b>lifespan</b>: create shared clients once, close them cleanly.",
            "Secrets come from the environment or a vault."]),

 job(M, "FastAPI", "FastAPI patterns you'll see at work", [
     ("Pagination dependency", '''
def page(limit: int = Query(20, le=100), offset: int = 0):
    return {"limit": limit, "offset": offset}'''),
     ("Background work", '''
@app.post("/signup")
def signup(bg: BackgroundTasks): bg.add_task(send_mail)'''),
     ("Response models hide fields", '''
@app.get("/me", response_model=UserOut)'''),
     ("Run in production", '''
uvicorn app.main:app --workers 4
# or gunicorn -k uvicorn.workers.UvicornWorker'''),
 ]),

 interview(M, "What is dependency injection in FastAPI? Why is it useful?",
     ["Endpoints <b>declare</b> what they need with <b>Depends()</b>; FastAPI creates it per request and passes it in.",
      "Dependencies can depend on others (token &#8594; user &#8594; admin), and <b>yield</b> dependencies clean up afterwards.",
      "It removes duplication (auth, DB sessions, pagination) and keeps endpoints thin.",
      "In tests, <b>app.dependency_overrides</b> swaps the real DB or external clients for fakes."],
     None,
     "\"401 vs 403?\" (401: not authenticated, send credentials; 403: authenticated but not allowed)."),

 interview(M, "How does FastAPI validate requests? What is 422?",
     ["Parameters and bodies are declared with <b>type hints</b> and <b>Pydantic</b> models.",
      "FastAPI parses path, query, headers and JSON, <b>converts types</b> and checks constraints.",
      "Invalid input gets a <b>422 Unprocessable Entity</b> with a list of field errors, before your code runs.",
      "The same models generate the <b>OpenAPI</b> docs at /docs."],
     None,
     "\"What is CORS and when do you need it?\" (a browser rule: a page from origin A may call API origin B only if B allows A via CORS headers)."),

 recap(M, "Module 22 in 6 lines",
     ["<b>Pydantic</b> validates and converts; separate In/Out models.",
      "<b>Depends()</b> for DB sessions, auth, pagination; chain them.",
      "401 = who are you, 403 = not allowed, 422 = bad input.",
      "Exception handlers map domain errors; middleware wraps every request.",
      "CORS: exact origins only.",
      "<b>BaseSettings</b> for env config; <b>lifespan</b> for startup/shutdown."],
     "Extend <b>02_routers_and_dependencies.py</b>: add <b>PATCH /books/{id}</b> for admins only, with a test."),
]
