import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(".env"))

api_key = os.getenv("OPENAI_API_KEY")

print("API key found:", bool(api_key))