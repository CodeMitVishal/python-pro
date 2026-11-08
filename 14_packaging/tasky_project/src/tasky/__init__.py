"""tasky: a tiny command-line to-do list.

__init__.py runs when someone does `import tasky`. Keep it small: expose the
public API and the version, nothing heavy.
"""
from tasky.store import Task, TaskStore

__all__ = ["Task", "TaskStore"]      # what `from tasky import *` exports
__version__ = "0.1.0"
