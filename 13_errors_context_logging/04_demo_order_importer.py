"""Module 13 · Demo: a robust order importer

Imports orders from CSV text. Bad rows must not crash the import:
  - custom exceptions describe WHAT is wrong with a row
  - a transaction context manager rolls back a whole batch on failure
  - logging records what happened, at the right level

Run it:  python 13_errors_context_logging/04_demo_order_importer.py
"""
import csv
import io
import logging
import sys
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO, format="%(levelname)-7s %(message)s",
                    stream=sys.stdout)          # same stream as print(), so lines stay in order
log = logging.getLogger("importer")


class ImportErrorBase(Exception):
    pass


class InvalidRow(ImportErrorBase):
    def __init__(self, line_no, reason):
        super().__init__(f"line {line_no}: {reason}")


DB = []                                          # pretend database


@contextmanager
def batch_transaction():
    snapshot = len(DB)
    try:
        yield
        log.info("batch committed (%d orders in DB)", len(DB))
    except ImportErrorBase:
        del DB[snapshot:]                        # undo everything from this batch
        log.warning("batch rolled back")
        raise


def parse_row(line_no, row):
    try:
        qty = int(row["qty"])
        price = float(row["price"])
    except ValueError as e:
        raise InvalidRow(line_no, f"not a number ({e})") from e
    if qty <= 0:
        raise InvalidRow(line_no, "qty must be positive")
    return {"customer": row["customer"], "total": round(qty * price, 2)}


def import_orders(text, strict):
    reader = csv.DictReader(io.StringIO(text))
    skipped = 0
    with batch_transaction():
        for line_no, row in enumerate(reader, start=2):      # line 1 is the header
            try:
                DB.append(parse_row(line_no, row))
            except InvalidRow as e:
                if strict:
                    raise                                    # fail the whole batch
                skipped += 1
                log.warning("skipped %s", e)
    log.info("imported, %d row(s) skipped", skipped)


CSV = """customer,qty,price
vishal,2,19.99
raj,abc,5.00
li,-1,3.50
sam,1,99.00"""

print("--- lenient mode: skip bad rows ---")
import_orders(CSV, strict=False)

print("\n--- strict mode: one bad row cancels the batch ---")
try:
    import_orders(CSV, strict=True)
except ImportErrorBase as e:
    log.error("import failed: %s", e)
print(f"\nDB holds {len(DB)} orders: {DB}")
