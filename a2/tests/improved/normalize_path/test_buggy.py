"""
Test buggy version of normalize_path to demonstrate fault detection.
"""

import pytest
import sys
from pathlib import Path

# Import buggy solution
BASE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE / "src"))
from buggy_normalize_path import normalize_path

def test_norm_trailing_dir_slash():
    """This test should FAIL with buggy version - trailing slash not preserved."""
    # This test from iteration_1 should catch the bug
    # The correct behavior should preserve trailing slashes for relative directory paths
    result = normalize_path('a/b/')
    # Expected: 'a/b/' but buggy version returns 'a/b' (trailing slash removed)
    assert result == 'a/b/', f"Expected 'a/b/' but got {result!r} - buggy version removes trailing slash"

