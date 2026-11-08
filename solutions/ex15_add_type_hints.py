"""Solution · Exercise 15: Add type hints and let mypy find the bug

The bug: biggest_order() can return None, but report() used the result as if
it were always an order. With the hints in place, mypy --strict reports
  error: Value of type "Order | None" is not indexable
so report([]) would crash with TypeError. The fix: handle the None case.

Run it:  python solutions/ex15_add_type_hints.py
"""
from typing import TypedDict


class Order(TypedDict):
    customer: str
    qty: int
    price: float


def parse_order(line: str) -> Order:
    customer, qty, price = line.split(",")
    return {"customer": customer, "qty": int(qty), "price": float(price)}


def order_total(order: Order) -> float:
    return order["qty"] * order["price"]


def biggest_order(orders: list[Order]) -> Order | None:
    if not orders:
        return None
    return max(orders, key=order_total)


def report(orders: list[Order]) -> str:
    best = biggest_order(orders)
    if best is None:                 # the fix mypy pushed us towards
        return "No orders yet"
    return f"Biggest order: {best['customer']} ({order_total(best):.2f})"


if __name__ == "__main__":
    orders = [parse_order(line) for line in ["vishal,3,19.99", "raj,10,2.50"]]
    assert order_total(orders[0]) == 3 * 19.99
    best = biggest_order(orders)
    assert best is not None and best["customer"] == "vishal"
    assert report(orders) == "Biggest order: vishal (59.97)"
    assert report([]) == "No orders yet"

    try:
        from mypy import api
        out, _, status = api.run(["--strict", __file__])
        assert status == 0, "mypy --strict still reports problems:\n" + out
        print("mypy --strict: no issues")
    except ImportError:
        print("(install mypy to also check the type hints: pip install mypy)")
    print("All checks passed!")
