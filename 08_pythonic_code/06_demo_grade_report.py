"""Module 8 · Demo: a grade report, written the Pythonic way

Everything from this module in one small program: comprehensions,
unpacking, enumerate, zip, sorted with key, any/all, f-string tables.

Run it:  python 08_pythonic_code/06_demo_grade_report.py
"""

raw = """Vishal,91,88,95
Raj,78,64,70
Li,85,92,79
Sam,45,52,38"""

# 1. Parse: split lines, unpack the name, convert the rest with a comprehension
students = {}
for line in raw.splitlines():
    name, *marks = line.split(",")
    students[name] = [int(m) for m in marks]

# 2. Average per student with a dict comprehension
averages = {name: sum(marks) / len(marks) for name, marks in students.items()}

# 3. Rank: sort the (name, average) pairs by average, best first
ranking = sorted(averages.items(), key=lambda pair: pair[1], reverse=True)

# 4. Print a neat table with enumerate + f-string alignment
print(f"{'#':<3}{'Name':<10}{'Avg':>6}  Result")
print("-" * 28)
for place, (name, avg) in enumerate(ranking, start=1):
    result = "PASS" if avg >= 50 else "FAIL"
    print(f"{place:<3}{name:<10}{avg:>6.1f}  {result}")

# 5. Class-level questions answered with any/all and a generator expression
print()
print(f"Everyone passed?  {all(avg >= 50 for avg in averages.values())}")
print(f"Any top scorer?   {any(avg >= 90 for avg in averages.values())}")
best_name, best_avg = ranking[0]
print(f"Best student:     {best_name} ({best_avg:.1f})")
