# Module 30 · AI with Python: LLM APIs, tools, RAG and agents

[← Back to the course](../README.md) · [Slides](../slides/modules/Module-30.pdf) · [Interview Q&A](INTERVIEW.md)

Build AI features the way production teams do. You'll call an LLM, get validated JSON back, let it use tools, answer from your own documents with RAG, serve an agent with FastAPI, and keep it safe, cheap and tested.

**Every lesson runs offline by default.** [`llm_client.py`](llm_client.py) gives you a fake client with the same shape as the official Anthropic SDK, so there's no key and no cost. Set one environment variable to run the same code against Claude.

## Lessons

| Lesson | File | Key idea |
|---|---|---|
| Shared client | [`llm_client.py`](llm_client.py) | real SDK or offline fake; Anthropic API or Microsoft Foundry (Azure) |
| LLM API basics | [`01_llm_api_basics.py`](01_llm_api_basics.py) | messages, system prompt, multi-turn, `stop_reason`, tokens, streaming, effort |
| Structured output & tools | [`02_structured_output_and_tools.py`](02_structured_output_and_tools.py) | `messages.parse` + pydantic, tool schemas, the agent loop |
| Embeddings & RAG | [`03_embeddings_and_rag.py`](03_embeddings_and_rag.py) | chunk → embed → retrieve (cosine, top-k) → answer with sources |
| Agent behind an API | [`04_agent_api.py`](04_agent_api.py) | FastAPI `/ask` + streaming, the LLM as a dependency, limits, token reporting |
| Safety, cost & evals | [`05_safety_cost_eval.py`](05_safety_cost_eval.py) | prompt injection, redaction, cost per request, budgets, eval sets |

```bash
pip install fastapi uvicorn httpx pydantic numpy
```

```bash
python 30_ai_with_python/01_llm_api_basics.py
```

### Run against the real Claude API (optional, paid)

```bash
pip install anthropic
```

Set `ANTHROPIC_API_KEY` and `USE_REAL_LLM=1`, then run any lesson again. The default model is `claude-opus-5-5`. Use `LLM_MODEL` to change it, for example to `claude-haiku-5-5` for cheap experiments.
To use Claude on Azure (Microsoft Foundry), also set `LLM_PROVIDER=foundry`, `ANTHROPIC_FOUNDRY_API_KEY` and `ANTHROPIC_FOUNDRY_RESOURCE`.

## Exercise: Your AI toolkit

Build the plain-Python parts every LLM app needs: chunking, cosine similarity, top-k retrieval, cost, redaction, and a tool-calling loop that handles errors and step limits.

- Start here: [`exercises/ex30_ai_toolkit.py`](../exercises/ex30_ai_toolkit.py)
- Solution: [`solutions/ex30_ai_toolkit.py`](../solutions/ex30_ai_toolkit.py)

## Knowledge check

Preparing for interviews? Read the [Module 30 interview questions](INTERVIEW.md) and the [Top 100](../interview_prep/TOP_100.md).

Test yourself with the [Module 30 quiz](QUIZ.md). The answer key is at the bottom.

🎉 **That's the end of Python Pro!** You've gone from Foundations to deployed web APIs, algorithms and AI agents.

---

## ☕ Enjoyed this module?

- **Buy me a coffee** at [buymeacoffee.com/codemitvishal](https://buymeacoffee.com/codemitvishal) ☕
- **Subscribe** to [CodeMitVishal](https://www.youtube.com/@CodeMitVishal) on YouTube
- **Star** this repo so others can find it
