# EvidenceDesk


EvidenceDesk is a retrieval-augmented generation (RAG) application that
answers questions about uploaded PDFs using retrieved document passages.
Built with Python, Streamlit, and OpenAI APIs, it combines semantic search
with source-referenced answers and inspectable evidence.

The application extracts page-level text, creates overlapping chunks,
and stores embeddings with source metadata. For each question, it ranks
passages using cosine similarity and supplies the top matches to an LLM.
Users can inspect the retrieved passages, document names, and page numbers
alongside the generated answer.

## Features

- PDF upload and local text extraction.
- Overlapping chunks with document, page, and chunk metadata.
- Explicit embedding preparation with saved progress and reuse.
- Cosine-similarity search returning the top three passages.
- Answers generated from retrieved evidence with source labels.
- Expandable evidence showing source text and PDF page numbers.
- Document-specific collections within each browser session.
- Previous answers cleared when the selected document changes.

## Architecture

```text
Document preparation
PDF → pypdf extraction → overlapping chunks → embeddings → local JSON

Question answering
Question → embedding → cosine-similarity ranking → top 3 passages
         → answer generation → answer and source display
```

Embeddings use `text-embedding-3-small`.
Answer generation uses `gpt-5-mini`.

## Setup

Development has been tested on Windows with Python 3.14.

Clone the repository:

```powershell
git clone https://github.com/Alankrutha18/evidence_desk.git
cd evidence_desk
```

Create an environment and install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and supply your own OpenAI API key:

```powershell
Copy-Item .env.example .env
```

The key needs permission to create embeddings and Responses.
API billing is separate from ChatGPT subscriptions.

## Run

From the repository root:

```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

1. Upload a text-based PDF.
2. Click **Read PDF and preview chunks**.
3. Inspect the preview.
4. Click **Create embeddings**.
5. Submit a question and inspect its retrieved evidence.

Current upload limits are 5 MB and 60 chunks.

## Costs and document handling

PDF extraction and similarity calculations run locally.
Embedding creation and answer generation use paid OpenAI API requests.

Extracted passage text is sent to OpenAI when embeddings are created.
Questions and retrieved passages are sent when answers are generated.

Local documents, embeddings, and `.env` are excluded from Git.
Uploaded files remain on disk until removed manually.
Browser-session folders are separate; starting a new session may require
embedding the same document again.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

The current suite contains 17 checks covering:

- Chunk boundaries, overlap, short inputs, and invalid settings.
- Known cosine-similarity results and invalid vectors.
- Retrieval ranking, source-context assembly, and API orchestration.
- Rejection of blank questions and empty collections.

Search tests mock external calls and require no API credit.

## Project organization

- `streamlit_app.py`: upload, preparation, question form, and evidence display.
- `app/ingestion.py`: PDF text extraction.
- `app/chunking.py`: character-based chunking.
- `app/pipeline.py`: reusable document preparation.
- `app/embeddings.py`: embedding API helper.
- `app/document_service.py`: resumable embedding preparation.
- `app/similarity.py`: cosine similarity.
- `app/search.py`: retrieval and question-answering orchestration.
- `app/answering.py`: evidence-based answer-generation request.
- `tests/`: automated checks.

Other small scripts preserve development experiments and terminal workflows.

## Limitations

- Scanned PDFs require OCR, which is not implemented.
- Character-based chunks can split words and sentences.
- Search compares every stored vector; no ANN index is implemented.
- Questions are independent; conversation history is not supplied.
- Source labels are generated references, not automatically verified proof.
- The model may miss evidence or produce unsupported statements.
- Automated tests do not establish real-world answer accuracy.
- Retrieval and answer quality have only been manually spot-checked.
- Authentication, global spending controls, and automatic file cleanup
  are not implemented.

This is a local portfolio prototype. Public deployment requires additional
access, spending, and document-lifecycle controls.
