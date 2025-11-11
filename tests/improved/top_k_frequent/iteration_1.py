"""
LLM-generated tests for top_k_frequent - Iteration 1
Targeting: k==0, k>unique, tie-breaking, negative numbers
"""

import pytest
import sys
from pathlib import Path

# Import solution
BASE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE / "src"))
from top_k_frequent import top_k_frequent

def test_kfreq_k_zero():
    """Test k == 0 should raise ValueError."""
    with pytest.raises(ValueError, match="k must be at least 1"):
        top_k_frequent([1, 2, 3], k=0)

def test_kfreq_k_greater_than_unique():
    """Test k greater than number of unique elements should raise."""
    with pytest.raises(ValueError, match="k cannot be greater"):
        top_k_frequent([1, 2], k=3)
    with pytest.raises(ValueError, match="k cannot be greater"):
        top_k_frequent([1, 1, 2, 2], k=3)

def test_kfreq_ties_prefer_smaller():
    """Test ties in frequency broken by smaller numeric value."""
    # [1,1,2,2,3] - both 1 and 2 appear twice, should prefer 1 then 2
    result = top_k_frequent([1, 1, 2, 2, 3], k=2)
    assert result == [1, 2]  # 1 and 2 tied, smaller first
    
    # [3,3,2,2,1] - 3 and 2 tied, should prefer 2 then 3
    result = top_k_frequent([3, 3, 2, 2, 1], k=2)
    assert result == [2, 3]  # 2 and 3 tied, smaller first

def test_kfreq_negative_numbers():
    """Test with negative numbers."""
    # -1 and -2 both appear twice, -2 < -1 so -2 should come first
    result = top_k_frequent([-1, -1, -2, -2], k=2)
    assert result == [-2, -1]  # -2 < -1, so -2 first

