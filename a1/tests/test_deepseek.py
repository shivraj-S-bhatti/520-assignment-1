"""
Test suite for DeepSeek V3 solutions from Assignment 1.
Tests all 10 problems using solutions from solutions/ directory.
"""

import pytest
import importlib
import sys
from pathlib import Path

# Add solutions to path
BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "solutions"))

# Import test runners
test_modules = {}
problems = [
    "cosine_similarity", "evaluate_rpn", "int_to_roman", "is_palindrome_sentence",
    "merge_intervals", "min_window_substring", "normalize_path", "parse_csv_line",
    "sudoku_is_valid", "top_k_frequent"
]

# Load test modules
import importlib.util
for problem in problems:
    test_file = BASE / "tests" / f"test_{problem}.py"
    if test_file.exists():
        spec = importlib.util.spec_from_file_location(f"test_{problem}", test_file)
        test_modules[problem] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_modules[problem])

@pytest.mark.parametrize("problem", problems)
def test_deepseek_solution(problem):
    """Test DeepSeek V3 solution for a specific problem."""
    try:
        # Import solution from solutions/
        solution_module = importlib.import_module(problem)
        solution_func = getattr(solution_module, problem)
        
        # Get test runner
        test_module = test_modules.get(problem)
        if not test_module:
            pytest.skip(f"No test module found for {problem}")
        
        # Run tests
        passed, failures = test_module.run_tests(solution_func)
        
        if not passed:
            failure_msg = f"problem-{problems.index(problem)} Test failures: {'; '.join(failures)}"
            pytest.fail(failure_msg)
        
        assert passed, f"Tests failed for {problem}"
    
    except ImportError as e:
        pytest.skip(f"Could not import {problem} from solutions/: {e}")
    except AttributeError as e:
        pytest.skip(f"Function {problem} not found in module: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error testing {problem}: {e}")

