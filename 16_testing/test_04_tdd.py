"""Module 16 · TDD: these tests were written BEFORE slugify(), one at a time.

Read them top to bottom: each one adds one small requirement.

Run:   pytest 16_testing/test_04_tdd.py -v
"""
from slugify import slugify


def test_lowercases():
    assert slugify("Python") == "python"


def test_replaces_spaces_and_symbols():
    assert slugify("Hello, World!") == "hello-world"


def test_no_leading_or_trailing_dash():
    assert slugify("  --Python Pro--  ") == "python-pro"


def test_removes_accents():
    assert slugify("Café Münchën") == "cafe-munchen"


def test_respects_max_length():
    slug = slugify("a very long title " * 10, max_length=20)
    assert len(slug) <= 20
    assert not slug.endswith("-")
