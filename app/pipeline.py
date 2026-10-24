import json
from pathlib import Path

from app.ingestion import extract_pages
from app.chunking import split_text

pages = extract_pages(Path("data/sample.pdf"))

chunk_records = []

for page in pages:
    print("Processing page:", page["page_number"])
    chunks = split_text(page["text"], chunk_size=500, overlap=100)
    print("Chunks on this page:", len(chunks))
    for chunk_number, chunk in enumerate(chunks, start=1):
        chunk_records.append({
            "document_name": page["document_name"],
            "page_number": page["page_number"],
            "chunk_number": chunk_number,
            "text": chunk,
        })
print("Total chunk records:", len(chunk_records))


output_path = Path("data/chunks.json")

with output_path.open("w", encoding="utf-8") as file:
    json.dump(chunk_records, file, ensure_ascii=False, indent=2)




