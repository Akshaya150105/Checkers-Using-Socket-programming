from checkers_game import *
import unittest
import logging

class CheckersGameTest(unittest.TestCase):

    def setUp(self):
        self.game = CheckersGame()

    def test_validate_move_no_piece(self):
        self.assertInvalidMovimentException(MSG_NO_PIECE, PLAYER_BLACK, 1, 0, 0, 0)
        self.assertInvalidMovimentException(MSG_NO_PIECE, PLAYER_BLACK, MAX_POS_BOARD + 1, 0, 0, 0)
        self.assertInvalidMovimentException(MSG_NO_PIECE, PLAYER_BLACK, 0, -1, 0, 0)
        self.assertInvalidMovimentException(MSG_NO_PIECE, PLAYER_BLACK, 0, MAX_POS_BOARD + 1, 0, 0)
        self.assertInvalidMovimentException(MSG_NO_PIECE, PLAYER_BLACK, 0, 1, 0, 0)
        self.assertInvalidMovimentException(MSG_NO_PIECE, PLAYER_BLACK, 4, 0, 0, 0)

    def test_validate_move_invalid_moviment(self):
        self.assertInvalidMovimentException(MSG_INVALID_MOVEMENT, PLAYER_BLACK, 0, 0, -1, 0)
        self.assertInvalidMovimentException(MSG_INVALID_MOVEMENT, PLAYER_BLACK, 0, 0, MAX_POS_BOARD + 1, 0)
        self.assertInvalidMovimentException(MSG_INVALID_MOVEMENT, PLAYER_BLACK, 0, 0, 0, -1)
        self.assertInvalidMovimentException(MSG_INVALID_MOVEMENT, PLAYER_BLACK, 0, 0, 0, MAX_POS_BOARD + 1)
        self.assertInvalidMovimentException(MSG_INVALID_MOVEMENT, PLAYER_BLACK, 0, 0, 0, 1)

    def test_validate_move_piece_belongs_other_player(self):
        self.assertInvalidMovimentException(MSG_PIECE_BELONGS_OTHER_PLAYER, PLAYER_BLACK, 0, 2, 0, 0)
        self.assertInvalidMovimentException(MSG_PIECE_BELONGS_OTHER_PLAYER, PLAYER_WHITE, 6, 0, 0, 0)

        self.game.init_board()
        self.game.board[0][2] = PIECE_KING_WHITE
        self.assertInvalidMovimentException(MSG_PIECE_BELONGS_OTHER_PLAYER, PLAYER_BLACK, 0, 2, 0, 0)

        self.game.board[5][1] = PIECE_KING_BLACK
        self.assertInvalidMovimentException(MSG_PIECE_BELONGS_OTHER_PLAYER, PLAYER_WHITE, 5, 1, 0, 0)

    def test_validate_move_move_to_same_pos(self):
        self.assertInvalidMovimentException(MSG_MOVE_TO_SAME_POS, PLAYER_WHITE, 0, 0, 0, 0)

    def test_validate_move_piece_in_target_pos(self):
        self.game.init_board()
        self.game.board[3][3] = PIECE_WHITE
        self.game.board[4][4] = PIECE_BLACK
        self.assertInvalidMovimentException(MSG_PIECE_IN_TARGET_POS, PLAYER_WHITE, 3, 3, 4, 4)

    def test_validate_move_wrong_direction(self):
        self.game.init_board()

        self.game.board[2][0] = PIECE_WHITE
        self.assertInvalidMovimentException(MSG_WRONG_DIRECTION, PLAYER_WHITE, 2, 0, 1, 1)
        self.assertInvalidMovimentException(MSG_WRONG_DIRECTION, PLAYER_WHITE, 2, 0, 2, 2)

        self.game.board[6][0] = PIECE_BLACK
        self.assertInvalidMovimentException(MSG_WRONG_DIRECTION, PLAYER_BLACK, 6, 0, 7, 1)
        self.assertInvalidMovimentException(MSG_WRONG_DIRECTION, PLAYER_BLACK, 6, 0, 6, 2)

        self.game.board[2][0] = PIECE_KING_WHITE
        self.assertInvalidMovimentException(MSG_WRONG_DIRECTION, PLAYER_WHITE, 2, 0, 2, 2)

        self.game.board[6][0] = PIECE_BLACK
        self.assertInvalidMovimentException(MSG_WRONG_DIRECTION, PLAYER_BLACK, 6, 0, 6, 2)

    def test_validate_move_only_one_field_per_round(self):
        self.game.init_board()

        self.game.board[2][0] = PIECE_WHITE
        self.assertInvalidMovimentException(MSG_ONLY_ONE_FIELD_PER_ROUND, PLAYER_WHITE, 2, 0, 4, 2)

        self.game.board[6][0] = PIECE_BLACK
        self.assertInvalidMovimentException(MSG_ONLY_ONE_FIELD_PER_ROUND, PLAYER_BLACK, 6, 0, 4, 2)

        self.game.board[2][0] = PIECE_KING_WHITE
        self.assertInvalidMovimentException(MSG_ONLY_ONE_FIELD_PER_ROUND, PLAYER_WHITE, 2, 0, 4, 2)

        self.game.board[6][0] = PIECE_KING_BLACK
        self.assertInvalidMovimentException(MSG_ONLY_ONE_FIELD_PER_ROUND, PLAYER_BLACK, 6, 0, 4, 2)

        self.game.init_board()
        self.game.board[2][0] = PIECE_WHITE
        self.assertInvalidMovimentException(MSG_ONLY_ONE_FIELD_PER_ROUND, PLAYER_WHITE, 2, 0, 3, 3)

        self.game.board[6][0] = PIECE_BLACK
        self.assertInvalidMovimentException(MSG_ONLY_ONE_FIELD_PER_ROUND, PLAYER_BLACK, 6, 0, 5, 3)

        self.game.board[2][0] = PIECE_KING_WHITE
        self.assertInvalidMovimentException(MSG_ONLY_ONE_FIELD_PER_ROUND, PLAYER_WHITE, 2, 0, 3, 3)

        self.game.board[6][0] = PIECE_KING_BLACK
        self.assertInvalidMovimentException(MSG_ONLY_ONE_FIELD_PER_ROUND, PLAYER_BLACK, 6, 0, 5, 3)

    def test_validate_compulsory_capture_player_white(self):
        self.game.init_board()
        self.game.board[0][0] = PIECE_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 0, 0, PIECE_WHITE)

        self.game.init_board()
        self.game.board[1][7] = PIECE_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 1, 7, PIECE_WHITE)

        self.game.init_board()
        self.game.board[1][1] = PIECE_KING_WHITE
        self.game.board[0][0] = PIECE_KING_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 1, 1, PIECE_KING_WHITE)

        self.game.init_board()
        self.game.board[2][MAX_POS_BOARD -1] = PIECE_KING_WHITE
        self.game.board[1][MAX_POS_BOARD] = PIECE_KING_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 2, MAX_POS_BOARD -1, PIECE_KING_WHITE)

        self.game.init_board()
        self.game.board[MAX_POS_BOARD -1][2] = PIECE_WHITE
        self.game.board[MAX_POS_BOARD][3] = PIECE_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, MAX_POS_BOARD -1, 2, PIECE_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_WHITE
        self.game.board[2][2] = PIECE_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 3, 3, PIECE_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_WHITE
        self.game.board[2][4] = PIECE_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 3, 3, PIECE_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_WHITE
        self.game.board[4][2] = PIECE_BLACK
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_WHITE
        self.game.board[4][4] = PIECE_BLACK
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_KING_WHITE
        self.game.board[2][2] = PIECE_BLACK
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_KING_WHITE
        self.game.board[2][4] = PIECE_BLACK
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_KING_WHITE
        self.game.board[4][2] = PIECE_BLACK
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_KING_WHITE
        self.game.board[4][4] = PIECE_BLACK
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_WHITE
        self.game.board[4][2] = PIECE_BLACK
        self.game.board[5][1] = PIECE_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 3, 3, PIECE_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_WHITE
        self.game.board[4][4] = PIECE_BLACK
        self.game.board[5][5] = PIECE_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 3, 3, PIECE_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_KING_WHITE
        self.game.board[2][2] = PIECE_BLACK
        self.game.board[1][1] = PIECE_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 3, 3, PIECE_KING_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_KING_WHITE
        self.game.board[2][4] = PIECE_BLACK
        self.game.board[1][5] = PIECE_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 3, 3, PIECE_KING_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_KING_WHITE
        self.game.board[4][2] = PIECE_BLACK
        self.game.board[5][1] = PIECE_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 3, 3, PIECE_KING_WHITE)

        self.game.init_board()
        self.game.board[3][3] = PIECE_KING_WHITE
        self.game.board[4][4] = PIECE_BLACK
        self.game.board[5][5] = PIECE_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_WHITE, 3, 3, PIECE_KING_WHITE)

    def test_validate_compulsory_capture_player_balck(self):
        self.game.init_board()
        self.game.board[7][7] = PIECE_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 7, 7, PIECE_BLACK)

        self.game.init_board()
        self.game.board[6][0] = PIECE_BLACK
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 6, 0, PIECE_BLACK)

        self.game.init_board()
        self.game.board[MAX_POS_BOARD -1][MAX_POS_BOARD -1] = PIECE_KING_BLACK
        self.game.board[MAX_POS_BOARD][MAX_POS_BOARD] = PIECE_KING_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, MAX_POS_BOARD -1, MAX_POS_BOARD -1, PIECE_KING_BLACK)

        self.game.init_board()
        self.game.board[5][1] = PIECE_KING_BLACK
        self.game.board[6][0] = PIECE_KING_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 5, 1, PIECE_KING_BLACK)

        self.game.init_board()
        self.game.board[1][3] = PIECE_BLACK
        self.game.board[0][4] = PIECE_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 1, 3, PIECE_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_BLACK
        self.game.board[5][3] = PIECE_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 4, 4, PIECE_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_BLACK
        self.game.board[5][5] = PIECE_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 4, 4, PIECE_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_BLACK
        self.game.board[3][3] = PIECE_WHITE
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_BLACK
        self.game.board[3][5] = PIECE_WHITE
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_KING_BLACK
        self.game.board[5][3] = PIECE_WHITE
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_KING_BLACK
        self.game.board[5][5] = PIECE_WHITE
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_KING_BLACK
        self.game.board[3][3] = PIECE_WHITE
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_KING_BLACK
        self.game.board[3][5] = PIECE_WHITE
        self.assertCompulsoryCaptureException(MSG_COMPULSORY_CAPTURE, PLAYER_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_BLACK
        self.game.board[5][5] = PIECE_WHITE
        self.game.board[6][6] = PIECE_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 4, 4, PIECE_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_BLACK
        self.game.board[5][3] = PIECE_WHITE
        self.game.board[6][2] = PIECE_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 4, 4, PIECE_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_BLACK
        self.game.board[3][3] = PIECE_WHITE
        self.game.board[2][2] = PIECE_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 4, 4, PIECE_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_BLACK
        self.game.board[3][5] = PIECE_WHITE
        self.game.board[2][6] = PIECE_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 4, 4, PIECE_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_KING_BLACK
        self.game.board[5][3] = PIECE_WHITE
        self.game.board[6][2] = PIECE_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 4, 4, PIECE_KING_BLACK)

        self.game.init_board()
        self.game.board[4][4] = PIECE_KING_BLACK
        self.game.board[5][5] = PIECE_WHITE
        self.game.board[6][6] = PIECE_WHITE
        self.assertNoCompulsoryCaptureException(PLAYER_BLACK, 4, 4, PIECE_KING_BLACK)

    def assertInvalidMovimentException(self, expected_msg, player, from_x, from_y, to_x, to_y):
        with self.assertRaises(InvalidMovimentException) as context:
            x_walk_diff = from_x - to_x
            y_walk_diff = from_y - to_y
            self.game.validate_move(player, from_x, from_y, to_x, to_y, x_walk_diff, y_walk_diff)

        self.assertTrue(expected_msg in str(context.exception))

    def assertCompulsoryCaptureException(self, expected_msg, player):
        with self.assertRaises(CompulsoryCaptureException) as context:
            self.game.validate_compulsory_capture(player)

        self.assertTrue(expected_msg in str(context.exception))

    def assertNoCompulsoryCaptureException(self, player, x, y, expected_piece):
        self.game.validate_compulsory_capture(player)
        self.assertEqual(self.game.board[x][y], expected_piece)
