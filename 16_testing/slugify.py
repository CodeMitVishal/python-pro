"""Module 16 · Built with TDD (test-driven development)

The tests in test_04_tdd.py were written FIRST, one at a time:
  RED      write a small failing test for the next behaviour
  GREEN    write the simplest code that makes it pass
  REFACTOR clean up, with the tests as a safety net
Then repeat. The comments show which test drove each line.
"""
import re
import unicodedata


def slugify(title: str, max_length: int = 50) -> str:
    """'Hello, World!' -> 'hello-world' (for URLs and file names)."""
    text = unicodedata.normalize("NFKD", title)                 # test_removes_accents
    text = text.encode("ascii", "ignore").decode()
    text = text.lower()                                         # test_lowercases
    text = re.sub(r"[^a-z0-9]+", "-", text)                    # test_replaces_spaces_and_symbols
    text = text.strip("-")                                      # test_no_leading_or_trailing_dash
    return text[:max_length].rstrip("-")                       # test_respects_max_length
