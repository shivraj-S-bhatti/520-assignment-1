"""
LLM-generated tests for normalize_path - Iteration 2
Additional edge cases for trailing slashes and complex relative paths
"""

import pytest
import sys
from pathlib import Path

# Import solution
BASE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE / "src"))
from normalize_path import normalize_path

def test_norm_complex_relative_with_trailing():
    """Test complex relative paths with trailing slashes."""
    assert normalize_path('a/b/c/../d/') == 'a/b/d/'
    assert normalize_path('x/./y/../z/') == 'x/z/'

def test_norm_parent_at_start():
    """Test paths starting with parent directory."""
    assert normalize_path('../a/b/') == '../a/b/'
    assert normalize_path('../../a/') == '../../a/'

def test_norm_mixed_dots_and_parents():
    """Test paths with mixed . and .. segments."""
    assert normalize_path('a/./../b/') == 'b/'
    assert normalize_path('a/.././b/') == 'b/'

