import json
from pathlib import Path

input_path = Path("data/chunks.json")

with input_path.open("r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Loaded chunks:", len(chunks))