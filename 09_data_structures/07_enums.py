"""Module 9 · Enums: a fixed set of named constants (StrEnum needs Python 3.11+)

Instead of magic strings ("pending", "shipped"...) that can be mistyped, an
Enum gives every allowed value a name. Typos become errors, editors autocomplete,
and you can loop over all the options.

TEACHING NOTES
  Why it matters  Magic strings like 'payed' vs 'paid' create silent bugs; enums make invalid
                  values impossible.
  Picture it      An enum is a menu: you can only order what's printed on it.
  Watch out       Compare members with 'is' or ==; StrEnum (3.11+) equals its string, plain Enum
                  does not.
  In real jobs    Order status, user roles, payment states stored in the DB and sent as JSON.
  Interview       Q: Why use an Enum instead of string constants?
                  A: A closed set of valid values: typos fail loudly, IDEs autocomplete, you can
                     iterate all options.

Run it:  python 09_data_structures/07_enums.py
"""
from enum import Enum, Flag, IntEnum, StrEnum, auto


class OrderStatus(StrEnum):            # members ARE strings: great for JSON and databases
    PENDING = auto()                   # auto() -> "pending" for StrEnum
    PAID = auto()
    SHIPPED = auto()
    CANCELLED = auto()

    @property
    def is_final(self) -> bool:        # enums can have methods and properties
        return self in (OrderStatus.SHIPPED, OrderStatus.CANCELLED)


status = OrderStatus.PAID
print(status, status == "paid", status.is_final)          # paid True False
print(OrderStatus("shipped").is_final)                    # build from a value: True
print([s.value for s in OrderStatus])                     # loop over every option
try:
    OrderStatus("shiped")                                 # a typo is caught
except ValueError as e:
    print("error:", e)


class Priority(IntEnum):               # members ARE ints: they compare and sort
    LOW = 1
    MEDIUM = 2
    HIGH = 3

print(sorted([Priority.HIGH, Priority.LOW]), Priority.HIGH > Priority.MEDIUM)


class Color(Enum):                     # a plain Enum: not equal to any str/int
    RED = "#ff0000"
    GREEN = "#00ff00"

print(Color.RED.name, Color.RED.value, Color["GREEN"])    # RED #ff0000 Color.GREEN


class Permission(Flag):                # combine options with |, test with in
    READ = auto()
    WRITE = auto()
    DELETE = auto()

editor = Permission.READ | Permission.WRITE
print(Permission.WRITE in editor, Permission.DELETE in editor)   # True False


# Enums work beautifully with match/case (lesson 08/07):
def next_step(s: OrderStatus) -> str:
    match s:
        case OrderStatus.PENDING:
            return "wait for payment"
        case OrderStatus.PAID:
            return "ship it"
        case _:
            return "nothing to do"

print(next_step(OrderStatus.PAID))
