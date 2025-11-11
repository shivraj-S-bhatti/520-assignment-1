from typing import List
from collections import Counter
import heapq

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Return the k most frequent integers in nums.
    If frequencies tie, break ties by smaller integer first.
    Output length must be exactly k.
    Raise ValueError if k < 1 or k > number of unique elements.
    """
    if k < 1:
        raise ValueError("k must be at least 1")

    counts = Counter(nums)
    num_unique = len(counts)

    if k > num_unique:
        raise ValueError("k cannot be greater than the number of unique elements")

    # Use a min-heap to keep track of the k most frequent elements.
    # The heap stores (frequency, number) tuples.
    heap = []
    for num, freq in counts.items():
        heapq.heappush(heap, (freq, -num))  # Negate num to get smaller number first in ties

    top_k = []
    for _ in range(k):
        freq, neg_num = heapq.heappop(heap)
        top_k.append(-neg_num)

    return top_k