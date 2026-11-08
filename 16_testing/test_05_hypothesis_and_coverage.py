"""Module 16 · Property-based testing (hypothesis) and coverage

  pip install hypothesis pytest-cov

EXAMPLE-based tests check the cases YOU think of. PROPERTY-based tests describe
a rule that must hold for ALL inputs, and hypothesis generates hundreds of inputs
(empty strings, huge numbers, unicode, edge cases) to try to break it. When it
finds a failure, it shrinks it to the smallest example.

COVERAGE shows which lines your tests never run:
    pytest 16_testing --cov=16_testing --cov-report=term-missing
100% coverage doesn't mean bug-free, but 40% means most code is untested.

TEACHING NOTES
  Why it matters  Hand-picked examples miss edge cases; property tests and coverage find what
                  you forgot.
  Picture it      Hypothesis is a fuzzing robot: you state a rule, it throws hundreds of nasty
                  inputs at it.
  Watch out       100% coverage doesn't mean correct; it only shows which lines ran.
  In real jobs    Property tests for parsers and serializers; coverage gates in CI (e.g. 85%).
  Interview       Q: Is 100% coverage the goal?
                  A: No; test behaviour and edge cases. Coverage is a tool to find untested
                     code.

Run:   pytest 16_testing/test_05_hypothesis_and_coverage.py -v
"""
from hypothesis import given
from hypothesis import strategies as st

from pricing import apply_discount
from slugify import slugify


@given(price=st.floats(min_value=0, max_value=1e6), percent=st.floats(min_value=0, max_value=100))
def test_discount_never_increases_price_or_goes_negative(price, percent):
    result = apply_discount(price, percent)
    assert 0 <= result <= round(price, 2) + 0.01          # a PROPERTY, true for every input


@given(st.text())
def test_slug_only_has_safe_characters(title):
    slug = slugify(title)
    assert all(c.isascii() and (c.isalnum() or c == "-") for c in slug)
    assert not slug.startswith("-") and not slug.endswith("-")


@given(st.text(max_size=200))
def test_slugify_is_idempotent(title):
    once = slugify(title)
    assert slugify(once) == once                          # slugifying twice changes nothing


@given(st.lists(st.integers()))
def test_sorting_properties(xs):
    out = sorted(xs)
    assert len(out) == len(xs)                            # nothing lost
    assert all(a <= b for a, b in zip(out, out[1:]))      # ordered
