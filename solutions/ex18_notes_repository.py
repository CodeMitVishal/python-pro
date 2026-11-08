"""Solution · Exercise 18: A notes database with sqlite3

Run it:  python solutions/ex18_notes_repository.py
"""
import json
import sqlite3


class NotesRepository:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id    INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    body  TEXT NOT NULL,
                    tags  TEXT NOT NULL DEFAULT '[]'
                )
            """)

    @staticmethod
    def _to_dict(row):
        return {"id": row["id"], "title": row["title"], "body": row["body"],
                "tags": json.loads(row["tags"])}

    def add(self, title, body, tags=None):
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO notes (title, body, tags) VALUES (?, ?, ?)",
                (title, body, json.dumps(tags or [])),
            )
        return cur.lastrowid

    def get(self, note_id):
        row = self.conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
        return self._to_dict(row) if row else None

    def search(self, text):
        pattern = f"%{text}%"              # the % wildcards go in the VALUE, not the SQL
        rows = self.conn.execute(
            "SELECT * FROM notes WHERE title LIKE ? OR body LIKE ? ORDER BY id",
            (pattern, pattern),            # LIKE is case-insensitive for ASCII in SQLite
        )
        return [self._to_dict(r) for r in rows]

    def delete(self, note_id):
        with self.conn:
            cur = self.conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        return cur.rowcount > 0

    def count(self):
        return self.conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]


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
    assert repo.search(evil) == []
    assert repo.delete(a) is True and repo.delete(a) is False
    assert repo.count() == 1
    print("All checks passed!")
