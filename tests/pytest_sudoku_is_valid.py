"""
Pytest wrapper for sudoku_is_valid coverage analysis.
"""
import pytest
import importlib

# Import solution
solution_module = importlib.import_module("src.sudoku_is_valid")
solution_func = solution_module.sudoku_is_valid

# Import test runner
import sys
from pathlib import Path
test_file = Path(__file__).parent / "test_sudoku_is_valid.py"
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", test_file)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

def test_sudoku_is_valid():
    """Run all tests for sudoku_is_valid."""
    passed, failures = test_module.run_tests(solution_func)
    assert passed, f"Test failures: {' '.join(failures)}"
