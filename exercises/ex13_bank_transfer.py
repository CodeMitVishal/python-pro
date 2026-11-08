"""Exercise 13 · Safe bank transfers

A transfer takes money from one account and puts it into another. If
anything fails halfway, NO money may disappear or appear.

  1. InsufficientFunds: a custom exception (subclass of BankError) that
     stores .account, .balance and .amount
  2. withdraw(accounts, name, amount): raise InsufficientFunds if the balance
     is too low, otherwise subtract the amount
  3. atomic(accounts): a context manager (use @contextmanager) that takes a
     snapshot (a copy!) of the balances and restores it if the block raises.
     It must re-raise the error.
  4. transfer(accounts, src, dst, amount): inside `with atomic(accounts):`,
     add to dst FIRST, then withdraw from src (so a failure really tests the rollback)

Run it to check your work:
    python exercises/ex13_bank_transfer.py

Stuck? Compare with solutions/ex13_bank_transfer.py
"""
from contextlib import contextmanager


class BankError(Exception):
    pass


# TODO 1: class InsufficientFunds(BankError): ...


def withdraw(accounts, name, amount):
    """TODO 2"""


@contextmanager
def atomic(accounts):
    """TODO 3"""
    yield


def transfer(accounts, src, dst, amount):
    """TODO 4"""


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    accounts = {"vishal": 100, "raj": 50}
    transfer(accounts, "vishal", "raj", 30)
    assert accounts == {"vishal": 70, "raj": 80}

    try:
        transfer(accounts, "raj", "vishal", 500)
        raise AssertionError("expected InsufficientFunds")
    except InsufficientFunds as e:                         # noqa: F821
        assert (e.account, e.balance, e.amount) == ("raj", 80, 500)
        assert isinstance(e, BankError)
    assert accounts == {"vishal": 70, "raj": 80}, "the failed transfer must be rolled back"
    print("All checks passed!")
