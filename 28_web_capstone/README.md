# Module 28 · Web capstone: taskboard

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-28.pdf) · [Interview Q&A](INTERVIEW.md)

Everything together: a team task board API with sign-up, JWT login, SQL, permissions, live WebSocket updates, tests, mypy-strict and a Dockerfile.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| The project | [`taskboard/`](taskboard/) | src layout: config, db, models, schemas, security, routers |
| Architecture | [`taskboard/README.md`](taskboard/README.md) | which module shows up where |
| Tests | [`taskboard/tests/`](taskboard/tests/) | auth, CRUD, permissions, validation, WebSocket |

```bash
pip install -e "28_web_capstone/taskboard[dev]"
```

```bash
uvicorn taskboard.main:app --reload
```

## Exercise: Web capstone challenges

8 features in 3 levels: due dates, Alembic, rate limiting, Redis, projects, deployment.

- Start here: [`exercises/ex28_web_capstone_challenges.md`](../exercises/ex28_web_capstone_challenges.md)

## Knowledge check

Preparing for interviews? Read the [Module 28 interview questions](INTERVIEW.md): short answers you can say out loud.


Take the [web development final exam](QUIZ.md): 15 questions across Modules 21–28.

**Next up:** [Module 29 · Algorithms & data structures](../29_algorithms/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
