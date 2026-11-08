"""Module 16 · Code that talks to the outside world (an HTTP API).

Tests must not call the real API: it's slow, needs a network and a key, and
its answers change. Two ways to swap it out in tests:
  1. dependency injection: pass the fetch function in (easy to replace)
  2. mocking: patch the real function during a test (test_03_mocking.py)
"""
import json
import urllib.request


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=5) as resp:   # real network call
        return json.load(resp)


def describe_weather(city: str, fetch=fetch_json) -> str:
    """`fetch` defaults to the real function, but tests can pass a fake one."""
    data = fetch(f"https://api.example.com/weather?city={city}")
    temp = data["temp_c"]
    if temp >= 25:
        feel = "hot"
    elif temp <= 5:
        feel = "cold"
    else:
        feel = "mild"
    return f"{city}: {temp:.0f}°C, {feel}"
