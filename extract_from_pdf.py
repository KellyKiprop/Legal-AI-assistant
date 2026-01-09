import pdfplumber
from pathlib import Path

PDF_PATH = Path("data/TheConstitutionOfKenya.pdf")
OUT_PATH = Path("data/constitution_raw.txt")

with pdfplumber.open(PDF_PATH) as pdf:
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                f.write(f"\n\n--- PAGE {i} ---\n\n")
                f.write(text)

print("✅ Extracted text from PDF")
