"""Module 14 · Modules, packages and how import really works

  module  = one .py file
  package = a folder of modules (with an __init__.py)

When you write  import json  Python:
  1. checks sys.modules: already imported? Reuse it (code runs only ONCE)
  2. otherwise searches the folders in sys.path, in order
  3. runs the file top to bottom and stores the result in sys.modules

Run it:  python 14_packaging/01_modules_and_imports.py
"""
import sys
import json
import importlib

# --- 1. Where does Python look for modules? -----------------------------------------
print("First places Python searches:")
for folder in sys.path[:3]:
    print("  ", folder)          # 1st is the folder of the script you ran

# --- 2. Modules are cached: importing twice doesn't run the code twice --------------------
print("json" in sys.modules)     # True
import json as again
print(again is json)             # True: the same module object

# --- 3. Import styles ------------------------------------------------------------------
from pathlib import Path         # one name
import collections.abc as cabc   # a submodule with a short alias
print(Path.__module__, cabc.__name__)
# Avoid  from module import *  : you can't tell where names come from.

# --- 4. __name__: "am I being run, or imported?" ------------------------------------------
print("This file's __name__ is", repr(__name__))   # '__main__' when run directly
# In an imported module, __name__ is its import name, e.g. 'tasky.store'.
# That's why scripts end with:
#     if __name__ == "__main__":
#         main()
# so importing the file (e.g. in tests) doesn't run the program.

# --- 5. Import a module by name at runtime (plugins, config-driven code) -------------------
mod = importlib.import_module("statistics")
print(mod.mean([1, 2, 3, 4]))    # 2.5

# --- 6. Absolute vs relative imports (inside a package) -----------------------------------
# absolute:  from tasky.store import load_tasks     <- clear, preferred
# relative:  from .store import load_tasks          <- "from this package"
# Relative imports only work inside a package, not in a script you run directly.
# See the real package in 14_packaging/tasky_project/src/tasky/
