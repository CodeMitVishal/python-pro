"""Module 8 · Structural pattern matching: match / case (Python 3.10+)

`match` checks the SHAPE of data, not just its value, and pulls pieces out in
the same step. It shines with nested data like JSON, commands and events.

Run it:  python 08_pythonic_code/07_pattern_matching.py
"""
from dataclasses import dataclass


# --- 1. Literal values, alternatives with |, and the wildcard _ ---------------------------
def http_message(status: int) -> str:
    match status:
        case 200 | 201:
            return "OK"
        case 404:
            return "Not found"
        case code if 500 <= code < 600:       # a GUARD: an extra condition
            return "Server error"
        case _:                               # matches anything (like "else")
            return "Something else"

print([http_message(s) for s in (201, 404, 503, 302)])


# --- 2. Sequences: match the length AND unpack ------------------------------------------------
def run(command: str) -> str:
    match command.split():
        case ["quit"]:
            return "bye"
        case ["go", direction]:                         # exactly 2 words
            return f"walking {direction}"
        case ["drop", *items] if items:                 # 2+ words, the rest collected
            return f"dropping {', '.join(items)}"
        case _:
            return "unknown command"

print(run("go north"), "|", run("drop key coin"), "|", run("dance"))


# --- 3. Mappings: perfect for JSON events ---------------------------------------------------------
def handle(event: dict) -> str:
    match event:
        case {"type": "order", "items": [first, *rest]}:      # extra keys are ignored
            return f"order: {first} (+{len(rest)} more)"
        case {"type": "refund", "amount": float(amount) | int(amount)} if amount > 0:
            return f"refund {amount:.2f}"
        case {"type": str(kind)}:
            return f"ignored event {kind!r}"
        case _:
            return "not an event"

print(handle({"type": "order", "items": ["book", "pen", "mug"], "user": 7}))
print(handle({"type": "refund", "amount": 19.9}))
print(handle({"type": "ping"}))


# --- 4. Classes: match on type and attributes -----------------------------------------------------
@dataclass
class Point:
    x: float
    y: float

@dataclass
class Circle:
    center: Point
    r: float

def describe(shape) -> str:
    match shape:
        case Point(x=0, y=0):
            return "the origin"
        case Point(x=0) | Point(y=0):
            return "a point on an axis"
        case Circle(center=Point(x=0, y=0), r=r):            # nested patterns
            return f"a circle around the origin, r={r}"
        case Circle(r=r) if r > 100:
            return "a huge circle"
        case _:
            return "some shape"

print([describe(s) for s in (Point(0, 0), Point(0, 5), Circle(Point(0, 0), 2), Circle(Point(1, 1), 500))])

# Gotcha: a bare name in a case CAPTURES (case x: matches anything, binds x).
# To compare with a constant, use a dotted name (case Color.RED:) or a literal.
