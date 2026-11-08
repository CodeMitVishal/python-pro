# Module 21 · HTTP fundamentals, Flask & Jinja2

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-21.pdf) · [Interview Q&A](INTERVIEW.md)

How the web really works (HTTP as plain text), then server-rendered pages with Flask: routes, JSON, templates, forms, sessions, and XSS protection.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| HTTP from scratch | [`01_http_from_scratch.py`](01_http_from_scratch.py) | a raw request over a socket, status codes, headers, cookies |
| Flask basics | [`02_flask_basics.py`](02_flask_basics.py) | routes, path/query params, JSON, status codes, error handlers |
| Templates, forms & sessions | [`03_templates_forms_sessions.py`](03_templates_forms_sessions.py) | Jinja2 inheritance, auto-escaping, POST→redirect→GET, flash, sessions |

```bash
pip install flask
```

```bash
python 21_web_flask/02_flask_basics.py
```

## Exercise: A Flask guestbook

HTML pages + a JSON API, validation, flash messages, escaping.

- Start here: [`exercises/ex21_flask_guestbook.py`](../exercises/ex21_flask_guestbook.py)
- Solution: [`solutions/ex21_flask_guestbook.py`](../solutions/ex21_flask_guestbook.py)

## Knowledge check

Preparing for interviews? Read the [Module 21 interview questions](INTERVIEW.md): short answers you can say out loud.


Test yourself with the [Module 21 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 22 · FastAPI in depth](../22_fastapi_in_depth/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
