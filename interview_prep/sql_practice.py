"""Interview prep · SQL questions you will be asked (runnable, with SQLite)

Each query answers a classic interview question on a tiny shop database.
Read the question, try to write the SQL yourself, then compare.

Run it:  python interview_prep/sql_practice.py
"""
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INT, manager_id INT);
INSERT INTO employees VALUES
  (1, 'Vishal', 'eng',   9000, NULL), (2, 'Li',    'eng',   7000, 1),
  (3, 'Sam',    'eng',   7000, 1),    (4, 'Priya', 'sales', 6000, 1),
  (5, 'Mia',    'sales', 5500, 4),    (6, 'Raj',   'ops',   4000, 1);

CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO customers VALUES
  (1, 'Alpha Corp', 'a@x.de'), (2, 'Beta GmbH', 'b@x.de'), (3, 'Gamma AG', 'a@x.de'), (4, 'Delta', 'd@x.de');

CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INT, total REAL, created TEXT);
INSERT INTO orders VALUES
  (1, 1, 120, '2026-10-02'), (2, 1, 80, '2026-10-15'), (3, 2, 300, '2026-10-20'),
  (4, 3, 50, '2026-11-01'),  (5, 2, 40, '2026-11-03'), (6, 1, 200, '2026-11-05');
""")


def ask(question: str, sql: str) -> None:
    print(f"\n-- {question}")
    for row in db.execute(sql):
        print("  ", row)


# 1. JOIN + GROUP BY
ask("Revenue per customer, including customers with NO orders (LEFT JOIN)", """
SELECT c.name, COUNT(o.id) AS orders, COALESCE(SUM(o.total), 0) AS revenue
FROM customers c LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id ORDER BY revenue DESC""")

# 2. HAVING filters groups (WHERE filters rows)
ask("Customers with more than 1 order", """
SELECT customer_id, COUNT(*) AS n FROM orders
GROUP BY customer_id HAVING COUNT(*) > 1""")

# 3. Second highest salary (the most famous one)
ask("Second highest DISTINCT salary", """
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees)""")

# 4. Window functions: rank inside a group
ask("Top earner per department (window function)", """
SELECT dept, name, salary FROM (
  SELECT dept, name, salary,
         RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
  FROM employees)
WHERE rnk = 1""")

# 5. Duplicates
ask("Find duplicate emails", """
SELECT email, COUNT(*) FROM customers GROUP BY email HAVING COUNT(*) > 1""")

# 6. Self join
ask("Employees with their manager's name (self join)", """
SELECT e.name, m.name AS manager
FROM employees e LEFT JOIN employees m ON m.id = e.manager_id""")

# 7. Anti-join
ask("Customers who never ordered (NOT EXISTS)", """
SELECT name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id)""")

# 8. Running total
ask("Running total of revenue by date (window SUM)", """
SELECT created, total, SUM(total) OVER (ORDER BY created) AS running
FROM orders ORDER BY created""")

# 9. Group by month
ask("Revenue per month", """
SELECT substr(created, 1, 7) AS month, SUM(total) FROM orders
GROUP BY month ORDER BY month""")

# 10. Above the department average (correlated subquery)
ask("Employees paid above their department's average", """
SELECT name, dept, salary FROM employees e
WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept = e.dept)""")

print("\nRemember the logical order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT.")
