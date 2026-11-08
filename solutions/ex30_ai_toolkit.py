"""Solution · Exercise 30: Your AI toolkit

Run it:  python solutions/ex30_ai_toolkit.py
"""
import re

PRICES = {"claude-opus-5-5": (4.00, 20.00), "claude-haiku-5-5": (0.10, 0.50)}
MODEL = "claude-opus-5-5"


def chunk_words(text, size, overlap):
    words = text.split()
    step = size - overlap                          # neighbours share `overlap` words
    return [" ".join(words[i:i + size]) for i in range(0, max(len(words) - overlap, 1), step)]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def top_k(query, docs, k):
    return sorted(docs, key=lambda name: cosine(query, docs[name]), reverse=True)[:k]


def cost_usd(input_tokens, output_tokens, model):
    if model not in PRICES:
        raise ValueError(f"no price for {model}")
    price_in, price_out = PRICES[model]
    return (input_tokens * price_in + output_tokens * price_out) / 1_000_000


def redact(text):
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[EMAIL]", text)
    return re.sub(r"\+?\d[\d /-]{6,}\d", "[PHONE]", text)       # 8+ digits, spaces or dashes inside


def run_tool_loop(client, question, tools, registry, max_steps=5):
    messages = [{"role": "user", "content": question}]
    for _ in range(max_steps):
        response = client.messages.create(model=MODEL, max_tokens=4000, tools=tools, messages=messages)
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")
        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            try:
                output = registry[block.name](**block.input)   # KeyError for an unknown tool
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": str(output)})
            except Exception as e:  # noqa: BLE001 - ANY tool error goes back to the model
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": f"error: {e!r}", "is_error": True})
        messages.append({"role": "user", "content": results})  # ALL results in ONE message
    raise RuntimeError("max_steps reached without a final answer")


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
