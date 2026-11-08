"""Exercise 14 · Build a command-line tool with argparse

Build `wordtool` with two subcommands:

  wordtool stats "the cat and the hat"
      -> words: 5, unique: 4, chars: 19

  wordtool top "the cat and the hat" --n 1
      -> the: 2

Rules:
  - main(argv=None) builds the parser and parses argv (None = real command line)
  - `top` has an optional --n (int, default 3)
  - counting is case-insensitive; split on whitespace
  - main() returns 0

Run it to check your work:
    python exercises/ex14_wordtool_cli.py
Then try it for real:
    python exercises/ex14_wordtool_cli.py top "a b a c a b" --n 2

Stuck? Compare with solutions/ex14_wordtool_cli.py
"""
import argparse
from collections import Counter


def main(argv=None):
    """TODO: build the parser with 'stats' and 'top' subcommands, then print the results."""
    return 0


# --- Checks: run `python exercises/ex14_wordtool_cli.py` with NO arguments ------------
def _check():
    import io
    from contextlib import redirect_stdout

    def run(args):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(args)
        return code, out.getvalue().strip()

    assert run(["stats", "the cat and the hat"]) == (0, "words: 5, unique: 4, chars: 19")
    assert run(["top", "The cat and the hat", "--n", "1"]) == (0, "the: 2")
    assert run(["top", "a b a c a b"]) == (0, "a: 3\nb: 2\nc: 1")
    print("All checks passed!")


if __name__ == "__main__":
    import sys
    _check() if len(sys.argv) == 1 else sys.exit(main())
