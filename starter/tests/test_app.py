import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)
    app_module.CURRENT['puzzle'] = None
    app_module.CURRENT['solution'] = None
    app_module.CURRENT['hinted_cells'] = set()
    app_module.CURRENT['hints_used'] = 0
    with app_module.app.test_client() as test_client:
        yield test_client


def test_index_route_renders_successfully(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.content_type.startswith('text/html')


def test_new_route_returns_puzzle_with_requested_number_of_clues(client):
    response = client.get('/new?clues=40')

    assert response.status_code == 200
    puzzle = response.get_json()['puzzle']
    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert sum(cell != 0 for row in puzzle for cell in row) == 40


@pytest.mark.parametrize('difficulty, clues', [
    ('easy', 45),
    ('medium', 35),
    ('hard', 30),
])
def test_new_route_supports_difficulty_presets(client, difficulty, clues):
    response = client.get(f'/new?difficulty={difficulty}')

    assert response.status_code == 200
    puzzle = response.get_json()['puzzle']
    assert sum(cell != 0 for row in puzzle for cell in row) == clues
    assert app_module.sudoku_logic.count_solutions(puzzle) == 1


def test_check_route_requires_an_active_game(client):
    response = client.post('/check', json={'board': []})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_route_reports_no_incorrect_cells_for_solution(client):
    client.get('/new')
    solution = app_module.CURRENT['solution']

    response = client.post('/check', json={'board': solution})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_check_route_reports_incorrect_cell_coordinates(client):
    client.get('/new')
    board = [row[:] for row in app_module.CURRENT['solution']]
    board[0][0] = 0 if board[0][0] != 0 else 1

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json()['incorrect'] == [[0, 0]]


def test_hint_fills_empty_cell_with_correct_value_and_locks_it(client):
    client.get('/new?clues=80')
    puzzle = app_module.CURRENT['puzzle']
    solution = app_module.CURRENT['solution']
    board = [row[:] for row in puzzle]

    response = client.post('/hint', json={'board': board})

    assert response.status_code == 200
    hint = response.get_json()
    assert puzzle[hint['row']][hint['col']] == 0
    assert hint['value'] == solution[hint['row']][hint['col']]
    assert (hint['row'], hint['col']) in app_module.CURRENT['hinted_cells']
    assert hint['hints'] == 1
    assert hint['locked'] is True


def test_hints_fill_different_cells_and_do_not_replace_prefilled_cells(client):
    client.get('/new?clues=79')
    puzzle = app_module.CURRENT['puzzle']
    board = [row[:] for row in puzzle]
    prefilled = next(
        (row, col) for row in range(9) for col in range(9) if puzzle[row][col] != 0
    )

    first = client.post('/hint', json={'board': board}).get_json()
    board[first['row']][first['col']] = first['value']
    second = client.post('/hint', json={'board': board}).get_json()

    assert (first['row'], first['col']) != (second['row'], second['col'])
    assert prefilled not in {
        (first['row'], first['col']), (second['row'], second['col'])
    }
    assert second['hints'] == 2


def test_hint_requires_an_active_game(client):
    response = client.post('/hint', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}