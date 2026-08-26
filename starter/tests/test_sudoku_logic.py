import sudoku_logic


def test_create_empty_board_has_expected_shape_and_values():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5

    assert sudoku_logic.is_safe(board, 0, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 0, 5) is False
    assert sudoku_logic.is_safe(board, 1, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 1, 4) is True


def test_generate_puzzle_returns_valid_solution_and_requested_clues():
    clues = 35
    puzzle, solution = sudoku_logic.generate_puzzle(clues)

    assert len(solution) == sudoku_logic.SIZE
    assert all(sorted(row) == list(range(1, sudoku_logic.SIZE + 1)) for row in solution)
    assert all(
        sorted(solution[row][column] for row in range(sudoku_logic.SIZE))
        == list(range(1, sudoku_logic.SIZE + 1))
        for column in range(sudoku_logic.SIZE)
    )
    assert all(
        solution[box_row + row][box_column + column] for row in range(3) for column in range(3)
        for box_row in range(0, sudoku_logic.SIZE, 3)
        for box_column in range(0, sudoku_logic.SIZE, 3)
    )

    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == clues
    assert all(
        puzzle[row][column] in (sudoku_logic.EMPTY, solution[row][column])
        for row in range(sudoku_logic.SIZE)
        for column in range(sudoku_logic.SIZE)
    )


def test_generate_puzzle_has_exactly_one_solution():
    puzzle, _ = sudoku_logic.generate_puzzle(35)

    assert sudoku_logic.count_solutions(puzzle) == 1


def test_count_solutions_rejects_a_board_with_multiple_solutions():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.count_solutions(board) == 2