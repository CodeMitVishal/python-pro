"""Exercise 30 · Your AI toolkit: the plain-Python parts of every LLM app

No API key needed: the checks use a tiny fake client with the same shape as the SDK.

  1. chunk_words(text, size, overlap)  -> list of word windows; neighbours share `overlap` words
  2. cosine(a, b)                      -> cosine similarity of two lists of floats (0.0 if a vector is all zeros)
  3. top_k(query, docs, k)             -> names of the k docs most similar to query (docs: {name: vector})
  4. cost_usd(input_tokens, output_tokens, model)
                                       -> price from PRICES (USD per 1M tokens); unknown model -> ValueError
  5. redact(text)                      -> emails become [EMAIL], phone numbers (8+ digits) become [PHONE]
  6. run_tool_loop(client, question, tools, registry, max_steps=5)
        call client.messages.create(model=MODEL, max_tokens=..., tools=tools, messages=messages)
        while stop_reason == "tool_use": run each tool_use block with registry[name](**input),
        send ALL results back in ONE user message:
            {"type": "tool_result", "tool_use_id": block.id, "content": str(result)}
        unknown tool or an exception -> a tool_result with "is_error": True and the error text.
        Return the final text. More than max_steps model calls -> RuntimeError.

Run it to check your work:
    python exercises/ex30_ai_toolkit.py

Stuck? Compare with solutions/ex30_ai_toolkit.py
"""
import re

PRICES = {"claude-opus-5-5": (4.00, 20.00), "claude-haiku-5-5": (0.10, 0.50)}
MODEL = "claude-opus-5-5"


def chunk_words(text, size, overlap):
    """TODO 1"""


def cosine(a, b):
    """TODO 2"""


def top_k(query, docs, k):
    """TODO 3"""


def cost_usd(input_tokens, output_tokens, model):
    """TODO 4"""


def redact(text):
    """TODO 5"""


def run_tool_loop(client, question, tools, registry, max_steps=5):
    """TODO 6"""


# --- Checks: do not change anything below this line ----------------------------------
if __name__ == "__main__":
    from types import SimpleNamespace as NS

    class FakeClient:
        """Plays the model: replies with the scripted turns and records what it was sent."""
        def __init__(self, turns):
            self.turns, self.sent = list(turns), []
            self.messages = self

        def create(self, **kwargs):
            self.sent.append(kwargs["messages"][-1])
            blocks = self.turns.pop(0)
            stop = "tool_use" if any(b.type == "tool_use" for b in blocks) else "end_turn"
            return NS(content=blocks, stop_reason=stop, usage=NS(input_tokens=10, output_tokens=5))

    def call(i, name, **inp):
        return NS(type="tool_use", id=f"t{i}", name=name, input=inp)

    def text(t):
        return NS(type="text", text=t)

    assert chunk_words("a b c d e f g", 3, 1) == ["a b c", "c d e", "e f g"]
    assert chunk_words("one two", 5, 2) == ["one two"]
    assert abs(cosine([1, 0], [1, 0]) - 1) < 1e-9 and abs(cosine([1, 0], [0, 1])) < 1e-9
    assert abs(cosine([1, 2, 3], [2, 4, 6]) - 1) < 1e-9 and cosine([0, 0], [1, 1]) == 0.0
    docs = {"refunds": [0.9, 0.1, 0.0], "shipping": [0.1, 0.9, 0.1], "privacy": [0.0, 0.2, 0.9]}
    assert top_k([1.0, 0.2, 0.0], docs, 2) == ["refunds", "shipping"]
    assert top_k([0.0, 0.0, 1.0], docs, 1) == ["privacy"]
    assert abs(cost_usd(3_000, 400, "claude-opus-5-5") - 0.02) < 1e-12
    assert abs(cost_usd(1_000_000, 0, "claude-haiku-5-5") - 0.10) < 1e-12
    try:
        cost_usd(1, 1, "some-unknown-model")
        raise AssertionError("unknown model must raise ValueError")
    except ValueError:
        pass
    assert redact("mail vishal@example.com or call +49 151 2345678") == "mail [EMAIL] or call [PHONE]"
    assert redact("order A-1042 costs 49 EUR") == "order A-1042 costs 49 EUR"

    registry = {"get_order": lambda order_id: {"A-1": "delivered"}.get(order_id, "unknown"),
                "add": lambda a, b: a + b}
    fake = FakeClient([[call(1, "get_order", order_id="A-1")], [text("Your order is delivered.")]])
    assert run_tool_loop(fake, "Where is A-1?", [], registry) == "Your order is delivered."
    first_result = fake.sent[1]["content"][0]
    assert first_result["content"] == "delivered" and first_result["tool_use_id"] == "t1"

    fake = FakeClient([[call(1, "add", a=2, b=3), call(2, "add", a=1, b=1)], [text("5 and 2")]])
    assert run_tool_loop(fake, "sums", [], registry) == "5 and 2"
    assert len(fake.sent[1]["content"]) == 2, "send ALL tool results in ONE user message"

    fake = FakeClient([[call(1, "delete_db")], [call(2, "add", a=1)], [text("recovered")]])
    assert run_tool_loop(fake, "x", [], registry) == "recovered"
    assert fake.sent[1]["content"][0].get("is_error") is True, "unknown tool -> is_error"
    assert fake.sent[2]["content"][0].get("is_error") is True, "exception in a tool -> is_error"

    fake = FakeClient([[call(i, "add", a=1, b=1)] for i in range(10)])
    try:
        run_tool_loop(fake, "loop forever", [], registry, max_steps=3)
        raise AssertionError("must raise RuntimeError after max_steps")
    except RuntimeError:
        pass
    assert len(fake.sent) == 3, "stop after max_steps model calls"
    print("All checks passed!")
