"""Solution · Exercise 16: Write tests that catch bugs

One test per rule, each with a password that breaks ONLY that rule.
That's the trick: if a test password breaks two rules, a bug in one
of them can hide behind the other.

    pytest solutions/ex16_test_password.py
    python solutions/ex16_test_password.py
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


# ===================== tests =====================

def test_example_strong_password():
    assert is_strong_password("Secret123") is True


def test_exactly_8_characters_is_enough():
    assert is_strong_password("Secret12") is True


@pytest.mark.parametrize(
    "weak",
    [
        "Secre12",        # 7 characters (only the length rule is broken)
        "secret123",      # no uppercase
        "SECRET123",      # no lowercase
        "SecretPass",     # no digit
        "Secret 123",     # a space
    ],
)
def test_weak_passwords(weak):
    assert is_strong_password(weak) is False


@pytest.mark.parametrize("not_text", [None, 12345678, ["Secret123"]])
def test_non_strings_raise(not_text):
    with pytest.raises(TypeError):
        is_strong_password(not_text)

# ==================================================


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
            except (Exception, pytest.fail.Exception):
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
