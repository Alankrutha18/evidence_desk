import json
from pathlib import Path

from app.embeddings import embed_text
from app.similarity import cosine_similarity


# Load the saved document chunks and their embeddings.
with Path("data/embedded_chunks.json").open(
    "r", encoding="utf-8"
) as file:
    chunks = json.load(file)

print("Searchable chunks:", len(chunks))


# Collect and validate the user's question.
question = input("Ask a question about the document: ").strip()

if not question:
    raise ValueError("Please enter a question")


# Make one API request to embed the question.
question_embedding = embed_text(question)

print("Question dimensions:", len(question_embedding))


# Compare the question with each saved chunk locally.
results = []

for chunk in chunks:
    score = cosine_similarity(
        question_embedding,
        chunk["embedding"],
    )

    results.append({
        "score": score,
        "chunk": chunk,
    })

results.sort(key=lambda result: result["score"], reverse=True)

top_results = results[:3]

for rank, result in enumerate(top_results, start=1):
    chunk = result["chunk"]

    print("\nRank:", rank)
    print("Similarity:", round(result["score"], 4))
    print("Document:", chunk["document_name"])
    print("Page:", chunk["page_number"])
    print("Chunk:", chunk["chunk_number"])
    print("Text:", chunk["text"])