import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(Path(".env"))


def embed_text(text: str) -> list[float]:
    if not text.strip():
        raise ValueError("Text must not be empty")

    client = OpenAI()

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

    return response.data[0].embedding


if __name__ == "__main__":
    text = "Employees can carry over five unused leave days."

    embedding = embed_text(text)

    print("Number of dimensions:", len(embedding))
    print("First five numbers:", embedding[:5])

    record = {
        "text": text,
        "embedding": embedding,
    }

    output_path = Path("data/example_embedding.json")

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(record, file, ensure_ascii=False, indent=2)