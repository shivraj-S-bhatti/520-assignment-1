from typing import List
from collections import Counter
import heapq

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Return the k most frequent integers in nums.
    
    NOTE: This is a buggy version for testing purposes.
    Bug: Reversed tie-breaking comparison - larger number chosen instead of smaller.
    """
    if k < 1:
        raise ValueError("k must be at least 1")

    counts = Counter(nums)
    num_unique = len(counts)

    if k > num_unique:
        raise ValueError("k cannot be greater than the number of unique elements")

    # Bug: Use positive num instead of negative - causes larger numbers to be preferred in ties
    heap = []
    for num, freq in counts.items():
        heapq.heappush(heap, (freq, num))

    top_k = []
    for _ in range(k):
        freq, num = heapq.heappop(heap)
        top_k.append(num)
    
    # Bug: Reverse to get larger numbers first (wrong tie-breaking)
    top_k.reverse()

    return top_k

