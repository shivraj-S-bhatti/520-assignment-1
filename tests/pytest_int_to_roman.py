"""
Pytest wrapper for int_to_roman coverage analysis.
"""
import pytest
import importlib

# Import solution
solution_module = importlib.import_module("src.int_to_roman")
solution_func = solution_module.int_to_roman

# Import test runner
import sys
from pathlib import Path
test_file = Path(__file__).parent / "test_int_to_roman.py"
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", test_file)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

def test_int_to_roman():
    """Run all tests for int_to_roman."""
    passed, failures = test_module.run_tests(solution_func)
    assert passed, f"Test failures: {' '.join(failures)}"
