"""
Pytest wrapper for merge_intervals coverage analysis.
"""
import pytest
import importlib

# Import solution
solution_module = importlib.import_module("src.merge_intervals")
solution_func = solution_module.merge_intervals

# Import test runner
import sys
from pathlib import Path
test_file = Path(__file__).parent / "test_merge_intervals.py"
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", test_file)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

def test_merge_intervals():
    """Run all tests for merge_intervals."""
    passed, failures = test_module.run_tests(solution_func)
    assert passed, f"Test failures: {' '.join(failures)}"
