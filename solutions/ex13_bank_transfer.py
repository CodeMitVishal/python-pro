"""Solution · Exercise 13: Safe bank transfers

Run it:  python solutions/ex13_bank_transfer.py
"""
from contextlib import contextmanager


class BankError(Exception):
    pass


class InsufficientFunds(BankError):
    def __init__(self, account, balance, amount):
        super().__init__(f"{account} has {balance}, can't withdraw {amount}")
        self.account, self.balance, self.amount = account, balance, amount


def withdraw(accounts, name, amount):
    balance = accounts[name]
    if balance < amount:
        raise InsufficientFunds(name, balance, amount)
    accounts[name] = balance - amount


@contextmanager
def atomic(accounts):
    snapshot = dict(accounts)        # a COPY; `snapshot = accounts` would share the dict
    try:
        yield
    except Exception:
        accounts.clear()
        accounts.update(snapshot)    # restore in place, so callers see the rollback
        raise                        # never hide the error


def transfer(accounts, src, dst, amount):
    with atomic(accounts):
        accounts[dst] += amount      # deliberately first: a failure below must undo it
        withdraw(accounts, src, amount)


if __name__ == "__main__":
    accounts = {"vishal": 100, "raj": 50}
    transfer(accounts, "vishal", "raj", 30)
    assert accounts == {"vishal": 70, "raj": 80}

    try:
        transfer(accounts, "raj", "vishal", 500)
        raise AssertionError("expected InsufficientFunds")
    except InsufficientFunds as e:
        assert (e.account, e.balance, e.amount) == ("raj", 80, 500)
        assert isinstance(e, BankError)
    assert accounts == {"vishal": 70, "raj": 80}
    print("All checks passed!")
