# Top-K Frequent Elements

**Function signature:**

```python
from typing import List

def top_k_frequent(nums: List[int], k: int) -> List[int]:
```

**Task:** Return the k most frequent integers in nums.

**Details & Constraints:**

If frequencies tie, break ties by smaller integer first. Output length must be exactly k. Raise ValueError if k < 1 or k > number of unique elements.
