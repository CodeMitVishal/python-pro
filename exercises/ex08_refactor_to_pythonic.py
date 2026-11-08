"""Exercise 8 · Refactor to Pythonic code

Every function below is written the long, "un-Pythonic" way, and money()
also has a formatting bug.
Your job: rewrite each one using what you learned in Module 8, so it is
shorter and easier to read. Keep the same name and the same results.

Tools to reach for:
  comprehensions · unpacking · enumerate · zip · sorted(key=...) ·
  any / all · "or" defaults · f-string formatting · " ".join(...)

Run this file now: the money() check fails. When you're done, every check
at the bottom must pass:
    python exercises/ex08_refactor_to_pythonic.py

Stuck? Compare with solutions/ex08_refactor_to_pythonic.py
"""


def squares_of_evens(numbers):
    """Return the squares of the even numbers only."""
    result = []
    for n in numbers:
        if n % 2 == 0:
            result.append(n * n)
    return result


def number_lines(lines):
    """Return lines prefixed with their line number, starting at 1."""
    result = []
    for i in range(len(lines)):
        result.append(str(i + 1) + ": " + lines[i])
    return result


def make_lookup(keys, values):
    """Pair up two lists into a dictionary."""
    lookup = {}
    for i in range(len(keys)):
        lookup[keys[i]] = values[i]
    return lookup


def has_negative(numbers):
    """True if at least one number is below zero."""
    for n in numbers:
        if n < 0:
            return True
    return False


def longest_word(words):
    """Return the longest word (the first one if there is a tie)."""
    best = words[0]
    for w in words:
        if len(w) > len(best):
            best = w
    return best


def greet(name):
    """Greet the user, or 'Guest' when the name is empty."""
    if name == "" or name is None:
        name = "Guest"
    return "Hello, " + name + "!"


def first_and_last(items):
    """Return the first and last item as a tuple."""
    first = items[0]
    last = items[len(items) - 1]
    return (first, last)


def money(amount):
    """Format a number as money with a thousands separator and 2 decimals."""
    return "€" + str(round(amount, 2))  # Bug-prone: 1234.5 -> '€1234.5'


def sentence(words):
    """Join words into one sentence with spaces."""
    text = ""
    for w in words:
        text = text + w + " "
    return text.strip()


# --- Checks: do not change anything below this line ----------------------------
if __name__ == "__main__":
    assert squares_of_evens([1, 2, 3, 4]) == [4, 16]
    assert number_lines(["a", "b"]) == ["1: a", "2: b"]
    assert make_lookup(["x", "y"], [1, 2]) == {"x": 1, "y": 2}
    assert has_negative([3, -1, 2]) is True
    assert has_negative([3, 1]) is False
    assert longest_word(["hi", "python", "code"]) == "python"
    assert greet("") == "Hello, Guest!"
    assert greet("Vishal") == "Hello, Vishal!"
    assert first_and_last([1, 2, 3]) == (1, 3)
    assert money(1234.5) == "€1,234.50", "Use an f-string format spec like :,.2f"
    assert sentence(["learn", "python"]) == "learn python"
    print("All checks passed! Now make each function Pythonic.")
