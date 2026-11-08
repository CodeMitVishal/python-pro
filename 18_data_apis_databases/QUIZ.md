# Python Pro – Module 18 Knowledge Check
**Data, APIs & databases**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson file to revisit.

---

### Part A – Multiple choice

**1. Why use `pathlib.Path` instead of joining strings like `"data/" + name`?**
- A) It's required
- B) `/` joins paths correctly on every OS, and paths get handy methods
- C) Strings can't hold paths
- D) It's faster to type

**2. `csv.DictReader` reads `total` as `"120.5"`. Why?**
- A) A bug
- B) CSV is plain text: every value is a string until you convert it
- C) DictReader rounds numbers
- D) It depends on the OS

**3. What's the most important argument to pass to `requests.get` in production code?**
- A) `verify=False`
- B) `timeout=...`
- C) `stream=True`
- D) `allow_redirects=False`

**4. What does `resp.raise_for_status()` do?**
- A) Prints the status
- B) Raises an `HTTPError` for 4xx/5xx responses
- C) Retries the request
- D) Converts JSON

**5. Which is the safe way to add a search term to a URL?**
- A) `url + "?q=" + term`
- B) `requests.get(url, params={"q": term})`
- C) `f"{url}?q={term}"`
- D) `url.replace("q", term)`

**6. Where should API tokens live?**
- A) In the source code
- B) In environment variables or a secrets manager
- C) In the README
- D) In the URL

**7. Why use `?` placeholders in SQL instead of f-strings?**
- A) Style
- B) They prevent SQL injection: values are never treated as SQL code
- C) They're required by SQLite
- D) They make queries shorter

**8. What does `with conn:` do in sqlite3?**
- A) Opens the database
- B) Starts a transaction: commit on success, rollback on error
- C) Closes the connection
- D) Locks the file forever

**9. What does `conn.row_factory = sqlite3.Row` give you?**
- A) Faster queries
- B) Rows you can access by column name: `row["name"]`
- C) Sorted rows
- D) Typed rows

**10. In FastAPI, what does a pydantic `BaseModel` parameter give an endpoint?**
- A) A database table
- B) Automatic validation of the JSON body (422 if invalid)
- C) Authentication
- D) Caching

**11. Which status code means "created"?**
- A) 200
- B) 201
- C) 204
- D) 404

**12. What is FastAPI's `TestClient` for?**
- A) Load testing
- B) Calling your API in tests without starting a server
- C) Deploying the API
- D) Writing docs

---

### Part B – What's the output?

**13.**
```python
user_input = "x' OR '1'='1"
sql = f"SELECT COUNT(*) FROM products WHERE name = '{user_input}'"
```
The table has 3 products. What does this query return, and why is that bad?

**14.** `POST /todos` with body `{"title": ""}`, where `title: str = Field(min_length=1)`. Which status code?

---

### Part C – Fix it

**15.**
```python
conn.execute(f"DELETE FROM users WHERE name = '{name}'")
```

**16.** This script sometimes hangs forever. Fix it:
```python
data = requests.get("https://api.example.com/rates").json()
```

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | Portable and readable. | `01_files_csv_json.py` |
| 2 | B | Convert with `float()` / `int()`. | `01_files_csv_json.py` |
| 3 | B | Without a timeout, a dead server hangs you. | `02_http_requests.py` |
| 4 | B | Fail loudly on HTTP errors. | `02_http_requests.py` |
| 5 | B | `params=` encodes the values correctly. | `02_http_requests.py` |
| 6 | B | Never commit secrets. | `02_http_requests.py` |
| 7 | B | Values stay data. | `03_sqlite.py` |
| 8 | B | All or nothing. | `03_sqlite.py` |
| 9 | B | Dict-like rows. | `03_sqlite.py` |
| 10 | B | Validation from type hints. | `04_fastapi_app.py` |
| 11 | B | 201 Created (204 = No Content). | `04_fastapi_app.py` |
| 12 | B | In-process calls, perfect for pytest. | `04_fastapi_app.py` |
| 13 | `3`: `OR '1'='1'` is always true. That's SQL injection. | Use `?` parameters. | `03_sqlite.py` |
| 14 | 422 Unprocessable Entity | pydantic rejected the body. | `04_fastapi_app.py` |
| 15 | `conn.execute("DELETE FROM users WHERE name = ?", (name,))`, inside `with conn:` | | `03_sqlite.py` |
| 16 | Add `timeout=10` and `resp.raise_for_status()`, and catch `requests.RequestException`. | | `02_http_requests.py` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
