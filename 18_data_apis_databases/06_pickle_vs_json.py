"""Module 18 · Serialization: pickle vs JSON (and why pickle can be dangerous)

pickle turns almost ANY Python object into bytes and back: classes, sets,
datetimes, nested structures. Convenient for caching your OWN data.

But loading a pickle can RUN CODE. An object can tell pickle "to rebuild me,
call this function". A crafted file can therefore run anything on your
machine. Never unpickle data from users, the internet, or anything you don't trust.

For data exchange (APIs, files, other languages) use JSON. It's plain data:
loading it never runs code.

Run it:  python 18_data_apis_databases/06_pickle_vs_json.py
"""
import json
import pickle
from dataclasses import asdict, dataclass
from datetime import date


@dataclass
class Invoice:
    number: int
    due: date
    tags: set[str]


inv = Invoice(42, date(2026, 12, 8), {"urgent", "b2b"})

# --- 1. pickle handles everything... -------------------------------------------------------------
blob = pickle.dumps(inv)
print("pickle round trip:", pickle.loads(blob) == inv, f"({len(blob)} bytes, not human-readable)")

# --- 2. ...JSON needs plain data, so convert first ---------------------------------------------------
as_json = json.dumps({**asdict(inv), "due": inv.due.isoformat(), "tags": sorted(inv.tags)})
print("json:", as_json)
back = json.loads(as_json)
restored = Invoice(back["number"], date.fromisoformat(back["due"]), set(back["tags"]))
print("json round trip:", restored == inv)


# --- 3. Why untrusted pickles are dangerous (a HARMLESS demonstration) --------------------------------
class Sneaky:
    def __reduce__(self):                        # "to unpickle me, call print(...)"
        return (print, ("!!! this ran just by LOADING the pickle: it could have been os.system(...)",))


evil_bytes = pickle.dumps(Sneaky())
pickle.loads(evil_bytes)                         # code runs during loading

# JSON can't do that: loading it only ever builds dicts, lists, strings and numbers.
print(json.loads('{"__reduce__": "print"}'))     # just a dict
