from pathlib import Path

from pypdf import PdfReader

def extract_pages(pdf_Path: Path) -> list[dict]:
    reader = PdfReader(pdf_Path)
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append({"document_name": pdf_Path.name, "page_number": page_number, "text": text})
    return pages

if __name__ == "__main__":
    records = extract_pages(Path("data/sample.pdf"))
    print(records)