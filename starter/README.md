# Flask Sudoku Game

## Project Description

This project is a modern Sudoku game built using Python and Flask. The project refactors a basic legacy Sudoku application and adds several new features to make the game more interactive, user-friendly, and maintainable.

The application generates Sudoku puzzles with unique solutions and provides different difficulty levels. Players can enter numbers, check their answers, request hints, track their solving time, and save their scores to a Top 10 leaderboard.

The project also includes responsive styling, dark mode, automated testing, and browser local storage for persistent leaderboard data.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/github-copilot-python.git
```

### 2. Navigate to the Project

```bash
cd github-copilot-python/starter
```

### 3. Create a Virtual Environment

For Windows:

```powershell
python -m venv .venv
```

### 4. Activate the Virtual Environment

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

## How to Run

Make sure the virtual environment is activated.

Start the Flask application:

```powershell
python app.py
```

The application will run locally.

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

## How to Test

The project uses `pytest` for automated testing.

Run all tests using:

```powershell
python -m pytest
```

The test suite checks important parts of the application, including Sudoku logic, puzzle generation, validation, and Flask functionality.

A successful test run should show that all tests have passed, for example:

```text
8 passed
```

The number of tests may increase as additional features are implemented.

## Features

### Difficulty Levels

The game supports three difficulty levels:

* Easy
* Medium
* Hard

Each difficulty level changes the number of prefilled cells.

### Unique Solution

Every generated Sudoku puzzle is checked to ensure that it has exactly one valid solution.

### Sudoku Validation

The application validates:

* Rows
* Columns
* 3 × 3 boxes
* User entries

Invalid entries are highlighted to provide immediate feedback.

### Hint Button

The Hint button:

* Fills one correct empty cell
* Locks the hinted cell
* Prevents the same cell from receiving another hint
* Tracks the number of hints used

### Check Button

The Check button identifies incorrect entries and highlights them so the player can correct mistakes.

### Timer

A timer tracks how long the player takes to solve a puzzle.

The timer starts when a new game begins and stops when the puzzle is completed.

### Top 10 Leaderboard

Completed games can be added to a Top 10 leaderboard.

The leaderboard stores:

* Player name
* Completion time
* Difficulty
* Number of hints

Scores are sorted by completion time.

The leaderboard uses browser `localStorage`, allowing scores to remain after refreshing or reopening the application.

### Dark Mode

The application includes a dark mode toggle that changes the appearance of the complete interface.

### Responsive Design

The interface is designed to work on:

* Desktop
* Laptop
* Tablet
* Mobile devices

The Sudoku board also uses different styling for the 3 × 3 sections to make the grid easier to understand.

## Technologies

The project uses the following technologies:

* **Python** — Application and Sudoku logic
* **Flask** — Web application framework
* **HTML5** — Page structure
* **CSS3** — Styling and responsive design
* **JavaScript** — Interactive game functionality
* **pytest** — Automated testing
* **localStorage** — Persistent leaderboard storage
* **Git** — Version control
* **GitHub** — Repository hosting
* **GitHub Copilot** — AI coding assistant

## How GitHub Copilot Was Used

GitHub Copilot was used throughout the project as a development assistant.

Copilot was used to help with:

1. **Testing Setup**

   * Set up the pytest testing framework.
   * Created baseline tests before major refactoring.
   * Helped explain existing application behavior.

2. **Sudoku Logic**

   * Helped implement Sudoku puzzle generation.
   * Added solution-counting logic.
   * Ensured generated puzzles have exactly one unique solution.

3. **Difficulty Levels**

   * Helped implement Easy, Medium, and Hard difficulty levels.
   * Adjusted the number of prefilled cells while maintaining unique solutions.

4. **Hint Feature**

   * Helped implement the Hint button.
   * Added logic to fill one correct cell.
   * Locked cells provided through hints.
   * Added hint-count tracking.

5. **Check Feature**

   * Helped implement validation of player entries.
   * Added visual feedback for incorrect values.

6. **Timer**

   * Helped implement the game timer.
   * Added logic to track completion time.

7. **Leaderboard**

   * Helped implement the Top 10 leaderboard.
   * Added player names, times, difficulty levels, and hint counts.
   * Used browser `localStorage` to preserve scores between sessions.

8. **Styling**

   * Helped style the Sudoku 3 × 3 sections.
   * Added responsive design.
   * Helped implement light and dark modes.

9. **Testing and Debugging**

   * Used Copilot to identify errors and suggest fixes.
   * Tests were run after major changes to ensure existing functionality continued to work.

Copilot suggestions were reviewed before being accepted. Suggestions were modified or rejected when they did not match the project requirements or could affect existing functionality.
