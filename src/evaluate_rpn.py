from typing import List

def evaluate_rpn(tokens: List[str]) -> int:
    """Evaluates an RPN expression.

    Args:
        tokens: A list of strings representing the RPN expression.

    Returns:
        The integer result of the evaluation.

    Raises:
        ValueError: If the expression is invalid (e.g., too few operands or division by zero).
    """
    stack = []
    operators = {"+", "-", "*", "/"}

    for token in tokens:
        if token not in operators:
            try:
                stack.append(int(token))
            except ValueError:
                raise ValueError("Invalid token: {}".format(token))
        else:
            if len(stack) < 2:
                raise ValueError("Too few operands for operator: {}".format(token))
            operand2 = stack.pop()
            operand1 = stack.pop()

            if token == "+":
                stack.append(operand1 + operand2)
            elif token == "-":
                stack.append(operand1 - operand2)
            elif token == "*":
                stack.append(operand1 * operand2)
            elif token == "/":
                if operand2 == 0:
                    raise ValueError("Division by zero")
                stack.append(int(operand1 / operand2))  # Truncate towards zero
    
    if len(stack) != 1:
        raise ValueError("Invalid RPN expression: too many operands remaining")

    return stack.pop()