import random

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        pass

class HumanPlayer(Player):
    def get_move(self, board):
        while True:
            try:
                row = int(input(f"Player {self.symbol}, enter your move row (0-2): "))
                col = int(input(f"Player {self.symbol}, enter your move column (0-2): "))
                if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == ' ':
                    return row, col
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 2.")

class ComputerPlayer(Player):
    def get_move(self, board):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
        return random.choice(empty_cells)

class TicTacToe:
    def __init__(self, player1, player2):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.players = [player1, player2]
        self.current_player = 0
        self.winner = None

    def print_board(self):
        for i, row in enumerate(self.board):
            if i != 0:
                print('-' * 5)  # 分割线
            print('|'.join(row))

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def make_move(self):
        row, col = self.players[self.current_player].get_move(self.board)
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' ':
            self.board[row][col] = self.players[self.current_player].symbol
            if self.check_winner(row, col):
                self.winner = self.players[self.current_player].symbol
            else:
                self.switch_player()
            return True
        else:
            return False

    def check_winner(self, row, col):
        player_symbol = self.players[self.current_player].symbol
        # Check horizontal, vertical, and both diagonals
        win = all(self.board[row][i] == player_symbol for i in range(3)) or \
              all(self.board[i][col] == player_symbol for i in range(3)) or \
              all(self.board[i][i] == player_symbol for i in range(3)) or \
              all(self.board[i][2 - i] == player_symbol for i in range(3))
        return win

    def is_draw(self):
        return all(self.board[row][col] != ' ' for row in range(3) for col in range(3)) and not self.winner

    def get_winner(self):
        return self.winner
