import math

import json
from pathlib import Path

with Path("data/example_embedding.json").open("r", encoding="utf-8") as file:
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

dot_product = 0.0

for passage_value, question_value in zip(
    passage_embedding, question_embedding
):
    dot_product += passage_value * question_value


passage_sum_of_squares = 0.0

for value in passage_embedding:
    passage_sum_of_squares += value ** 2

passage_magnitude = math.sqrt(passage_sum_of_squares)


question_sum_of_squares = 0.0 

for value in question_embedding:
    question_sum_of_squares += value ** 2

question_magnitude = math.sqrt(question_sum_of_squares)

similarity = dot_product / (passage_magnitude * question_magnitude)

print("Cosine similarity:", similarity)


