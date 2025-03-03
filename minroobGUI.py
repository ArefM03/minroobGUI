import tkinter as tk
from tkinter import messagebox
import random

ROWS = 8
COLS = 7
TOTAL_MINES = 15
WIN_THRESHOLD = 8

class MinesweeperGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.master.configure(bg="#34495E")
        
        self.players = [{"name": "Player 1", "color": "#E74C3C", "score": 0},
                        {"name": "Player 2", "color": "#3498DB", "score": 0}]
        self.current_player = 0
        self.revealed = set()
        self.mines_found = {"#E74C3C": set(), "#3498DB": set()}
        
        self.board, self.mines = self.create_board()
        self.buttons = []
        self.create_widgets()
        self.update_status()

    def create_board(self):
        all_cells = [(r, c) for r in range(ROWS) for c in range(COLS)]
        mines = random.sample(all_cells, TOTAL_MINES)
        board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        for r, c in mines:
            board[r][c] = 'M'
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] != 'M':
                    count = sum((nr, nc) in mines for nr, nc in self.get_neighbors(r, c))
                    board[r][c] = count
        return board, mines

    def create_widgets(self):
        self.status_label = tk.Label(self.master, text="", font=("Arial", 14, "bold"), fg="white", bg="#34495E")
        self.status_label.pack(pady=10)
        
        self.frame = tk.Frame(self.master, bg="#34495E")
        self.frame.pack()
        
        for r in range(ROWS):
            row_buttons = []
            for c in range(COLS):
                btn = tk.Button(self.frame, width=5, height=2, font=("Arial", 14, "bold"),
                                bg="#BDC3C7", fg="black", relief=tk.RAISED,
                                command=lambda r=r, c=c: self.reveal_cell(r, c))
                btn.grid(row=r, column=c, padx=3, pady=3)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def update_status(self):
        player = self.players[self.current_player]
        player1_score = self.players[0]['score']
        player2_score = self.players[1]['score']
        self.status_label.config(text=f"{player['name']}'s Turn (Score: {player['score']}) | Player 1: {player1_score} | Player 2: {player2_score}", fg=player['color'])

    def reveal_cell(self, r, c):
        if (r, c) in self.revealed:
            return
        self.revealed.add((r, c))
        
        if self.board[r][c] == 'M':
            player = self.players[self.current_player]
            player['score'] += 1
            self.mines_found[player['color']].add((r, c))
            self.buttons[r][c].config(text="💣", bg=player['color'], fg="white")
            
            if player['score'] >= WIN_THRESHOLD:
                messagebox.showinfo("Game Over", f"{player['name']} wins!")
                self.master.quit()
        else:
            self.buttons[r][c].config(text=str(self.board[r][c]), state="disabled", bg="#ECF0F1", relief=tk.SUNKEN)
            if self.board[r][c] == 0:
                for nr, nc in self.get_neighbors(r, c):
                    self.reveal_cell(nr, nc)
            self.current_player = 1 - self.current_player
        
        self.update_status()
        if len(self.mines_found['#E74C3C']) + len(self.mines_found['#3498DB']) == TOTAL_MINES:
            self.end_game()

    def get_neighbors(self, r, c):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [(r+dr, c+dc) for dr, dc in directions if 0 <= r+dr < ROWS and 0 <= c+dc < COLS]

    def end_game(self):
        scores = [p['score'] for p in self.players]
        winner = self.players[0]['name'] if scores[0] > scores[1] else self.players[1]['name'] if scores[1] > scores[0] else "It's a tie!"
        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = MinesweeperGUI(root)
    root.mainloop()
