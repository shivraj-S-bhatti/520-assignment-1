"""
Pytest wrapper for cosine_similarity coverage analysis.
"""
import pytest
import importlib

# Import solution
solution_module = importlib.import_module("src.cosine_similarity")
solution_func = solution_module.cosine_similarity

# Import test runner
import sys
from pathlib import Path
test_file = Path(__file__).parent / "test_cosine_similarity.py"
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", test_file)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

def test_cosine_similarity():
    """Run all tests for cosine_similarity."""
    passed, failures = test_module.run_tests(solution_func)
    assert passed, f"Test failures: {' '.join(failures)}"
