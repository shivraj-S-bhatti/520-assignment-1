#!/usr/bin/env python3
"""
Create pytest-compatible test wrappers for coverage analysis.
"""

import pathlib
import importlib.util

def create_pytest_wrapper(problem_name: str, base_dir: pathlib.Path):
    """Create a pytest-compatible test file."""
    test_file = base_dir / "tests" / f"test_{problem_name}.py"
    wrapper_file = base_dir / "tests" / f"pytest_{problem_name}.py"
    
    # Load the original test module
    spec = importlib.util.spec_from_file_location("test_module", str(test_file))
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)
    
    # Import the solution
    solution_module_name = f"solutions.{problem_name}"
    
    # Create pytest wrapper
    wrapper_content = f'''"""
Pytest wrapper for {problem_name} coverage analysis.
"""
import pytest
import importlib

# Import solution
solution_module = importlib.import_module("{solution_module_name}")
solution_func = solution_module.{problem_name}

# Import test runner
import sys
from pathlib import Path
test_file = Path(__file__).parent / "test_{problem_name}.py"
import importlib.util
spec = importlib.util.spec_from_file_location("test_module", test_file)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

def test_{problem_name}():
    """Run all tests for {problem_name}."""
    passed, failures = test_module.run_tests(solution_func)
    assert passed, f"Test failures: {{' '.join(failures)}}"
'''
    
    with open(wrapper_file, 'w') as f:
        f.write(wrapper_content)
    
    print(f"Created pytest wrapper: {wrapper_file.name}")

def main():
    """Create pytest wrappers for all problems."""
    BASE = pathlib.Path(__file__).resolve().parents[1]
    
    problems = [
        "cosine_similarity", "evaluate_rpn", "int_to_roman", "is_palindrome_sentence",
        "merge_intervals", "min_window_substring", "normalize_path", "parse_csv_line",
        "sudoku_is_valid", "top_k_frequent"
    ]
    
    for problem in problems:
        create_pytest_wrapper(problem, BASE)
    
    print(f"\nCreated {len(problems)} pytest wrappers")

if __name__ == "__main__":
    main()
