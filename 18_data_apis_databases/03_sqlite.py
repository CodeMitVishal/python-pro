"""Module 18 · Databases with sqlite3 (built into Python)

SQLite is a full SQL database stored in ONE file (or in memory). Perfect for
learning SQL, tests, small apps and prototypes. The same ideas work with
PostgreSQL or MySQL.

Run it:  python 18_data_apis_databases/03_sqlite.py
"""
import sqlite3

conn = sqlite3.connect(":memory:")       # use a file name like "shop.db" to keep the data
conn.row_factory = sqlite3.Row           # rows behave like dicts: row["name"]

# --- 1. Create a table ---------------------------------------------------------------
conn.execute("""
    CREATE TABLE products (
        id    INTEGER PRIMARY KEY,       -- unique id, filled in automatically
        name  TEXT    NOT NULL UNIQUE,
        price REAL    NOT NULL CHECK (price >= 0),
        stock INTEGER NOT NULL DEFAULT 0
    )
""")

# --- 2. Insert with PARAMETERS (?): never build SQL with f-strings ---------------------------
products = [("Laptop", 899.0, 5), ("Mouse", 19.9, 50), ("Monitor", 249.0, 0)]
with conn:                               # a transaction: commit on success, rollback on error
    conn.executemany("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", products)

# --- 3. Query ------------------------------------------------------------------------------
for row in conn.execute("SELECT name, price FROM products WHERE stock > ? ORDER BY price", (0,)):
    print(f"{row['name']:<8} {row['price']:>7.2f}")

total = conn.execute("SELECT SUM(price * stock) AS value FROM products").fetchone()["value"]
print(f"stock value: {total:,.2f}")       # 5,490.00

# --- 4. Why parameters matter: SQL injection ----------------------------------------------------
user_input = "x' OR '1'='1"
unsafe_sql = f"SELECT COUNT(*) FROM products WHERE name = '{user_input}'"
print("f-string query matched:", conn.execute(unsafe_sql).fetchone()[0], "rows  <- attacker sees everything!")
safe = conn.execute("SELECT COUNT(*) FROM products WHERE name = ?", (user_input,)).fetchone()[0]
print("parameter query matched:", safe, "rows")

# --- 5. Transactions: all or nothing ----------------------------------------------------------
try:
    with conn:
        conn.execute("UPDATE products SET stock = stock - 1 WHERE name = 'Laptop'")
        conn.execute("INSERT INTO products (name, price) VALUES ('Mouse', 9.9)")   # duplicate name!
except sqlite3.IntegrityError as e:
    print("rolled back:", e)
laptops = conn.execute("SELECT stock FROM products WHERE name = 'Laptop'").fetchone()["stock"]
print("laptop stock is still", laptops)   # 5: the UPDATE was undone too

conn.close()
