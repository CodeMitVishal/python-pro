"""Solution · Exercise 12: A Vector class that feels built-in

Run it:  python solutions/ex12_vector.py
"""
import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, pair):
        return cls(*pair)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):              # v * 2
        return Vector(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__                      # 2 * v: Python tries int.__mul__ first, then this

    def __abs__(self):
        return math.hypot(self.x, self.y)

    @property
    def length(self):                       # no setter -> read-only
        return abs(self)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):                     # equal vectors -> equal hashes
        return hash((self.x, self.y))

    def __iter__(self):                     # enables  x, y = v
        yield self.x
        yield self.y

    def __bool__(self):
        return bool(self.x or self.y)


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
