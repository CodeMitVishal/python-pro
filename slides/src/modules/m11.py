"""Slides · Module 11 · Iterators & generators"""
from teach_kit import code_out, cover, interview, job, mistake, picture, recap, trace, why

M = "Module 11 · Iterators &amp; generators"
SLIDES = [
 cover("11", "Iterators &amp; generators", "Process a 10 GB log file with 10 MB of memory. Every interview asks about yield.",
       [("How a for loop really works", "01_iteration_protocol.py"), ("Generators &amp; yield", "02_generators.py"),
        ("Lazy pipelines", "03_pipelines.py"), ("itertools", "04_itertools.py"),
        ("Demo: a 200,000-row CSV", "05_demo_big_csv.py"), ("send() &amp; async generators", "06_send_and_async_generators.py"),
        ("Interview Q&amp;A", "INTERVIEW.md")], M),

 why(M, "Generators", "Big data, small memory",
     "You must sum the prices in a <b>10 GB</b> CSV. <b>f.readlines()</b> loads it all into RAM and the server crashes.<br><br>"
     "You only ever need <b>one line at a time</b>.",
     "A <b>generator</b> produces values <b>one by one, on demand</b>, and forgets each value after you've used it."),

 picture(M, "Iteration protocol", "What a for loop really does",
     "&#127915; Think of a <b>ticket dispenser</b>. <b>iter()</b> gives you the dispenser; each <b>next()</b> hands out one ticket; "
     "when it's empty it says <b>StopIteration</b> and the loop ends.",
     [("for x in items:", "you write this"), ("it = iter(items)", "Python gets an iterator"),
      ("x = next(it)", "again and again"), ("StopIteration", "the loop stops quietly")]),

 code_out(M, "Iteration protocol", "Do the loop by hand", '''
items = ["a", "b"]
it = iter(items)
print(next(it))
print(next(it))
try:
    next(it)
except StopIteration:
    print("StopIteration: the for loop would end here")

print(iter(items) is iter(items))   # a new iterator each time
print(iter(it) is it)               # an iterator returns itself''',
     steps=["An <b>iterable</b> (list, str, dict, file) can give you an iterator.",
            "An <b>iterator</b> remembers its position and has <b>__next__</b>.", "Iterators are <b>single-use</b>."]),

 code_out(M, "Generators", "yield pauses the function", '''
def countdown(n):
    print("  (start)")
    while n > 0:
        yield n               # hand out n, then PAUSE here
        n -= 1
    print("  (done)")

gen = countdown(3)
print(gen)                    # nothing has run yet!
for x in gen:
    print("got", x)''',
     steps=["Calling the function only <b>creates</b> a generator.", "Each <b>next()</b> runs to the next <b>yield</b>, then pauses.",
            "Local variables survive between pauses."]),

 trace(M, "Generators", "Memory: list vs generator", ["", "List  [x*2 for x in data]", "Generator  (x*2 for x in data)"],
       [["Computed", "<b>all</b> values immediately", "one value per <b>next()</b>"],
        ["Memory for 10 million items", "~80 MB+", "~200 bytes"],
        ["Use it twice?", "yes", "no: it's empty after one pass"],
        ["len(), indexing [3]", "yes", "no"],
        ["Best for", "small data you reuse", "big data, streams, pipelines"]],
       "<b>sum(x * 2 for x in data)</b>: no extra brackets needed when it's the only argument."),

 picture(M, "Lazy pipelines", "Chain generators like an assembly line",
     "&#127981; Each station takes items from the previous one, does <b>one</b> job, and passes them on. "
     "Only <b>one item</b> is on the belt at a time, so a huge file uses almost no memory.",
     [("read_lines(path)", "yield each line"), ("parse(lines)", "yield a dict per line"),
      ("only_errors(rows)", "yield rows with status &gt;= 500"), ("count", "sum(1 for _ in rows)")]),

 code_out(M, "Lazy pipelines", "A log pipeline in 10 lines", '''
LOG = ["GET /home 200 12", "GET /api 500 340", "POST /pay 503 900",
       "GET /shop 200 30"]                    # imagine 10 GB

def parse(lines):
    for line in lines:
        method, path, status, ms = line.split()
        yield {"path": path, "status": int(status), "ms": int(ms)}

def errors(rows):
    return (r for r in rows if r["status"] >= 500)

bad = list(errors(parse(LOG)))
print([r["path"] for r in bad])
print("slowest:", max(r["ms"] for r in parse(LOG)), "ms")''',
     steps=["Each step is small, testable and named.", "Nothing runs until something <b>asks</b> for values (list, max, for).",
            "With a real file, <b>for line in open(path)</b> is already lazy."]),

 mistake(M, "Generators", "Using a generator twice",
     '''
squares = (n * n for n in range(5))
print(sum(squares))    # 30
print(sum(squares))    # 0  ???''',
     "A generator is <b>used up</b> after one pass. The second sum gets nothing and silently returns 0.",
     '''
def squares():
    return (n * n for n in range(5))

print(sum(squares()))  # 30
print(sum(squares()))  # 30''',
     "Need it twice? Create a new generator each time, or store a <b>list</b> if the data is small."),

 code_out(M, "itertools", "Ready-made lazy tools", '''
from itertools import batched, chain, groupby, islice, count

print(list(islice(count(100), 3)))          # endless, take 3
print(list(chain([1, 2], (3, 4))))          # glue iterables
print(list(batched(range(7), 3)))           # chunks (3.12+)

rows = [("de", "lamp"), ("de", "cable"), ("in", "plug")]
for country, group in groupby(rows, key=lambda r: r[0]):
    print(country, [item for _, item in group])''',
     steps=["<b>islice</b>: take a slice of any iterator.", "<b>batched</b>: send 1,000 rows per DB insert.",
            "<b>groupby</b> groups <b>neighbours</b>: sort by the key first."]),

 job(M, "Generators", "Where they show up at work", [
     ("Stream a big CSV export", '''
def rows():
    for order in Order.objects.iterator():
        yield [order.id, order.total]'''),
     ("FastAPI streaming response", '''
return StreamingResponse(rows_as_csv(),
                         media_type="text/csv")'''),
     ("Paginate an external API", '''
def all_users(client):
    page = 1
    while batch := client.get(page):
        yield from batch; page += 1'''),
     ("pytest fixtures with cleanup", '''
@pytest.fixture
def db():
    conn = connect(); yield conn; conn.close()'''),
 ]),

 interview(M, "What is a generator, and when do you use one?",
     ["A function with <b>yield</b>. Calling it returns a generator object; values are produced <b>lazily</b>, one per <b>next()</b>.",
      "Its state (local variables, position) is kept between calls.",
      "Use it for <b>large or infinite data</b>, streaming and pipelines: memory stays constant.",
      "A <b>generator expression</b> <b>(x for x in xs)</b> is the one-line version.",
      "It's single-use, has no len(), and raises StopIteration when finished."],
     '''
def read_big(path):
    with open(path) as f:
        for line in f:
            yield line.rstrip()

total = sum(len(l) for l in read_big("app.log"))''',
     "\"What's the difference between an iterable and an iterator?\" (an iterable can create iterators via __iter__; an iterator has __next__ and remembers its position)."),

 interview(M, "What does yield from do? What about yield in pytest?",
     ["<b>yield from other</b> hands out every value of another iterable, as if you looped and yielded each one.",
      "It's how you <b>delegate</b> to a sub-generator (e.g. walking a tree recursively).",
      "In a pytest fixture or a <b>@contextmanager</b>, code <b>before</b> yield is setup and code <b>after</b> yield is teardown."],
     '''
def walk(tree):
    for name, child in tree.items():
        if isinstance(child, dict):
            yield from walk(child)
        else:
            yield name''',
     "\"How would you read a 10 GB file in Python?\" (iterate the file object line by line or in chunks; never read() it all)."),

 recap(M, "Module 11 in 6 lines",
     ["<b>for</b> = <b>iter()</b> + <b>next()</b> until <b>StopIteration</b>.",
      "<b>yield</b> pauses a function and keeps its state.",
      "Generators are <b>lazy</b>: constant memory, but single-use.",
      "Chain small generators into a <b>pipeline</b>.",
      "<b>itertools</b>: islice, chain, batched, groupby (sort first!).",
      "<b>yield from</b> delegates; <b>yield</b> in fixtures = setup / teardown."],
     "Do <b>exercises/ex11_generators.py</b>: build a lazy pipeline over a big log."),
]
