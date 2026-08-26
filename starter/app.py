from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None,
    'hinted_cells': set(),
    'hints_used': 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty')
    if difficulty is not None:
        try:
            clues = sudoku_logic.clues_for_difficulty(difficulty)
        except ValueError as error:
            return jsonify({'error': str(error)}), 400
    else:
        clues = int(request.args.get('clues', 35))
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    CURRENT['hinted_cells'] = set()
    CURRENT['hints_used'] = 0
    return jsonify({'puzzle': puzzle})

@app.route('/hint', methods=['POST'])
def give_hint():
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    data = request.get_json(silent=True) or {}
    board = data.get('board')
    if not isinstance(board, list) or len(board) != sudoku_logic.SIZE:
        return jsonify({'error': 'A valid board is required'}), 400
    if any(not isinstance(row, list) or len(row) != sudoku_logic.SIZE for row in board):
        return jsonify({'error': 'A valid board is required'}), 400

    hint = sudoku_logic.find_hint(puzzle, solution, CURRENT['hinted_cells'], board)
    if hint is None:
        return jsonify({'error': 'No empty cells remain'}), 400

    row, col, value = hint
    CURRENT['hinted_cells'].add((row, col))
    CURRENT['hints_used'] += 1
    return jsonify({
        'row': row,
        'col': col,
        'value': value,
        'hints': CURRENT['hints_used'],
        'locked': True
    })

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})

if __name__ == '__main__':
    app.run(debug=True)