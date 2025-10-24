# Evaluate Reverse Polish Notation

**Function signature:**

```python
from typing import List

def evaluate_rpn(tokens: List[str]) -> int:
```

**Task:** Evaluate an RPN expression with +, -, *, / (truncating toward zero).

**Details & Constraints:**

Supported tokens are integers and operators + - * /. Division truncates toward zero like int(a/b).
Raise ValueError for invalid expressions (e.g., too few operands or division by zero).
