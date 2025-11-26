#!/usr/bin/env python3
"""
Generate formal specifications for Assignment 3 problems.
"""

import sys
import pathlib

# Add eval to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'eval'))
from model_clients import ModelConfig, get_client

def generate_normalize_path_specs():
    """Generate specifications for normalize_path."""
    prompt = """You are helping with specification-guided testing.

Problem description:
Implement a function normalize_path(path: str) that normalizes a Unix-style filesystem path string. The function must:
- Treat "." as a no-op segment.
- Treat ".." as "go to parent directory" when possible (for absolute paths, do not go above root).
- Collapse repeated slashes ("//" → "/").
- Preserve a leading "/" for absolute paths; keep relative paths relative.
- Ensure the result has no trailing slash, except when the normalized result is exactly "/".
- Preserve empty relative paths appropriately (e.g., "" or ".").

Method signature:
    def normalize_path(path: str) -> str

Task:
Write formal specifications as Python assertions that describe necessary properties of the correct result.

Let:
- `path` be the input string,
- `res` denote the correct normalized result for this path (do NOT call normalize_path inside the assertions).

Constraints:
- Do NOT call normalize_path or any other implementation in the assertions.
- Do NOT use I/O, randomness, or time.
- Use only pure string/sequence logic, arithmetic, and boolean operations.
- Express global semantic properties such as:
  - Behavior for absolute vs relative paths.
  - Elimination of "." segments.
  - Parent-directory ("..") behavior.
  - Rules for trailing slash.
  - Idempotence (a normalized path is already in normal form).

Generate 6–8 Python `assert` statements over `path`, `res`, and helper variables if needed.
Return ONLY the assertion code lines, no prose or explanations."""

    # Use Google Gemini (free tier)
    config = ModelConfig(provider="google", model="gemini-2.0-flash", temperature=0.6)
    client = get_client(config)
    
    results = client.generate(prompt, n=1)
    return results[0]

def generate_evaluate_rpn_specs():
    """Generate specifications for evaluate_rpn."""
    prompt = """You are helping with specification-guided testing.

Problem description:
Implement evaluate_rpn(tokens: List[str]) -> int, which evaluates an expression in Reverse Polish Notation.

Details:
- tokens is a list of strings.
- Valid tokens are:
  - integer literals, possibly with a leading minus sign (e.g. "3", "-7"),
  - operators: "+", "-", "*", "/".
- The expression is evaluated with a stack:
  - A number pushes one value.
  - An operator pops the top two operands (left, right) and pushes the result.
- Division uses integer division with truncation toward zero, equivalent to int(a / b) in Python for integers a, b != 0.
- A well-formed RPN expression must:
  - never require more operands than currently on the stack,
  - end with exactly one value on the stack.

Method signature:
    def evaluate_rpn(tokens: List[str]) -> int

Task:
Write formal specifications as Python assertions that describe necessary properties of the correct result.

Let:
- `tokens` be the input token list,
- `res` denote the mathematically correct result of evaluating this RPN expression.

Constraints:
- Do NOT call evaluate_rpn inside the assertions.
- Do NOT use I/O, randomness, or time.
- Use only arithmetic, sequence operations, and boolean logic.
- Specifications should capture:
  - token domain constraints,
  - stack-depth discipline for well-formed inputs,
  - truncation-toward-zero semantics for division,
  - correct behavior on simple examples (e.g., ["2","3","+"] gives 5),
  - necessary conditions for invalid expressions (stack underflow / leftover values).

Generate 6–8 Python `assert` statements over `tokens`, `res`, and helper variables if needed.
Return ONLY the assertion code lines, no prose."""

    # Use Google Gemini (free tier)
    config = ModelConfig(provider="google", model="gemini-2.0-flash", temperature=0.6)
    client = get_client(config)
    
    results = client.generate(prompt, n=1)
    return results[0]

if __name__ == "__main__":
    print("Generating specifications for normalize_path...")
    norm_specs = generate_normalize_path_specs()
    print("\n" + "="*60)
    print("NORMALIZE_PATH SPECIFICATIONS:")
    print("="*60)
    print(norm_specs)
    
    print("\n\nGenerating specifications for evaluate_rpn...")
    rpn_specs = generate_evaluate_rpn_specs()
    print("\n" + "="*60)
    print("EVALUATE_RPN SPECIFICATIONS:")
    print("="*60)
    print(rpn_specs)

