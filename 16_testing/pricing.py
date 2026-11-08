"""Module 16 · The code under test: small pricing functions."""


def apply_discount(price: float, percent: float) -> float:
    """Return the price after a percentage discount (0-100)."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)


def cart_total(cart: dict[str, tuple[float, int]]) -> float:
    """cart maps item -> (unit price, quantity)."""
    return round(sum(price * qty for price, qty in cart.values()), 2)


def parse_price(text: str) -> float:
    """'€1,234.50' or '12.5' -> 1234.5 / 12.5"""
    cleaned = text.strip().lstrip("€$").replace(",", "")
    return float(cleaned)
