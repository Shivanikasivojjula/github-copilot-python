import copy
import random

SIZE = 9
EMPTY = 0
DIFFICULTY_CLUES = {'easy': 45, 'medium': 35, 'hard': 30}

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def _find_empty_cell_with_fewest_candidates(board):
    best_cell = None
    best_candidates = None
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] != EMPTY:
                continue
            candidates = [
                number for number in range(1, SIZE + 1)
                if is_safe(board, row, col, number)
            ]
            if not candidates:
                return (row, col), []
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_cell = (row, col)
                best_candidates = candidates
    return best_cell, best_candidates or []

def count_solutions(board, limit=2):
    if limit < 1:
        return 0

    working_board = deep_copy(board)

    def count(remaining):
        cell, candidates = _find_empty_cell_with_fewest_candidates(working_board)
        if cell is None:
            return 1
        if not candidates:
            return 0

        row, col = cell
        total = 0
        for candidate in candidates:
            working_board[row][col] = candidate
            total += count(remaining - total)
            working_board[row][col] = EMPTY
            if total >= remaining:
                return total
        return total

    return count(limit)

def remove_cells(board, clues):
    if not 0 <= clues <= SIZE * SIZE:
        raise ValueError('clues must be between 0 and 81')

    while True:
        cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
        random.shuffle(cells)
        removed = False
        for row, col in cells:
            if sum(cell != EMPTY for row_values in board for cell in row_values) <= clues:
                return
            value = board[row][col]
            if value == EMPTY:
                continue
            board[row][col] = EMPTY
            if count_solutions(board) == 1:
                removed = True
            else:
                board[row][col] = value
        if not removed:
            break

    if sum(cell != EMPTY for row_values in board for cell in row_values) != clues:
        raise ValueError('Unable to generate a uniquely solvable puzzle with this clue count')

def clues_for_difficulty(difficulty):
    try:
        return DIFFICULTY_CLUES[difficulty.lower()]
    except (AttributeError, KeyError):
        raise ValueError('difficulty must be easy, medium, or hard')

def find_hint(puzzle, solution, hinted_cells=(), board=None):
    hinted = set(hinted_cells)
    for row in range(SIZE):
        for col in range(SIZE):
            if (puzzle[row][col] == EMPTY and (row, col) not in hinted
                    and (board is None or board[row][col] == EMPTY)):
                return row, col, solution[row][col]
    return None

def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution
