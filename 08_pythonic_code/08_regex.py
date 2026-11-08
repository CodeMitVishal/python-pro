"""Module 8 · Regular expressions with `re`: find patterns in text

A regex describes the SHAPE of text: "digits, a dash, more digits".
Use it to validate input, extract data from logs, and clean text.
(For simple cases, str methods like .startswith() or .split() are clearer.)

Cheat sheet:  \\d digit   \\w letter/digit/_   \\s whitespace   .  any char
              +  1 or more   *  0 or more   ?  optional   {2,4}  2 to 4 times
              [abc] one of   [^abc] none of   ^ start   $ end   ( ) capture group

TEACHING NOTES
  Why it matters  Logs, emails and IDs hide in text; string methods alone can't describe
                  patterns.
  Picture it      A regex is a stencil laid over text: wherever the text fits the stencil, you
                  have a match.
  Watch out       Always use raw strings r'...'; and don't validate complex formats (HTML, full
                  emails) with one giant regex.
  In real jobs    Masking secrets in logs, parsing log lines, validating IDs and postcodes.
  Interview       Q: search vs match vs fullmatch?
                  A: match checks at the start, search anywhere, fullmatch requires the whole
                     string to match.

Run it:  python 08_pythonic_code/08_regex.py
"""
import re

log = """2026-11-08 10:14:20 ERROR payment failed user=vishal amount=49.90
2026-11-08 10:15:02 INFO  login ok user=raj
2026-11-08 10:16:45 ERROR db timeout user=li amount=12.00"""

# --- 1. search vs match vs fullmatch ------------------------------------------------------
print(bool(re.search(r"ERROR", log)))                 # anywhere in the text
print(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", "2026-11-08")))   # the WHOLE string must match

# --- 2. findall: every match -----------------------------------------------------------------
print(re.findall(r"user=(\w+)", log))                 # ['vishal', 'raj', 'li']  (the group only)

# --- 3. Named groups: readable extraction -----------------------------------------------------
pattern = re.compile(                                  # compile once, reuse many times
    r"^(?P<date>\S+) (?P<time>\S+) (?P<level>ERROR)\s+(?P<msg>.+?) user=(?P<user>\w+)"
    r"(?: amount=(?P<amount>\d+\.\d{2}))?$",            # (?: ) = group without capturing
    re.MULTILINE,                                      # ^ and $ match at every line
)
for m in pattern.finditer(log):
    print(m["time"], m["user"], m["msg"], float(m["amount"]))

# --- 4. sub: search and replace (with a function, too) ------------------------------------------
masked = re.sub(r"user=\w+", "user=***", log.splitlines()[0])
print(masked)
print(re.sub(r"\d+\.\d{2}", lambda m: f"{float(m[0]) * 1.19:.2f}", "net 10.00 / 20.00"))

# --- 5. Validation (keep it simple!) ---------------------------------------------------------------
GERMAN_PLZ = re.compile(r"\d{5}")
for plz in ["86150", "8615", "86150a"]:
    print(plz, bool(GERMAN_PLZ.fullmatch(plz)))

# --- 6. split on several separators ---------------------------------------------------------------
print(re.split(r"[,;\s]+", "python, sql;  docker azure"))   # ['python', 'sql', 'docker', 'azure']

# Always use raw strings r"..." so backslashes reach the regex engine untouched.
# Beware of "catastrophic backtracking" patterns like (a+)+ on untrusted input.
