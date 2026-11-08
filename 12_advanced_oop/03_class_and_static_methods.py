"""Module 12 · Instance, class and static methods

  def method(self, ...)          -> works on ONE object (most methods)
  @classmethod def m(cls, ...)   -> works on the CLASS: alternative constructors,
                                    class-wide settings. Subclasses get their own cls.
  @staticmethod def m(...)       -> a plain helper that lives in the class
                                    for organisation; no self, no cls.

TEACHING NOTES
  Why it matters  Creating objects from JSON or DB rows needs constructors that aren't __init__.
  Picture it      classmethod = a second front door that knows which house (class) it belongs
                  to; staticmethod = a tool in the shed.
  Watch out       Use cls(...) in classmethods, not the hard-coded class name, so subclasses
                  work.
  In real jobs    User.from_json(...), datetime.fromtimestamp(), dict.fromkeys().
  Interview       Q: classmethod vs staticmethod vs instance method?
                  A: Instance gets self, classmethod gets cls (alternative constructors),
                     staticmethod gets nothing.

Run it:  python 12_advanced_oop/03_class_and_static_methods.py
"""
from datetime import date


class Employee:
    raise_rate = 1.05                          # class-wide setting

    def __init__(self, name, salary, joined):
        self.name = name
        self.salary = salary
        self.joined = joined

    # --- instance method: needs a specific employee -------------------------------
    def apply_raise(self):
        self.salary = round(self.salary * self.raise_rate)

    # --- class methods: alternative constructors ----------------------------------
    @classmethod
    def from_csv(cls, line):
        """Build an Employee from 'name,salary,YYYY-MM-DD'."""
        name, salary, joined = line.split(",")
        return cls(name, int(salary), date.fromisoformat(joined))   # cls, not Employee!

    @classmethod
    def set_raise_rate(cls, rate):
        cls.raise_rate = rate

    # --- static method: a helper that doesn't need self or cls ---------------------
    @staticmethod
    def is_valid_salary(amount):
        return 0 < amount < 1_000_000

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.salary})"


class Manager(Employee):
    raise_rate = 1.10


e = Employee.from_csv("Vishal,60000,2025-02-01")
m = Manager.from_csv("Li,90000,2020-06-15")   # cls is Manager here -> a Manager!
print(e, m)                                    # Employee('Vishal', 60000) Manager('Li', 90000)

e.apply_raise(); m.apply_raise()
print(e.salary, m.salary)                      # 63000 99000

print(Employee.is_valid_salary(50_000))        # True
print(Employee.is_valid_salary(-5))            # False

Employee.set_raise_rate(1.03)                  # changes the setting for Employee only
print(Employee.raise_rate, Manager.raise_rate) # 1.03 1.1
