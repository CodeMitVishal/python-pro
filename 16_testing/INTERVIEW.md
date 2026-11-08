# Module 16 · Interview questions (with answers)

Short answers you can say out loud, with code and the usual follow-up.

[← Module 16](README.md) · [Quiz](QUIZ.md)

---

### 1. What kinds of tests do you write?

**Say:** I follow the **testing pyramid**:
- Many **unit** tests: one function or class, no I/O, milliseconds each.
- Some **integration** tests: my code plus a real DB or HTTP client.
- A few **end-to-end** tests through the API or a browser.

Unit tests give fast feedback. The higher layers prove the parts actually work together.

---

### 2. What is a pytest fixture?

**Say:** A function decorated with `@pytest.fixture` that provides setup to any test that names it as an argument. Code after `yield` is teardown. `scope` controls how often it runs (function, module, session). Shared fixtures go in `conftest.py`.

```python
@pytest.fixture
def client():
    app.dependency_overrides[get_db] = lambda: test_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

---

### 3. Mock vs stub vs fake?

**Say:**
- A **stub** returns canned answers.
- A **fake** is a lightweight working implementation, like an in-memory repository.
- A **mock** also **records calls** so you can assert how it was used (`assert_called_once_with`).

I prefer fakes for my own interfaces and mocks for third-party boundaries.

---

### 4. Where do you patch with `mock.patch`?

**Say:** **Where the name is looked up**, not where it's defined. If `weather.py` does `import requests` and calls `requests.get`, patch `"weather.requests.get"`. With `from requests import get`, patch `"weather.get"`.

---

### 5. How do you test code that depends on time or randomness?

**Say:** Inject the dependency: pass a `clock` or `now()` function, or a seeded `random.Random`. In tests, pass a fixed value. Libraries like `freezegun` or `time-machine` can also freeze `datetime.now()`.

---

### 6. What is `parametrize` for?

**Say:** It runs one test function with many input/expected pairs. Each pair is reported as a separate test, so you cover edge cases without copy-pasting:

```python
@pytest.mark.parametrize("pw, ok", [("abc", False), ("Str0ng!pw", True)])
def test_password(pw, ok):
    assert is_strong(pw) is ok
```

---

### 7. What is TDD? Do you use it?

**Say:** Test-Driven Development is a loop of **red → green → refactor**: write a small failing test, write the minimal code to pass it, then clean up. It leads to small, testable designs. I use it especially for bug fixes (write a test that reproduces the bug first) and for business rules.

---

### 8. Is 100% coverage the goal?

**Say:** No. Coverage shows which lines **ran**, not whether the behaviour is **correct**. I aim for high coverage on business logic (80–90% is common) and focus on edge cases and error paths. Coverage is most useful for finding **untested** code.

---

### 9. How do you test a FastAPI or Django endpoint?

**Say:** FastAPI: `TestClient(app)` plus `app.dependency_overrides` to swap the DB or external clients. Django: `django.test.TestCase` with the test client, where each test runs in a transaction that is rolled back. I assert the status code, the response JSON and side effects (a DB row created, an email queued).

---

### 10. What is property-based testing?

**Say:** Instead of writing examples, you state a **property** that must always hold, for example "decode(encode(x)) == x" or "the result is sorted". A library like **hypothesis** generates hundreds of inputs, including nasty edge cases, and shrinks any failure to the smallest example.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
