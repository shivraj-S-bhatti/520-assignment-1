from typing import List

def evaluate_rpn(tokens: List[str]) -> int:
    stack = []
    for token in tokens:
        if token in '+-*/':
            if len(stack) < 2:
                raise ValueError("Insufficient operands for operation")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ValueError("Division by zero")
                stack.append(int(a / b))  # truncates toward zero
        else:
            try:
                stack.append(int(token))
            except ValueError:
                raise ValueError(f"Invalid token: {token}")
    
    if len(stack) != 1:
        raise ValueError("Invalid expression: too many operands")
    return stack[0]