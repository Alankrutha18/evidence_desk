import json
from pathlib import Path
# from urllib import response

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(Path(".env"))
client = OpenAI()

print("Client created")

text = "Employees can carry over five unused leave days."

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text,
)

embedding = response.data[0].embedding

print("Number of dimensions:", len(embedding))
print("First five numbers:", embedding[:5])

record = {
    "text": text,
    "embedding": embedding,
}

output_path = Path("data/example_embedding.json")

with output_path.open("w", encoding="utf-8") as file:
    json.dump(record, file, ensure_ascii=False, indent=2)