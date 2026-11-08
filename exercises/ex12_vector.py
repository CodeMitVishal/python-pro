"""Exercise 12 · A Vector class that feels built-in

Make Vector behave like a real Python type by adding dunder methods and a
property. Every TODO is one small method.

  v = Vector(3, 4)
  repr(v)          -> 'Vector(3, 4)'
  v + Vector(1, 1) -> Vector(4, 5)
  v * 2            -> Vector(6, 8)
  2 * v            -> Vector(6, 8)        (hint: __rmul__)
  abs(v)           -> 5.0                 (the length)
  v == Vector(3, 4)-> True, and equal vectors work as set items (__hash__)
  x, y = v         -> unpacking works      (hint: __iter__)
  bool(Vector(0,0))-> False
  v.length         -> 5.0, a read-only @property
  Vector.from_tuple((1, 2)) -> Vector(1, 2)   (a @classmethod)

Run it to check your work:
    python exercises/ex12_vector.py

Stuck? Compare with solutions/ex12_vector.py
"""
import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # TODO: __repr__, __add__, __mul__, __rmul__, __abs__, __eq__, __hash__,
    #       __iter__, __bool__, a 'length' property and a 'from_tuple' classmethod


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    v = Vector(3, 4)
    assert repr(v) == "Vector(3, 4)"
    assert v + Vector(1, 1) == Vector(4, 5)
    assert v * 2 == Vector(6, 8) and 2 * v == Vector(6, 8)
    assert abs(v) == 5.0 and v.length == 5.0
    assert len({Vector(1, 2), Vector(1, 2)}) == 1
    x, y = v
    assert (x, y) == (3, 4)
    assert not Vector(0, 0) and Vector(0, 1)
    assert Vector.from_tuple((1, 2)) == Vector(1, 2)
    try:
        v.length = 10
        raise AssertionError("length must be read-only")
    except AttributeError:
        pass
    print("All checks passed!")
