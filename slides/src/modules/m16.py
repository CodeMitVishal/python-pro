"""Slides · Module 16 · Testing with pytest"""
from teach_kit import PYTEST, code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 16 · Testing with pytest"
SLIDES = [
 cover("16", "Testing with pytest", "Prove your code works, change it without fear, and pass the \"how do you test?\" interview question.",
       [("pytest basics", "test_01_basics.py"), ("Fixtures &amp; parametrize", "test_02_fixtures_and_parametrize.py"),
        ("Mocks, fakes, monkeypatch", "test_03_mocking.py"), ("TDD: test first", "test_04_tdd.py"),
        ("Property tests &amp; coverage", "test_05_hypothesis_and_coverage.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Testing", "Why write tests at all?",
     "You fix a discount bug on Friday. On Monday, refunds are broken: your fix changed a function that refunds also used.<br><br>"
     "Clicking through the app by hand after every change doesn't scale.",
     "Automated tests check the behaviour <b>in seconds, every time</b>. They are the safety net that lets you change code with confidence."),

 picture(M, "Testing", "The testing pyramid",
     "&#128314; Many <b>small, fast</b> tests at the bottom, fewer <b>slow, broad</b> ones at the top. "
     "Each layer catches different bugs.",
     [("unit tests (~70%)", "one function, no DB, no network: milliseconds"),
      ("integration (~20%)", "your code + real DB / API client"),
      ("end-to-end (~10%)", "the whole app through HTTP or a browser")],
     "Interviewers love this picture. Name the layers and say what you test in each."),

 code_out(M, "pytest basics", "A test is a function that asserts", '''
import pytest

def price_with_vat(net, rate=0.19):
    if net < 0:
        raise ValueError("net price can't be negative")
    return round(net * (1 + rate), 2)

def test_adds_vat():
    assert price_with_vat(100) == 119.0

def test_custom_rate():
    assert price_with_vat(100, rate=0.07) == 107.0

def test_negative_price_is_rejected():
    with pytest.raises(ValueError, match="negative"):
        price_with_vat(-1)''', after=PYTEST,
     steps=["Files <b>test_*.py</b>, functions <b>test_*</b>: pytest finds them.", "A plain <b>assert</b>; pytest shows both values on failure.",
            "<b>pytest.raises</b> tests the error path too."]),

 code_out(M, "Fixtures and parametrize", "Reuse setup, test many cases", '''
import pytest

class Cart:
    def __init__(self): self.items = []
    def add(self, price, qty=1): self.items.append(price * qty)
    def total(self): return sum(self.items)

@pytest.fixture
def cart():                      # fresh setup for EVERY test
    c = Cart()
    c.add(10, qty=2)
    return c

def test_total(cart):
    assert cart.total() == 20

@pytest.mark.parametrize("price, qty, expected", [
    (5, 1, 25), (5, 2, 30), (0, 9, 20),
])
def test_add(cart, price, qty, expected):
    cart.add(price, qty)
    assert cart.total() == expected''', after=PYTEST,
     steps=["A <b>fixture</b> is requested by its <b>name</b> as an argument.", "<b>parametrize</b>: one test, many inputs.",
            "Shared fixtures live in <b>conftest.py</b>."]),

 mistake(M, "Mocking", "Tests that call the real world",
     '''
def test_weather():
    # calls the REAL API: slow, flaky,
    # needs internet, may cost money
    assert get_temperature("Augsburg") > -50''',
     "The test fails when the Wi-Fi drops or the API changes, and you can't test \"API is down\" at all.",
     '''
def test_weather(monkeypatch):
    def fake_get(url, **kw):
        return FakeResponse({"temp": 21.5})
    monkeypatch.setattr("weather.requests.get", fake_get)
    assert get_temperature("Augsburg") == 21.5''',
     "Replace the <b>boundary</b> (HTTP, DB, clock) with a fake. Fast, repeatable, and you can simulate errors."),

 code_out(M, "Mocking", "unittest.mock: check how it was called", '''
from unittest.mock import Mock

def notify_if_low(stock, item, mailer):
    if stock < 5:
        mailer.send("ops@shop.de", f"{item} low: {stock} left")

mailer = Mock()
notify_if_low(3, "lamp", mailer)
mailer.send.assert_called_once_with("ops@shop.de", "lamp low: 3 left")
print("called:", mailer.send.call_args)

mailer = Mock()
notify_if_low(50, "lamp", mailer)
mailer.send.assert_not_called()
print("not called when stock is fine")

flaky = Mock(side_effect=ConnectionError("timeout"))
try:
    flaky()
except ConnectionError as e:
    print("simulated failure:", e)''',
     steps=["A <b>Mock</b> accepts any call and records it.", "<b>side_effect</b> simulates errors.",
            "Mock <b>where it's used</b>: patch <b>\"weather.requests.get\"</b>, not \"requests.get\"."]),

 trace(M, "TDD", "Test-driven development: red, green, refactor", ["Step", "You do", "Result"],
       [["<b style=\"color:#C2413B\">1 RED</b>", "write ONE small failing test for the next behaviour", "the test fails (good!)"],
        ["<b style=\"color:#2E7D5B\">2 GREEN</b>", "write the simplest code that passes", "all tests pass"],
        ["<b>3 REFACTOR</b>", "clean up names and duplication", "tests stay green"],
        ["repeat", "the next behaviour", "the design grows in small, safe steps"]],
       "Lesson <b>test_04_tdd.py</b> builds <b>slugify()</b> exactly like this, one test at a time."),

 code_out(M, "Property-based testing", "Let hypothesis invent the inputs", '''
from hypothesis import given, strategies as st

def slugify(text):
    return "-".join(text.lower().split())

@given(st.text())
def test_slug_has_no_spaces(text):
    assert " " not in slugify(text)

@given(st.text())
def test_slug_is_stable(text):          # slugify twice = once
    assert slugify(slugify(text)) == slugify(text)''', after=PYTEST,
     steps=["You state a <b>rule</b>; hypothesis tries hundreds of inputs.", "It finds edge cases you'd never type: tabs, emoji, empty strings.",
            "Coverage: <b>pytest --cov=src</b> shows untested lines."]),

 job(M, "Testing", "Testing at work", [
     ("API tests with TestClient", '''
def test_create_order(client):
    r = client.post("/orders", json={"item": "lamp"})
    assert r.status_code == 201'''),
     ("A test database per run", '''
@pytest.fixture
def db(): engine = create_engine("sqlite://"); ...'''),
     ("Django tests", '''
class OrderTests(TestCase):
    def test_list(self): ...'''),
     ("CI runs everything", '''
- run: pytest --cov=src --cov-fail-under=85'''),
 ]),

 interview(M, "How do you test code that calls an external API or database?",
     ["Keep the external call behind a small boundary (a client class or repository).",
      "In <b>unit</b> tests, replace it with a <b>fake</b> or a <b>Mock</b> (monkeypatch / mock.patch where it's <b>used</b>).",
      "Simulate failures too: timeouts, 500s, empty results.",
      "In <b>integration</b> tests, use a real test database (SQLite in memory or a Postgres container).",
      "Run a few <b>end-to-end</b> tests against the deployed staging app."],
     None,
     "\"Mock vs stub vs fake?\" (a stub returns canned answers; a fake is a working light version, like an in-memory repo; a mock also records and verifies calls)."),

 interview(M, "What is a pytest fixture? What is conftest.py?",
     ["A fixture is a function that provides <b>setup</b> (and optional teardown) for tests that ask for it by name.",
      "Code after <b>yield</b> runs as teardown: close connections, delete temp files.",
      "<b>scope</b> controls reuse: function (default), module, session.",
      "<b>conftest.py</b> holds fixtures shared by every test in its folder; pytest loads it automatically."],
     '''
@pytest.fixture(scope="session")
def engine():
    eng = create_engine("sqlite://")
    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()''',
     "\"What's a good coverage percentage?\" (80-90% is common, but 100% coverage doesn't mean correct code: test behaviour and edge cases, not lines)."),

 recap(M, "Module 16 in 6 lines",
     ["Pyramid: many <b>unit</b>, some <b>integration</b>, few <b>end-to-end</b> tests.",
      "<b>assert</b> + <b>pytest.raises</b> for the happy and the error path.",
      "<b>Fixtures</b> for setup, <b>parametrize</b> for many cases, <b>conftest.py</b> to share.",
      "Fake the <b>boundaries</b> (HTTP, DB, time); patch where it's used.",
      "TDD: <b>red, green, refactor</b> in tiny steps.",
      "<b>hypothesis</b> finds edge cases; coverage finds untested code."],
     "Do <b>exercises/ex16_test_password.py</b>: write the tests for a password checker."),
]
