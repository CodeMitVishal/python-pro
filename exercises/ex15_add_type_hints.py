"""Exercise 15 · Add type hints and let mypy find the bug

1. Add type hints to EVERY function below (parameters and return types).
   Use list[...], dict[...], X | None and a TypedDict for the order rows.
2. Run mypy in strict mode:
       pip install mypy
       mypy --strict exercises/ex15_add_type_hints.py
   Once the hints are in, mypy reports a real bug that the tests below don't
   catch. Fix it.
3. Run this file: the checks must pass, AND mypy --strict must report no issues.

Stuck? Compare with solutions/ex15_add_type_hints.py
"""


def parse_order(line):
    """'vishal,3,19.99' -> {'customer': 'vishal', 'qty': 3, 'price': 19.99}"""
    customer, qty, price = line.split(",")
    return {"customer": customer, "qty": int(qty), "price": float(price)}


def order_total(order):
    return order["qty"] * order["price"]


def biggest_order(orders):
    """Return the order with the largest total, or None for an empty list."""
    if not orders:
        return None
    return max(orders, key=order_total)


def report(orders):
    best = biggest_order(orders)
    return f"Biggest order: {best['customer']} ({order_total(best):.2f})"


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    orders = [parse_order(line) for line in ["vishal,3,19.99", "raj,10,2.50"]]
    assert order_total(orders[0]) == 3 * 19.99
    assert biggest_order(orders)["customer"] == "vishal"
    assert report(orders) == "Biggest order: vishal (59.97)"
    try:
        assert report([]) == "No orders yet", "report([]) should say 'No orders yet'"
    except TypeError:
        raise AssertionError("report([]) crashes: that's the bug mypy found!")

    try:
        from mypy import api
        out, _, status = api.run(["--strict", __file__])
        assert status == 0, "mypy --strict still reports problems:\n" + out
        print("mypy --strict: no issues")
    except ImportError:
        print("(install mypy to also check the type hints: pip install mypy)")
    print("All checks passed!")
