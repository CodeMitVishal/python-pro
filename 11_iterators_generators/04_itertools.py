"""Module 11 · itertools: a toolbox of fast, lazy iterators

TEACHING NOTES
  Why it matters  Slicing, chunking, grouping and combining iterators are solved problems; don't
                  rewrite them.
  Picture it      A toolbox of conveyor-belt attachments: slicers, joiners, batchers, groupers.
  Watch out       groupby only groups NEIGHBOURS with the same key: sort by the key first.
  In real jobs    batched() for bulk DB inserts, islice for previews, chain for combining
                  sources.
  Interview       Q: Name some itertools functions you have used.
                  A: islice, chain, batched, groupby, count, product, permutations, accumulate.

Run it:  python 11_iterators_generators/04_itertools.py
"""
from itertools import (accumulate, chain, combinations, count, cycle,
                       groupby, islice, pairwise, product, zip_longest)

# count / cycle: infinite counters, use islice to take a few
print(list(islice(count(10, 5), 4)))            # [10, 15, 20, 25]
print(list(islice(cycle("AB"), 5)))             # ['A', 'B', 'A', 'B', 'A']

# chain: loop over several iterables as one
print(list(chain([1, 2], (3, 4), "ab")))        # [1, 2, 3, 4, 'a', 'b']

# accumulate: running totals
print(list(accumulate([5, 10, 20])))            # [5, 15, 35]

# pairwise: neighbours (Python 3.10+)
temps = [12, 15, 11, 18]
print([b - a for a, b in pairwise(temps)])      # [3, -4, 7]  change per day

# groupby: group CONSECUTIVE items with the same key (sort first!)
sales = [("DE", 100), ("IN", 80), ("DE", 50), ("IN", 20)]
sales.sort(key=lambda s: s[0])
for country, rows in groupby(sales, key=lambda s: s[0]):
    print(country, sum(amount for _, amount in rows))   # DE 150 / IN 100

# product: every combination, like nested for loops
print(list(product("SM", ["red", "blue"])))
# [('S', 'red'), ('S', 'blue'), ('M', 'red'), ('M', 'blue')]

# combinations: pick r items, order doesn't matter
print(list(combinations(["Vishal", "Raj", "Li"], 2)))
# [('Vishal', 'Raj'), ('Vishal', 'Li'), ('Raj', 'Li')]

# zip_longest: like zip, but fills the shorter one
print(list(zip_longest([1, 2, 3], "ab", fillvalue="-")))
# [(1, 'a'), (2, 'b'), (3, '-')]
