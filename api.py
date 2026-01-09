from fastapi import FastAPI
from pydantic import BaseModel
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
import os
from dotenv import load_dotenv

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
load_dotenv()

ARTICLES_PATH = "data/constitution_articles_clean.jsonl"
FAISS_INDEX_PATH = "constitution.index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.1-8b-instant"

# --------------------------------------------------
# APP
# --------------------------------------------------

app = FastAPI(title="Kenya Constitution RAG API 🇰🇪")

# --------------------------------------------------
# LOAD EVERYTHING ONCE (IMPORTANT)
# --------------------------------------------------

print("🔄 Loading embedder...")
embedder = SentenceTransformer(EMBEDDING_MODEL)

print("🔄 Loading FAISS index...")
index = faiss.read_index(FAISS_INDEX_PATH)

print("🔄 Loading article data...")
articles = []
with open(ARTICLES_PATH, "r", encoding="utf-8") as f:
    for line in f:
        articles.append(json.loads(line))

print("✅ System ready")

# --------------------------------------------------
# GROQ CLIENT
# --------------------------------------------------

groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str

# --------------------------------------------------
# CORE LOGIC
# --------------------------------------------------

SYSTEM_PROMPT = """
You are a civic education assistant for the Constitution of Kenya.

Explain answers in SIMPLE PLAIN ENGLISH.
Avoid legal jargon.
Explain as if speaking to a secondary school student.

Return ONLY valid JSON in this structure:

{
  "summary": string,
  "key_points": [string],
  "limitations": [string],
  "articles": [
    {
      "article": string,
      "description": string
    }
  ]
}
"""

def retrieve_articles(query: str, k: int = 5):
    query_embedding = embedder.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, k)

    results = []
    for idx in indices[0]:
        article = articles[idx]
        results.append(
            f"Article {article['article_number']}: {article['text']}"
        )

    return "\n\n".join(results)

def ask_constitution(question: str):
    context = retrieve_articles(question)

    prompt = f"""
QUESTION:
{question}

CONSTITUTION EXCERPTS:
{context}
"""

    response = groq.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    raw = response.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "summary": raw,
            "key_points": [],
            "limitations": [],
            "articles": []
        }

# --------------------------------------------------
# API ENDPOINT
# --------------------------------------------------

@app.post("/ask")
def ask(request: QuestionRequest):
    answer = ask_constitution(request.question)

    return {
        "question": request.question,
        **answer
    }
