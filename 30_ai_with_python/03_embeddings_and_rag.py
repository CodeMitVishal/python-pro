"""Module 30 · Embeddings and RAG (retrieval-augmented generation)

An LLM doesn't know YOUR documents. RAG fixes that without any training:

  1. CHUNK    split documents into small overlapping pieces
  2. EMBED    turn every chunk into a vector (a list of numbers)
  3. STORE    keep the vectors (a numpy array here; pgvector / Azure AI Search / Chroma in prod)
  4. RETRIEVE embed the question, take the top-k chunks by cosine similarity
  5. GENERATE send ONLY those chunks + the question; ask for an answer with sources

We build the vectoriser ourselves (TF-IDF with numpy) so you can see every step.
Real embedding models (Voyage AI, OpenAI, sentence-transformers) capture MEANING,
so "money back" also finds "refund". The pipeline around them stays the same.

TEACHING NOTES
  Why it matters  The model doesn't know your documents; RAG lets it answer from them, with
                  sources.
  Picture it      An open-book exam: find the right pages first (retrieve), then answer from
                  them (generate).
  Watch out       Word matching misses synonyms; real embeddings capture meaning. No relevant
                  chunk: say 'I don't know'.
  In real jobs    Help-centre bots, internal docs search, contract Q&A.
  Interview       Q: What is RAG?
                  A: Retrieve relevant chunks via embeddings and similarity search, then answer
                     from that context with citations.

Run it:  python 30_ai_with_python/03_embeddings_and_rag.py
"""
import math
import re
from collections import Counter

import numpy as np
from llm_client import MODEL, get_client, last_user_text, text_of

DOCS = {
    "returns.md": "Returns are free within 30 days of delivery. Items must be unused and in the "
                  "original box. Damaged items are refunded in full, including shipping. Refunds reach "
                  "your account in 5 to 7 business days.",
    "shipping.md": "We ship to Germany, Austria and Switzerland. Standard shipping takes 2 to 4 business "
                   "days and costs 4.90 EUR. Orders above 50 EUR ship free. Express shipping costs 9.90 EUR.",
    "warranty.md": "All electronics have a 2 year warranty. The warranty covers manufacturing defects, "
                   "not drops or water damage. Keep your invoice as proof of purchase.",
    "privacy.md": "We store your address and order history for 10 years because German tax law requires "
                  "it. We never sell personal data. Ask privacy@example.com to see your data.",
}


# --- 1. Chunking: small pieces retrieve better than whole documents ------------------------
def chunk(text: str, size: int = 2, overlap: int = 1) -> list[str]:
    """Windows of `size` sentences; neighbours share `overlap` sentences so no fact is cut in half."""
    sentences = re.split(r"(?<=\.)\s+", text.strip())
    step = size - overlap
    return [" ".join(sentences[i:i + size]) for i in range(0, max(len(sentences) - overlap, 1), step)]


chunks, sources = [], []
for name, text in DOCS.items():
    for piece in chunk(text):
        chunks.append(piece)
        sources.append(name)
print(f"1) {len(DOCS)} documents -> {len(chunks)} chunks")

# --- 2. Embedding: TF-IDF vectors (rare words weigh more) -------------------------------------
STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "be", "we", "your", "you",
        "for", "it", "how", "do", "does", "what", "my", "i", "can", "not", "on", "if", "much"}


def tokens(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w[:5] for w in words if w not in STOP]   # cheap "stemmer": refunds/refunded -> refun


vocab = sorted({t for c in chunks for t in tokens(c)})
index = {word: i for i, word in enumerate(vocab)}
doc_freq = Counter(t for c in chunks for t in set(tokens(c)))
idf = np.array([math.log(len(chunks) / doc_freq[w]) + 1 for w in vocab])


def embed(text: str) -> np.ndarray:
    vec = np.zeros(len(vocab))
    for t, count in Counter(tokens(text)).items():
        if t in index:                               # unknown words are ignored
            vec[index[t]] = count
    vec *= idf
    norm = np.linalg.norm(vec)
    return vec / norm if norm else vec               # unit length: dot product == cosine


matrix = np.array([embed(c) for c in chunks])        # our "vector database": one row per chunk
print(f"2) embedded into a {matrix.shape[0]} x {matrix.shape[1]} matrix")


# --- 3. Retrieval: cosine similarity, top-k ------------------------------------------------------
def retrieve(question: str, k: int = 2, min_score: float = 0.1) -> list[tuple[float, str, str]]:
    scores = matrix @ embed(question)                # cosine with EVERY chunk in one line
    best = np.argsort(scores)[::-1][:k]
    return [(float(scores[i]), sources[i], chunks[i]) for i in best if scores[i] >= min_score]


for q in ["How many days until my refund arrives?", "Is shipping free?"]:
    print(f"3) '{q}'")
    for score, src, text in retrieve(q):
        print(f"     {score:.2f} [{src}] {text[:60]}...")


# --- 4. Generation: answer ONLY from the retrieved context, with sources ----------------------------
SYSTEM = ("Answer the question using ONLY the documents in <context>. Cite the source in square "
          "brackets, like [returns.md]. If the answer is not in the context, say \"I don't know\".")


def rag_brain(system, messages, tools):
    """Offline stand-in: picks the context sentence that shares the most words with the question."""
    prompt = last_user_text(messages)
    question = set(tokens(prompt.split("Question:")[-1]))
    best, best_overlap = "I don't know.", 0
    for src, text in re.findall(r'<doc source="([^"]+)">(.*?)</doc>', prompt, re.DOTALL):
        for sentence in re.split(r"(?<=\.)\s+", text):
            overlap = len(question & set(tokens(sentence)))
            if overlap > best_overlap:
                best, best_overlap = f"{sentence} [{src}]", overlap
    return best


client = get_client(rag_brain)


def answer(question: str) -> str:
    hits = retrieve(question, k=3)
    if not hits:                                      # nothing relevant: don't pay for an LLM call
        return "I don't know. (no matching documents)"
    context = "\n".join(f'<doc source="{src}">{text}</doc>' for _, src, text in hits)
    response = client.messages.create(
        model=MODEL, max_tokens=1000, system=SYSTEM,
        messages=[{"role": "user", "content": f"<context>\n{context}\n</context>\n\nQuestion: {question}"}],
    )
    return text_of(response)


print()
for q in ["How many days until my refund arrives?", "What does express shipping cost?",
          "Does the warranty cover water damage?", "What are your opening hours?"]:
    print(f"4) Q: {q}\n   A: {answer(q)}")

# --- 5. The limit of word matching ------------------------------------------------------------------------
print("\n5) 'Can I get my money back?' ->", retrieve("Can I get my money back?") or "no hits!",
      "\n   TF-IDF only matches WORDS. A real embedding model knows 'money back' ~ 'refund'.")
print("""
Notes
  * Swap embed() for a real model; keep chunk -> embed -> store -> retrieve -> generate.
  * Tune chunk size, overlap and k on real questions (an eval set, lesson 05).
  * Put retrieved text inside tags and say it is DATA: documents can contain attacks (lesson 05).
  * Store vectors in pgvector (PostgreSQL), Azure AI Search, Chroma or Qdrant in production.""")
