"""
Pytest wrapper for is_palindrome_sentence coverage analysis.
"""
import pytest
import importlib
import sys
from pathlib import Path

# Add a2/ to path so we can import src
BASE = Path(__file__).resolve().parents[1]  # a2/
sys.path.insert(0, str(BASE))

# Import solution
solution_module = importlib.import_module("src.is_palindrome_sentence")
solution_func = solution_module.is_palindrome_sentence

# Import test runner - baseline tests are in root tests/
test_file = BASE.parent / "tests" / "test_is_palindrome_sentence.py"
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", test_file)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

def test_is_palindrome_sentence():
    """Run all tests for is_palindrome_sentence."""
    passed, failures = test_module.run_tests(solution_func)
    assert passed, f"Test failures: {' '.join(failures)}"
