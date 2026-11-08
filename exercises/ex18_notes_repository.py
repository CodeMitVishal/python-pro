"""Exercise 18 · A notes database with sqlite3

Build NotesRepository: a class that hides all the SQL behind clean methods
(the "repository pattern"). The rest of an app then never touches SQL.

  repo = NotesRepository(":memory:")       # or a file name like "notes.db"
  note_id = repo.add("Shopping", "milk, eggs", tags=["home"])
  repo.get(note_id)      -> {"id": 1, "title": "Shopping", "body": "milk, eggs", "tags": ["home"]}
  repo.get(999)          -> None
  repo.search("milk")    -> notes whose title OR body contains the text (case-insensitive)
  repo.delete(note_id)   -> True if a note was deleted, else False
  repo.count()           -> number of notes

Rules:
  - ALWAYS use ? parameters, never f-strings in SQL
  - store tags as JSON text (json.dumps / json.loads)
  - use `with self.conn:` for writes, so they're committed (or rolled back)

Run it to check your work:
    python exercises/ex18_notes_repository.py

Stuck? Compare with solutions/ex18_notes_repository.py
"""
import json
import sqlite3


class NotesRepository:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        # TODO: create the notes table (id, title, body, tags)

    def add(self, title, body, tags=None):
        """TODO: insert and return the new id (cursor.lastrowid)"""

    def get(self, note_id):
        """TODO: return a dict, or None"""

    def search(self, text):
        """TODO: LIKE '%text%' on title OR body; return a list of dicts"""

    def delete(self, note_id):
        """TODO: return True if a row was deleted (cursor.rowcount)"""

    def count(self):
        """TODO"""


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    repo = NotesRepository(":memory:")
    a = repo.add("Shopping", "milk, eggs", tags=["home"])
    b = repo.add("Work", "Record MILK video")
    assert repo.count() == 2
    assert repo.get(a) == {"id": a, "title": "Shopping", "body": "milk, eggs", "tags": ["home"]}
    assert repo.get(b)["tags"] == []
    assert repo.get(999) is None
    assert {n["id"] for n in repo.search("milk")} == {a, b}
    assert repo.search("nothing") == []
    evil = "x' OR '1'='1"
    assert repo.search(evil) == [], "use ? parameters: f-strings allow SQL injection"
    assert repo.delete(a) is True and repo.delete(a) is False
    assert repo.count() == 1
    print("All checks passed!")
