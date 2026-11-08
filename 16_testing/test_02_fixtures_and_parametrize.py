"""Module 16 · Fixtures and parametrize

FIXTURE      = reusable setup. A test asks for it by NAME as a parameter, and
               pytest builds it fresh for that test (and cleans up afterwards).
PARAMETRIZE  = run the same test with many inputs; each one is reported separately.

TEACHING NOTES
  Why it matters  Copy-pasted setup and near-identical tests make suites slow to write and hard
                  to change.
  Picture it      A fixture is a kitchen helper that prepares ingredients for any test that asks
                  for them by name.
  Watch out       Fixtures with scope='session' share state between tests: use them only for
                  expensive, read-only setup.
  In real jobs    Test clients, test databases and fake users as fixtures in conftest.py.
  Interview       Q: What is a pytest fixture?
                  A: A function that provides setup (and teardown after yield) to tests that
                     request it by name.

Run:   pytest 16_testing/test_02_fixtures_and_parametrize.py -v
"""
import json

import pytest

from pricing import apply_discount, cart_total, parse_price


# --- 1. Using a fixture from conftest.py -----------------------------------------------
def test_cart_total_with_fixture(sample_cart):
    assert cart_total(sample_cart) == pytest.approx(28.6)


def test_fixture_is_fresh_every_time(sample_cart):
    sample_cart["laptop"] = (899.0, 1)          # changing it here...
    assert len(sample_cart) == 3                # ...doesn't affect any other test


# --- 2. A fixture with clean-up: code after yield runs after the test ------------------
@pytest.fixture
def price_file(tmp_path):                       # tmp_path: a built-in fixture, a temp folder
    path = tmp_path / "prices.json"
    path.write_text(json.dumps({"tea": "€2.50", "cake": "€3,10"}))
    yield path
    # clean-up would go here (tmp_path is deleted automatically anyway)


def test_load_prices(price_file):
    raw = json.loads(price_file.read_text())
    assert parse_price(raw["tea"]) == 2.5


# --- 3. Parametrize: one test function, many cases -----------------------------------------
@pytest.mark.parametrize(
    ("price", "percent", "expected"),
    [
        (100, 10, 90.0),
        (100, 0, 100.0),
        (19.99, 50, 9.99),    # 9.995 is stored as 9.99499..., so it rounds DOWN: floats!
        (10, 100, 0.0),
    ],
)
def test_discount_cases(price, percent, expected):
    assert apply_discount(price, percent) == expected


@pytest.mark.parametrize("bad_percent", [-1, 101, 1000])
def test_invalid_percent(bad_percent):
    with pytest.raises(ValueError):
        apply_discount(10, bad_percent)
