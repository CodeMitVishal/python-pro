"""Exercise 16 · Write tests that catch bugs

is_strong_password() below is CORRECT. Your job is to write pytest tests for it
that are good enough to catch BUGGY versions of it.

The rules a strong password must follow:
  - at least 8 characters
  - at least one uppercase letter
  - at least one lowercase letter
  - at least one digit
  - no spaces
  - it must be a str: anything else raises TypeError

Write your tests in the TODO section (test_... functions using assert and
pytest.raises; @pytest.mark.parametrize is welcome).

Check your tests in two ways:
    pytest exercises/ex16_test_password.py        <- your tests pass on the real function
    python exercises/ex16_test_password.py        <- your tests must FAIL on each of 6 buggy versions

Stuck? Compare with solutions/ex16_test_password.py
"""
import pytest


def is_strong_password(pw):
    if not isinstance(pw, str):
        raise TypeError("password must be a string")
    return (
        len(pw) >= 8
        and any(c.isupper() for c in pw)
        and any(c.islower() for c in pw)
        and any(c.isdigit() for c in pw)
        and " " not in pw
    )


# ===================== TODO: write your tests below =====================

def test_example_strong_password():
    assert is_strong_password("Secret123") is True


# =========================================================================


# --- The bug hunt: do not change anything below this line ----------------------------------
MUTANTS = {
    "allows 7 characters": lambda pw: len(pw) >= 7 and any(c.isupper() for c in pw)
        and any(c.islower() for c in pw) and any(c.isdigit() for c in pw) and " " not in pw,
    "forgets uppercase": lambda pw: len(pw) >= 8 and any(c.islower() for c in pw)
        and any(c.isdigit() for c in pw) and " " not in pw,
    "forgets lowercase": lambda pw: len(pw) >= 8 and any(c.isupper() for c in pw)
        and any(c.isdigit() for c in pw) and " " not in pw,
    "forgets digits": lambda pw: len(pw) >= 8 and any(c.isupper() for c in pw)
        and any(c.islower() for c in pw) and " " not in pw,
    "allows spaces": lambda pw: len(pw) >= 8 and any(c.isupper() for c in pw)
        and any(c.islower() for c in pw) and any(c.isdigit() for c in pw),
    "no TypeError": lambda pw: isinstance(pw, str) and len(pw) >= 8 and any(c.isupper() for c in pw)
        and any(c.islower() for c in pw) and any(c.isdigit() for c in pw) and " " not in pw,
}


def _run_my_tests():
    """Run every test_ function in this file; return True if all pass."""
    for name, func in list(globals().items()):
        if not name.startswith("test_"):
            continue
        params = getattr(func, "pytestmark", [])
        cases = [()]
        for mark in params:
            if mark.name == "parametrize":
                cases = [c if isinstance(c, tuple) else (c,) for c in mark.args[1]]
        for case in cases:
            try:
                func(*case)
            except (Exception, pytest.fail.Exception):   # assert failed, or pytest.raises failed
                return False
    return True


if __name__ == "__main__":
    real = is_strong_password
    assert _run_my_tests(), "your tests fail on the CORRECT function: fix your tests first"
    survivors = []
    for bug, mutant in MUTANTS.items():
        globals()["is_strong_password"] = mutant
        if _run_my_tests():
            survivors.append(bug)
    globals()["is_strong_password"] = real
    caught = len(MUTANTS) - len(survivors)
    print(f"Your tests caught {caught}/{len(MUTANTS)} bugs.")
    for bug in survivors:
        print(f"  not caught: {bug}")
    assert not survivors, "add tests until every bug is caught"
    print("All checks passed!")
