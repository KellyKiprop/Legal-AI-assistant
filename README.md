# 🇰🇪 Kenya Constitution AI Chatbot

A production-ready **Retrieval-Augmented Generation (RAG)** system that allows users to ask questions about the Constitution of Kenya and receive **clear, plain-English explanations** — understandable by anyone, not just legal experts.

---

## 🚀 Overview

This project transforms the Constitution of Kenya from a dense legal document into an **interactive AI assistant**.

Users can:

* Ask legal questions in natural language
* Get simplified explanations
* See the exact constitutional articles backing the answer

---

## 🧠 Architecture

```
Frontend (Lovable UI)
        ↓
FastAPI Backend (api.py)
        ↓
FAISS Vector Search
        ↓
Relevant Articles Retrieved
        ↓
Groq LLM (LLM reasoning + simplification)
        ↓
Structured Plain-English Response
```

---

## ✨ Features

* 📄 **Article-level retrieval** (high accuracy vs chunk-based noise)
* ⚡ **Fast FAISS similarity search**
* 🧠 **LLM-powered explanations (Groq)**
* 🗣️ **Plain English output (non-legal language)**
* 🔍 **Cited constitutional sources**
* 🔌 **API-first design (ready for any frontend)**

---

## 📂 Project Structure

```
.
├── api.py                          # FastAPI backend
├── rag_answer_engine_groq.py       # Core RAG pipeline
├── extract_from_pdf.py             # Extract raw text from PDF
├── chunk_by_article.py             # Split into articles
├── clean_articles.py               # Clean & normalize text
├── build_index.py                  # Create FAISS index
├── constitution.index              # Vector index
├── data/
│   └── constitution_articles_clean.jsonl
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Setup

### 1. Clone repo

```bash
git clone https://github.com/your-username/kenya-constitution-rag.git
cd kenya-constitution-rag
```

### 2. Create environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set API key

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the API

```bash
uvicorn api:app --reload
```

Then open:

```
http://127.0.0.1:8000/docs
```

---

## 🔌 API Usage

### Endpoint

```
POST /ask
```

### Request

```json
{
  "question": "What does the Constitution say about freedom of expression?"
}
```

### Response

```json
{
  "answer": "The Constitution guarantees freedom of expression, including the right to share ideas and information...",
  "sources": ["Article 33", "Article 34"]
}
```

---

## 🧪 Example Output

**Question:**

> What does the Constitution say about freedom of expression?

**Answer (simplified):**

* You have the right to express ideas and opinions
* You can share information and create content
* Media is independent

**Limitations:**

* No hate speech
* No inciting violence
* Must respect others

**Sources:**

* Article 33
* Article 34

---

## 🏗️ How It Works

### 1. Data Pipeline

* Constitution PDF → raw text
* Raw text → article-level chunks
* Cleaned → structured JSONL

### 2. Indexing

* SentenceTransformers embeddings
* Stored in FAISS for fast retrieval

### 3. Query Flow

1. User question → embedding
2. FAISS → top relevant articles
3. Context → Groq LLM
4. LLM → simplified answer + citations

---

## ⚡ Performance Design

* Preloaded models (no reload per request)
* FAISS for millisecond retrieval
* Minimal context for faster LLM responses
* API-first architecture for scalability

---

## 🧩 Future Improvements

* 🔎 Hybrid search (keyword + vector)
* 🧠 Re-ranking for better relevance
* 💬 Conversational memory
* 🌍 Multilingual support (Swahili)
* 📱 Mobile-first UI
* ☁️ Cloud deployment

---

## 📌 Tech Stack

* **Backend:** FastAPI
* **Vector DB:** FAISS
* **Embeddings:** SentenceTransformers
* **LLM:** Groq
* **Frontend:** Lovable

---

## 🎯 Goal

To make the Constitution:

> **Accessible, understandable, and usable by every Kenyan — not just lawyers.**

---

## 🤝 Contributing

Contributions are welcome. Feel free to:

* Improve retrieval accuracy
* Enhance UI/UX
* Add new features

---

## 📜 License

MIT License

---

## 👤 Author

Built as part of an AI engineering journey focused on:

* Real-world RAG systems
* Legal AI applications
* Production-ready ML systems

---
