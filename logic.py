# logic.py

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            if self.check_winner(row, col):
                self.winner = self.current_player
            else:
                self.switch_player()
            return True
        else:
            return False

    def check_winner(self, row, col):
        # Check horizontal, vertical, and both diagonals
        win = all(self.board[row][i] == self.current_player for i in range(3)) or \
              all(self.board[i][col] == self.current_player for i in range(3)) or \
              all(self.board[i][i] == self.current_player for i in range(3)) or \
              all(self.board[i][2 - i] == self.current_player for i in range(3))
        return win

    def is_draw(self):
        return all(self.board[row][col] != ' ' for row in range(3) for col in range(3)) and not self.winner

    def get_current_player(self):
        return self.current_player

    def get_winner(self):
        return self.winner





