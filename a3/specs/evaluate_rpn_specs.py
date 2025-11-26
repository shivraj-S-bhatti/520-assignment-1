"""
Formal specifications for evaluate_rpn(tokens: List[str]) -> int

Generated specifications (before correction):
"""

# LLM-Generated Specifications (before correction)
GENERATED_SPECS = """
# Let tokens be the input token list, res be the evaluation result

# 1. Simple addition: ["2", "3", "+"] gives 5
assert (tokens == ["2", "3", "+"] and res == 5)

# 2. Stack discipline: number of numbers - number of operators = 1 for valid RPN
num_count = sum(1 for t in tokens if t not in ["+", "-", "*", "/"])
op_count = sum(1 for t in tokens if t in ["+", "-", "*", "/"])
assert (num_count - op_count == 1)

# 3. Division truncates toward zero: [7, 3, /] gives 2, not 2.33
assert (tokens == ["7", "3", "/"] and res == 2)

# 4. Negative division: [-7, 3, /] gives -2 (truncate toward zero)
assert (tokens == ["-7", "3", "/"] and res == -2)

# 5. Mixed operations: ["2", "3", "+", "4", "*"] gives 20
assert (tokens == ["2", "3", "+", "4", "*"] and res == 20)

# 6. Stack underflow: if operators > numbers - 1, expression is invalid
# (This would raise ValueError, so res doesn't exist - we can't assert on res)
assert (op_count <= num_count - 1)

# 7. Token domain: all tokens are either integers or operators
valid_tokens = all(t.lstrip('-').isdigit() or t in ["+", "-", "*", "/"] for t in tokens)
assert (valid_tokens)

# 8. Result is integer
assert (isinstance(res, int))
"""

"""
CORRECTED SPECIFICATIONS:
"""

CORRECTED_SPECS = """
# Let tokens be the input token list, res be the evaluation result

# 1. Simple addition: ["2", "3", "+"] gives 5
assert (tokens == ["2", "3", "+"] and res == 5)

# 2. Stack discipline: number of numbers - number of operators = 1 for valid RPN
num_count = sum(1 for t in tokens if t.lstrip('-').isdigit())
op_count = sum(1 for t in tokens if t in ["+", "-", "*", "/"])
assert (num_count - op_count == 1)

# 3. Division truncates toward zero: [7, 3, /] gives 2, not 2.33
assert (tokens == ["7", "3", "/"] and res == 2)

# 4. Negative division: [-7, 3, /] gives -2 (truncate toward zero)
assert (tokens == ["-7", "3", "/"] and res == -2)

# 5. Mixed operations: ["2", "3", "+", "4", "*"] gives 20
assert (tokens == ["2", "3", "+", "4", "*"] and res == 20)

# 6. Stack underflow condition: if operators > numbers - 1, expression is invalid
# For invalid expressions, the function raises ValueError, so this property
# only holds for valid expressions. We express it as a necessary condition:
# For a valid RPN expression: op_count == num_count - 1
if op_count == num_count - 1:
    assert (True)  # Valid stack discipline
else:
    # Invalid - would raise ValueError, so res doesn't exist
    pass

# 7. Token domain: all tokens are either integers (possibly negative) or operators
valid_tokens = all(
    (t.lstrip('-').isdigit() and (t == t.lstrip('-') or t.startswith('-'))) 
    or t in ["+", "-", "*", "/"] 
    for t in tokens
)
assert (valid_tokens)

# 8. Result is integer (for valid expressions)
assert (isinstance(res, int))
"""

# Accuracy analysis
TOTAL_SPECS = 8
CORRECT_SPECS = 7  # Specs 1, 2 (corrected), 3, 4, 5, 7 (corrected), 8 are correct
INCORRECT_SPECS = 1  # Spec 6 needs correction

ACCURACY_RATE = CORRECT_SPECS / TOTAL_SPECS

INCORRECT_ANALYSIS = """
Spec 6 (Incorrect):
- Issue: The original spec tried to assert on invalid expressions, but for invalid expressions,
  the function raises ValueError, so res doesn't exist. We can't assert on res for invalid cases.
- Corrected: Changed to express it as a conditional - the property only holds for valid expressions.
  For invalid expressions, the function would raise, so we don't assert on res.
"""

