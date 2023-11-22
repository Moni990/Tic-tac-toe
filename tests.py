import unittest
from unittest.mock import patch
from logic import TicTacToe, HumanPlayer, ComputerPlayer

class TestTicTacToe(unittest.TestCase):
    
    def setUp(self):
        self.player1 = HumanPlayer('X')
        self.player2 = HumanPlayer('O')
        self.game = TicTacToe(self.player1, self.player2)

    def test_init(self):
        self.assertEqual(self.game.board, [[' ' for _ in range(3)] for _ in range(3)])
        self.assertIs(self.game.players[0], self.player1)
        self.assertIs(self.game.players[1], self.player2)
        self.assertEqual(self.game.current_player, 0)
        self.assertIsNone(self.game.winner)

    def test_switch_player(self):
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 1)

    # Other tests for make_move, check_winner, etc.

class TestHumanPlayer(unittest.TestCase):
    
    def setUp(self):
        self.player = HumanPlayer('X')

    # Mock input for get_move
    @patch('builtins.input', side_effect=['0', '0'])
    def test_get_move(self, mock_input):
        self.assertEqual(self.player.get_move([[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]), (0, 0))

    # Other tests for invalid inputs, etc.

class TestComputerPlayer(unittest.TestCase):
    
    def setUp(self):
        self.player = ComputerPlayer('O')

    def test_get_move(self):
        board = [['X', 'X', 'O'], ['O', 'X', 'X'], ['X', 'O', ' ']]
        move = self.player.get_move(board)
        self.assertIn(move, [(2, 2)])

if __name__ == '__main__':
    unittest.main()
