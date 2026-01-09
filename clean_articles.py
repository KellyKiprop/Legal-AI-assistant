import json
import re

INPUT = "data/constitution_articles.jsonl"
OUTPUT = "data/constitution_articles_clean.jsonl"

CHAPTER_PATTERN = re.compile(
    r"\nCHAPTER\s+[A-Z]+\n.*?$", re.DOTALL
)

with open(INPUT, "r") as fin, open(OUTPUT, "w") as fout:
    for line in fin:
        record = json.loads(line)
        text = record["text"]

        # Remove chapter/part bleed
        text = re.sub(CHAPTER_PATTERN, "", text).strip()

        record["text"] = text
        fout.write(json.dumps(record, ensure_ascii=False) + "\n")

print("✅ Cleaned article chunks saved")
