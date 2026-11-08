"""Solution · Exercise 11: Write lazy generators

Run it:  python solutions/ex11_generators.py
"""
from itertools import count, islice


def chunked(items, size):
    chunk = []
    for item in items:               # works for any iterable, even endless ones
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []               # start a NEW list for the next chunk
    if chunk:                        # leftovers at the end
        yield chunk


def running_average(numbers):
    total = 0
    for n, value in enumerate(numbers, start=1):
        total += value               # only two numbers in memory: total and n
        yield total / n


def valid_numbers(lines):
    for line in lines:
        try:
            yield int(line)          # int() ignores surrounding spaces
        except ValueError:
            continue                 # skip "x", "3.5", ...


if __name__ == "__main__":
    import types
    for f in (chunked, running_average, valid_numbers):
        assert isinstance(f([], 1) if f is chunked else f([]), types.GeneratorType)

    assert list(chunked("abcde", 2)) == [["a", "b"], ["c", "d"], ["e"]]
    assert list(islice(chunked(count(), 3), 2)) == [[0, 1, 2], [3, 4, 5]]
    assert list(running_average([2, 4, 6])) == [2.0, 3.0, 4.0]
    assert list(valid_numbers(["10", "x", " 7 ", "3.5", "-2"])) == [10, 7, -2]
    print("All checks passed!")
