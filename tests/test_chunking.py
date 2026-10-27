import pytest

from app.chunking import split_text


def test_chunks_preserve_overlap_and_remaining_text():
    chunks = split_text("ABCDEFGHIJKL", chunk_size=4, overlap=1)

    assert chunks == ["ABCD", "DEFG", "GHIJ", "JKL"]


def test_short_text_is_preserved():
    chunks = split_text("Hello", chunk_size=500, overlap=100)

    assert chunks == ["Hello"]


def test_empty_text_produces_no_chunks():
    chunks = split_text("", chunk_size=500, overlap=100)

    assert chunks == []


@pytest.mark.parametrize(
    "chunk_size, overlap",
    [
        (0, 0),
        (-1, 0),
        (4, -1),
        (4, 4),
        (4, 5),
    ],
)
def test_invalid_settings_are_rejected(chunk_size, overlap):
    with pytest.raises(ValueError):
        split_text("Example text", chunk_size, overlap)