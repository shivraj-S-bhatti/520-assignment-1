"""
Pytest wrapper for parse_csv_line coverage analysis.
"""
import pytest
import importlib

# Import solution
solution_module = importlib.import_module("src.parse_csv_line")
solution_func = solution_module.parse_csv_line

# Import test runner
import sys
from pathlib import Path
test_file = Path(__file__).parent / "test_parse_csv_line.py"
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", test_file)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

def test_parse_csv_line():
    """Run all tests for parse_csv_line."""
    passed, failures = test_module.run_tests(solution_func)
    assert passed, f"Test failures: {' '.join(failures)}"
