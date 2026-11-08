"""Module 12 · Inheritance, super() and the MRO

With multiple inheritance, Python needs ONE clear order to search for
methods: the Method Resolution Order (MRO). super() means "the NEXT class
in the MRO", not simply "my parent". That's what makes cooperative classes
and mixins work.

Run it:  python 12_advanced_oop/04_inheritance_and_mro.py
"""
import json


# --- 1. The diamond --------------------------------------------------------------
class Base:
    def hello(self):
        return "Base"

class Left(Base):
    def hello(self):
        return "Left -> " + super().hello()

class Right(Base):
    def hello(self):
        return "Right -> " + super().hello()

class Child(Left, Right):
    def hello(self):
        return "Child -> " + super().hello()

print(Child().hello())        # Child -> Left -> Right -> Base  (each runs ONCE)
print([c.__name__ for c in Child.__mro__])
# ['Child', 'Left', 'Right', 'Base', 'object']
# Rule of thumb: left to right, children before parents, each class once.


# --- 2. Mixins: small classes that ADD one ability -------------------------------
class JsonMixin:
    def to_json(self):
        return json.dumps(self.__dict__)

class ReprMixin:
    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{type(self).__name__}({fields})"

class User(JsonMixin, ReprMixin):
    def __init__(self, name, role):
        self.name, self.role = name, role

u = User("Vishal", "admin")
print(u)                      # User(name='Vishal', role='admin')
print(u.to_json())            # {"name": "Vishal", "role": "admin"}


# --- 3. isinstance vs type ---------------------------------------------------------
print(isinstance(u, JsonMixin), type(u) is JsonMixin)   # True False
# isinstance respects inheritance; prefer it over type(x) == ...

# --- 4. When NOT to inherit -------------------------------------------------------------
# Inheritance means "IS-A": a Manager IS an Employee.
# If it's "HAS-A" (a Car HAS an Engine), use composition instead -> lesson 06.
