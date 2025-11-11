"""
Test buggy version of top_k_frequent to demonstrate fault detection.
"""

import pytest
import sys
from pathlib import Path

# Import buggy solution
BASE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE / "src"))
from buggy_top_k_frequent import top_k_frequent

def test_kfreq_ties_prefer_smaller():
    """This test should FAIL with buggy version - tie-breaking is reversed."""
    # This test from iteration_1 should catch the bug
    result = top_k_frequent([1, 1, 2, 2, 3], k=2)
    # Expected: [1, 2] (smaller first) but buggy version returns [2, 1] (larger first)
    assert result == [1, 2], f"Expected [1, 2] but got {result!r}"

