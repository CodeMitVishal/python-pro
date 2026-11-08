"""Module 18 · Text vs bytes: Unicode, UTF-8 and encoding bugs

  str   = TEXT: a sequence of Unicode characters ("é", "₹", "日", "🐍")
  bytes = raw DATA: numbers 0-255, which is what files, networks and disks store

  text  --encode("utf-8")-->  bytes  --decode("utf-8")-->  text

Every file read and every network call is a decode/encode. Use the wrong
encoding and you get errors or "mojibake" (Ã© instead of é).
Rule: UTF-8 everywhere, and ALWAYS pass encoding="utf-8" to open().

Run it:  python 18_data_apis_databases/07_text_and_bytes.py
"""
import sys
import tempfile
import unicodedata
from pathlib import Path

# Real-world encoding bug #1, right here: a Windows console often uses cp1252, which
# can't print "₹" or "日" and raises UnicodeEncodeError. Tell stdout to speak UTF-8:
sys.stdout.reconfigure(encoding="utf-8")       # or run with:  python -X utf8 file.py

# --- 1. Characters vs bytes ------------------------------------------------------------------
for text in ["A", "é", "₹", "日"]:
    data = text.encode("utf-8")
    print(f"{text!r}: 1 character -> {len(data)} byte(s) {data}  code point U+{ord(text):04X}")
# UTF-8 uses 1 byte for English, 2-4 for everything else. len(str) != len(bytes)!

price = "Preis: 10 €"
print(len(price), "characters,", len(price.encode("utf-8")), "bytes")

# --- 2. Mojibake: decoding with the WRONG encoding -----------------------------------------------
raw = "Café Müller".encode("utf-8")
print("wrong:", raw.decode("latin-1"))          # CafÃ© MÃ¼ller  <- classic mojibake
print("right:", raw.decode("utf-8"))

# --- 3. Errors, and how to handle them ---------------------------------------------------------------
broken = b"Caf\xe9"                               # Latin-1 bytes, not valid UTF-8
try:
    broken.decode("utf-8")
except UnicodeDecodeError as e:
    print("UnicodeDecodeError:", e.reason)
print("replace:", broken.decode("utf-8", errors="replace"))   # Caf<?> : keep going, mark the bad byte
print("latin-1:", broken.decode("latin-1"))                    # if you KNOW the real encoding

# --- 4. Files: always say the encoding -------------------------------------------------------------------
path = Path(tempfile.mkdtemp()) / "names.txt"
path.write_text("Vishal\nRenée\nŁukasz\n", encoding="utf-8")
print(path.read_text(encoding="utf-8").split())
print("size on disk:", path.stat().st_size, "bytes")
# Without encoding=, Python uses the OS default (often cp1252 on Windows) and
# non-English names break. Opening in binary mode ("rb") gives you bytes.

# --- 5. Same look, different characters: normalise before comparing --------------------------------------
a = "é"                    # one character: U+00E9
b = "é"              # "e" + a combining accent: looks identical
print("equal?", a == b, "| after NFC:", unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b))
print("case-insensitive:", "STRASSE".casefold() == "straße".casefold())   # casefold > lower()

# --- 6. bytes in real life ------------------------------------------------------------------------------------
print(bytes.fromhex("48656c6c6f"), "Hello".encode().hex())   # hex dumps, hashes, binary protocols
