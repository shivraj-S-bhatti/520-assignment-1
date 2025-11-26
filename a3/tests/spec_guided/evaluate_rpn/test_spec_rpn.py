import pytest
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
