from typing import List

def sudoku_is_valid(board: List[List[str]]) -> bool:
    """Check if a partially filled Sudoku board is valid."""

    # Check rows
    for row in board:
        seen = set()
        for cell in row:
            if cell != '.':
                if cell in seen:
                    return False
                seen.add(cell)

    # Check columns
    for col in range(9):
        seen = set()
        for row in range(9):
            cell = board[row][col]
            if cell != '.':
                if cell in seen:
                    return False
                seen.add(cell)

    # Check 3x3 boxes
    for box_row in range(3):
        for box_col in range(3):
            seen = set()
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cell = board[row][col]
                    if cell != '.':
                        if cell in seen:
                            return False
                        seen.add(cell)

    return True