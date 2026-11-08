"""Module 16 · TDD: these tests were written BEFORE slugify(), one at a time.

Read them top to bottom: each one adds one small requirement.

TEACHING NOTES
  Why it matters  Writing the test first forces a clear, small design and proves the test can
                  fail.
  Picture it      Red, green, refactor: a traffic light cycle repeated in tiny steps.
  Watch out       Don't write five tests at once; one failing test, then the simplest code that
                  passes.
  In real jobs    Bug fixes start with a failing test that reproduces the bug.
  Interview       Q: What is TDD?
                  A: Write a failing test, make it pass with minimal code, refactor, repeat.

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
