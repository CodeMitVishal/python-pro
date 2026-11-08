"""Module 30 · Structured output (JSON you can trust) and tool calling

Free text is fine for humans. Your CODE needs data, so ask for a schema:

  STRUCTURED OUTPUT  client.messages.parse(output_format=PydanticModel)
                     -> response.parsed_output is a validated object, not a string
  TOOLS              you describe functions (name + JSON schema); the model answers
                     with stop_reason == "tool_use" and the arguments; YOUR code
                     runs the function and sends back a tool_result; repeat until
                     the model gives a final text answer. That loop is an "agent".

Run it:  python 30_ai_with_python/02_structured_output_and_tools.py
"""
import json
import re
from typing import Literal

from llm_client import MODEL, get_client, last_user_text, text_of, tool_results
from pydantic import BaseModel, Field, ValidationError


# ======================== PART A: structured output ===========================================
class Ticket(BaseModel):
    customer: str
    order_id: str
    category: Literal["refund", "delivery", "bug", "other"]
    urgency: int = Field(ge=1, le=5)
    summary: str


EMAIL = """Hi, this is Priya Sharma. My order A-1042 arrived broken and I need my
money back before Friday, it was a birthday gift!! Please hurry."""


def extract_brain(system, messages, tools):
    """Offline stand-in: what a real model would return for the email above."""
    text = last_user_text(messages)
    order = re.search(r"[A-Z]-\d{4}", text)
    return json.dumps({
        "customer": "Priya Sharma" if "Priya" in text else "unknown",
        "order_id": order.group() if order else "",
        "category": "refund" if "money back" in text else "other",
        "urgency": 4 if "hurry" in text.lower() else 2,
        "summary": "Order arrived broken; customer wants a refund before Friday.",
    })


client = get_client(extract_brain)
response = client.messages.parse(
    model=MODEL, max_tokens=2000,
    system="Extract a support ticket from the customer email.",
    messages=[{"role": "user", "content": EMAIL}],
    output_format=Ticket,                         # the SDK turns the class into a JSON schema
)
ticket: Ticket = response.parsed_output
print("A) parsed ticket:", ticket.model_dump())
print("   route it in code:", "-> refunds queue" if ticket.category == "refund" else "-> general queue")

# The API guarantees the JSON matches the schema; pydantic still guards YOUR rules:
try:
    Ticket.model_validate_json('{"customer": "x", "order_id": "1", "category": "refund", '
                               '"urgency": 9, "summary": "x"}')
except ValidationError as e:
    print("   pydantic catches bad data:", e.errors()[0]["msg"])

# ======================== PART B: tools + the agent loop ===========================================
ORDERS = {"A-1042": {"status": "delivered", "item": "ceramic lamp", "price_eur": 49.0, "damaged": True},
          "B-2001": {"status": "in transit", "item": "keyboard", "price_eur": 89.0, "damaged": False}}


def get_order(order_id: str) -> dict:
    if order_id not in ORDERS:
        raise KeyError(f"no order {order_id}")
    return ORDERS[order_id]


def issue_refund(order_id: str, amount_eur: float) -> dict:
    order = get_order(order_id)
    if amount_eur > order["price_eur"]:            # the rule lives in CODE, not in the prompt
        raise ValueError("refund larger than the price")
    return {"refunded": amount_eur, "order_id": order_id}


TOOLS = [
    {"name": "get_order", "description": "Look up an order's status, item and price by its ID.",
     "strict": True,
     "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}},
                      "required": ["order_id"], "additionalProperties": False}},
    {"name": "issue_refund", "description": "Refund a damaged order. Only after checking it with get_order.",
     "strict": True,
     "input_schema": {"type": "object",
                      "properties": {"order_id": {"type": "string"}, "amount_eur": {"type": "number"}},
                      "required": ["order_id", "amount_eur"], "additionalProperties": False}},
]
REGISTRY = {"get_order": get_order, "issue_refund": issue_refund}


def support_brain(system, messages, tools):
    """Offline stand-in: decides which tool to call next from what it has seen so far."""
    question, results = last_user_text(messages), tool_results(messages)
    order_id = re.search(r"[A-Z]-\d{4}", question).group()
    if not results:
        return {"tool": "get_order", "input": {"order_id": order_id}}
    last = json.loads(results[-1]["content"]) if not results[-1].get("is_error") else {}
    if "damaged" in last and last["damaged"] and "refund" in question.lower():
        return {"tool": "issue_refund", "input": {"order_id": order_id, "amount_eur": last["price_eur"]}}
    if "refunded" in last:
        return f"Done: I refunded {last['refunded']:.2f} EUR for order {order_id}. Sorry about the lamp!"
    return f"Order {order_id} is {last.get('status', 'unknown')}."


def run_agent(client, question: str, max_steps: int = 5) -> str:
    messages = [{"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        response = client.messages.create(model=MODEL, max_tokens=4000, tools=TOOLS, messages=messages,
                                          system="You are a support agent. Use tools; never guess order data.")
        if response.stop_reason != "tool_use":
            return text_of(response)                               # final answer
        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            print(f"   step {step}: model calls {block.name}({block.input})")
            try:
                output = REGISTRY[block.name](**block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(output)})
            except Exception as e:  # noqa: BLE001 - ANY tool error goes back to the model
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": f"error: {e}", "is_error": True})
        messages.append({"role": "user", "content": results})      # ALL results in ONE message
    raise RuntimeError("agent did not finish: max_steps reached")


print("\nB) agent: 'Order A-1042 arrived broken, I want a refund.'")
print("   answer:", run_agent(get_client(support_brain), "Order A-1042 arrived broken, I want a refund."))
print("\n   agent: 'Where is my order B-2001?'")
print("   answer:", run_agent(get_client(support_brain), "Where is my order B-2001?"))
print("""
Notes
  * strict: true + additionalProperties: false -> tool arguments always match the schema.
  * Run tools with validation and permissions in YOUR code: the model only asks.
  * Return errors as tool_result with is_error=True; the model can recover and retry.
  * Shortcut: the SDK's tool runner (@beta_tool + client.beta.messages.tool_runner) runs
    this loop for you. Write the loop by hand once so you know what it does.""")
