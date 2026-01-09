import re
import json
from pathlib import Path

RAW_PATH = Path("data/constitution_raw.txt")
OUT_PATH = Path("data/constitution_articles.jsonl")

ARTICLE_RE = re.compile(r"\n(\d+)\.\s([A-Z][^\n]+)")

with open(RAW_PATH, "r", encoding="utf-8") as f:
    text = f.read()

matches = list(ARTICLE_RE.finditer(text))

print(f"Found {len(matches)} articles")

with open(OUT_PATH, "w", encoding="utf-8") as out:
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        article_num = match.group(1)
        article_title = match.group(2).strip()

        article_text = text[start:end].strip()

        record = {
            "article_number": int(article_num),
            "title": article_title,
            "text": article_text
        }

        out.write(json.dumps(record, ensure_ascii=False) + "\n")

print("✅ Article-level chunks created")
