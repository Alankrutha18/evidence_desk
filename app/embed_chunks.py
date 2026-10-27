import json
from pathlib import Path

from app.embeddings import embed_text


# Load the chunks prepared from the PDF.
with Path("data/chunks.json").open("r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Chunks ready:", len(chunks))


# Load previously completed records, if available.
output_path = Path("data/embedded_chunks.json")

if output_path.exists():
    with output_path.open("r", encoding="utf-8") as file:
        embedded_chunks = json.load(file)
else:
    embedded_chunks = []


for chunk in chunks:
    already_saved = False

    # Check whether this exact chunk was embedded with the same model.
    for saved_chunk in embedded_chunks:
        if (
            saved_chunk["document_name"] == chunk["document_name"]
            and saved_chunk["page_number"] == chunk["page_number"]
            and saved_chunk["chunk_number"] == chunk["chunk_number"]
            and saved_chunk["text"] == chunk["text"]
            and saved_chunk.get("embedding_model")
            == "text-embedding-3-small"
        ):
            already_saved = True
            break

    if already_saved:
        print(
            "Skipping saved — Page:",
            chunk["page_number"],
            "Chunk:",
            chunk["chunk_number"],
        )
        continue

    # This function call makes a paid API request.
    embedding = embed_text(chunk["text"])

    # Keep the source information alongside the embedding.
    embedded_record = chunk.copy()
    embedded_record["embedding_model"] = "text-embedding-3-small"
    embedded_record["embedding"] = embedding

    embedded_chunks.append(embedded_record)

    # Save progress after every completed chunk.
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(embedded_chunks, file, ensure_ascii=False, indent=2)

    print(
        "Saved — Page:",
        chunk["page_number"],
        "Chunk:",
        chunk["chunk_number"],
    )

print("Embedding preparation complete.")