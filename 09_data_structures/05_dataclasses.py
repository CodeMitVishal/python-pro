"""Module 9 · dataclasses: classes for data, without the boilerplate

@dataclass writes __init__, __repr__ and __eq__ for you, based on the
fields you list with type hints. Perfect for "records": a product, an
order, a user, a config.

Run it:  python 09_data_structures/05_dataclasses.py
"""
from dataclasses import dataclass, field, asdict

# --- 1. Without dataclass: lots of repetitive code ----------------------------------
class ProductOld:
    def __init__(self, name, price, qty=0):
        self.name = name
        self.price = price
        self.qty = qty

    def __repr__(self):
        return f"ProductOld(name={self.name!r}, price={self.price}, qty={self.qty})"


# --- 2. With dataclass: just list the fields ----------------------------------------
@dataclass
class Product:
    name: str
    price: float
    qty: int = 0                           # a default value

    def total(self) -> float:              # normal methods still work
        return self.price * self.qty


laptop = Product("Laptop", 899.0, 2)
print(laptop)                              # Product(name='Laptop', price=899.0, qty=2)
print(laptop.total())                      # 1798.0
print(laptop == Product("Laptop", 899.0, 2))   # True: __eq__ compares the fields
print(asdict(laptop))                      # {'name': 'Laptop', 'price': 899.0, 'qty': 2}

# --- 3. Mutable defaults: use field(default_factory=...) ------------------------------
@dataclass
class Order:
    customer: str
    items: list = field(default_factory=list)   # a NEW list for every order
    # items: list = []  -> ValueError: mutable default is not allowed (and for good reason)

    def add(self, product: Product):
        self.items.append(product)

o1, o2 = Order("Vishal"), Order("Raj")
o1.add(laptop)
print(len(o1.items), len(o2.items))        # 1 0  (each order has its own list)

# --- 4. frozen=True: read-only, hashable objects --------------------------------------
@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(3, 7)
# p.x = 5 -> FrozenInstanceError
print({p: "start"}[Point(3, 7)])           # start (frozen dataclasses can be dict keys)

# --- 5. order=True: compare and sort by the fields, in order ---------------------------
@dataclass(order=True)
class Version:
    major: int
    minor: int

print(sorted([Version(1, 4), Version(0, 9), Version(1, 0)]))
# [Version(major=0, minor=9), Version(major=1, minor=0), Version(major=1, minor=4)]
