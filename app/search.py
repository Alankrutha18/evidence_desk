import json
from pathlib import Path

from app.answering import generate_answer
from app.embeddings import embed_text
from app.similarity import cosine_similarity


def ask_question(
    question: str,
    top_k: int = 3,
    embeddings_path: Path = Path("data/embedded_chunks.json"),
) -> dict:
    question = question.strip()

    if not question:
        raise ValueError("Please enter a question")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    # Load the prepared document collection.
    with embeddings_path.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        raise ValueError("No embedded chunks are available")

    # Check compatibility before making paid requests.
    for chunk in chunks:
        if chunk.get("embedding_model") != "text-embedding-3-small":
            raise ValueError("Document embedding model does not match")

    # One paid request: embed the question.
    question_embedding = embed_text(question)

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
    top_results = results[:top_k]

    # Build labeled evidence and source records.
    context_parts = []
    sources = []

    for source_number, result in enumerate(top_results, start=1):
        chunk = result["chunk"]

        source_label = (
            f"[Source {source_number}] "
            f"Document: {chunk['document_name']} | "
            f"Page: {chunk['page_number']} | "
            f"Chunk: {chunk['chunk_number']}"
        )

        context_parts.append(source_label + "\n" + chunk["text"])

        sources.append({
            "source_number": source_number,
            "document_name": chunk["document_name"],
            "page_number": chunk["page_number"],
            "chunk_number": chunk["chunk_number"],
            "text": chunk["text"],
            "score": result["score"],
        })

    context = "\n\n".join(context_parts)

    # One paid request: generate an answer from the evidence.
    answer = generate_answer(question, context)

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }


if __name__ == "__main__":
    question = input("Ask a question about the document: ")
    result = ask_question(question)

    print("\nANSWER")
    print(result["answer"])

    print("\nRETRIEVED SOURCES")

    for source in result["sources"]:
        print(
            f"[Source {source['source_number']}] "
            f"{source['document_name']} | "
            f"Page {source['page_number']} | "
            f"Chunk {source['chunk_number']} | "
            f"Similarity {source['score']:.4f}"
        )