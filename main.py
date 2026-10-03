import tkinter as tk
from tkinter import messagebox

ROWS = 6
COLS = 7
CELL_SIZE = 80
CONNECT = 4

EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2


class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four")
        self.root.resizable(False, False)

        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = PLAYER_ONE
        self.game_over = False

        self.status = tk.Label(
            root,
            text="Player 1's turn",
            font=("Arial", 16, "bold"),
            pady=10
        )
        self.status.pack()

        self.canvas = tk.Canvas(
            root,
            width=COLS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            bg="#1769aa",
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.handle_click)

        self.reset_button = tk.Button(
            root,
            text="New Game",
            font=("Arial", 12, "bold"),
            command=self.reset_game,
            padx=15,
            pady=6
        )
        self.reset_button.pack(pady=(0, 15))

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")

        colors = {
            EMPTY: "#f5f5f5",
            PLAYER_ONE: "#e53935",
            PLAYER_TWO: "#fdd835"
        }

        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * CELL_SIZE + 8
                y1 = row * CELL_SIZE + 8
                x2 = (col + 1) * CELL_SIZE - 8
                y2 = (row + 1) * CELL_SIZE - 8

                self.canvas.create_oval(
                    x1, y1, x2, y2,
                    fill=colors[self.board[row][col]],
                    outline=""
                )

    def handle_click(self, event):
        if self.game_over:
            return

        col = event.x // CELL_SIZE

        if not 0 <= col < COLS:
            return

        row = self.get_available_row(col)

        if row is None:
            self.status.config(text="That column is full. Choose another column.")
            return

        self.board[row][col] = self.current_player
        self.draw_board()

        if self.check_winner(row, col):
            self.game_over = True
            self.status.config(text=f"Player {self.current_player} wins!")
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            return

        if self.is_draw():
            self.game_over = True
            self.status.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            return

        self.current_player = (
            PLAYER_TWO if self.current_player == PLAYER_ONE else PLAYER_ONE
        )
        self.status.config(text=f"Player {self.current_player}'s turn")

    def get_available_row(self, col):
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == EMPTY:
                return row
        return None

    def check_winner(self, row, col):
        player = self.board[row][col]

        directions = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal down-right
            (1, -1)   # diagonal down-left
        ]

        for dr, dc in directions:
            count = 1
            count += self.count_direction(row, col, dr, dc, player)
            count += self.count_direction(row, col, -dr, -dc, player)

            if count >= CONNECT:
                return True

        return False

    def count_direction(self, row, col, dr, dc, player):
        count = 0
        r, c = row + dr, col + dc

        while (
            0 <= r < ROWS
            and 0 <= c < COLS
            and self.board[r][c] == player
        ):
            count += 1
            r += dr
            c += dc

        return count

    def is_draw(self):
        return all(self.board[0][col] != EMPTY for col in range(COLS))

    def reset_game(self):
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = PLAYER_ONE
        self.game_over = False
        self.status.config(text="Player 1's turn")
        self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()
    ConnectFour(root)
    root.mainloop()
