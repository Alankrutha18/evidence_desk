import json
from pathlib import Path

from app.similarity import cosine_similarity


with Path("data/example_embedding.json").open(
    "r", encoding="utf-8"
) as file:
    passage = json.load(file)

passage_embedding = passage["embedding"]


with Path("data/question_embedding.json").open(
    "r", encoding="utf-8"
) as file:
    question_record = json.load(file)

question = question_record["text"]
question_embedding = question_record["embedding"]


print("Passage dimensions:", len(passage_embedding))
print("Question dimensions:", len(question_embedding))

similarity = cosine_similarity(passage_embedding, question_embedding)

print("Cosine similarity:", similarity)