# Chess Game (Pygame + python-chess + Stockfish)

Simple, clean chess GUI built with **Pygame** and **python-chess**, with an optional **Stockfish** engine for Human vs AI play. Includes drag-and-drop moves, a right-side control panel, player timers, selectable time presets, and popup messages for resign/draw.

> **Why this repo?** Quick to run, easy to read, interview-friendly code structure.

---

## ✨ Features
- **Modes:** Human vs Human ↔ Human vs AI (toggle button).
- **Engine:** Uses Stockfish via `python-chess` (UCI) for AI moves.
- **UI:** Drag & drop pieces, legal-move enforcement, popups on **Resign** / **Draw**.
- **Timers:** White/Black countdown clocks with preset time options.
- **Controls panel:** Start Game, Resign, Draw, New Game, Game Mode, Time Control.

> **Note:** The time options are simple presets (e.g., `30`, `10`, `5`, `3`, `1` minutes). Labels like `30+10` are placeholders; **per-move increments are not implemented yet**.

---

## 📦 Requirements
- Python **3.9+**
- [Pygame](https://www.pygame.org/)
- [python-chess](https://python-chess.readthedocs.io/)
- [Stockfish](https://stockfishchess.org/download/) engine (local executable)

```bash
pip install pygame python-chess
```

> Windows users: download the Stockfish zip, extract, and note the path to the `.exe`.

---

## 🗂️ Project Structure
```
project/
├─ images/
│  ├─ white_pawn.png  white_rook.png  white_knight.png  white_bishop.png  white_queen.png  white_king.png
│  └─ black_pawn.png  black_rook.png  black_knight.png  black_bishop.png  black_queen.png  black_king.png
├─ chess_game.py
└─ README.md
```

Place all piece images under `images/` with the exact filenames used in `PIECE_IMAGES`.

---

## ⚙️ Configuration
All key settings live at the top of `chess_game.py`:

- **Window/Board:** `self.window_size = (1000, 800)`, `self.board_size = 700`
- **Colors:** `LIGHT_BROWN`, `DARK_BROWN`, button and popup colors
- **Images:** `PIECE_IMAGES` mapping (ensure file paths exist)
- **Engine path** (Windows example):
  ```py
  STOCKFISH_PATH = r"C:\\stockfish\\stockfish-windows-x86-64-avx2.exe"
  ```
  On macOS/Linux, set the path to your `stockfish` binary (e.g., `/usr/local/bin/stockfish`).

---

## 🚀 Run
```bash
python chess_game.py
```

---

## 🕹️ How to Play
1. **Start Game:** Click *Start Game* to (re)start the timers and reset the board.
2. **Pick Mode:** Click the *Game Mode* button to toggle **Human vs Human** / **Human vs AI**.
3. **Choose Time:** Click *Time: X* to open the dropdown and select a preset.
4. **Move Pieces:** Left-click and drag a piece; only legal moves are accepted.  
   - In **Human vs AI**, the AI plays **Black** and moves automatically after you.
5. **Resign / Draw:** Buttons show a popup and stop the game.
6. **New Game:** Full reset of state and UI.

---

## 📸 Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/6f9ed39d-9e12-4669-b1a1-c8a6ee3d7fe2" alt="Board view" width="45%">
  <img src="https://github.com/user-attachments/assets/920c5553-2317-40b4-8894-936a9b4de5c9" alt="AIvsHuman" width="45%">
  <img src="https://github.com/user-attachments/assets/55ae51c1-6c17-4a97-a695-e0e4cac32f4c" alt="Resign" width="45%">
  <img src="https://github.com/user-attachments/assets/f8c112c6-20a7-4414-975e-45330f94c188" alt="time controls" width="45%">
</p>

- **Left:** Board view with drag-and-drop pieces  
- **Right:** Control panel (Start/Resign/Draw/New Game, Game Mode, Time)

> Tip: On macOS use `Shift`+`Cmd`+`4`, on Windows use `Win`+`Shift`+`S` to grab clean crops.

---

## 🧠 Implementation Notes
- **Rules/Legality:** `python-chess` enforces legal moves and board state.
- **AI:** `chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)` then `engine.play(board, Limit(time=2.0))` for a quick move.
- **Timers:** Simple per-side countdown updated on each frame while the side is to move.
- **UI Layout:** 8×8 board (derived `grid_size` from `board_size`), plus a right-side panel for controls.

---

## 🔧 Common Issues & Fixes
- **Image load error:** Check `images/` filenames and relative paths used in `PIECE_IMAGES`.
- **Stockfish not found:** Verify `STOCKFISH_PATH`; ensure the binary is executable on macOS/Linux (`chmod +x`).
- **No AI move:** The engine starts on demand; confirm `STOCKFISH_PATH` is valid and `python-chess` is installed.
- **Fonts or window issues:** Ensure SDL dependencies are present (usually handled by `pygame` install).

---

## 🗺️ Roadmap (Nice-to-Have)
- Add true **increment** (e.g., +2s) per move.
- Detect **checkmate/stalemate** and show result automatically.
- Highlight legal moves and last move.
- Sound effects and move list (PGN export).
- Difficulty control (depth/time) for the AI.

---

## 📜 License
MIT — use it freely.

---

## 🙌 Credits
- [python-chess](https://python-chess.readthedocs.io/)
- [Stockfish](https://stockfishchess.org/)
- Pygame for the rendering
