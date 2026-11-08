"""Solution · Exercise 8: Refactor to Pythonic code

Each function now uses the Module 8 tool that fits it best.
Run it:  python solutions/ex08_refactor_to_pythonic.py
"""


def squares_of_evens(numbers):
    # comprehension with a filter
    return [n * n for n in numbers if n % 2 == 0]


def number_lines(lines):
    # enumerate gives the number; start=1 so we don't add 1 by hand
    return [f"{i}: {line}" for i, line in enumerate(lines, start=1)]


def make_lookup(keys, values):
    # zip pairs the lists; dict() turns the pairs into a dictionary
    return dict(zip(keys, values))


def has_negative(numbers):
    # any() stops at the first True, just like the early return did
    return any(n < 0 for n in numbers)


def longest_word(words):
    # max with key=len; on a tie max keeps the first one
    return max(words, key=len)


def greet(name):
    # "" and None are both falsy, so "or" picks the default
    return f"Hello, {name or 'Guest'}!"


def first_and_last(items):
    # negative index -1 is the last item
    return items[0], items[-1]


def money(amount):
    # :,.2f = thousands separator + exactly 2 decimals
    return f"€{amount:,.2f}"


def sentence(words):
    # join is the right tool for building text from a list
    return " ".join(words)


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
    assert money(1234.5) == "€1,234.50"
    assert sentence(["learn", "python"]) == "learn python"
    print("All checks passed!")
