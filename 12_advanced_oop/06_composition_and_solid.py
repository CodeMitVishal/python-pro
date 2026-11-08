"""Module 12 · Composition and the SOLID principles, in plain words

COMPOSITION: build objects out of other objects ("HAS-A") instead of deep
inheritance trees ("IS-A"). Swap parts without rewriting classes.

SOLID, simplified:
  S  Single responsibility   - one class, one reason to change
  O  Open/closed             - add new behaviour by adding code, not editing old code
  L  Liskov substitution     - a subclass must work wherever its parent works
  I  Interface segregation   - small, focused interfaces beat one giant one
  D  Dependency inversion    - depend on an abstraction, pass the details in

Run it:  python 12_advanced_oop/06_composition_and_solid.py
"""
from typing import Protocol


# --- Small, single-purpose parts (S) ------------------------------------------------
class PriceCalculator:
    def total(self, items):
        return sum(price for _, price in items)


class Discount(Protocol):                      # an abstraction (I, D)
    def apply(self, total: float) -> float: ...


class NoDiscount:
    def apply(self, total):
        return total


class PercentOff:
    def __init__(self, percent):
        self.percent = percent

    def apply(self, total):
        return total * (1 - self.percent / 100)


class Notifier(Protocol):
    def send(self, msg: str) -> None: ...


class ConsoleNotifier:
    def send(self, msg):
        print(f"[notify] {msg}")


# --- The Checkout HAS a calculator, a discount and a notifier (composition) ---------
class Checkout:
    def __init__(self, discount: Discount, notifier: Notifier):   # injected (D)
        self.calc = PriceCalculator()
        self.discount = discount
        self.notifier = notifier

    def pay(self, items):
        total = self.discount.apply(self.calc.total(items))
        self.notifier.send(f"charged {total:.2f} EUR")
        return total


cart = [("book", 30.0), ("pen", 5.0)]
Checkout(NoDiscount(), ConsoleNotifier()).pay(cart)        # charged 35.00 EUR
Checkout(PercentOff(20), ConsoleNotifier()).pay(cart)      # charged 28.00 EUR

# Need a "buy 2, get 10 off" rule? Write a NEW class with apply() (O).
# Checkout never changes. Need SMS instead of console? Pass another notifier.


# --- Testing becomes easy: pass a fake ----------------------------------------------
class FakeNotifier:
    def __init__(self):
        self.sent = []

    def send(self, msg):
        self.sent.append(msg)


fake = FakeNotifier()
Checkout(NoDiscount(), fake).pay(cart)
print(fake.sent)                    # ['charged 35.00 EUR']  <- no printing, easy to assert
