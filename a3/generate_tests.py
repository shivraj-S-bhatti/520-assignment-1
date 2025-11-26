#!/usr/bin/env python3
"""
Generate spec-guided tests for Assignment 3 problems.
"""

import sys
import pathlib

# Add eval to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'eval'))
from model_clients import ModelConfig, get_client

def generate_normalize_path_tests(corrected_specs: str):
    """Generate tests for normalize_path from corrected specs."""
    prompt = f"""You are now given a set of CORRECTED formal specifications for normalize_path(path: str) → str. These specs describe properties such as:
- absolute vs relative behavior,
- elimination of "." segments and collapse of "//",
- behavior of ".." with and without a parent segment,
- rules for trailing slash (only "/" may end with a slash),
- idempotence of normalization.

Corrected Specifications:
{corrected_specs}

Using ONLY these corrected specifications (do not look at coverage information), generate pytest unit tests for normalize_path.

Requirements:
- Use pytest style, not unittest.
- Import from a2.src.normalize_path (e.g., `from a2.src.normalize_path import normalize_path`).
- Each test must be named `test_norm_<short_description>`.
- Cover:
  - simple absolute and simple relative cases,
  - paths with multiple ".." segments (including when they would go "above root"),
  - combinations of ".", "..", and multiple slashes,
  - empty string / "." / "./" cases,
  - the special case where the result is exactly "/".

Produce 6–10 tests in total.
Avoid redundant tests that clearly exercise the same behavior; prefer parametrization when multiple inputs share one property.
Return ONLY valid Python test code."""

    # Use Google Gemini (free tier)
    config = ModelConfig(provider="google", model="gemini-2.0-flash", temperature=0.6)
    client = get_client(config)
    
    results = client.generate(prompt, n=1)
    return results[0]

def generate_evaluate_rpn_tests(corrected_specs: str):
    """Generate tests for evaluate_rpn from corrected specs."""
    prompt = f"""You are now given a set of CORRECTED formal specifications for evaluate_rpn(tokens: List[str]) -> int. These specs describe:
- constraints on valid tokens,
- stack discipline (never negative depth, ends at 1),
- truncation-toward-zero for division,
- necessary conditions for invalid expressions (stack underflow, extra operands),
- basic arithmetic semantics.

Corrected Specifications:
{corrected_specs}

Using only these corrected specifications (do not reference coverage or branches), generate pytest unit tests for evaluate_rpn.

Requirements:
- Use pytest.
- Import from a2.src.evaluate_rpn (e.g., `from a2.src.evaluate_rpn import evaluate_rpn`).
- Name tests `test_rpn_<short_description>`.
- Include tests for:
  - a simple addition expression,
  - a mixed expression with multiple operators and negative numbers,
  - positive and negative division where truncation toward zero matters,
  - clearly invalid RPN expressions that should raise an error (e.g., stack underflow, extra operands),
  - at least one more complex valid expression that combines 3+ operators.

Aim for about 6–10 tests. Use parametrization when several inputs share one property.
Return ONLY Python test code."""

    # Use Google Gemini (free tier)
    config = ModelConfig(provider="google", model="gemini-2.0-flash", temperature=0.6)
    client = get_client(config)
    
    results = client.generate(prompt, n=1)
    return results[0]

def generate_normalize_path_tests_manual():
    """Manually generate tests based on corrected specs."""
    return '''import pytest
import sys
from pathlib import Path

# Add a2 to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "a2"))
from src.normalize_path import normalize_path

def test_norm_absolute_simple():
    """Test simple absolute path normalization."""
    assert normalize_path("/a/b/c") == "/a/b/c"
    assert normalize_path("/a") == "/a"

def test_norm_relative_simple():
    """Test simple relative path normalization."""
    assert normalize_path("a/b/c") == "a/b/c"
    assert normalize_path("a") == "a"

def test_norm_collapse_slashes():
    """Test collapsing multiple slashes."""
    assert normalize_path("/a//b//c") == "/a/b/c"
    assert normalize_path("a//b") == "a/b"

def test_norm_eliminate_dot_segments():
    """Test elimination of '.' segments."""
    assert normalize_path("/a/./b/./c") == "/a/b/c"
    assert normalize_path("a/./b") == "a/b"
    assert normalize_path("./a") == "a"

def test_norm_parent_directory():
    """Test '..' segment resolution."""
    assert normalize_path("/a/b/../c") == "/a/c"
    assert normalize_path("a/b/../c") == "a/c"
    assert normalize_path("../../a") == "../../a"  # Preserved when no parent

def test_norm_parent_above_root():
    """Test '..' cannot go above root for absolute paths."""
    assert normalize_path("/../a") == "/a"
    assert normalize_path("/a/../../b") == "/b"

def test_norm_trailing_slash():
    """Test trailing slash rules (only root can have trailing slash)."""
    assert normalize_path("/") == "/"
    assert normalize_path("/a/") == "/a"
    assert normalize_path("a/") == "a"

def test_norm_empty_and_dot():
    """Test empty string and '.' inputs."""
    assert normalize_path("") == "."
    assert normalize_path(".") == "."

def test_norm_complex_combination():
    """Test complex combination of rules."""
    assert normalize_path("/a//b/./c/../d/") == "/a/b/d"
    assert normalize_path("a/../b/./c") == "b/c"

@pytest.mark.parametrize("path,expected", [
    ("/a/b/c", "/a/b/c"),
    ("a/b/c", "a/b/c"),
    ("/a//b", "/a/b"),
    ("a/./b", "a/b"),
    ("/a/../b", "/b"),
    ("../../a", "../../a"),
])
def test_norm_parametrized(path, expected):
    """Parametrized tests for various normalization cases."""
    assert normalize_path(path) == expected
'''

def generate_evaluate_rpn_tests_manual():
    """Manually generate tests based on corrected specs."""
    return '''import pytest
import sys
from pathlib import Path

# Add a2 to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "a2"))
from src.evaluate_rpn import evaluate_rpn

def test_rpn_simple_addition():
    """Test simple addition expression."""
    assert evaluate_rpn(["2", "3", "+"]) == 5
    assert evaluate_rpn(["10", "20", "+"]) == 30

def test_rpn_mixed_operations():
    """Test mixed expression with multiple operators."""
    assert evaluate_rpn(["2", "3", "+", "4", "*"]) == 20
    assert evaluate_rpn(["10", "6", "-", "4", "+"]) == 8

def test_rpn_negative_numbers():
    """Test expressions with negative numbers."""
    assert evaluate_rpn(["-2", "3", "+"]) == 1
    assert evaluate_rpn(["5", "-3", "-"]) == 8

def test_rpn_division_truncate_positive():
    """Test division truncates toward zero (positive case)."""
    assert evaluate_rpn(["7", "3", "/"]) == 2
    assert evaluate_rpn(["10", "3", "/"]) == 3

def test_rpn_division_truncate_negative():
    """Test division truncates toward zero (negative case)."""
    assert evaluate_rpn(["-7", "3", "/"]) == -2
    assert evaluate_rpn(["7", "-3", "/"]) == -2

def test_rpn_complex_expression():
    """Test complex expression with 3+ operators."""
    assert evaluate_rpn(["2", "3", "+", "4", "*", "5", "-"]) == 15
    assert evaluate_rpn(["10", "2", "/", "3", "+", "4", "*"]) == 32

def test_rpn_stack_underflow():
    """Test invalid expression: stack underflow."""
    with pytest.raises(ValueError, match="Too few operands"):
        evaluate_rpn(["2", "+"])
    with pytest.raises(ValueError, match="Too few operands"):
        evaluate_rpn(["+"])

def test_rpn_extra_operands():
    """Test invalid expression: extra operands remaining."""
    with pytest.raises(ValueError, match="too many operands"):
        evaluate_rpn(["2", "3", "4", "+"])
    with pytest.raises(ValueError, match="too many operands"):
        evaluate_rpn(["2", "3", "+", "4"])

def test_rpn_division_by_zero():
    """Test division by zero raises error."""
    with pytest.raises(ValueError, match="Division by zero"):
        evaluate_rpn(["5", "0", "/"])

def test_rpn_invalid_token():
    """Test invalid token raises error."""
    with pytest.raises(ValueError, match="Invalid token"):
        evaluate_rpn(["2", "abc", "+"])

@pytest.mark.parametrize("tokens,expected", [
    (["2", "3", "+"], 5),
    (["10", "5", "-"], 5),
    (["3", "4", "*"], 12),
    (["8", "2", "/"], 4),
])
def test_rpn_parametrized(tokens, expected):
    """Parametrized tests for basic operations."""
    assert evaluate_rpn(tokens) == expected
'''

if __name__ == "__main__":
    print("Generating tests for normalize_path...")
    # Use manual generation (API may not be available)
    norm_tests = generate_normalize_path_tests_manual()
    test_file = pathlib.Path(__file__).parent / "tests" / "spec_guided" / "normalize_path" / "test_spec_norm.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    with open(test_file, 'w') as f:
        f.write(norm_tests)
    print(f"Saved tests to {test_file}")
    
    print("\n\nGenerating tests for evaluate_rpn...")
    # Use manual generation (API may not be available)
    rpn_tests = generate_evaluate_rpn_tests_manual()
    test_file = pathlib.Path(__file__).parent / "tests" / "spec_guided" / "evaluate_rpn" / "test_spec_rpn.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    with open(test_file, 'w') as f:
        f.write(rpn_tests)
    print(f"Saved tests to {test_file}")

