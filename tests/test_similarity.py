import pytest

from app.similarity import cosine_similarity


def test_identical_vectors_have_similarity_one():
    score = cosine_similarity([1, 2, 3], [1, 2, 3])

    assert score == pytest.approx(1.0)


def test_perpendicular_vectors_have_similarity_zero():
    score = cosine_similarity([1, 0], [0, 1])

    assert score == pytest.approx(0.0)


def test_opposite_vectors_have_similarity_negative_one():
    score = cosine_similarity([1, 0], [-1, 0])

    assert score == pytest.approx(-1.0)


def test_different_dimensions_are_rejected():
    with pytest.raises(ValueError):
        cosine_similarity([1, 2], [1, 2, 3])


def test_empty_vectors_are_rejected():
    with pytest.raises(ValueError):
        cosine_similarity([], [])


def test_zero_vector_is_rejected():
    with pytest.raises(ValueError):
        cosine_similarity([0, 0], [1, 2])