"""Solution · Exercise 14: Build a command-line tool with argparse

Run the checks:  python solutions/ex14_wordtool_cli.py
Use it:          python solutions/ex14_wordtool_cli.py top "a b a c a b" --n 2
"""
import argparse
from collections import Counter


def build_parser():
    parser = argparse.ArgumentParser(prog="wordtool", description="Word statistics.")
    sub = parser.add_subparsers(dest="command", required=True)

    stats = sub.add_parser("stats", help="count words and characters")
    stats.add_argument("text")

    top = sub.add_parser("top", help="most common words")
    top.add_argument("text")
    top.add_argument("--n", type=int, default=3, help="how many (default 3)")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    words = args.text.lower().split()

    if args.command == "stats":
        print(f"words: {len(words)}, unique: {len(set(words))}, chars: {len(args.text)}")
    elif args.command == "top":
        for word, count in Counter(words).most_common(args.n):
            print(f"{word}: {count}")
    return 0


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
