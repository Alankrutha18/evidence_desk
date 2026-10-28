import json
from unittest.mock import patch

import pytest

from app.search import ask_question


def test_search_ranks_evidence_and_passes_it_to_answering(tmp_path):
    records = [
        {
            "document_name": "demo.pdf",
            "page_number": 1,
            "chunk_number": 1,
            "text": "An unrelated passage.",
            "embedding_model": "text-embedding-3-small",
            "embedding": [0.0, 1.0],
        },
        {
            "document_name": "demo.pdf",
            "page_number": 2,
            "chunk_number": 1,
            "text": "The relevant passage.",
            "embedding_model": "text-embedding-3-small",
            "embedding": [1.0, 0.0],
        },
    ]

    embeddings_path = tmp_path / "embedded_chunks.json"
    embeddings_path.write_text(json.dumps(records), encoding="utf-8")

    with (
        patch(
            "app.search.embed_text",
            return_value=[1.0, 0.0],
        ) as mock_embed,
        patch(
            "app.search.generate_answer",
            return_value="A supported answer [Source 1].",
        ) as mock_answer,
    ):
        result = ask_question(
            "A test question",
            top_k=1,
            embeddings_path=embeddings_path,
        )

    mock_embed.assert_called_once_with("A test question")

    assert result["answer"] == "A supported answer [Source 1]."
    assert len(result["sources"]) == 1
    assert result["sources"][0]["page_number"] == 2
    assert result["sources"][0]["text"] == "The relevant passage."

    mock_answer.assert_called_once()
    question, context = mock_answer.call_args.args

    assert question == "A test question"
    assert "[Source 1]" in context
    assert "Page: 2" in context
    assert "The relevant passage." in context
    assert "An unrelated passage." not in context


def test_blank_question_is_rejected_before_api_call():
    with patch("app.search.embed_text") as mock_embed:
        with pytest.raises(ValueError, match="Please enter a question"):
            ask_question("   ")

    mock_embed.assert_not_called()


def test_empty_collection_is_rejected_before_api_call(tmp_path):
    embeddings_path = tmp_path / "empty.json"
    embeddings_path.write_text("[]", encoding="utf-8")

    with patch("app.search.embed_text") as mock_embed:
        with pytest.raises(ValueError, match="No embedded chunks"):
            ask_question(
                "A test question",
                embeddings_path=embeddings_path,
            )

    mock_embed.assert_not_called()