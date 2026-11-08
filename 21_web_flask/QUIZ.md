# Python Pro – Module 21 Knowledge Check
**HTTP fundamentals, Flask & Jinja2**

Try to answer without looking. The answer key is at the bottom, and each answer says which lesson file to revisit.

---

### Part A – Multiple choice

**1. What is an HTTP request, at its core?**
- A) A binary file
- B) Text: a request line, headers, a blank line, then an optional body
- C) A Python object
- D) A database query

**2. Which HTTP method should create a new resource?**
- A) GET
- B) POST
- C) DELETE
- D) HEAD

**3. Which status code family means "the client made a mistake"?**
- A) 2xx
- B) 3xx
- C) 4xx
- D) 5xx

**4. What does a `Set-Cookie` header do?**
- A) Deletes the session
- B) Asks the browser to store a value and send it back on later requests
- C) Encrypts the response
- D) Sets the content type

**5. In Flask, how do you read `?after=2010` as an int?**
- A) `request.form["after"]`
- B) `request.args.get("after", type=int)`
- C) `request.json["after"]`
- D) `int(request.path)`

**6. What does `@app.get("/books/<int:book_id>")` do with `book_id`?**
- A) Nothing
- B) Takes it from the URL and converts it to an int
- C) Reads it from the body
- D) Reads it from a cookie

**7. How do you return "201 Created" with a JSON body in Flask?**
- A) `return book`
- B) `return book, 201`
- C) `return 201`
- D) `abort(201)`

**8. Why does `{{ review }}` in Jinja2 turn `<script>` into `&lt;script&gt;`?**
- A) A bug
- B) Auto-escaping, which prevents XSS (malicious scripts injected through user input)
- C) To save space
- D) Only in debug mode

**9. What does `{% extends "base.html" %}` do?**
- A) Imports Python code
- B) Reuses a layout and fills in its `{% block %}` sections
- C) Copies the file
- D) Loads CSS

**10. Why redirect after a successful form POST (POST → redirect → GET)?**
- A) It's faster
- B) So refreshing the page doesn't submit the form again
- C) Flask requires it
- D) To clear cookies

**11. What is Flask's `session`?**
- A) A database table
- B) A signed cookie: the browser stores it but can't change it without the secret key
- C) Server memory shared by all users
- D) A thread

**12. Where must `app.secret_key` come from in production?**
- A) The source code
- B) An environment variable or a secrets store
- C) The URL
- D) A cookie

---

### Part B – What happens?

**13.** A client calls `GET /books/99`, and book 99 doesn't exist. With `abort(404, description=...)` and an `@app.errorhandler(404)` that returns JSON, what does the client receive?

**14.** A template uses `{{ comment|safe }}`, and the comment is `<script>steal()</script>`. What happens in the browser?

---

### Part C – Fix it

**15.** Refreshing the page after adding a book adds it again. Fix the end of the view:
```python
@app.post("/books")
def add_book():
    BOOKS.append(...)
    return render_template("shop.html", books=BOOKS)
```

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Revisit |
|---|--------|---------|
| 1 | B | `01_http_from_scratch.py` |
| 2 | B | `01_http_from_scratch.py` |
| 3 | C (5xx = the server's fault) | `01_http_from_scratch.py` |
| 4 | B | `01_http_from_scratch.py` |
| 5 | B | `02_flask_basics.py` |
| 6 | B | `02_flask_basics.py` |
| 7 | B | `02_flask_basics.py` |
| 8 | B | `03_templates_forms_sessions.py` |
| 9 | B | `templates/shop.html` |
| 10 | B | `03_templates_forms_sessions.py` |
| 11 | B | `03_templates_forms_sessions.py` |
| 12 | B | `03_templates_forms_sessions.py` |
| 13 | Status 404 with `{"error": "book 99 not found"}` | `02_flask_basics.py` |
| 14 | The script runs: `|safe` turns off escaping. That's an XSS hole. Never use it on user input. | `03_templates_forms_sessions.py` |
| 15 | `flash("Added!")` then `return redirect(url_for("shop"))` | `03_templates_forms_sessions.py` |

</details>

---

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
