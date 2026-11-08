# Python Pro – Module 16 Knowledge Check
**Testing with pytest**

Try to answer without looking. The answer key is at the bottom, and each answer says which file to revisit.

---

### Part A – Multiple choice

**1. Which files and functions does pytest run automatically?**
- A) Every `.py` file
- B) Files named `test_*.py` and functions named `test_*`
- C) Only files in a `tests` folder
- D) Functions marked `@test`

**2. What are the three steps of a clear test?**
- A) Import, run, print
- B) Arrange, act, assert
- C) Setup, teardown, report
- D) Write, commit, push

**3. How do you test that code raises a `ValueError`?**
- A) `assert raises ValueError`
- B) `with pytest.raises(ValueError): ...`
- C) `try: ... except: pass`
- D) `assert ValueError in code`

**4. Why is `assert 0.1 + 0.2 == 0.3` a bad test?**
- A) It's slow
- B) Floats are approximations, so it fails; use `pytest.approx`
- C) pytest doesn't support floats
- D) It's a good test

**5. What is a fixture?**
- A) A broken test
- B) Reusable setup that a test requests by naming it as a parameter
- C) A global variable
- D) A type of assert

**6. Where do you put fixtures that several test files share?**
- A) `__init__.py`
- B) `conftest.py`
- C) `setup.py`
- D) `fixtures.txt`

**7. What does `@pytest.mark.parametrize` do?**
- A) Runs tests in parallel
- B) Runs the same test with many inputs, each reported separately
- C) Skips a test
- D) Sets up a fixture

**8. What is `tmp_path`?**
- A) A setting
- B) A built-in fixture: a fresh temporary folder for each test
- C) The current folder
- D) A mock

**9. Why shouldn't unit tests call a real web API?**
- A) It's not allowed
- B) It's slow, needs a network, and its answers change, so tests become flaky
- C) APIs can't be called from Python
- D) pytest blocks it

**10. What can a `Mock` do that a simple fake function can't?**
- A) Run faster
- B) Record how it was called (`assert_called_once`, `call_args`)
- C) Connect to the internet
- D) Nothing

**11. What's the TDD cycle?**
- A) Code, test, deploy
- B) Red (failing test), green (make it pass), refactor
- C) Write all tests at the end
- D) Test only in production

**12. To catch a bug in the "needs a digit" rule, a test password should…**
- A) Break every rule at once
- B) Break ONLY the digit rule, for example `"SecretPass"`
- C) Be very long
- D) Be empty

---

### Part B – What happens?

**13.**
```python
def test_total():
    assert cart_total({"a": (2.0, 3)}) == 7
```
`cart_total` returns `6.0`. What does pytest show?

**14.**
```python
@pytest.mark.parametrize("n", [1, 2, 3])
def test_positive(n):
    assert n > 0
```
How many tests does pytest report?

---

### Part C – Fix it

**15.** This test passes even though `apply_discount(10, 150)` doesn't raise. Why?
```python
def test_invalid():
    try:
        apply_discount(10, 150)
    except ValueError:
        pass
```

**16.** Two tests share and change the same global `cart` list, so they pass or fail depending on their order. Fix it.

---

<details>
<summary><b>Answer key (click to open)</b></summary>

| # | Answer | Explanation | Revisit |
|---|--------|-------------|---------|
| 1 | B | Naming conventions drive discovery. | `test_01_basics.py` |
| 2 | B | Arrange, act, assert. | `test_01_basics.py` |
| 3 | B | It fails if nothing is raised. | `test_01_basics.py` |
| 4 | B | `0.1 + 0.2` is `0.30000000000000004`. | `test_01_basics.py` |
| 5 | B | Requested by name, built fresh. | `test_02_fixtures_and_parametrize.py` |
| 6 | B | It's loaded automatically. | `conftest.py` |
| 7 | B | One function, many cases. | `test_02_fixtures_and_parametrize.py` |
| 8 | B | It's cleaned up for you. | `test_02_fixtures_and_parametrize.py` |
| 9 | B | Use fakes, mocks or dependency injection. | `weather.py`, `test_03_mocking.py` |
| 10 | B | It records calls for assertions. | `test_03_mocking.py` |
| 11 | B | Red → green → refactor. | `test_04_tdd.py`, `slugify.py` |
| 12 | B | One broken rule per test. | `ex16_test_password.py` |
| 13 | A failure with `assert 6.0 == 7`, showing both values. | pytest rewrites plain asserts. | `test_01_basics.py` |
| 14 | 3 | One per parameter. | `test_02_fixtures_and_parametrize.py` |
| 15 | Nothing fails when no error is raised. Use `with pytest.raises(ValueError):`. | | `test_01_basics.py` |
| 16 | Make `cart` a fixture so each test gets a fresh one. | Tests must be independent. | `conftest.py` |

</details>

---

If this module helped you, you can support the channel:

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
