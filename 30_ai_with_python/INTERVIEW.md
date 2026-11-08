# Module 30 · Interview questions (with answers)

[← Module 30](README.md) · [Quiz](QUIZ.md)

---

### 1. How does an LLM API call work?

**Say:** It's one HTTP endpoint. You send a model name, a system prompt, the conversation (`messages`) and `max_tokens`. You get back content blocks (text, tool calls, thinking), a `stop_reason` and token `usage`. The API is **stateless**: you resend the history every turn.

---

### 2. What are tokens, and why do they matter?

**Say:** Models read and write text as tokens (roughly 4 characters of English each). You pay per input and output token, context windows are measured in tokens, and latency grows with output tokens. Log `usage` per request.

---

### 3. How do you get reliable structured data from an LLM?

**Say:** Use structured outputs: give a JSON schema or Pydantic model (`messages.parse(output_format=Model)`) so the response is guaranteed to match, then still validate business rules in code. Tools with `strict: true` give schema-valid arguments.

---

### 4. What is tool use (function calling)? What is an agent?

**Say:** You describe functions with a name, a description and a JSON schema. The model replies with `stop_reason == "tool_use"` and arguments, your code runs the function and returns a `tool_result`, and this loops until a final answer. An **agent** is that loop: the model decides which tools to call to reach a goal. Always add step limits and permission checks.

---

### 5. What is RAG? RAG vs fine-tuning?

**Say:** **Retrieval-Augmented Generation** means retrieving relevant chunks of your data (embeddings + vector search) and putting them in the prompt so the model answers from them, with citations. Use RAG for knowledge that changes or needs sources. **Fine-tuning** changes model behaviour or style for narrow tasks. Most products start with RAG.

---

### 6. What are embeddings? What is cosine similarity?

**Say:** Embeddings are vectors that represent meaning: similar texts get vectors pointing in similar directions. Cosine similarity measures the angle between two vectors (1 means the same direction). Top-k retrieval returns the chunks with the highest similarity to the question.

---

### 7. What is prompt injection, and how do you defend against it?

**Say:** Untrusted text (user input, emails, web pages, retrieved documents) contains instructions that the model follows. Defences: least-privilege tools; limits, allow-lists and human approval enforced **in code**; mark untrusted content as data; validate outputs; log tool calls. Regex filters only raise a flag.

---

### 8. How do you control cost and latency?

**Say:** Use a smaller model for easy routes, prompt caching for repeated prefixes, the Batch API for offline work, fewer and shorter RAG chunks, capped and concise outputs, streaming for perceived latency, budgets, and per-request usage logging.

---

### 9. How do you test an LLM feature?

**Say:** Unit-test the code around the model with a **fake client** (deterministic, free). For the model itself, keep an **eval set** of real questions with checks (contains, JSON valid, LLM-as-judge with a rubric). Run it on every prompt or model change and track the score.

---

### 10. How do you handle refusals and failures?

**Say:** Check `stop_reason` before reading text (`max_tokens` means truncated, `refusal` means declined). Retry 429/5xx with backoff (the SDK does this by default). Use fallbacks where available, show a helpful message, and log for review.

---

☕ [Buy me a coffee](https://buymeacoffee.com/codemitvishal) · ▶️ [Subscribe to CodeMitVishal](https://www.youtube.com/@CodeMitVishal)
