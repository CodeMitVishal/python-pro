"""Module 30 · Shared helper: one client for every lesson, real or offline.

By default every lesson runs OFFLINE with FakeClient: no API key, no cost, same
output every run. FakeClient copies the shape of the official Anthropic SDK
(client.messages.create / .parse / .stream, content blocks, stop_reason, usage),
so the lesson code is exactly the code you would ship.

Switch to the real Claude API (costs money, needs a key):
    pip install anthropic
    set ANTHROPIC_API_KEY=sk-ant-...        (PowerShell: $env:ANTHROPIC_API_KEY="...")
    set USE_REAL_LLM=1

Claude on Microsoft Foundry (Azure) instead:
    set LLM_PROVIDER=foundry
    set ANTHROPIC_FOUNDRY_API_KEY=...  and  ANTHROPIC_FOUNDRY_RESOURCE=<your-resource-name>
"""
from __future__ import annotations

import json
import os
import time
from collections.abc import Callable
from types import SimpleNamespace
from typing import Any

MODEL = os.getenv("LLM_MODEL", "claude-opus-5-5")     # current default Claude model

# A "brain" plays the model offline: brain(system, messages, tools) returns
#   "some text"                                  -> a normal text answer
#   {"tool": "name", "input": {...}}             -> a tool call
#   [ {...tool call...}, {...tool call...} ]     -> several tool calls at once
Brain = Callable[[str, list, list], Any]


def get_client(fake_brain: Brain | None = None):
    """Real SDK client when USE_REAL_LLM=1, otherwise the offline FakeClient."""
    if os.getenv("USE_REAL_LLM") == "1":
        import anthropic  # imported only when needed
        if os.getenv("LLM_PROVIDER") == "foundry":
            return anthropic.AnthropicFoundry(
                api_key=os.environ["ANTHROPIC_FOUNDRY_API_KEY"],
                resource=os.environ["ANTHROPIC_FOUNDRY_RESOURCE"],
            )
        return anthropic.Anthropic()                        # reads ANTHROPIC_API_KEY
    return FakeClient(fake_brain or echo_brain)


def is_real() -> bool:
    return os.getenv("USE_REAL_LLM") == "1"


# --- Helpers that work on real AND fake responses ------------------------------------
def text_of(message) -> str:
    """Join the text blocks. Responses can also hold thinking / tool_use blocks: skip them."""
    return "".join(b.text for b in message.content if b.type == "text")


def last_user_text(messages: list) -> str:
    """The newest plain-text user message (what the fake brains react to)."""
    for msg in reversed(messages):
        if msg["role"] == "user" and isinstance(msg["content"], str):
            return msg["content"]
    return ""


def tool_results(messages: list) -> list[dict]:
    """Every tool_result block sent so far, oldest first."""
    found = []
    for msg in messages:
        if msg["role"] == "user" and isinstance(msg["content"], list):
            found += [b for b in msg["content"] if isinstance(b, dict) and b.get("type") == "tool_result"]
    return found


def echo_brain(system: str, messages: list, tools: list) -> str:
    return f"(offline model) You said: {last_user_text(messages)}"


# --- The offline stand-in ---------------------------------------------------------------
def _tokens(obj) -> int:
    """Rough rule of thumb: 1 token is about 4 characters of English text."""
    return max(1, len(json.dumps(obj, default=str)) // 4)


class FakeClient:
    def __init__(self, brain: Brain):
        self.messages = _FakeMessages(brain)


class _FakeMessages:
    def __init__(self, brain: Brain):
        self.brain = brain
        self._ids = 0

    def create(self, *, model: str, max_tokens: int, messages: list, system: str = "",
               tools: list | None = None, **_ignored) -> SimpleNamespace:
        reply = self.brain(system, messages, tools or [])
        calls = reply if isinstance(reply, list) else [reply]
        content, stop = [], "end_turn"
        for item in calls:
            if isinstance(item, dict):                      # a tool call
                self._ids += 1
                content.append(SimpleNamespace(type="tool_use", id=f"toolu_{self._ids:03d}",
                                               name=item["tool"], input=item["input"]))
                stop = "tool_use"
            else:
                text = str(item)
                words = text.split(" ")
                if len(words) > max_tokens:                 # the model ran out of room
                    text, stop = " ".join(words[:max_tokens]), "max_tokens"
                content.append(SimpleNamespace(type="text", text=text))
        usage = SimpleNamespace(input_tokens=_tokens([system, messages, tools]),
                                output_tokens=_tokens([vars(b) for b in content]))
        return SimpleNamespace(model=model, content=content, stop_reason=stop,
                               stop_details=None, usage=usage)

    def parse(self, *, output_format, **kwargs) -> SimpleNamespace:
        message = self.create(**kwargs)
        message.parsed_output = output_format.model_validate_json(text_of(message))
        return message

    def stream(self, **kwargs) -> _FakeStream:
        return _FakeStream(self.create(**kwargs))


class _FakeStream:
    def __init__(self, message):
        self._message = message

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    @property
    def text_stream(self):
        for i, word in enumerate(text_of(self._message).split(" ")):
            time.sleep(0.03)                                # pretend tokens arrive one by one
            yield word if i == 0 else " " + word

    def get_final_message(self):
        return self._message
