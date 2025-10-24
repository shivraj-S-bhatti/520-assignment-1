
def run_tests(impl):
    failures = []
    valid = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"],
    ]
    invalid_row = [row[:] for row in valid]
    invalid_row[0][0] = "8"
    invalid_row[0][1] = "8"
    invalid_box = [row[:] for row in valid]
    invalid_box[0][0] = "9"
    invalid_col = [row[:] for row in valid]
    invalid_col[1][0] = "5"

    try:
        if not impl(valid):
            failures.append("valid board flagged invalid")
    except Exception as e:
        failures.append(f"valid board raised {e.__class__.__name__}: {e}")

    for name, board in [("invalid_row", invalid_row), ("invalid_box", invalid_box), ("invalid_col", invalid_col)]:
        try:
            if impl(board):
                failures.append(f"{name} board flagged valid")
        except Exception as e:
            failures.append(f"{name} board raised {e.__class__.__name__}: {e}")

    return (len(failures) == 0, failures)
