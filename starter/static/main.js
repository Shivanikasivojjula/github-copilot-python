// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const LEADERBOARD_KEY = 'sudoku-leaderboard-v1';
const DARK_MODE_KEY = 'sudoku-dark-mode';
let puzzle = [];
let currentDifficulty = 'medium';
let hintsUsed = 0;
let elapsedSeconds = 0;
let timerId = null;
let scoreRecorded = false;

function setDarkMode(enabled) {
  document.body.classList.toggle('dark-mode', enabled);
  const button = document.getElementById('dark-mode');
  if (button) {
    button.setAttribute('aria-pressed', enabled ? 'true' : 'false');
    button.innerText = enabled ? 'Light Mode' : 'Dark Mode';
  }
}

function toggleDarkMode() {
  const enabled = !document.body.classList.contains('dark-mode');
  setDarkMode(enabled);
  window.localStorage.setItem(DARK_MODE_KEY, enabled ? 'true' : 'false');
}

function sortScores(scores) {
  return scores
    .slice()
    .sort((first, second) => first.completionTime - second.completionTime)
    .slice(0, 10);
}

function loadLeaderboard(storage = window.localStorage) {
  try {
    const scores = JSON.parse(storage.getItem(LEADERBOARD_KEY) || '[]');
    return Array.isArray(scores) ? sortScores(scores) : [];
  } catch (error) {
    return [];
  }
}

function saveScore(score, storage = window.localStorage) {
  const scores = sortScores(loadLeaderboard(storage).concat(score));
  storage.setItem(LEADERBOARD_KEY, JSON.stringify(scores));
  return scores;
}

function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
  const seconds = (totalSeconds % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}

function renderLeaderboard() {
  const scores = loadLeaderboard();
  const body = document.getElementById('leaderboard-body');
  body.innerHTML = '';
  scores.forEach((score) => {
    const row = document.createElement('tr');
    [score.playerName, formatTime(score.completionTime), score.difficulty, score.hints]
      .forEach((value) => {
        const cell = document.createElement('td');
        cell.innerText = value;
        row.appendChild(cell);
      });
    body.appendChild(row);
  });
}

function stopTimer() {
  if (timerId !== null) {
    window.clearInterval(timerId);
    timerId = null;
  }
}

function startTimer() {
  stopTimer();
  timerId = window.setInterval(() => {
    elapsedSeconds += 1;
    document.getElementById('timer').innerText = formatTime(elapsedSeconds);
  }, 1000);
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function updateHintButton() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const hasEmptyCell = Array.from(inputs).some((input) => !input.disabled && !input.value);
  document.getElementById('hint').disabled = !hasEmptyCell;
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
  updateHintButton();
}

async function newGame() {
  currentDifficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${currentDifficulty}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  hintsUsed = 0;
  elapsedSeconds = 0;
  scoreRecorded = false;
  document.getElementById('hints').innerText = hintsUsed;
  document.getElementById('timer').innerText = formatTime(elapsedSeconds);
  startTimer();
  updateHintButton();
  document.getElementById('message').innerText = '';
}

async function useHint() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const value = inputs[i * SIZE + j].value;
      board[i][j] = value ? parseInt(value, 10) : 0;
    }
  }
  const response = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await response.json();
  const message = document.getElementById('message');
  if (data.error) {
    message.innerText = data.error;
    updateHintButton();
    return;
  }
  const input = inputs[data.row * SIZE + data.col];
  input.value = data.value;
  input.disabled = true;
  input.className = 'sudoku-cell hinted';
  hintsUsed = data.hints;
  document.getElementById('hints').innerText = hintsUsed;
  updateHintButton();
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    stopTimer();
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';
    if (!scoreRecorded) {
      const playerName = document.getElementById('player-name').value.trim() || 'Anonymous';
      saveScore({
        playerName,
        completionTime: elapsedSeconds,
        difficulty: currentDifficulty,
        hints: hintsUsed
      });
      scoreRecorded = true;
      renderLeaderboard();
    }
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
if (typeof window !== 'undefined') {
  window.addEventListener('load', () => {
    document.getElementById('new-game').addEventListener('click', newGame);
    document.getElementById('check-solution').addEventListener('click', checkSolution);
    document.getElementById('hint').addEventListener('click', useHint);
    document.getElementById('dark-mode').addEventListener('click', toggleDarkMode);
    setDarkMode(window.localStorage.getItem(DARK_MODE_KEY) === 'true');
    renderLeaderboard();
    // initialize
    newGame();
  });
}

if (typeof module !== 'undefined') {
  module.exports = { LEADERBOARD_KEY, sortScores, loadLeaderboard, saveScore, formatTime };
}