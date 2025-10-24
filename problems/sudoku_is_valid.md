# Validate Sudoku Board

**Function signature:**

```python
from typing import List

def sudoku_is_valid(board: List[List[str]]) -> bool:
```

**Task:** Check whether a partially filled 9x9 Sudoku board is valid.

**Details & Constraints:**

Board uses '.' for empty and '1'-'9' for digits. Check rows, columns, and 3x3 boxes for duplicates (ignoring '.').
