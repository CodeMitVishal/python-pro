"""Module 30 · Talking to an LLM: messages, system prompt, tokens, streaming

An LLM API is one HTTP endpoint: you send a list of MESSAGES and get the next
assistant message back. Everything else (chat, agents, RAG) is built on that.

  messages      the conversation so far: [{"role": "user", "content": "..."}, ...]
  system        instructions that set the role and rules for the whole chat
  max_tokens    the hard limit on the answer's length (1 token is about 4 characters)
  stop_reason   why it stopped: end_turn | max_tokens | tool_use | refusal
  usage         input_tokens + output_tokens: what you pay for
  streaming     show the answer word by word instead of waiting for all of it

Run it offline (default):   python 30_ai_with_python/01_llm_api_basics.py
Run it against Claude:      pip install anthropic, set ANTHROPIC_API_KEY, set USE_REAL_LLM=1
"""
from llm_client import MODEL, get_client, is_real, last_user_text, text_of


def tutor_brain(system: str, messages: list, tools: list) -> str:
    """Offline stand-in for the model, so the lesson runs without a key."""
    q = last_user_text(messages).lower()
    if "list comprehension" in q:
        return "A list comprehension builds a list in one line: [x * 2 for x in nums]."
    if "example" in q:
        return "Squares of even numbers: [n * n for n in range(10) if n % 2 == 0]."
    if "generator" in q:
        return ("A generator produces values lazily, one at a time, with yield. "
                "It saves memory because the whole sequence never sits in RAM at once. "
                "Use it for big files, streams and endless sequences.")
    return "I am a concise Python tutor. Ask me about Python."


client = get_client(tutor_brain)
print("mode:", "REAL Claude API" if is_real() else "offline FakeClient", "| model:", MODEL)

# --- 1. One request, one response -------------------------------------------------------------------
response = client.messages.create(
    model=MODEL,
    max_tokens=1000,
    messages=[{"role": "user", "content": "What is a list comprehension? One sentence."}],
)
print("\n1) answer:", text_of(response))
print("   stop_reason:", response.stop_reason)
print("   tokens in/out:", response.usage.input_tokens, "/", response.usage.output_tokens)
# response.content is a LIST of blocks (text, thinking, tool_use...). text_of() keeps only text.

# --- 2. A system prompt sets the role, tone and rules --------------------------------------------------
SYSTEM = "You are a concise Python tutor. Answer in at most 2 sentences. Always include code."
response = client.messages.create(
    model=MODEL, max_tokens=1000, system=SYSTEM,
    messages=[{"role": "user", "content": "Explain list comprehension."}],
)
print("\n2) with system prompt:", text_of(response))

# --- 3. Multi-turn: the API is STATELESS, you resend the whole history every time -------------------------
history = [{"role": "user", "content": "What is a list comprehension?"}]
first = client.messages.create(model=MODEL, max_tokens=1000, system=SYSTEM, messages=history)
history.append({"role": "assistant", "content": first.content})      # keep the model's turn
history.append({"role": "user", "content": "Give me an example with a filter."})
second = client.messages.create(model=MODEL, max_tokens=1000, system=SYSTEM, messages=history)
print("\n3) turn 1:", text_of(first))
print("   turn 2:", text_of(second))
print("   input tokens grow with history:", first.usage.input_tokens, "->", second.usage.input_tokens)


# --- 4. Always check WHY it stopped before you trust the text ----------------------------------------------
def ask(question: str, max_tokens: int = 1000) -> str:
    r = client.messages.create(model=MODEL, max_tokens=max_tokens, system=SYSTEM,
                               messages=[{"role": "user", "content": question}])
    if r.stop_reason == "max_tokens":
        return text_of(r) + " ...[CUT OFF: raise max_tokens]"
    if r.stop_reason == "refusal":                       # a safety classifier declined
        return "[The model declined this request]"
    return text_of(r)


print("\n4) tiny max_tokens:", ask("What is a generator?", max_tokens=8))

# --- 5. Streaming: print tokens as they arrive (chat UIs, long answers) -------------------------------------
print("\n5) streaming: ", end="")
with client.messages.stream(
    model=MODEL, max_tokens=2000, system=SYSTEM,
    messages=[{"role": "user", "content": "What is a generator?"}],
) as stream:
    for chunk in stream.text_stream:
        print(chunk, end="", flush=True)
    final = stream.get_final_message()                   # full message + usage at the end
print("\n   streamed output tokens:", final.usage.output_tokens)

# --- 6. Knobs worth knowing ------------------------------------------------------------------------------------
response = client.messages.create(
    model=MODEL, max_tokens=1000,
    output_config={"effort": "low"},                     # low | medium | high | xhigh | max
    messages=[{"role": "user", "content": "Explain list comprehension."}],
)
print("\n6) effort=low:", text_of(response))
print("""
Notes for real projects
  * Never hard-code the key: anthropic.Anthropic() reads ANTHROPIC_API_KEY from the environment.
  * effort trades depth for speed and cost. Current Claude models think adaptively on their own.
  * temperature / top_p are NOT accepted by current Claude models (400 error): steer with
    the system prompt and effort instead.
  * The SDK retries 429 / 5xx twice by default. Catch anthropic.RateLimitError,
    anthropic.APIStatusError and anthropic.APIConnectionError separately.
  * The same client works on Azure: anthropic.AnthropicFoundry(api_key=..., resource=...).""")
