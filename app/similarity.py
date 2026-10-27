import math


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same number of dimensions")

    if len(vector_a) == 0:
        raise ValueError("Vectors must not be empty")
    
    dot_product = 0.0

    for value_a, value_b in zip(vector_a, vector_b):
        dot_product += value_a * value_b

    sum_of_squares_a = 0.0
    sum_of_squares_b = 0.0

    for value in vector_a:
        sum_of_squares_a += value ** 2

    for value in vector_b:
        sum_of_squares_b += value ** 2

    magnitude_a = math.sqrt(sum_of_squares_a)
    magnitude_b = math.sqrt(sum_of_squares_b)

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Cosine similarity is undefined for a zero vector")

    return dot_product / (magnitude_a * magnitude_b)


if __name__ == "__main__":
    print(cosine_similarity([1, 2], [3, 4]))