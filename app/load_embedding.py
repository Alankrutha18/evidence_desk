import json
from pathlib import Path

input_path = Path("data/example_embedding.json")

with input_path.open("r", encoding="utf-8") as file:
    record = json.load(file)

text = record["text"]
embedding = record["embedding"]

print("Saved text:", text)
print("Saved dimensions:", len(embedding))