"""
Pytest wrapper for min_window_substring coverage analysis.
"""
import pytest
import importlib
import sys
from pathlib import Path

# Add a2/ to path so we can import src
BASE = Path(__file__).resolve().parents[1]  # a2/
sys.path.insert(0, str(BASE))

# Import solution
solution_module = importlib.import_module("src.min_window_substring")
solution_func = solution_module.min_window_substring

# Import test runner - baseline tests are in root tests/
test_file = BASE.parent / "tests" / "test_min_window_substring.py"
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", test_file)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

def test_min_window_substring():
    """Run all tests for min_window_substring."""
    passed, failures = test_module.run_tests(solution_func)
    assert passed, f"Test failures: {' '.join(failures)}"
