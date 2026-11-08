"""Module 12 · Abstract base classes and Protocols: defining contracts

Two ways to say "anything used here must have these methods":

  ABC (abc module)  -> NOMINAL: classes must INHERIT from the base and
                       implement every @abstractmethod, or they can't be created.
  Protocol (typing) -> STRUCTURAL ("duck typing"): any class that simply HAS
                       the right methods fits, no inheritance needed.

Run it:  python 12_advanced_oop/05_abc_and_protocols.py
"""
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


# --- 1. ABC: a contract enforced at creation time -----------------------------------
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

    def describe(self):                       # normal methods can use the abstract ones
        return f"{type(self).__name__} with area {self.area():.2f}"


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return 3.14159 * self.r ** 2


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


for s in [Circle(1), Square(3)]:
    print(s.describe())        # Circle with area 3.14 / Square with area 9.00

try:
    Shape()
except TypeError as e:
    print("Can't create:", e)  # can't instantiate abstract class Shape...

class Broken(Shape):           # forgot to implement area()
    pass

try:
    Broken()
except TypeError:
    print("Broken() fails too: the missing method is caught early")


# --- 2. Protocol: "if it has .send(), it's a Notifier" -------------------------------
@runtime_checkable
class Notifier(Protocol):
    def send(self, message: str) -> None: ...


class EmailNotifier:            # does NOT inherit from Notifier
    def send(self, message):
        print(f"email: {message}")


class SlackNotifier:
    def send(self, message):
        print(f"slack: {message}")


def alert_all(notifiers: list[Notifier], msg: str):
    for n in notifiers:
        n.send(msg)


alert_all([EmailNotifier(), SlackNotifier()], "deploy finished")
print(isinstance(SlackNotifier(), Notifier))   # True: it has the right shape
# Use ABCs for your own class families; Protocols to accept "anything that fits",
# including classes from other libraries you can't change.
