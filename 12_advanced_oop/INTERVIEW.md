# Module 12 · Interview questions (with answers)

Short answers you can say out loud, with code and the usual follow-up.

[← Module 12](README.md) · [Quiz](QUIZ.md)

---

### 1. What are the four pillars of OOP?

**Say:**
- **Encapsulation**: data and the methods that use it live together, behind a clear interface. Python uses `_name` by convention, and `@property` for rules.
- **Abstraction**: callers use what an object does, not how it does it (ABCs, Protocols).
- **Inheritance**: reuse and specialise behaviour.
- **Polymorphism**: different classes answer the same method call in their own way, e.g. every `PaymentGateway` has `.charge()`.

---

### 2. `@classmethod` vs `@staticmethod` vs instance method?

**Say:** An instance method gets `self` (the object). A classmethod gets `cls` (the class): use it for **alternative constructors** like `User.from_json()`, and it builds the correct subclass. A staticmethod gets nothing: it's a plain helper function grouped in the class.

---

### 3. `__str__` vs `__repr__`?

**Say:** `__repr__` is for **developers**: unambiguous, ideally valid code like `Money(1999, 'EUR')`. It's used in the shell, in logs and inside containers. `__str__` is for **users**: friendly text used by `print()` and f-strings. If only `__repr__` exists, `str()` falls back to it.

---

### 4. `__new__` vs `__init__`?

**Say:** `__new__` **creates** and returns the instance (it's a static method that receives the class). `__init__` **initialises** the instance that already exists. You override `__new__` rarely: for immutable types (subclassing `int` or `str`), singletons, or caching instances.

---

### 5. What is the MRO, and how does `super()` work?

**Say:** The **Method Resolution Order** is the order Python searches classes for an attribute, computed with C3 linearisation (see `Class.__mro__`). `super()` returns the **next class in the MRO** of the object's actual type, not simply "the parent". That way, with cooperative multiple inheritance, every class in a diamond runs exactly once.

---

### 6. What is a property, and why use it?

**Say:** `@property` turns method calls into attribute access. You can add validation or computed values **later** without changing callers (`obj.balance` stays `obj.balance`). That's Python's answer to Java-style getters and setters.

---

### 7. ABC vs Protocol?

**Say:** An **ABC** is a **nominal** contract: classes must inherit from it, and you can't instantiate a subclass until it implements every `@abstractmethod`. A **Protocol** is **structural** (static duck typing): any class with matching methods fits, without inheriting. mypy checks it. I use Protocols for dependencies such as repositories and notifiers, and ABCs when I also want shared base behaviour.

---

### 8. Composition vs inheritance?

**Say:** Inheritance means **is-a**; composition means **has-a**. I prefer composition with dependency injection: objects receive their collaborators in `__init__`, so I can swap implementations and pass in fakes in tests. Deep inheritance trees are fragile ("the fragile base class problem").

---

### 9. Explain SOLID briefly.

**Say:**
- **S**ingle responsibility: one reason to change.
- **O**pen/closed: extend by adding code, not by editing old code.
- **L**iskov: subclasses must be substitutable for their parent.
- **I**nterface segregation: small, focused interfaces.
- **D**ependency inversion: depend on abstractions and inject the details.

---

### 10. Which design patterns have you used in Python?

**Say:**
- **Factory**: classmethods like `from_json`, or a dict of classes.
- **Strategy**: pass a function or object, e.g. `key=`, or a pricing strategy.
- **Repository**: all SQL in one class, behind a Protocol.
- **Observer**: Django signals, event hooks.
- **Decorator**: `@timer`, middleware.
- **Singleton**: usually just a **module-level** object, because modules are imported only once.

**Follow-up:** *"How do you make a singleton?"* The simplest way is a module-level instance. Otherwise override `__new__` to return a cached instance, or use `functools.cache` on a factory function.

---

### 11. What are dunder methods? Name some.

**Say:** Special methods Python calls for built-in syntax:
- `__init__`, `__repr__`, `__str__`
- `__eq__` and `__hash__` (define both together)
- `__lt__` for sorting
- `__add__` for `+`
- `__len__`, `__getitem__` and `__iter__` for containers
- `__enter__` and `__exit__` for `with`
- `__call__` for `obj()`

**Follow-up:** *"What happens if you define `__eq__` but not `__hash__`?"* Python sets `__hash__` to `None`, so instances become unhashable and can't be used as dict keys or in sets.

---

### 12. What is a descriptor? What is a metaclass?

**Say:** A **descriptor** is an object with `__get__`/`__set__` stored on a class. It controls attribute access, and it's how `property`, `classmethod` and Django model fields work. A **metaclass** is the class of a class. It customises class creation, as in Django's `ModelBase`. Today, `__init_subclass__` and class decorators cover most needs more simply.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
