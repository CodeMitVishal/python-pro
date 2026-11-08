"""Module 12 · Properties: attributes with rules

A @property looks like a plain attribute from outside (acc.balance), but
runs a method inside. Use it to:
  - validate values when they're set
  - compute a value on the fly
  - make an attribute read-only
...without changing how other code uses your class.

TEACHING NOTES
  Why it matters  Validation rules spread over callers get forgotten; properties keep them in
                  one place.
  Picture it      A property is a receptionist in front of an attribute: it checks everything
                  that goes in.
  Watch out       Store the value in a differently named attribute (_balance) or the setter
                  calls itself forever.
  In real jobs    Computed fields (full_name), validated fields (price >= 0), read-only
                  attributes.
  Interview       Q: Why use @property instead of getters and setters?
                  A: Callers keep plain attribute syntax while you add logic later without
                     changing their code.

Run it:  python 12_advanced_oop/02_properties.py
"""


class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius       # goes through the setter below, so it's validated

    @property
    def celsius(self):               # the "getter": runs on  t.celsius
        return self._celsius         # the real value lives in _celsius (convention: internal)

    @celsius.setter
    def celsius(self, value):        # the "setter": runs on  t.celsius = value
        if value < -273.15:
            raise ValueError("below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):            # computed, read-only: no setter defined
        return self._celsius * 9 / 5 + 32


t = Temperature(25)
print(t.celsius, t.fahrenheit)       # 25 77.0
t.celsius = 30                       # validated
print(t.fahrenheit)                  # 86.0
try:
    t.celsius = -500
except ValueError as e:
    print("Rejected:", e)            # Rejected: below absolute zero!
try:
    t.fahrenheit = 100
except AttributeError as e:
    print("Read-only:", e)           # property 'fahrenheit' ... has no setter


# --- Class attributes vs instance attributes ----------------------------------------
class Account:
    bank = "Python Bank"             # CLASS attribute: shared by all accounts
    count = 0

    def __init__(self, owner):
        self.owner = owner           # INSTANCE attribute: one per object
        Account.count += 1


x, y = Account("Vishal"), Account("Raj")
print(x.bank, y.bank, Account.count)    # Python Bank Python Bank 2

# --- __slots__: fixed attributes, less memory, no typos --------------------------------
class Point:
    __slots__ = ("x", "y")           # only these attributes are allowed

    def __init__(self, x, y):
        self.x, self.y = x, y


p = Point(1, 2)
try:
    p.z = 3
except AttributeError:
    print("No 'z' allowed: __slots__ blocks typos and saves memory")
