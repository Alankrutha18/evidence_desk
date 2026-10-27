import json
from pathlib import Path

from app.embeddings import embed_text


def prepare_embeddings(
    chunks: list[dict],
    output_path: Path,
) -> list[dict]:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        with output_path.open("r", encoding="utf-8") as file:
            saved_records = json.load(file)
    else:
        saved_records = []

    completed_records = []

    for chunk in chunks:
        matching_record = None

        for saved in saved_records:
            if (
                saved["document_name"] == chunk["document_name"]
                and saved["page_number"] == chunk["page_number"]
                and saved["chunk_number"] == chunk["chunk_number"]
                and saved["text"] == chunk["text"]
                and saved.get("embedding_model")
                == "text-embedding-3-small"
            ):
                matching_record = saved
                break

        if matching_record is None:
            matching_record = chunk.copy()
            matching_record["embedding"] = embed_text(chunk["text"])
            matching_record["embedding_model"] = "text-embedding-3-small"
            saved_records.append(matching_record)

            temporary_path = output_path.with_suffix(".tmp")

            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(
                    saved_records,
                    file,
                    ensure_ascii=False,
                    indent=2,
                )

            temporary_path.replace(output_path)

        completed_records.append(matching_record)

    return completed_records