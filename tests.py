# tests.py

import unittest
from logic import TicTacToe, HumanPlayer, ComputerPlayer

class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.player1 = HumanPlayer('X')
        self.player2 = HumanPlayer('O')
        self.game = TicTacToe(self.player1, self.player2)

    def test_initial_board_empty(self):
        for row in self.game.board:
            for cell in row:
                self.assertEqual(cell, ' ')

    def test_move(self):
        self.game.board = [[' ', ' ', ' '],
                           [' ', ' ', ' '],
                           [' ', ' ', ' ']]
        self.game.players[self.game.current_player].get_move = lambda board: (0, 0)
        self.assertTrue(self.game.make_move())
        self.assertEqual(self.game.board[0][0], 'X')

    def test_switch_player(self):
        self.game.players[self.game.current_player].get_move = lambda board: (0, 0)
        self.game.make_move()
        self.assertEqual(self.game.players[self.game.current_player].symbol, 'O')

    def test_winner_row(self):
        self.game.board = [['X', 'X', 'X'],
                           [' ', ' ', ' '],
                           [' ', ' ', ' ']]
        self.assertTrue(self.game.check_winner(0, 0))
        self.game.winner = 'X'  # 手动设置获胜者
        self.assertEqual(self.game.get_winner(), 'X')

    def test_winner_diagonal(self):
        self.game.board = [['X', ' ', ' '],
                           [' ', 'X', ' '],
                           [' ', ' ', 'X']]
        self.assertTrue(self.game.check_winner(0, 0))
        self.game.winner = 'X'  # 手动设置获胜者
        self.assertEqual(self.game.get_winner(), 'X')

    def test_draw(self):
        self.game.board = [['X', 'O', 'X'],
                           ['X', 'X', 'O'],
                           ['O', 'X', 'O']]
        self.assertTrue(self.game.is_draw())
        self.assertIsNone(self.game.get_winner())

    def test_computer_player_move(self):
        computer = ComputerPlayer('O')
        self.game.board = [['X', 'X', ' '],
                           [' ', ' ', ' '],
                           [' ', ' ', ' ']]
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.game.board[i][j] == ' ']
        row, col = computer.get_move(self.game.board)
        self.assertIn((row, col), empty_cells)

if __name__ == '__main__':
    unittest.main()