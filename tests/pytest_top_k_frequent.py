"""
Pytest wrapper for top_k_frequent coverage analysis.
"""
import pytest
import importlib

# Import solution
solution_module = importlib.import_module("src.top_k_frequent")
solution_func = solution_module.top_k_frequent

# Import test runner
import sys
from pathlib import Path
test_file = Path(__file__).parent / "test_top_k_frequent.py"
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", test_file)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

def test_top_k_frequent():
    """Run all tests for top_k_frequent."""
    passed, failures = test_module.run_tests(solution_func)
    assert passed, f"Test failures: {' '.join(failures)}"
