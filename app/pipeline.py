import json
from pathlib import Path

from app.chunking import split_text
from app.ingestion import extract_pages


def prepare_chunks(pdf_path: Path) -> list[dict]:
    pages = extract_pages(pdf_path)
    chunk_records = []

    for page in pages:
        if not page["text"].strip():
            continue

        chunks = split_text(
            page["text"],
            chunk_size=500,
            overlap=100,
        )

        for chunk_number, chunk in enumerate(chunks, start=1):
            chunk_records.append({
                "document_name": page["document_name"],
                "page_number": page["page_number"],
                "chunk_number": chunk_number,
                "text": chunk,
            })

    if not chunk_records:
        raise ValueError(
            "No readable text found. Please use a text-based PDF."
        )

    return chunk_records


if __name__ == "__main__":
    records = prepare_chunks(Path("data/sample.pdf"))

    output_path = Path("data/chunks.json")

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)

    print("Total chunk records:", len(records))