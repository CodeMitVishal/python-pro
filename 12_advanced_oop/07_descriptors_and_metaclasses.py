"""Module 12 · Under the hood of classes: descriptors, __new__, __init_subclass__, metaclasses

You rarely need these in app code, but frameworks use them everywhere
(Django models, SQLAlchemy columns, pydantic fields, dataclasses).
Understanding them makes "magic" libraries make sense.

Run it:  python 12_advanced_oop/07_descriptors_and_metaclasses.py
"""


# --- 1. Descriptors: reusable attribute logic (this is how @property works) ------------------
class Positive:
    def __set_name__(self, owner, name):           # called when the class is created
        self.private = f"_{name}"

    def __get__(self, obj, objtype=None):          # runs on  obj.attr
        return getattr(obj, self.private)

    def __set__(self, obj, value):                 # runs on  obj.attr = value
        if value <= 0:
            raise ValueError(f"{self.private[1:]} must be positive, got {value}")
        setattr(obj, self.private, value)


class Product:
    price = Positive()                             # ONE descriptor object, reused per field
    stock = Positive()

    def __init__(self, price, stock):
        self.price = price                         # goes through Positive.__set__
        self.stock = stock


p = Product(9.99, 3)
print(p.price, p.stock)
try:
    p.stock = 0
except ValueError as e:
    print("descriptor:", e)


# --- 2. __new__: control object CREATION (runs before __init__) ------------------------------------
class Config:
    _instance = None

    def __new__(cls):                              # a singleton: always the same object
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


print("singleton:", Config() is Config())


# --- 3. __init_subclass__: react whenever someone subclasses you (plugin registries) ---------------
class Exporter:
    registry: dict[str, type] = {}

    def __init_subclass__(cls, fmt: str, **kwargs):
        super().__init_subclass__(**kwargs)
        Exporter.registry[fmt] = cls               # auto-register every subclass


class CsvExporter(Exporter, fmt="csv"):
    pass


class JsonExporter(Exporter, fmt="json"):
    pass


print("plugins:", {k: v.__name__ for k, v in Exporter.registry.items()})


# --- 4. Metaclasses: the class of a class (type is the default one) --------------------------------
print(type(42), type(int), type(type))             # int -> type -> type


class UpperAttrs(type):                            # runs when a CLASS is created
    def __new__(mcls, name, bases, ns):
        constants = {k.upper() if not k.startswith("__") else k: v for k, v in ns.items()}
        return super().__new__(mcls, name, bases, constants)


class Settings(metaclass=UpperAttrs):
    timeout = 30
    retries = 3


print("metaclass:", Settings.TIMEOUT, Settings.RETRIES, hasattr(Settings, "timeout"))

# Rule of thumb: try a decorator, __init_subclass__ or a descriptor first.
# Reach for a metaclass only when you're building a framework.
