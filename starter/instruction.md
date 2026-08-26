# Sudoku Project Instructions

## Project Goal

Build a modern, maintainable Flask Sudoku game by refactoring
the existing legacy application.

## Technology

- Python
- Flask
- HTML
- CSS
- JavaScript
- Browser localStorage
- pytest for testing

## Code Quality

- Keep the code modular and reusable.
- Use clear function and variable names.
- Prefer small functions with a single responsibility.
- Use type hints where appropriate.
- Avoid unnecessary dependencies.
- Keep Flask routes separate from Sudoku game logic.
- Add useful comments for non-obvious logic.
- Handle errors gracefully.

## Sudoku Rules

- The board must contain 9 rows and 9 columns.
- Every row must contain numbers 1-9 without repetition.
- Every column must contain numbers 1-9 without repetition.
- Every 3x3 box must contain numbers 1-9 without repetition.
- Every generated puzzle must have exactly one solution.
- Prefilled cells must be locked.

## Difficulty

Support:

- Easy
- Medium
- Hard

Difficulty should control the number of prefilled cells.

## Game Features

The application must support:

- New puzzle
- Difficulty selection
- Timer
- Check button
- Hint button
- Invalid-entry highlighting
- Completion message
- Top 10 leaderboard
- Player name
- Difficulty
- Completion time
- Number of hints
- Browser localStorage
- Dark mode

## UI Requirements

- Responsive desktop and mobile layout.
- Alternating styling for the 3x3 Sudoku boxes.
- Support light and dark modes.
- Buttons must be readable and usable.
- Use accessible labels and controls.
- Avoid unnecessary layout shifts.

## Testing

- Create tests before refactoring the application.
- Run tests after every major change.
- Test Sudoku generation and solution uniqueness.
- Test difficulty levels.
- Test validation.
- Test Flask routes where appropriate.

## Git and Copilot

- Make small, understandable changes.
- Review Copilot suggestions before accepting them.
- Do not blindly accept generated code.
- Explain unfamiliar code before using it.
- Preserve working functionality during refactoring.