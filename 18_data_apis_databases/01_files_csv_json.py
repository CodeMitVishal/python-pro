"""Module 18 · Files, CSV and JSON the professional way

  pathlib  -> paths as objects: join with /, read/write in one call, works on every OS
  csv      -> DictReader/DictWriter handle quoting, commas inside values, headers
  json     -> the format every web API speaks

TEACHING NOTES
  Why it matters  Every integration starts with reading or writing files: CSV exports, JSON
                  configs.
  Picture it      pathlib treats paths as objects; csv.DictReader turns each row into a labelled
                  dict.
  Watch out       Always pass encoding='utf-8' (and newline='' for CSV); CSV values are strings.
  In real jobs    Partner CSV imports, JSON fixtures and configs, report exports.
  Interview       Q: How do you read a large CSV safely?
                  A: csv.DictReader over the open file, row by row, with explicit encoding and
                     type conversion.

Run it:  python 18_data_apis_databases/01_files_csv_json.py
"""
import csv
import json
import tempfile
from pathlib import Path

work = Path(tempfile.mkdtemp(prefix="pypro_"))      # a scratch folder for this demo

# --- 1. pathlib basics ------------------------------------------------------------
report = work / "reports" / "2026" / "sales.csv"    # "/" joins path parts
report.parent.mkdir(parents=True, exist_ok=True)    # create all missing folders
print(report.name, report.stem, report.suffix)      # sales.csv sales .csv
print(report.parent.name)                           # 2026

# --- 2. Write and read CSV with dictionaries --------------------------------------------
rows = [
    {"customer": "Vishal", "city": "Augsburg", "total": 120.5},
    {"customer": "Raj", "city": "Mumbai, MH", "total": 80.0},   # a comma inside a value!
]
with report.open("w", newline="", encoding="utf-8") as f:   # newline="" is required for csv
    writer = csv.DictWriter(f, fieldnames=["customer", "city", "total"])
    writer.writeheader()
    writer.writerows(rows)

print(report.read_text(encoding="utf-8"))
# customer,city,total
# Vishal,Augsburg,120.5
# Raj,"Mumbai, MH",80.0      <- csv quoted it for us

with report.open(newline="", encoding="utf-8") as f:
    loaded = list(csv.DictReader(f))
print(loaded[1]["city"], type(loaded[1]["total"]).__name__)   # Mumbai, MH str  <- CSV is all text!
total = sum(float(r["total"]) for r in loaded)
print(f"total: {total}")                                      # total: 200.5

# --- 3. JSON: Python objects <-> text ------------------------------------------------
config = {"app": "shop", "debug": False, "ports": [8000, 8001], "owner": None}
path = work / "config.json"
path.write_text(json.dumps(config, indent=2), encoding="utf-8")
again = json.loads(path.read_text(encoding="utf-8"))
print(again == config, again["ports"][0])           # True 8000
# JSON has no dates or sets: convert them first (date.isoformat(), list(my_set)).

# --- 4. Find files with glob -------------------------------------------------------------
for p in sorted(work.rglob("*")):                   # every file and folder, recursively
    if p.is_file():
        print("found:", p.relative_to(work))
