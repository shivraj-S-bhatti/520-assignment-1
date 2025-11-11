from typing import List
from collections import Counter

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """Return the k most frequent integers in nums, breaking ties by smaller integer."""
    if k < 1:
        raise ValueError("k must be at least 1")
    if not nums:
        raise ValueError("nums cannot be empty")
    if k > len(set(nums)):
        raise ValueError("k cannot exceed the number of unique elements in nums")
    
    # Count frequencies and sort by frequency (desc) then value (asc)
    freq = Counter(nums)
    sorted_elements = sorted(freq.keys(), key=lambda x: (-freq[x], x))
    
    return sorted_elements[:k]