"""Exercise 11 · Write lazy generators

Write each function as a GENERATOR (use yield). None of them may build a
full list of the input, so they must work on endless streams too.

  1. chunked(items, size)      -> yield lists of `size` items; the last may be shorter
                                  chunked("abcde", 2) -> ['a','b'], ['c','d'], ['e']
  2. running_average(numbers)  -> after each number, yield the average so far
                                  running_average([2, 4, 6]) -> 2.0, 3.0, 4.0
  3. valid_numbers(lines)      -> yield int(line) for each line that is a whole
                                  number; silently skip anything else

Run it to check your work:
    python exercises/ex11_generators.py

Stuck? Compare with solutions/ex11_generators.py
"""
from itertools import count, islice


def chunked(items, size):
    """TODO 1"""


def running_average(numbers):
    """TODO 2"""


def valid_numbers(lines):
    """TODO 3"""


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    import types
    for f in (chunked, running_average, valid_numbers):
        assert isinstance(f([], 1) if f is chunked else f([]), types.GeneratorType), \
            f"{f.__name__} must be a generator (use yield)"

    assert list(chunked("abcde", 2)) == [["a", "b"], ["c", "d"], ["e"]]
    assert list(islice(chunked(count(), 3), 2)) == [[0, 1, 2], [3, 4, 5]], "must work on endless input"
    assert list(running_average([2, 4, 6])) == [2.0, 3.0, 4.0]
    assert list(valid_numbers(["10", "x", " 7 ", "3.5", "-2"])) == [10, 7, -2]
    print("All checks passed!")
