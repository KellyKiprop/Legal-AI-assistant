import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

INPUT_FILE = "data/constitution_articles_clean.jsonl"
INDEX_FILE = "constitution.index"

# Load articles
articles = []
with open(INPUT_FILE, "r") as f:
    for line in f:
        record = json.loads(line)
        articles.append(record)

print(f"Loaded {len(articles)} articles")

# Initialize embedder
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
texts = [a["text"] for a in articles]
embeddings = model.encode(texts, convert_to_numpy=True)

# Create FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# Save index and metadata
faiss.write_index(index, INDEX_FILE)
with open("constitution_meta.json", "w") as f:
    json.dump(articles, f, ensure_ascii=False)

print(f"✅ FAISS index saved ({INDEX_FILE}) with metadata")
