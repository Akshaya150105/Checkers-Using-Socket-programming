from tkinter import Tk, Canvas, messagebox
from itertools import product
from json_socket import *
from checkers_game import (
    PIECE_KING_WHITE,
    PIECE_KING_BLACK,
    PIECE_WHITE,
    PIECE_BLACK,
    FIELD_WHITE,
    MIN_POS_BOARD,
    MAX_POS_BOARD
)
import logging
import sys

from server import Server


class Board(Tk):
    def __init__(self, width, height, cellsize, address=BIND_ADDRESS, port=BIND_PORT):
        Tk.__init__(self)
        self.cellsize = cellsize
        self.width = width
        self.height = height
        self.canvas = Canvas(self, width=width, height=height)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.pack()

        self.selected = None
        self.logic_board = [[0] * (MAX_POS_BOARD + 1) for _ in range(MAX_POS_BOARD + 1)]  # Initialize the board

        self.connection = JsonSocketClient(address, port)
        self.connection.on('connect_response', self.connect_response)
        self.connection.on('board_response', self.update_board)
        self.connection.on('move_response', self.update_board)
        self.connection.on('start_game', self.update_board)
        self.connection.on('reset_game', self.reset_game)
        self.connection.on('error', self.show_error)
        self.connection.on('show_winner', self.show_winner)

    def connect_response(self, color, _):
        self.title('Checkers - ' + ('BLACKS' if color == 0 else 'WHITES'))

    def start_game(self, logic_board, _):
        self.logic_board = logic_board
        self.update_board(logic_board)

    def reset_game(self, _=None):
        self.canvas.delete("all")
        self.canvas.create_text(self.width / 2, self.height / 2, text="Aguardando oponente...")
        self.logic_board = [[0] * (MAX_POS_BOARD + 1) for _ in range(MAX_POS_BOARD + 1)]  # Reset the board

    def update_board(self, logic_board, _):
        self.logic_board = logic_board
        self.draw_board()

    def show_error(self, error, _):
        messagebox.showinfo('Erro', error)

    def show_winner(self, msg, _):
        messagebox.showinfo('Winner', msg)

    def draw_board(self):
        self.canvas.delete('all')
        for i in range(MIN_POS_BOARD, MAX_POS_BOARD + 1):
            for j in range(MIN_POS_BOARD, MAX_POS_BOARD + 1):
                x1, y1 = (i * self.cellsize), (j * self.cellsize)
                x2, y2 = x1 + self.cellsize, y1 + self.cellsize
                cell = self.logic_board[i][j]
                color = '#f7d19c' if cell == FIELD_WHITE else '#694418'
                self.draw_rectangle(x1, y1, x2, y2, color)
                pawn_color = None
                if cell == PIECE_WHITE:
                    pawn_color = 'white'
                elif cell == PIECE_BLACK:
                    pawn_color = 'black'
                elif cell == PIECE_KING_WHITE:
                    pawn_color = '#c9c9c9'
                elif cell == PIECE_KING_BLACK:
                    pawn_color = '#c40404'

                if pawn_color:
                    self.draw_circle(x1, y1, x2, y2, pawn_color)

    def draw_rectangle(self, x1, y1, x2, y2, color):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def draw_circle(self, x1, y1, x2, y2, color):
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="black")

    def on_click(self, event):
        x = int(event.x / self.cellsize)
        y = int(event.y / self.cellsize)

        # Boundary check
        if 0 <= x < len(self.logic_board) and 0 <= y < len(self.logic_board[0]):
            cell_value = self.logic_board[x][y]
            if cell_value is not None:
                if self.selected is not None:
                    from_x, from_y = self.selected
                    self.selected = None
                    self.connection.call('move', [from_x, from_y, x, y])
                elif cell_value > 0:
                    self.selected = (x, y)
            else:
                print("Selected cell value is None")
        else:
            print("Click position is out of bounds")

    def run(self):
        self.title('Checkers')
        self.reset_game()
        self.connection.connect()
        self.mainloop()
        self.connection.call('leave', [])
        self.connection.call(SOCKET_CLOSE_HANDLE, [])

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    address = BIND_ADDRESS
    if len(sys.argv) > 1:
        address = sys.argv[1]

    port = BIND_PORT
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    board = Board(400, 400, 40, address=address, port=port)
    board.run()
