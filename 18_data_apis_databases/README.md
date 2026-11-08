# Module 18 · Data, APIs & databases

[← Back to the course](../README.md) · [Slides](../slides/python-pro-slides.pdf)

Work with real data: files, CSV and JSON, web APIs, SQL databases, and your own REST API with FastAPI.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Files, CSV & JSON | [`01_files_csv_json.py`](01_files_csv_json.py) | pathlib, `DictReader`/`DictWriter`, JSON round trips |
| Calling web APIs | [`02_http_requests.py`](02_http_requests.py) | `requests` with params, timeouts, status codes |
| SQLite | [`03_sqlite.py`](03_sqlite.py) | SQL, `?` parameters vs SQL injection, transactions |
| Your own REST API | [`04_fastapi_app.py`](04_fastapi_app.py) | FastAPI + pydantic + SQLite, tested with `TestClient` |
| Dates & time zones | [`05_dates_and_timezones.py`](05_dates_and_timezones.py) | UTC, `zoneinfo`, DST, ISO 8601 |
| pickle vs JSON | [`06_pickle_vs_json.py`](06_pickle_vs_json.py) | why untrusted pickles run code |

Install the libraries:

```bash
pip install requests fastapi uvicorn httpx
```

Run the API server and open http://127.0.0.1:8000/docs:

```bash
cd 18_data_apis_databases
```

```bash
uvicorn 04_fastapi_app:app --reload
```

## Exercise: A notes database

A `NotesRepository` class that hides all SQL behind clean methods, injection-safe.

- Start here: [`exercises/ex18_notes_repository.py`](../exercises/ex18_notes_repository.py)
- Solution: [`solutions/ex18_notes_repository.py`](../solutions/ex18_notes_repository.py)

## Knowledge check

Test yourself with the [Module 18 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 19 · Performance & internals](../19_performance_internals/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
