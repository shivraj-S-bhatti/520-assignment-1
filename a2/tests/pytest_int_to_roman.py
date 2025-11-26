"""
Pytest wrapper for int_to_roman coverage analysis.
"""
import pytest
import importlib
import sys
from pathlib import Path

# Add a2/ to path so we can import src
BASE = Path(__file__).resolve().parents[1]  # a2/
sys.path.insert(0, str(BASE))

# Import solution
solution_module = importlib.import_module("src.int_to_roman")
solution_func = solution_module.int_to_roman

# Import test runner - baseline tests are in root tests/
test_file = BASE.parent / "tests" / "test_int_to_roman.py"
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", test_file)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

def test_int_to_roman():
    """Run all tests for int_to_roman."""
    passed, failures = test_module.run_tests(solution_func)
    assert passed, f"Test failures: {' '.join(failures)}"
