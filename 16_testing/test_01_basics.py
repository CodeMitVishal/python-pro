"""Module 16 · pytest basics

pytest finds files named test_*.py, runs every function named test_*, and
reports each plain `assert` that fails, with the actual values. No classes
or special assert methods needed.

Run:   pytest 16_testing/test_01_basics.py -v
"""
import pytest

from pricing import apply_discount, cart_total, parse_price


# --- 1. A test = arrange, act, assert ------------------------------------------------
def test_discount_takes_percentage_off():
    price = 100.0                               # arrange: set up the input
    result = apply_discount(price, 20)          # act: call the code
    assert result == 80.0                       # assert: check the result


def test_zero_discount_keeps_price():
    assert apply_discount(59.99, 0) == 59.99


# --- 2. Test the edges, not just the happy path ---------------------------------------
def test_full_discount_is_free():
    assert apply_discount(10, 100) == 0


def test_empty_cart_costs_nothing():
    assert cart_total({}) == 0


# --- 3. Test that errors ARE raised ---------------------------------------------------
def test_discount_over_100_is_rejected():
    with pytest.raises(ValueError, match="between 0 and 100"):
        apply_discount(10, 150)


# --- 4. Floats: compare with pytest.approx, never == on raw float maths -------------------
def test_float_maths_needs_approx():
    assert 0.1 + 0.2 != 0.3                     # True! floats are approximations
    assert 0.1 + 0.2 == pytest.approx(0.3)


def test_cart_total():
    cart = {"book": (12.5, 2), "pen": (1.2, 3)}
    assert cart_total(cart) == pytest.approx(28.6)


def test_parse_price_handles_symbols_and_commas():
    assert parse_price(" €1,234.50 ") == 1234.5
