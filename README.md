# EvidenceDesk

A work-in-progress document question-answering application using
retrieval-augmented generation (RAG).

The goal is to answer questions using relevant PDF passages and provide
source references. The current version implements document preparation
and a standalone embedding-similarity experiment.

## Implemented

- Extract text from PDFs with document names and original page numbers.
- Split page text into overlapping character-based chunks.
- Validate chunk-size and overlap settings.
- Save and load chunk records using JSON.
- Create an embedding for a sample passage and a sample question.
- Save and reload embeddings.
- Calculate cosine similarity locally using saved vectors.

## Current workflow

PDF → extract page text → split into chunks → attach source metadata
→ save chunk records to JSON

A separate experiment creates and saves passage/question embeddings,
then compares them without further API calls.

## Project structure

- `app/ingestion.py`: PDF text extraction.
- `app/chunking.py`: overlapping text chunks and input validation.
- `app/pipeline.py`: document preparation and JSON output.
- `app/load_chunks.py`: loads saved chunk records.
- `app/check_config.py`: checks whether an API key is available without displaying it.
- `app/embeddings.py`: creates and saves a sample passage embedding.
- `app/load_embedding.py`: loads the saved passage embedding.
- `app/compare_embeddings.py`: compares saved passage and question embeddings.
- `data/`: local documents and generated files; excluded from Git.

## Setup

Requires Python. Development currently uses Python 3.14.

Create a virtual environment:

```powershell
py -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

For API requests, create a local `.env` file:

```dotenv
OPENAI_API_KEY=your_key_here
```

Never commit the real key. API usage is billed separately.

## Run document preparation

Place a text-based PDF at `data/sample.pdf`, then run from the project root:

```powershell
.\.venv\Scripts\python.exe -m app.pipeline
```

The pipeline writes `data/chunks.json`.

## Embedding experiment

The sample passage embedding is created with:

```powershell
.\.venv\Scripts\python.exe -m app.embeddings
```

This makes a paid API request and writes `data/example_embedding.json`.

The comparison script requires that file and
`data/question_embedding.json`. The question embedding was generated
during development; its generation workflow still needs to be made reusable.

Once both files exist:

```powershell
.\.venv\Scripts\python.exe -m app.compare_embeddings
```

The comparison runs locally without API calls.

## Limitations and next steps

- PDF extraction has been demonstrated on a one-page sample.
- Character-based chunks can split words and sentences.
- PDF chunk embeddings are not yet connected to retrieval.
- Automated tests have not yet been added.
- Answer generation, citation validation, API endpoints, and a user interface
  are planned.
- Similarity scores are not probabilities of answer correctness.
