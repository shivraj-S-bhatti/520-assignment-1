from typing import List
import math

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two equal-length vectors.

    Return 0.0 if either vector has zero magnitude. Use float return.
    Raise ValueError if lengths differ.
    """
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")

    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x ** 2 for x in a))
    magnitude_b = math.sqrt(sum(x ** 2 for x in b))

    if magnitude_a == 0.0 or magnitude_b == 0.0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)