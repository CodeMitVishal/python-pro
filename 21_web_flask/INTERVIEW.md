# Module 21 · Interview questions (with answers)

[← Module 21](README.md) · [Quiz](QUIZ.md)

---

### 1. What happens when you type a URL and press Enter?

**Say:**
1. The browser parses the URL and checks its cache.
2. **DNS** resolves the host name to an IP address.
3. A **TCP** connection opens, followed by a **TLS** handshake for HTTPS.
4. The browser sends an **HTTP request** (method, path, headers, cookies).
5. The server stack (load balancer → app server → framework → view → database) builds a **response**.
6. The browser renders the HTML and makes more requests for CSS, JS and images.

---

### 2. What does an HTTP request and response look like?

**Say:** A request is a request line (`GET /orders?page=2 HTTP/1.1`), headers (`Host`, `Accept`, `Cookie`, `Authorization`), a blank line and an optional body. A response is a status line (`HTTP/1.1 200 OK`), headers (`Content-Type`, `Set-Cookie`, `Cache-Control`) and a body.

---

### 3. Cookie vs session?

**Say:** A **cookie** is small data the browser stores and sends back with every request to that site. A **session** is server-side state about a user. Usually the cookie holds only a session ID, or, in Flask, a signed copy of the data. Set cookies with `HttpOnly`, `Secure` and `SameSite`.

---

### 4. What is Post/Redirect/Get?

**Say:** After a successful form POST, redirect (303) to a GET page. Refreshing then repeats the harmless GET instead of re-submitting the form, which would create a duplicate order or payment.

---

### 5. How do templates prevent XSS?

**Say:** Jinja2 and Django templates **auto-escape** variables, so `<script>` from user input is shown as text instead of running. Never mark user input as `|safe`. Add a Content-Security-Policy header for defence in depth.

---

### 6. What are WSGI and ASGI?

**Say:** They are the standard interfaces between Python web apps and servers. **WSGI** is synchronous, one request per worker thread (Flask and Django under gunicorn). **ASGI** adds async, WebSockets and long-lived connections (FastAPI and Django-async under uvicorn).

---

### 7. Flask vs Django vs FastAPI?

**Say:**
- **Flask** is minimal and flexible: you choose the extensions.
- **Django** is batteries-included: ORM, admin, auth, migrations, forms. It's best for full web products.
- **FastAPI** is async and type-hint driven, with automatic validation and OpenAPI docs. It's best for JSON APIs.

---

### 8. What is a Flask Blueprint / application factory?

**Say:** A **Blueprint** groups related routes (e.g. `/orders`) into a reusable module. An **application factory** (`create_app(config)`) builds the app in a function, so tests and environments can create apps with different settings.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
