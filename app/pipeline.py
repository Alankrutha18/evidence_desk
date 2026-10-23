from pathlib import Path

from app.ingestion import extract_pages
from app.chunking import split_text

pages = extract_pages(Path("data/sample.pdf"))

chunk_records = []

for page in pages:
    print("Processing page:", page["page_number"])
    chunks = split_text(page["text"], chunk_size=500, overlap=100)
    print("Chunks on this page:", len(chunks))
    for chunk_number, chunk in enumerate(chunks, start=1):
        chunk_records.append({
            "document_name": page["document_name"],
            "page_number": page["page_number"],
            "chunk_number": chunk_number,
            "text": chunk,
        })
print("Total chunk records:", len(chunk_records))







# pages = extract_pages(Path("data/sample.pdf"))
# print("Pages extracted:", len(pages))

# first_page = pages[0]
# text = first_page["text"]
# print("Characters:", len(text))

# chunks = split_text(text, chunk_size=500, overlap=100)
# print("Chunks created:", len(chunks))
# print("First chunk:", chunks[0])

# chunk_records = []
# for chunk_number, chunk in enumerate(chunks, start=1):
#         chunk_records.append({
#         "document_name": first_page["document_name"],
#         "page_number": first_page["page_number"],
#         "chunk_number": chunk_number,
#         "text": chunk,
#     })

# print("Chunk records:", len(chunk_records))
# print("First chunk number:", chunk_records[0]["chunk_number"])
# print("Source page:", chunk_records[0]["page_number"])