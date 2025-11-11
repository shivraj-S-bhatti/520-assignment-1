"""
Pytest wrapper for is_palindrome_sentence coverage analysis.
"""
import pytest
import importlib

# Import solution
solution_module = importlib.import_module("src.is_palindrome_sentence")
solution_func = solution_module.is_palindrome_sentence

# Import test runner
import sys
from pathlib import Path
test_file = Path(__file__).parent / "test_is_palindrome_sentence.py"
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", test_file)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

def test_is_palindrome_sentence():
    """Run all tests for is_palindrome_sentence."""
    passed, failures = test_module.run_tests(solution_func)
    assert passed, f"Test failures: {' '.join(failures)}"
