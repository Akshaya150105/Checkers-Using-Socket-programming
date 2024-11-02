from itertools import product

FIELD_WHITE = None
FIELD_BLACK = 0

PIECE_WHITE = 1
PIECE_BLACK = 2

PIECE_KING_WHITE = 3
PIECE_KING_BLACK = 4

PIECES_WHITE = [PIECE_WHITE, PIECE_KING_WHITE]
PIECES_BLACK = [PIECE_BLACK, PIECE_KING_BLACK]
PIECES_KING = [PIECE_KING_WHITE, PIECE_KING_BLACK]
PIECES = [PIECE_WHITE, PIECE_KING_WHITE, PIECE_BLACK, PIECE_KING_BLACK]

MIN_POS_BOARD = 0
MAX_POS_BOARD = 9

PLAYER_BLACK = 0
PLAYER_WHITE = 1
PLAYER_BLACK_WINNER = 2
PLAYER_WHITE_WINNER = 3

MSG_NO_PIECE = 'There are no piece in this position'
MSG_INVALID_MOVEMENT = 'Invalid moviment'
MSG_PIECE_BELONGS_OTHER_PLAYER = 'The piece to be moved belongs to the other player'
MSG_MOVE_TO_SAME_POS = 'You cannot move a piece to the same position'
MSG_PIECE_IN_TARGET_POS = 'There are a piece in the target position'
MSG_WRONG_DIRECTION = 'You are walking in the wrong direction'
MSG_ONLY_ONE_FIELD_PER_ROUND = 'Only one field can be advanced per round'
MSG_COMPULSORY_CAPTURE = 'Piece capture is required'

class CheckersGame():

    def __init__(self):
        self.init_board_with_pieces()

    def init_board(self):
        self.board = [
            self.generate_row_start_field_black(),
            self.generate_row_start_field_white(),
            self.generate_row_start_field_black(),
            self.generate_row_start_field_white(),
            self.generate_row_start_field_black(),
            self.generate_row_start_field_white(),
            self.generate_row_start_field_black(),
            self.generate_row_start_field_white(),
            self.generate_row_start_field_black(),
            self.generate_row_start_field_white()
        ]

    def init_board_with_pieces(self):
        self.board = [
            self.generate_row_start_piece_white(),
            self.generate_row_start_field_white_piece_white(),
            self.generate_row_start_piece_white(),
            self.generate_row_start_field_white_piece_white(),
            self.generate_row_start_field_black(),
            self.generate_row_start_field_white(),
            self.generate_row_start_piece_black(),
            self.generate_row_start_field_white_piece_black(),
            self.generate_row_start_piece_black(),
            self.generate_row_start_field_white_piece_black()
        ]

    def generate_row_start_field_black(self):
        return [FIELD_BLACK, FIELD_WHITE, FIELD_BLACK, FIELD_WHITE, FIELD_BLACK, FIELD_WHITE, FIELD_BLACK, FIELD_WHITE, FIELD_BLACK, FIELD_WHITE]

    def generate_row_start_field_white(self):
        return [FIELD_WHITE, FIELD_BLACK, FIELD_WHITE, FIELD_BLACK, FIELD_WHITE, FIELD_BLACK, FIELD_WHITE, FIELD_BLACK, FIELD_WHITE, FIELD_BLACK]

    def generate_row_start_piece_black(self):
        return [PIECE_BLACK, FIELD_WHITE, PIECE_BLACK, FIELD_WHITE, PIECE_BLACK, FIELD_WHITE, PIECE_BLACK, FIELD_WHITE, PIECE_BLACK, FIELD_WHITE]

    def generate_row_start_piece_white(self):
        return [PIECE_WHITE, FIELD_WHITE, PIECE_WHITE, FIELD_WHITE, PIECE_WHITE, FIELD_WHITE, PIECE_WHITE, FIELD_WHITE, PIECE_WHITE, FIELD_WHITE]

    def generate_row_start_field_white_piece_black(self):
        return [FIELD_WHITE, PIECE_BLACK, FIELD_WHITE, PIECE_BLACK, FIELD_WHITE, PIECE_BLACK, FIELD_WHITE, PIECE_BLACK, FIELD_WHITE, PIECE_BLACK]

    def generate_row_start_field_white_piece_white(self):
        return [FIELD_WHITE, PIECE_WHITE, FIELD_WHITE, PIECE_WHITE, FIELD_WHITE, PIECE_WHITE, FIELD_WHITE, PIECE_WHITE, FIELD_WHITE, PIECE_WHITE]

    def move(self, player, from_x, from_y, to_x, to_y):
        x_walk_diff = from_x - to_x
        y_walk_diff = from_y - to_y
        self.validate_move(player, from_x, from_y, to_x, to_y, x_walk_diff, y_walk_diff)

        turn = None
        pieces_enemies = PIECES_BLACK if player == PLAYER_WHITE else PIECES_WHITE
        piece = self.capture(from_x, from_y, x_walk_diff, y_walk_diff, pieces_enemies)
        if piece != None:
            turn = player
            self.kill(piece[0], piece[1])

        self.board[to_x][to_y] = self.board[from_x][from_y]
        self.board[from_x][from_y] = FIELD_BLACK

        if self.board[to_x][to_y] == PIECE_WHITE and to_x == MAX_POS_BOARD:
            self.make_king(to_x, to_y, PIECE_KING_WHITE)
        elif self.board[to_x][to_y] == PIECE_BLACK and to_x == MIN_POS_BOARD:
            self.make_king(to_x, to_y, PIECE_KING_BLACK)

        if turn == None:
            if player == PLAYER_WHITE:
                turn = PLAYER_BLACK
            else:
                turn = PLAYER_WHITE

        if self.is_winner(player):
            turn = player + 2

        return turn

    def kill(self, x, y):
        self.board[x][y] = FIELD_BLACK

    def make_king(self, x, y, king):
        self.board[x][y] = king

    def validate_move(self, player, from_x, from_y, to_x, to_y, x_walk_diff, y_walk_diff):
        if not self.is_within_board(from_x, from_y) or not self.has_piece(from_x, from_y):
            raise InvalidMovimentException(MSG_NO_PIECE)

        if not self.is_within_board(to_x, to_y) or self.is_field_white(to_x, to_y):
            raise InvalidMovimentException(MSG_INVALID_MOVEMENT)

        if player == PLAYER_BLACK and self.is_pieces_white(from_x, from_y) or player == PLAYER_WHITE and self.is_pieces_black(from_x, from_y):
            raise InvalidMovimentException(MSG_PIECE_BELONGS_OTHER_PLAYER)

        if from_x == to_x and from_y == to_y:
            raise InvalidMovimentException(MSG_MOVE_TO_SAME_POS)

        if self.has_piece(to_x, to_y):
            raise InvalidMovimentException(MSG_PIECE_IN_TARGET_POS)

        piece_white_incorrect_direction = self.is_piece_white(from_x, from_y) and x_walk_diff >= 0
        piece_black_incorrect_direction = self.is_piece_black(from_x, from_y) and x_walk_diff <= 0
        pieces_enemies = PIECES_BLACK if player == PLAYER_WHITE else PIECES_WHITE
        if piece_white_incorrect_direction or piece_black_incorrect_direction or x_walk_diff == 0 or y_walk_diff == 0:
            raise InvalidMovimentException(MSG_WRONG_DIRECTION)
        elif self.capture(from_x, from_y, x_walk_diff, y_walk_diff, pieces_enemies) == None:
            if abs(x_walk_diff) > 1 or abs(y_walk_diff) > 1:
                raise InvalidMovimentException(MSG_ONLY_ONE_FIELD_PER_ROUND)

            self.validate_compulsory_capture(player)

    def validate_compulsory_capture(self, player):
        r = range(MIN_POS_BOARD, MAX_POS_BOARD + 1)
        for (x, y) in product(r, r):
            if player == PLAYER_WHITE and self.is_pieces_white(x, y):
                self.check_neighbors_compulsory_capture(x, y, 1, PIECE_KING_WHITE, PIECES_BLACK)
            elif player == PLAYER_BLACK and self.is_pieces_black(x, y):
                self.check_neighbors_compulsory_capture(x, y, -1, PIECE_KING_BLACK, PIECES_WHITE)

    def capture(self, from_x, from_y, x_walk_diff, y_walk_diff, pieces_enemies):
        if abs(x_walk_diff) == 2 and abs(y_walk_diff) == 2:
            x = from_x - x_walk_diff / 2
            y = from_y - y_walk_diff / 2
            enemy_pos = (int(x), int(y))
            valid_div = x % 1 == 0 and y % 1 == 0
            if valid_div and self.is_within_board(enemy_pos[0], enemy_pos[1]) and self.board[enemy_pos[0]][enemy_pos[1]] in pieces_enemies:
                return enemy_pos

        return None

    def check_neighbors_compulsory_capture(self, x, y, direction, piece_king, pieces_enemies):
        direction_2x = direction * 2

        x_pos = x + direction
        y_pos = y + direction
        x_pos_2x = x + direction_2x
        y_pos_2x = y + direction_2x
        if self.can_capture_neighbor(x_pos_2x, y_pos_2x, x_pos, y_pos, pieces_enemies):
            raise CompulsoryCaptureException(MSG_COMPULSORY_CAPTURE)

        y_pos = y - direction
        y_pos_2x = y - direction_2x
        if self.can_capture_neighbor(x_pos_2x, y_pos_2x, x_pos, y_pos, pieces_enemies):
            raise CompulsoryCaptureException(MSG_COMPULSORY_CAPTURE)

        if self.board[x][y] == piece_king:
            x_pos = x - direction
            x_pos_2x = x - direction_2x
            if self.can_capture_neighbor(x_pos_2x, y_pos_2x, x_pos, y_pos, pieces_enemies):
                raise CompulsoryCaptureException(MSG_COMPULSORY_CAPTURE)

            y_pos = y + direction
            y_pos_2x = y + direction_2x
            if self.can_capture_neighbor(x_pos_2x, y_pos_2x, x_pos, y_pos, pieces_enemies):
                raise CompulsoryCaptureException(MSG_COMPULSORY_CAPTURE)

    def has_piece(self, x, y):
        return self.is_pos(x, y, PIECES)

    def is_pos(self, x, y, pos_type):
        return self.board[x][y] in pos_type

    def is_piece_white(self, x, y):
        return self.board[x][y] == PIECE_WHITE

    def is_piece_black(self, x, y):
        return self.board[x][y] == PIECE_BLACK

    def is_pieces_white(self, x, y):
        return self.is_pos(x, y, PIECES_WHITE)

    def is_pieces_black(self, x, y):
        return self.is_pos(x, y, PIECES_BLACK)

    def is_field_white(self, x, y):
        return self.board[x][y] == FIELD_WHITE

    def is_within_board(self, x, y):
        return x <= MAX_POS_BOARD and y <= MAX_POS_BOARD and x >= MIN_POS_BOARD and y >= MIN_POS_BOARD

    def is_winner(self, player):
        pieces_enemies = PIECES_BLACK if player == PLAYER_WHITE else PIECES_WHITE

        count = 0
        r = range(MIN_POS_BOARD, MAX_POS_BOARD + 1)
        for (x, y) in product(r, r):
            if self.board[x][y] in pieces_enemies:
                count += 1

        return count == 0

    def can_capture_neighbor(self, to_x, to_y, target_x, target_y, pieces_enemies):
        return self.is_within_board(to_x, to_y) and self.board[target_x][target_y] in pieces_enemies and not self.has_piece(to_x, to_y)

class CheckersGameException(Exception):
    pass

class InvalidMovimentException(CheckersGameException):
    pass

class CompulsoryCaptureException(CheckersGameException):
    pass