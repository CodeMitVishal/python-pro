"""Slides · Course intro: cover, module index, how each module works"""
from teach_kit import foot

M = "Course intro"

CORE = [("08", "Pythonic code", "write short, idiomatic Python"),
        ("09", "Data structures", "the right structure, Big-O"),
        ("10", "Advanced functions", "closures, decorators, recursion"),
        ("11", "Iterators &amp; generators", "process big data lazily"),
        ("12", "Advanced OOP", "dunders, MRO, Protocols, SOLID"),
        ("13", "Errors &amp; logging", "fail safely, log clearly, debug"),
        ("14", "Packaging", "imports, venvs, a CLI"),
        ("15", "Type hints &amp; code quality", "mypy, ruff, generics"),
        ("16", "Testing with pytest", "fixtures, mocks, TDD, coverage"),
        ("17", "Concurrency", "threads, processes, asyncio, the GIL"),
        ("18", "Data, APIs &amp; databases", "CSV/JSON, HTTP, SQL, REST, time zones"),
        ("19", "Performance &amp; internals", "memory model, profiling, NumPy"),
        ("20", "Capstone: budget", "CLI + API + tests")]
WEB = [("21", "HTTP, Flask &amp; Jinja2", "how the web works"),
       ("22", "FastAPI in depth", "validation, DI, middleware"),
       ("23", "SQLAlchemy 2.0 &amp; Alembic", "ORM, N+1, indexes, migrations"),
       ("24", "Authentication &amp; security", "hashing, JWT, permissions, OWASP"),
       ("25", "Django + DRF", "ORM, admin, REST APIs"),
       ("26", "Real-time, tasks, caching", "WebSockets, jobs, Redis"),
       ("27", "Docker, CI/CD &amp; Azure", "containers, pipelines, cloud deploys"),
       ("28", "Web capstone", "a secure, tested API")]
EXTRA = [("29", "Algorithms &amp; data structures", "solve coding-interview problems"),
         ("30", "AI with Python", "LLM APIs, tools, RAG, agents")]


def table(rows):
    trs = "".join(f"<tr><td><b>{n}</b></td><td><b>{name}</b></td><td>{goal}</td></tr>" for n, name, goal in rows)
    return f'<table style="flex:1"><tr><th>#</th><th>Module</th><th>You\'ll be able to…</th></tr>{trs}</table>'


SLIDES = [
 f"""<section class="dark cover" style="justify-content:center;gap:28px">
  <img class="brand-big" src="channel-icon.png" alt="CodeMitVishal logo">
  <p class="num">CODEMITVISHAL · FREE COURSE</p>
  <h1 style="font-size:110px">Python Pro</h1>
  <p style="font-size:38px;color:#E6E9F0;max-width:1300px;line-height:1.3">From Python Foundations to <b style="color:#7EE2A8">job-ready</b>
     Python and web development: clean code, testing, concurrency, FastAPI, Django, security, Azure, algorithms and AI.</p>
  <div style="display:flex;gap:70px;margin-top:30px">
    <div><p class="big" style="font-size:96px">23</p><p style="font-size:24px">modules (08–30)</p></div>
    <div><p class="big" style="font-size:96px">100+</p><p style="font-size:24px">runnable lessons</p></div>
    <div><p class="big" style="font-size:96px">300+</p><p style="font-size:24px">interview answers</p></div>
    <div><p class="big" style="font-size:96px">0 €</p><p style="font-size:24px">always free</p></div>
  </div>
  <p class="foot-l">Python Pro · Prerequisite: Python Foundations (Modules 0–7)</p>
  <p class="foot-r">github.com/CodeMitVishal/python-pro</p>
</section>""",

 f"""<section>
  <div><p class="eyebrow">Course map · 1 of 2</p><h2>Core track: Modules 08–20</h2></div>
  <div class="row" style="gap:40px">{table(CORE[:7])}{table(CORE[7:])}</div>
  {foot("Course map")}
</section>""",

 f"""<section>
  <div><p class="eyebrow">Course map · 2 of 2</p><h2>Web track (21–28), then interviews &amp; AI (29–30)</h2></div>
  <div class="row" style="gap:40px">{table(WEB)}
    <div class="col" style="flex:1">{table(EXTRA)}
      <div class="tip"><b>Interview prep</b>: Top 100 questions, SQL practice, Git workflow and system design in <b>interview_prep/</b>.</div>
    </div></div>
  {foot("Course map")}
</section>""",

 f"""<section>
  <div><p class="eyebrow">How every module works</p><h2>The same 8 steps for every topic</h2></div>
  <div class="row" style="gap:48px">
    <div class="steps" style="flex:1">
      <div class="step"><span>1</span><p><b>Why</b>: the real problem this solves</p></div>
      <div class="step"><span>2</span><p><b>Picture it</b>: an everyday analogy + a diagram</p></div>
      <div class="step"><span>3</span><p><b>Try it</b>: code with its <b>real output</b></p></div>
      <div class="step"><span>4</span><p><b>Step by step</b>: what happens on each line</p></div>
      <div class="step"><span>5</span><p><b>Common mistake</b>: wrong vs right, side by side</p></div>
      <div class="step"><span>6</span><p><b>In real jobs</b>: where you'll meet it at work</p></div>
      <div class="step"><span>7</span><p><b>Interview</b>: what to say + the follow-up question</p></div>
      <div class="step"><span>8</span><p><b>Recap</b> + a practice task</p></div>
    </div>
    <div class="col" style="width:660px">
      <p class="label">IN EVERY MODULE FOLDER</p>
      <table class="tbig">
        <tr><td>Slides</td><td>slides/modules/Module-NN.pdf</td></tr>
        <tr><td>Lessons</td><td>runnable files with teaching notes</td></tr>
        <tr><td>Exercise</td><td>a starter that fails until you solve it</td></tr>
        <tr><td>Quiz</td><td>QUIZ.md with an answer key</td></tr>
        <tr><td>Interview</td><td>INTERVIEW.md with model answers</td></tr>
      </table>
    </div>
  </div>
  {foot("How it works")}
</section>""",

 f"""<section>
  <div><p class="eyebrow">How to study</p><h2>Get the most out of Python Pro</h2></div>
  <div class="row" style="gap:48px">
    <div class="steps" style="flex:1">
      <div class="step"><span>1</span><p>Watch or read the module's <b>slides</b>.</p></div>
      <div class="step"><span>2</span><p><b>Run every lesson</b> and change things to see what happens.</p></div>
      <div class="step"><span>3</span><p>Do the <b>exercise</b> until it prints <b>All checks passed!</b></p></div>
      <div class="step"><span>4</span><p>Take the <b>quiz</b>, then answer the <b>INTERVIEW.md</b> questions out loud.</p></div>
      <div class="step"><span>5</span><p>Open a <b>Pull Request</b> with your solution: I review it.</p></div>
    </div>
    <div class="code" style="width:780px;font-size:24px"><span class="c"># get started</span>
git clone https://github.com/
    CodeMitVishal/python-pro.git
cd python-pro
python -m venv .venv
pip install -r requirements.txt
python 08_pythonic_code/01_comprehensions.py</div>
  </div>
  {foot("How to study")}
</section>""",
]
