def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be at least 0 and smaller than chunk_size")

    chunks = []
    step = chunk_size - overlap 

    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)

    return chunks

if __name__ == "__main__":
    results = split_text("ABCDEFGHIJKL", 4, 1)
    print(results)