# Module 16 · Testing with pytest

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-16.pdf) · [Interview Q&A](INTERVIEW.md)

Prove your code works, and keep it working. Plain asserts, fixtures, parametrize, mocks and test-driven development.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| pytest basics | [`test_01_basics.py`](test_01_basics.py) | arrange-act-assert, `pytest.raises`, `pytest.approx` |
| Fixtures & parametrize | [`test_02_fixtures_and_parametrize.py`](test_02_fixtures_and_parametrize.py) | reusable setup, `tmp_path`, many cases |
| Fakes, mocks & monkeypatch | [`test_03_mocking.py`](test_03_mocking.py) | test code that calls a web API, without the network |
| TDD | [`test_04_tdd.py`](test_04_tdd.py) | red → green → refactor, building `slugify()` |
| Property-based tests & coverage | [`test_05_hypothesis_and_coverage.py`](test_05_hypothesis_and_coverage.py) | hypothesis, `pytest --cov` |

Install pytest and run the whole module:

```bash
pip install pytest
```

```bash
pytest 16_testing -v
```

The code under test is in `pricing.py`, `weather.py` and `slugify.py`; shared fixtures live in `conftest.py`.

## Exercise: Write tests that catch bugs

Your tests must catch 6 planted bugs in a password checker (mutation testing).

- Start here: [`exercises/ex16_test_password.py`](../exercises/ex16_test_password.py)
- Solution: [`solutions/ex16_test_password.py`](../solutions/ex16_test_password.py)

## Knowledge check

Preparing for interviews? Read the [Module 16 interview questions](INTERVIEW.md): short answers you can say out loud.


Test yourself with the [Module 16 quiz](QUIZ.md). The answer key is at the bottom.

**Next up:** [Module 17 · Concurrency](../17_concurrency/README.md) →

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
