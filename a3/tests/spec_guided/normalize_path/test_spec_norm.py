import pytest
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
