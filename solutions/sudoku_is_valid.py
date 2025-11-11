from typing import List

def sudoku_is_valid(board: List[List[str]]) -> bool:
    # Check rows
    for row in board:
        seen = set()
        for num in row:
            if num != '.':
                if num in seen:
                    return False
                seen.add(num)
    
    # Check columns
    for col in range(9):
        seen = set()
        for row in range(9):
            num = board[row][col]
            if num != '.':
                if num in seen:
                    return False
                seen.add(num)
    
    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            seen = set()
            for row in range(box_row, box_row + 3):
                for col in range(box_col, box_col + 3):
                    num = board[row][col]
                    if num != '.':
                        if num in seen:
                            return False
                        seen.add(num)
    
    return True