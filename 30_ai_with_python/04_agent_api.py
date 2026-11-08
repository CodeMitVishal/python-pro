"""Module 30 · An AI agent behind a FastAPI endpoint

Put lessons 02 and 03 behind HTTP so a web app or mobile app can use them:

  POST /ask          {"question": "..."} -> {"answer", "steps", "tools_used", "tokens"}
  POST /ask/stream   the same answer, streamed as plain text while it is generated
  GET  /health

Production habits shown here:
  * the LLM client is a DEPENDENCY -> tests swap in the offline fake (no key, no cost)
  * input limits (pydantic Field) and a max_steps limit on the agent loop
  * every response reports token usage, so you can log and bill it
  * tool rules (who may be refunded, how much) are enforced in Python, not in the prompt

TEACHING NOTES
  Why it matters  An AI feature becomes a product when it sits behind a reliable, testable API.
  Picture it      The agent is a new employee behind a service desk: clear tools, limits, and a
                  manager (your code).
  Watch out       Limit input size and agent steps; report token usage for every request.
  In real jobs    /ask endpoints for apps, streaming answers, swapping the model for a fake in
                  tests.
  Interview       Q: How do you test an LLM feature?
                  A: Fake the client in unit tests; run an eval set of real questions on every
                     prompt or model change.

Run the demo:  python 30_ai_with_python/04_agent_api.py
Serve it:      cd 30_ai_with_python  then  uvicorn 04_agent_api:app --reload   (docs at /docs)
"""
import json
import re
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient
from llm_client import MODEL, get_client, last_user_text, text_of, tool_results
from pydantic import BaseModel, Field

# --- The agent's tools --------------------------------------------------------------------------
ORDERS = {"A-1042": {"status": "delivered", "price_eur": 49.0},
          "B-2001": {"status": "in transit", "price_eur": 89.0}}
FAQ = {"refund": "Refunds reach your account in 5 to 7 business days.",
       "shipping": "Standard shipping takes 2 to 4 business days. Orders above 50 EUR ship free."}


def get_order(order_id: str) -> dict:
    return ORDERS.get(order_id) or {"error": f"no order {order_id}"}


def search_faq(topic: str) -> str:
    return next((v for k, v in FAQ.items() if k in topic.lower()), "No FAQ entry.")


TOOLS = [
    {"name": "get_order", "description": "Status and price of an order by ID, e.g. A-1042.",
     "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}},
                      "required": ["order_id"], "additionalProperties": False}},
    {"name": "search_faq", "description": "Search the shop FAQ by topic, e.g. 'refund' or 'shipping'.",
     "input_schema": {"type": "object", "properties": {"topic": {"type": "string"}},
                      "required": ["topic"], "additionalProperties": False}},
]
REGISTRY = {"get_order": get_order, "search_faq": search_faq}
SYSTEM = "You are the shop's support agent. Use the tools. Answer in one or two friendly sentences."
MAX_STEPS = 4


def shop_brain(system, messages, tools):
    """Offline stand-in for the model."""
    question, results = last_user_text(messages), tool_results(messages)
    order = re.search(r"[A-Z]-\d{4}", question)
    if not tools:                                    # /ask/stream sends no tools: answer directly
        return search_faq(question)
    if not results:
        if order:
            return {"tool": "get_order", "input": {"order_id": order.group()}}
        return {"tool": "search_faq", "input": {"topic": question}}
    data = results[-1]["content"]
    if order:
        info = json.loads(data)
        return f"Your order {order.group()} is {info.get('status', 'not found')}."
    return data if data != "No FAQ entry." else "Sorry, I can't help with that. A human will reply soon."


# --- The agent loop (lesson 02) wrapped as a function the API can call -------------------------------
class AskIn(BaseModel):
    question: str = Field(min_length=3, max_length=500)


class AskOut(BaseModel):
    answer: str
    steps: int
    tools_used: list[str]
    tokens: dict[str, int]


def run_agent(client, question: str) -> AskOut:
    messages = [{"role": "user", "content": question}]
    used, tokens_in, tokens_out = [], 0, 0
    for step in range(1, MAX_STEPS + 1):
        r = client.messages.create(model=MODEL, max_tokens=4000, system=SYSTEM,
                                   tools=TOOLS, messages=messages)
        tokens_in, tokens_out = tokens_in + r.usage.input_tokens, tokens_out + r.usage.output_tokens
        if r.stop_reason != "tool_use":
            return AskOut(answer=text_of(r), steps=step, tools_used=used,
                          tokens={"input": tokens_in, "output": tokens_out})
        messages.append({"role": "assistant", "content": r.content})
        results = []
        for block in (b for b in r.content if b.type == "tool_use"):
            used.append(block.name)
            func = REGISTRY.get(block.name)
            output = func(**block.input) if func else {"error": "unknown tool"}
            results.append({"type": "tool_result", "tool_use_id": block.id,
                            "content": output if isinstance(output, str) else json.dumps(output)})
        messages.append({"role": "user", "content": results})
    raise HTTPException(status_code=504, detail="agent needed too many steps")


# --- The API ---------------------------------------------------------------------------------------
app = FastAPI(title="Shop support agent")


def get_llm():
    """Dependency: the real client in production, overridable in tests."""
    return get_client(shop_brain)


LLM = Annotated[Any, Depends(get_llm)]              # reusable "inject the LLM client" type


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL}


@app.post("/ask", response_model=AskOut)
def ask(body: AskIn, llm: LLM):
    return run_agent(llm, body.question)


@app.post("/ask/stream")
def ask_stream(body: AskIn, llm: LLM):
    def generate():                                  # FastAPI sends each yield as it comes
        with llm.messages.stream(model=MODEL, max_tokens=2000, system=SYSTEM,
                                 messages=[{"role": "user", "content": body.question}]) as stream:
            yield from stream.text_stream
    return StreamingResponse(generate(), media_type="text/plain")


# --- Demo: call the API like a frontend would --------------------------------------------------------
if __name__ == "__main__":
    api = TestClient(app)
    print("GET /health ->", api.get("/health").json())
    for q in ["Where is my order A-1042?", "How long does a refund take?", "Can you fix my bike?"]:
        r = api.post("/ask", json={"question": q})
        print(f"\nPOST /ask {q!r}\n  -> {r.status_code} {r.json()}")
    print("\nPOST /ask with a 1-letter question ->", api.post("/ask", json={"question": "a"}).status_code,
          "(pydantic validation)")

    # In tests, swap the LLM for a fake with a fixed answer: fast, free and repeatable.
    app.dependency_overrides[get_llm] = lambda: get_client(lambda s, m, t: "TEST ANSWER")
    print("with dependency override ->", api.post("/ask", json={"question": "anything?"}).json()["answer"])
    app.dependency_overrides.clear()

    print("\nPOST /ask/stream ->", api.post("/ask/stream", json={"question": "How long does a refund take?"}).text)
