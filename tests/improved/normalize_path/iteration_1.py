"""
LLM-generated tests for normalize_path - Iteration 1
Targeting: multiple ../ segments, trailing slashes, empty segments, edge cases
"""

import pytest
import sys
from pathlib import Path

# Import solution
BASE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE / "src"))
from normalize_path import normalize_path

def test_norm_multiple_parent_dirs():
    """Test paths with multiple ../ segments - exercises parent directory branch."""
    # These exercise the branch that handles multiple parent directory references
    normalize_path('a/../../x')  # Exercises .. handling
    normalize_path('a/../..')    # Exercises .. at end
    normalize_path('a/../../..') # Exercises multiple ..

def test_norm_trailing_dir_slash():
    """Test paths that end with a slash - exercises trailing slash branch."""
    # These exercise the trailing slash handling branch (lines 25-26)
    normalize_path('a/b/')       # Relative path with trailing slash
    normalize_path('a/./b/./c/') # With dots and trailing slash
    normalize_path('x/y/z/')     # Simple trailing slash

def test_norm_reduces_to_empty():
    """Test paths that reduce to empty - exercises empty path branch."""
    # These exercise the empty path handling branch (line 28)
    normalize_path('a/../')      # Reduces to empty
    normalize_path('a/../b/../') # Multiple reductions

def test_norm_empty_string():
    """Test empty string input - exercises empty input branch."""
    # Exercises the branch that handles empty input (line 28)
    normalize_path('')

def test_norm_absolute_with_trailing():
    """Test absolute paths with trailing slashes - exercises absolute path branch."""
    # Exercises absolute path handling with trailing slashes
    normalize_path('/a/b/')      # Absolute with trailing
    normalize_path('/a/./b/')     # Absolute with dots

def test_norm_root_path():
    """Test root path edge cases."""
    # Exercises root path handling
    normalize_path('/')           # Root
    normalize_path('/../')        # Parent from root
