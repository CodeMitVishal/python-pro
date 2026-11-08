"""Slide data for the newer bonus lessons and the interviews & AI track (Modules 29-30).
Imported by build_module_slides.py, which passes in its layout functions."""


def ai_slides(title, code, table, cards, exercise):
    S = []
    M = "Bonus lessons · Modules 10, 13, 18"
    S += [
     table(M, "Bonus · Recursion, debugging, text &amp; bytes", "Three skills every pro needs",
           ["Lesson", "Key idea"],
           [["<b>10 · 07_recursion.py</b>", "base case + smaller problem; the call stack; <span class=\"m\">@lru_cache</span> turns fib(30) from 2.7M calls into 31"],
            ["<b>13 · 06_debugging_like_a_pro.py</b>", "<span class=\"m\">breakpoint()</span>, pdb commands, post-mortem, <span class=\"m\">faulthandler</span>, VS Code launch.json"],
            ["<b>18 · 07_text_and_bytes.py</b>", "<span class=\"m\">str</span> is text, <span class=\"m\">bytes</span> is data; always <span class=\"m\">encoding=\"utf-8\"</span>; mojibake; NFC"]],
           src='''def total_size(folder):
    if folder.is_file():          # base case
        return folder.size
    return sum(total_size(c)      # smaller problem
               for c in folder.children)

(Pdb) n  s  c  p total  w  q''', width=640),
    ]

    # ---------------------------------------------------------------- Module 29
    M = "Module 29 · Algorithms &amp; data structures"
    S += [
     title("29", "Algorithms &amp; data structures", "The classics behind every coding interview, timed so you see Big-O.",
           [("Sorting &amp; searching", "01_sorting_and_searching.py"), ("Stacks, queues, linked lists", "02_stacks_queues_linked_lists.py"),
            ("Trees", "03_trees.py"), ("Graphs", "04_graphs.py"), ("Dynamic programming", "05_dynamic_programming.py"),
            ("Problem-solving patterns", "06_problem_solving_patterns.py"), ("Exercise: interview problems", "ex29_interview_problems.py")]),
     table(M, "Lessons 01-03 · Cheat sheet", "Pick the algorithm by its Big-O", ["Algorithm / structure", "Time", "Remember"],
           [["<b>bubble / insertion sort</b>", "O(n²)", "fine for tiny or almost-sorted data"],
            ["<b>merge sort</b> · <span class=\"m\">sorted()</span>", "O(n log n)", "stable; Python's Timsort is merge-based"],
            ["<b>quick sort</b>", "O(n log n) avg", "O(n²) on a bad pivot"],
            ["<b>binary search</b>", "O(log n)", "data must be <b>sorted</b>; <span class=\"m\">bisect</span>"],
            ["<b>stack</b> (list) · <b>queue</b> (deque)", "O(1) push/pop", "undo, brackets · BFS, jobs"],
            ["<b>BST</b>", "O(log n) … O(n)", "in-order = sorted; sorted inserts make it a list"]],
           tip="Measure, don't guess: the lesson times bubble vs merge sort on 2,000 numbers."),
     code(M, "Lesson 04 · Graphs", "Dijkstra: cheapest route with a heap", '''
def dijkstra(graph, start):
    best = {start: 0}
    heap = [(0, start)]                    # (distance, city)
    while heap:
        dist, city = heapq.heappop(heap)   # closest unfinished city
        if dist > best.get(city, inf):
            continue                       # outdated entry
        for nxt, km in graph[city].items():
            if dist + km < best.get(nxt, inf):
                best[nxt] = dist + km
                heapq.heappush(heap, (dist + km, nxt))
    return best''',
          ["<b>BFS</b> (queue): fewest hops when every edge counts the same.",
           "<b>DFS</b> (stack): explore everything, find cycles.",
           "<b>Topological sort</b>: a valid order for tasks with dependencies."], size=23, width=980),
     table(M, "Lessons 05-06 · Patterns", "Most interview problems are one of these", ["Pattern", "Signal in the question", "Example"],
           [["<b>Hash map</b>", "\"have I seen …?\", pairs, counts", "two sum O(n), anagrams"],
            ["<b>Two pointers</b>", "sorted data, both ends", "palindrome, pair sum"],
            ["<b>Sliding window</b>", "longest / best sub-array or substring", "longest unique substring"],
            ["<b>Prefix sums</b>", "many range-sum questions", "sales of days i..j in O(1)"],
            ["<b>BFS / DFS</b>", "grid, network, connected parts", "count islands"],
            ["<b>Dynamic programming</b>", "overlapping subproblems, \"fewest / most ways\"", "coin change, edit distance"]],
           tip="Process: restate → brute force → find the pattern → code → edge cases → state Big-O."),
     exercise(29, "Six classic interview problems", ["two_sum in O(n)", "valid_brackets with a stack",
                                                     "merge_intervals · longest_unique_substring",
                                                     "count_islands (BFS) · min_coins (DP)"],
              "ex29_interview_problems.py", '''$ python exercises/ex29_interview_problems.py
AssertionError            # until you solve it

$ python solutions/ex29_interview_problems.py
All checks passed!        # incl. a 1 s time limit'''),
    ]

    # ---------------------------------------------------------------- Module 30
    M = "Module 30 · AI with Python"
    S += [
     title("30", "AI with Python", "LLM APIs, tools, RAG and agents behind FastAPI: safe, cheap and tested.",
           [("Shared client (offline or real)", "llm_client.py"), ("LLM API basics", "01_llm_api_basics.py"),
            ("Structured output &amp; tools", "02_structured_output_and_tools.py"), ("Embeddings &amp; RAG", "03_embeddings_and_rag.py"),
            ("Agent behind an API", "04_agent_api.py"), ("Safety, cost &amp; evals", "05_safety_cost_eval.py"),
            ("Exercise: AI toolkit", "ex30_ai_toolkit.py")]),
     code(M, "Lesson 01 · LLM API basics", "One endpoint: messages in, a message out", '''
client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1000,
    system="You are a concise Python tutor.",
    messages=[{"role": "user", "content": "What is a generator?"}],
)
if response.stop_reason == "max_tokens": ...   # cut off!
text = "".join(b.text for b in response.content if b.type == "text")
print(response.usage.input_tokens, response.usage.output_tokens)

with client.messages.stream(...) as stream:     # word by word
    for chunk in stream.text_stream: print(chunk, end="")''',
          ["The API is <b>stateless</b>: resend the history every turn.",
           "<span class=\"m\">content</span> is a list of blocks: text, thinking, tool_use.",
           "Steer with the <b>system prompt</b> and <span class=\"m\">effort</span>; current models reject <span class=\"m\">temperature</span>."],
          tip="Every lesson runs <b>offline</b> with a fake client. <span class=\"m\">USE_REAL_LLM=1</span> switches to Claude (or Azure Foundry).",
          size=22, width=1000),
     code(M, "Lesson 02 · Tools", "The agent loop: the model asks, your code acts", '''
messages = [{"role": "user", "content": question}]
for step in range(max_steps):
    r = client.messages.create(model=MODEL, max_tokens=4000,
                               tools=TOOLS, messages=messages)
    if r.stop_reason != "tool_use":
        return text_of(r)                      # final answer
    messages.append({"role": "assistant", "content": r.content})
    results = []
    for b in r.content:
        if b.type == "tool_use":
            try:    out = REGISTRY[b.name](**b.input)
            except Exception as e:
                out, err = f"error: {e}", True   # is_error=True
            results.append({"type": "tool_result",
                            "tool_use_id": b.id, "content": str(out)})
    messages.append({"role": "user", "content": results})''',
          ["Tools = name + description + <b>JSON schema</b>; <span class=\"m\">strict: true</span> keeps arguments valid.",
           "<b>Structured output:</b> <span class=\"m\">client.messages.parse(output_format=Ticket)</span> → a validated pydantic object.",
           "Send <b>all</b> tool results back in <b>one</b> message."], size=21, width=1000),
     table(M, "Lesson 03 · Embeddings &amp; RAG", "Answer from YOUR documents, with sources", ["Step", "What happens", "In the lesson"],
           [["<b>1 Chunk</b>", "split docs into small overlapping pieces", "2-sentence windows"],
            ["<b>2 Embed</b>", "text → vector of numbers", "TF-IDF with numpy (real: Voyage, OpenAI…)"],
            ["<b>3 Store</b>", "keep the vectors", "a matrix (prod: pgvector, Azure AI Search)"],
            ["<b>4 Retrieve</b>", "cosine similarity, top-k", "<span class=\"m\">matrix @ embed(q)</span>"],
            ["<b>5 Generate</b>", "send ONLY those chunks + the question", "\"cite [returns.md] or say I don't know\""]],
           tip="No relevant chunk? Answer \"I don't know\" <b>without</b> calling the LLM: cheaper and honest."),
     code(M, "Lesson 04 · Agent behind an API", "FastAPI + the LLM as a dependency", '''
class AskIn(BaseModel):
    question: str = Field(min_length=3, max_length=500)

def get_llm():
    return get_client()             # real SDK in production
LLM = Annotated[Any, Depends(get_llm)]

@app.post("/ask", response_model=AskOut)
def ask(body: AskIn, llm: LLM):
    return run_agent(llm, body.question)   # max_steps, tokens used

# tests: fast, free, repeatable
app.dependency_overrides[get_llm] = lambda: FakeClient(...)''',
          ["Limit input size and <b>agent steps</b>; return 504 if it loops.",
           "Report <b>token usage</b> per request: log it, bill it.",
           "<span class=\"m\">/ask/stream</span>: <span class=\"m\">StreamingResponse</span> over <span class=\"m\">stream.text_stream</span>."],
          size=23, width=980),
     table(M, "Lesson 05 · Ship it safely", "Injection, privacy, cost, evals", ["Risk", "Do this"],
           [["<b>Prompt injection</b>", "least privilege tools; limits &amp; approvals in <b>code</b>; untrusted text in tags = data"],
            ["<b>Privacy</b>", "redact emails, IBANs, phones <b>before</b> the API call"],
            ["<b>Cost</b>", "tokens in × price + tokens out × price; budgets; smaller model for easy routes; caching; Batch API"],
            ["<b>Quality</b>", "an <b>eval set</b>: questions + checks, run on every prompt or model change"],
            ["<b>Refusals</b>", "check <span class=\"m\">stop_reason == \"refusal\"</span>; server-side fallbacks"]],
           src='''3,000 in + 400 out, 10k chats/day, 30 days
opus-5-5   0.0200 USD/chat -> 6,000 USD/month
sonnet-5-5 0.0100 USD/chat -> 3,000 USD/month
haiku-5-5  0.0005 USD/chat ->   150 USD/month''', width=640),
     exercise(30, "Your AI toolkit", ["chunk_words · cosine · top_k", "cost_usd from a price table",
                                      "redact emails and phone numbers", "run_tool_loop: errors, all results in one message, max_steps"],
              "ex30_ai_toolkit.py", '''$ python exercises/ex30_ai_toolkit.py
AssertionError            # until you solve it

$ python solutions/ex30_ai_toolkit.py
All checks passed!        # no API key needed'''),
    ]
    return S
