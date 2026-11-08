"""Module 16 · Fakes, mocks and monkeypatch: testing code with outside dependencies

TEACHING NOTES
  Why it matters  Tests that call real APIs are slow, flaky and can't simulate outages.
  Picture it      A mock is a stunt double: it stands in for the dangerous part and records what
                  happened.
  Watch out       Patch where the name is USED ('weather.requests.get'), not where it is
                  defined.
  In real jobs    Faking payment providers, email services and the clock in unit tests.
  Interview       Q: Mock vs stub vs fake?
                  A: Stub: canned answers. Fake: working light version. Mock: also records and
                     verifies calls.

Run:   pytest 16_testing/test_03_mocking.py -v
"""
from unittest.mock import Mock

import pytest

import weather
from weather import describe_weather


# --- 1. Dependency injection: pass a simple fake function ----------------------------------
def test_hot_city_with_a_fake():
    def fake_fetch(url):
        return {"temp_c": 31.4}
    assert describe_weather("Mumbai", fetch=fake_fetch) == "Mumbai: 31°C, hot"


# --- 2. Mock: a fake that also RECORDS how it was called ---------------------------------------
def test_mock_records_the_call():
    fake = Mock(return_value={"temp_c": 3})
    assert describe_weather("Oslo", fetch=fake) == "Oslo: 3°C, cold"
    fake.assert_called_once()                              # called exactly once?
    assert "city=Oslo" in fake.call_args.args[0]           # with the right URL?


# --- 3. Mock side_effect: simulate failures ---------------------------------------------------
def test_api_failure_bubbles_up():
    fake = Mock(side_effect=TimeoutError("api down"))
    with pytest.raises(TimeoutError):
        describe_weather("Augsburg", fetch=fake)


# --- 4. monkeypatch: replace something for the duration of ONE test ------------------------
def test_monkeypatch_the_real_function(monkeypatch):
    monkeypatch.setattr(weather, "fetch_json", lambda url: {"temp_c": 14})
    # describe_weather's default argument was bound at definition time,
    # so pass the patched function explicitly:
    assert describe_weather("Augsburg", fetch=weather.fetch_json) == "Augsburg: 14°C, mild"
    # after this test, pytest restores the original fetch_json automatically


@pytest.mark.parametrize(("temp", "feel"), [(25, "hot"), (5, "cold"), (6, "mild"), (24.9, "mild")])
def test_boundaries(temp, feel):
    assert describe_weather("X", fetch=lambda url: {"temp_c": temp}).endswith(feel)
