# Sudoku

A browser-based Sudoku game built as a single self-contained HTML file. No dependencies, no build step — just open and play.

## How to Play

Open `sudoku.html` in any modern browser. A new puzzle is generated automatically on load.

**Entering numbers**
- Click a cell to select it, then type a digit (1–9).
- On mobile, use the on-screen numpad.
- Press `⌫` (or `Backspace` / `Delete`) to erase a cell.

**Keyboard navigation**
- Arrow keys move the selection between cells.

**Highlighted cells**
- The selected cell is highlighted in blue.
- All cells in the same row, column, and 3×3 box are dimly highlighted to help you scan for conflicts.

## Controls

| Button    | Action                                                  |
|-----------|---------------------------------------------------------|
| New Game  | Generates a fresh puzzle with a unique solution         |
| Check     | Highlights incorrect entries in red                     |
| Solve     | Fills in the complete solution automatically            |
| Clear     | Erases all your entries and resets the board            |

## How It Works

Everything runs in plain JavaScript inside the single HTML file.

- **Puzzle generation** — a full valid solution is built using a backtracking algorithm with shuffled candidates, ensuring randomness.
- **Puzzle creation** — cells are removed one at a time; before each removal a quick solver verifies the puzzle still has exactly one solution.
- **Solver** — a standard backtracking solver, used both for uniqueness checks and the "Solve" button.
- **UI** — the 9×9 grid is rendered as `<input>` elements inside a CSS Grid layout. Bold borders divide the board into 3×3 boxes.

## Requirements

Any modern browser (Chrome, Firefox, Safari, Edge). No internet connection required after the file is downloaded.

## File Structure

```
sudoku.html   — complete application (HTML + CSS + JS in one file)
```
