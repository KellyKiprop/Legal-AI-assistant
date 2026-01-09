import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
load_dotenv()

DATA_PATH = "data/constitution_articles_clean.jsonl"
INDEX_PATH = "constitution.index"
EMBED_MODEL = "all-MiniLM-L6-v2"
GROQ_MODEL =  "llama-3.3-70b-versatile" # supported, stable

TOP_K = 4

# ---------------------------------------------------
# SYSTEM PROMPT (VERY IMPORTANT)
# ---------------------------------------------------
SYSTEM_PROMPT = """
You are a Kenyan constitutional assistant.

RULES:
- Use ONLY the provided constitutional text.
- Do NOT use outside knowledge.
- Do NOT guess or invent article numbers.
- If the Constitution does not clearly answer the question, say:
  "The Constitution does not clearly address this."

OUTPUT FORMAT (MANDATORY):

PLAIN ENGLISH SUMMARY:
<Explain the answer in very simple language>

KEY POINTS:
- Bullet points of what the Constitution guarantees

LIMITATIONS / EXCEPTIONS:
- Bullet points of restrictions or limits

OFFICIAL CONSTITUTIONAL BASIS:
- Article <number>: "<short direct quote>"
"""

# ---------------------------------------------------
# LOAD RESOURCES (ONCE)
# ---------------------------------------------------
print("🔄 Loading embedder...")
embedder = SentenceTransformer(EMBED_MODEL)

print("🔄 Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)

print("🔄 Loading article data...")
articles = []
with open(DATA_PATH, "r", encoding="utf-8") as f:
    for line in f:
        articles.append(json.loads(line))

groq = Groq()

# ---------------------------------------------------
# CORE RAG FUNCTION
# ---------------------------------------------------
def ask_constitution(question: str) -> str:
    # Embed question
    q_vec = embedder.encode([question], normalize_embeddings=True)
    
    # Search FAISS
    scores, indices = index.search(np.array(q_vec).astype("float32"), TOP_K)

    # Build context
    context_blocks = []
    for idx in indices[0]:
        art = articles[idx]
        block = (
            f"Article {art['article_number']} – {art['title']}\n"
            f"{art['text']}"
        )
        context_blocks.append(block)

    context = "\n\n---\n\n".join(context_blocks)

    # Build messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"QUESTION:\n{question}\n\nCONSTITUTIONAL TEXT:\n{context}"
        }
    ]

    # Call Groq
    response = groq.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.0,
        max_tokens=600
    )

    return response.choices[0].message.content


# ---------------------------------------------------
# CLI LOOP
# ---------------------------------------------------
print("\n🇰🇪 Kenya Constitution Chat (Production RAG)\n")

while True:
    q = input("❓ Ask a question (or 'exit'): ").strip()
    if q.lower() in {"exit", "quit"}:
        break

    answer = ask_constitution(q)
    print("\n" + "=" * 60)
    print(answer)
    print("=" * 60 + "\n")
