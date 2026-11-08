"""Slides · Module 12 · Advanced OOP"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 12 · Advanced OOP"
SLIDES = [
 cover("12", "Advanced OOP", "Classes that feel built-in, clean designs, and the OOP questions every interview asks.",
       [("Dunder methods", "01_dunder_methods.py"), ("Properties", "02_properties.py"),
        ("class &amp; static methods", "03_class_and_static_methods.py"), ("Inheritance, super(), MRO", "04_inheritance_and_mro.py"),
        ("ABCs &amp; Protocols", "05_abc_and_protocols.py"), ("Composition &amp; SOLID", "06_composition_and_solid.py"),
        ("Descriptors, __new__, metaclasses", "07_descriptors_and_metaclasses.py"), ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Dunder methods", "Make your objects feel built-in",
     "You built a <b>Money</b> class. Now <b>print(price)</b> shows <b>&lt;Money object at 0x7f...&gt;</b>, "
     "<b>price1 + price2</b> crashes, and <b>==</b> says two equal amounts are different.",
     "Python calls special <b>__dunder__</b> methods behind the scenes. Define them and <b>+</b>, <b>==</b>, <b>print</b>, <b>len</b>, <b>for</b> just work."),

 trace(M, "Dunder methods", "You write this, Python calls that", ["You write", "Python calls", "Typical use"],
       [["print(obj), f\"{obj}\"", "<span class=\"m\">__str__</span>", "friendly text for users"],
        ["obj in a shell / logs", "<span class=\"m\">__repr__</span>", "unambiguous text for developers"],
        ["a + b, a * 3", "<span class=\"m\">__add__</span>, <span class=\"m\">__mul__</span>", "Money, Vector, Duration"],
        ["a == b, a &lt; b", "<span class=\"m\">__eq__</span>, <span class=\"m\">__lt__</span>", "compare and sort"],
        ["len(obj), obj[i], for x in obj", "<span class=\"m\">__len__</span>, <span class=\"m\">__getitem__</span>, <span class=\"m\">__iter__</span>", "act like a container"],
        ["with obj:", "<span class=\"m\">__enter__</span>, <span class=\"m\">__exit__</span>", "clean-up (Module 13)"]]),

 code_out(M, "Dunder methods", "A Money class that behaves", '''
class Money:
    def __init__(self, cents, currency="EUR"):
        self.cents, self.currency = cents, currency

    def __repr__(self):
        return f"Money({self.cents}, {self.currency!r})"

    def __str__(self):
        return f"{self.cents / 100:.2f} {self.currency}"

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("currency mismatch")
        return Money(self.cents + other.cents, self.currency)

    def __eq__(self, other):
        return (self.cents, self.currency) == (other.cents, other.currency)

a, b = Money(1999), Money(500)
print(a + b, "|", repr(a + b), "|", a == Money(1999))
print(sum([a, b], Money(0)))''',
     steps=["<b>__repr__</b> for developers, <b>__str__</b> for users.", "Store money as <b>integer cents</b> (or Decimal), never float.",
            "<b>sum()</b> works because <b>__add__</b> exists."]),

 code_out(M, "Properties", "Attributes with rules", '''
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance        # goes through the setter!

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("balance can't be negative")
        self._balance = value

acc = Account("vishal", 100)
acc.balance += 50
print(acc.balance)
try:
    acc.balance = -5
except ValueError as e:
    print("ValueError:", e)''',
     steps=["Callers still write <b>acc.balance</b>: no getters and setters.", "The rule lives in <b>one</b> place.",
            "<b>_balance</b> with one underscore = \"internal, please don't touch\"."]),

 trace(M, "Methods", "Instance vs class vs static methods", ["", "First argument", "Can use", "Typical use"],
       [["instance method", "<span class=\"m\">self</span>", "this object's data", "almost everything"],
        ["<span class=\"m\">@classmethod</span>", "<span class=\"m\">cls</span>", "the class (works for subclasses)", "<b>alternative constructors</b>: <span class=\"m\">User.from_json(...)</span>"],
        ["<span class=\"m\">@staticmethod</span>", "nothing", "neither", "a helper that belongs to the topic"]],
       "Interview one-liner: <b>classmethod</b> gets the class, <b>staticmethod</b> gets nothing, a normal method gets the instance."),

 code_out(M, "Methods", "classmethod as a second constructor", '''
import json

class User:
    def __init__(self, name, email):
        self.name, self.email = name, email

    @classmethod
    def from_json(cls, text):
        data = json.loads(text)
        return cls(data["name"], data["email"])    # cls, not User

    @staticmethod
    def is_valid_email(email):
        return "@" in email and "." in email.split("@")[-1]

class Admin(User):
    pass

a = Admin.from_json('{"name": "vishal", "email": "v@ex.com"}')
print(type(a).__name__, a.name, User.is_valid_email(a.email))''',
     steps=["<b>cls(...)</b> builds the <b>right</b> class: Admin.from_json gives an Admin.",
            "Static methods are plain functions grouped inside the class."]),

 # ------------------------------------------------------------------ INHERITANCE + MRO
 picture(M, "Inheritance and MRO", "Who answers a method call?",
     "&#129517; Python searches classes in a fixed order called the <b>MRO</b> (Method Resolution Order). "
     "<b>super()</b> means \"the <b>next</b> class in the MRO\", not just \"my parent\".",
     [("AdminUser", "look here first"), ("Admin", "then here"), ("Auditable", "then the next mixin"),
      ("User", "then the base"), ("object", "always last")],
     "See it with <b>AdminUser.__mro__</b>. The diamond problem is solved by this one fixed order."),

 code_out(M, "Inheritance and MRO", "super() follows the MRO", '''
class User:
    def describe(self):
        return ["user"]

class Admin(User):
    def describe(self):
        return ["admin"] + super().describe()

class Auditable(User):
    def describe(self):
        return ["audited"] + super().describe()

class AdminUser(Admin, Auditable):
    pass

print([c.__name__ for c in AdminUser.__mro__])
print(AdminUser().describe())''',
     steps=["Admin's <b>super()</b> goes to <b>Auditable</b>, not User!", "Every class is visited <b>once</b>.",
            "Prefer shallow hierarchies; use mixins for small add-ons."]),

 # ------------------------------------------------------------------ ABC / PROTOCOL
 code_out(M, "ABCs and Protocols", "Define a contract", '''
from abc import ABC, abstractmethod
from typing import Protocol

class PaymentGateway(ABC):                 # nominal: must inherit
    @abstractmethod
    def charge(self, cents: int) -> str: ...

class Stripe(PaymentGateway):
    def charge(self, cents): return f"stripe charged {cents}"

class Notifier(Protocol):                  # structural: just match
    def send(self, msg: str) -> None: ...

class Slack:                               # no inheritance needed
    def send(self, msg): print("slack:", msg)

def alert(n: Notifier): n.send("disk full")
alert(Slack())
print(Stripe().charge(500))''',
     steps=["<b>ABC</b>: subclasses <b>must</b> implement the abstract methods.", "<b>Protocol</b>: \"anything with a .send()\" (duck typing, checked by mypy).",
            "Code depends on the contract, so tests can pass in fakes."]),

 # ------------------------------------------------------------------ COMPOSITION / SOLID
 mistake(M, "Composition", "Inheritance for code reuse",
     '''
class Database: ...
class EmailSender: ...

class OrderService(Database, EmailSender):
    ...   # an OrderService IS a Database??''',
     "Inheriting just to <b>reuse</b> code creates weird \"is-a\" relationships, deep hierarchies and classes that are hard to test.",
     '''
class OrderService:
    def __init__(self, db, mailer):
        self.db = db            # HAS a db
        self.mailer = mailer    # HAS a mailer

service = OrderService(FakeDB(), FakeMailer())''',
     "<b>Composition</b>: pass collaborators in (dependency injection). Swap real ones for fakes in tests."),

 trace(M, "SOLID", "SOLID in plain words", ["Letter", "Principle", "In one sentence"],
       [["<b>S</b>", "Single responsibility", "a class has one reason to change"],
        ["<b>O</b>", "Open / closed", "add features by adding code, not editing old code"],
        ["<b>L</b>", "Liskov substitution", "a subclass must work wherever the parent works"],
        ["<b>I</b>", "Interface segregation", "small, focused interfaces (Protocols)"],
        ["<b>D</b>", "Dependency inversion", "depend on abstractions, inject the details"]],
       "You won't recite these at work, but interviews love them. Give one example for each."),

 code_out(M, "Under the hood", "__new__ and __init_subclass__: a plugin registry", '''
class Exporter:
    registry = {}

    def __init_subclass__(cls, fmt, **kw):
        super().__init_subclass__(**kw)
        Exporter.registry[fmt] = cls        # auto-register

class CSVExporter(Exporter, fmt="csv"):
    def run(self): return "a,b"

class JSONExporter(Exporter, fmt="json"):
    def run(self): return "{}"

print(Exporter.registry)
print(Exporter.registry["json"]().run())''',
     steps=["<b>__init_subclass__</b> runs when a subclass is <b>defined</b>.",
            "<b>__new__</b> <b>creates</b> the object; <b>__init__</b> fills it in.",
            "Metaclasses can do this too, but are rarely needed."]),

 job(M, "OOP", "OOP in real web code", [
     ("Django models and DRF serializers", '''
class Order(models.Model):
    def __str__(self): return f"#{self.pk}"'''),
     ("Pydantic models for API bodies", '''
class OrderIn(BaseModel):
    @classmethod ...   # validators'''),
     ("Service layer with injected repos", '''
class OrderService:
    def __init__(self, repo: OrderRepo): ...'''),
     ("Swappable integrations", '''
class Notifier(Protocol):
    def send(self, msg: str) -> None: ...'''),
 ]),

 interview(M, "@classmethod vs @staticmethod vs instance method?",
     ["An <b>instance method</b> gets <b>self</b>: it works with one object's data.",
      "A <b>classmethod</b> gets <b>cls</b>: used for <b>alternative constructors</b> (<b>from_json</b>, <b>from_row</b>), and it respects subclasses.",
      "A <b>staticmethod</b> gets nothing: a utility function that belongs to the class's topic.",
      "Example: <b>datetime.fromtimestamp()</b> and <b>dict.fromkeys()</b> are classmethods."],
     None,
     "\"What is the MRO? How does super() work with multiple inheritance?\" (C3 linearisation; super() calls the next class in the MRO, so each class runs once)."),

 interview(M, "Composition vs inheritance: which do you prefer?",
     ["<b>Inheritance</b> models \"<b>is-a</b>\" (an Admin is a User) and is good for small, stable hierarchies.",
      "<b>Composition</b> models \"<b>has-a</b>\" (a service has a repository) and is more flexible.",
      "I prefer <b>composition + dependency injection</b>: parts are swappable and easy to test with fakes.",
      "I use ABCs or Protocols to define the contract between the parts."],
     '''
class OrderService:
    def __init__(self, repo: OrderRepo,
                 payments: PaymentGateway):
        self.repo = repo
        self.payments = payments''',
     "\"Explain the SOLID principles\" and \"What design patterns have you used?\" (factory, strategy, repository, singleton via a module, observer via signals)."),

 recap(M, "Module 12 in 6 lines",
     ["<b>__repr__</b>, <b>__str__</b>, <b>__eq__</b>, <b>__add__</b>... make objects feel built-in.",
      "<b>@property</b> adds rules without changing how callers use the attribute.",
      "classmethod = <b>cls</b> (constructors); staticmethod = nothing; method = <b>self</b>.",
      "<b>super()</b> = the next class in the <b>MRO</b>.",
      "ABC = must inherit; Protocol = just match the shape.",
      "Prefer <b>composition</b> and inject dependencies."],
     "Do <b>exercises/ex12_vector.py</b>: a Vector class with +, *, ==, abs() and len()."),
]
