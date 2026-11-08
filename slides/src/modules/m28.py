"""Slides · Module 28 · Web capstone: taskboard"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 28 · Web capstone"
SLIDES = [
 cover("28", "Web capstone: taskboard", "Auth, SQL, permissions, live updates, tests and Docker, all in one API you can show in interviews.",
       [("The project", "taskboard/"), ("Architecture", "taskboard/README.md"), ("Tests", "taskboard/tests/"),
        ("Challenges", "ex28_web_capstone_challenges.md"), ("Final exam", "QUIZ.md")], M),

 why(M, "Capstone", "A portfolio project beats a certificate",
     "Interviewers ask: <b>\"Show me something you built.\"</b> A to-do list from a tutorial doesn't stand out. "
     "A secure, tested, deployed API with real-time updates does.",
     "<b>taskboard</b> uses every web module. Understand it, extend it, deploy it, and talk about its design."),

 picture(M, "Architecture", "How taskboard fits together",
     "&#127959;&#65039; A request travels through the same layers as in the core capstone, plus the web pieces: auth, permissions, "
     "a database session per request, and a WebSocket hub that pushes changes to every open browser.",
     [("routers/", "HTTP + validation (22)"), ("deps.py · security.py", "JWT &#8594; current_user, 401/403 (24)"),
      ("models.py · db.py", "SQLAlchemy, session per request (23)"), ("realtime.py", "WebSocket broadcast (26)"),
      ("Dockerfile · CI", "ship it (27)")]),

 trace(M, "Architecture", "Files and the module they come from", ["File", "Job", "Module"],
       [["<span class=\"m\">config.py</span>", "TASKBOARD_* env vars via BaseSettings", "22, 27"],
        ["<span class=\"m\">db.py · models.py</span>", "engine, session per request, User 1---&lt; Task", "23"],
        ["<span class=\"m\">schemas.py</span>", "Pydantic in/out models", "22"],
        ["<span class=\"m\">security.py · deps.py</span>", "scrypt hashes, JWT, current_user", "24"],
        ["<span class=\"m\">routers/tasks.py</span>", "CRUD, owner-or-admin checks, pagination", "22-24"],
        ["<span class=\"m\">realtime.py</span>", "push every change over WebSockets", "26"],
        ["<span class=\"m\">tests/</span> · <span class=\"m\">Dockerfile</span>", "pytest, mypy --strict, ruff; container", "16, 27"]]),

 code_out(M, "Permissions", "Owner-or-admin, the heart of the API", '''
from fastapi import HTTPException

def can_edit(task, user):
    return task.owner_id == user.id or user.role == "admin"

def update_task(task, user, changes):
    if not can_edit(task, user):
        raise HTTPException(404, "task not found")   # don't leak existence
    for field, value in changes.items():
        setattr(task, field, value)
    return task

class Obj:
    def __init__(self, **kw): self.__dict__.update(kw)

task = Obj(id=1, owner_id=7, title="Write slides", done=False)
owner, other, admin = Obj(id=7, role="user"), Obj(id=8, role="user"), Obj(id=1, role="admin")
print(update_task(task, owner, {"done": True}).done)
try:
    update_task(task, other, {"title": "hacked"})
except HTTPException as e:
    print(e.status_code, e.detail)
print(update_task(task, admin, {"title": "Write ALL slides"}).title)''',
     steps=["Authorisation in <b>one</b> function, tested on its own.", "<b>404</b> instead of 403 hides other users' task IDs.",
            "The real code is in <b>routers/tasks.py</b>."]),

 trace(M, "Quality gate", "What \"done\" means in this project", ["Check", "Command", "Why"],
       [["Tests", "<span class=\"m\">pytest</span>", "auth, permissions, CRUD, WebSocket messages"],
        ["Types", "<span class=\"m\">mypy --strict</span>", "no None bugs, typed dependencies"],
        ["Lint + format", "<span class=\"m\">ruff check</span> · <span class=\"m\">ruff format</span>", "consistent, no smells"],
        ["Container", "<span class=\"m\">docker build</span>", "runs the same everywhere"],
        ["Docs", "<span class=\"m\">/docs</span> + README", "anyone can try the API in 2 minutes"]]),

 job(M, "Capstone", "Make it yours: the challenges", [
     ("Level 1", '''
due dates + an admin view
filter: ?done=false&sort=-due'''),
     ("Level 2", '''
Alembic migrations · login rate limit
Redis counters for tasks per user'''),
     ("Level 3", '''
projects with members (many-to-many)
without N+1 queries'''),
     ("Level 3", '''
per-user WebSocket channels
deploy to Azure Container Apps'''),
 ]),

 interview(M, "Tell me about a backend project you built.",
     ["<b>What and why</b>: a task API with accounts, permissions and live updates.",
      "<b>Stack</b>: FastAPI, SQLAlchemy, JWT auth, WebSockets, Docker, GitHub Actions.",
      "<b>A design decision</b>: owner-or-admin checks centralised in one dependency; 404 instead of 403 to avoid leaking IDs.",
      "<b>A problem you solved</b>: e.g. N+1 queries when listing tasks with owners, fixed with selectinload and a query-count test.",
      "<b>Quality</b>: tests, mypy --strict, ruff in CI. <b>Next</b>: Postgres, Alembic, rate limiting, deployment."],
     None,
     "\"How would you scale it to 1 million users?\" (stateless replicas behind a load balancer, Postgres with indexes and read replicas, Redis cache and pub/sub for WebSockets, background workers, CDN)."),

 recap(M, "Web track done: what you can do now",
     ["Explain HTTP and build pages with Flask/Jinja2.",
      "Design typed, validated APIs with FastAPI and dependency injection.",
      "Use SQLAlchemy and Django ORM without N+1; migrate safely.",
      "Secure apps: hashing, JWT, permissions, OWASP defences.",
      "Add real-time, background jobs and caching.",
      "Containerise, test in CI, deploy to Azure."],
     "Pick 2 challenges from <b>ex28_web_capstone_challenges.md</b>, deploy taskboard, and put the link on your CV and LinkedIn."),
]
