from pathlib import Path

from app.ingestion import extract_pages
from app.chunking import split_text

pages = extract_pages(Path("data/sample.pdf"))
print("Pages extracted:", len(pages))