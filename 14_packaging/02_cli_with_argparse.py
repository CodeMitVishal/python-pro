"""Module 14 · Command-line tools with argparse

argparse turns  python tool.py add "Buy milk" --priority high
into a clean object:  args.command == "add", args.title == "Buy milk", ...
and gives you --help, type checking and error messages for free.

Run it:  python 14_packaging/02_cli_with_argparse.py
Try:     python 14_packaging/02_cli_with_argparse.py --help
         python 14_packaging/02_cli_with_argparse.py greet Vishal --times 2 --shout
"""
import argparse


def build_parser():
    parser = argparse.ArgumentParser(prog="demo", description="A tiny argparse demo.")
    parser.add_argument("-v", "--verbose", action="store_true", help="print more details")

    sub = parser.add_subparsers(dest="command", required=True)   # git-style subcommands

    greet = sub.add_parser("greet", help="say hello")
    greet.add_argument("name")                                   # positional, required
    greet.add_argument("--times", type=int, default=1)           # converted to int for you
    greet.add_argument("--shout", action="store_true")           # a True/False flag

    add = sub.add_parser("add", help="add numbers")
    add.add_argument("numbers", nargs="+", type=float)           # one or more values
    return parser


def main(argv=None):
    """argv=None reads sys.argv; passing a list makes main() easy to test."""
    args = build_parser().parse_args(argv)
    if args.verbose:
        print("parsed:", vars(args))
    if args.command == "greet":
        text = f"Hello, {args.name}!"
        for _ in range(args.times):
            print(text.upper() if args.shout else text)
    elif args.command == "add":
        print(sum(args.numbers))
    return 0


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:                       # no arguments: run a few examples
        for example in (["greet", "Vishal", "--times", "2"],
                        ["-v", "add", "1.5", "2", "3"]):
            print(f"$ demo {' '.join(example)}")
            main(example)
    else:
        raise SystemExit(main())
