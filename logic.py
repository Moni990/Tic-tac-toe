# logic.py

import os
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

class Player:
    def __init__(self, symbol, player_type):
        self.symbol = symbol
        self.player_type = player_type  # 'human' or 'computer'

    def get_move(self, board):
        pass

class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol, 'human')

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
    def __init__(self, symbol):
        super().__init__(symbol, 'computer')

    def get_move(self, board):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
        return random.choice(empty_cells)

class TicTacToe:
    def __init__(self, player1, player2):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.players = [player1, player2]
        self.current_player = 0
        self.winner = None
        self.first_mover = None
        self.move_count = 0

    def print_board(self):
        for i, row in enumerate(self.board):
            if i != 0:
                print('-' * 5)
            print('|'.join(row))

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def make_move(self):
        if self.move_count == 0:
            self.first_mover = self.players[self.current_player].player_type

        row, col = self.players[self.current_player].get_move(self.board)

        if self.move_count == 0:
            self.first_move_position = 3 * row + col + 1  # 现在 row 和 col 已被赋值

        self.move_count += 1

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
        horizontal_win = all(self.board[row][i] == player_symbol for i in range(3))
        vertical_win = all(self.board[i][col] == player_symbol for i in range(3))
        diagonal_win1 = all(self.board[i][i] == player_symbol for i in range(3))
        diagonal_win2 = all(self.board[i][2 - i] == player_symbol for i in range(3))
        return horizontal_win or vertical_win or diagonal_win1 or diagonal_win2

    def is_draw(self):
        return all(cell != ' ' for row in self.board for cell in row) and not self.winner

    def get_winner(self):
        return self.winner

    def get_first_move_result(self):
        first_player_symbol = 'X'
        if self.check_winner(0, 0) or self.is_draw():
            if self.get_winner() == first_player_symbol:
                return 'Win'
            elif self.is_draw():
                return 'Draw'
            else:
                return 'Lose'
        else:
            return 'Inconclusive'

def log_game_result(is_single_player, player1_type, player2_type, winner, first_move_result, first_move_position):
    game_type = 'Single Player' if is_single_player else 'Multiplayer'
    winner_type = 'Human' if winner == 'X' or winner == 'O' else 'Computer' if winner else 'Draw'

    game_data = pd.DataFrame([{
        'Game Type': game_type,
        'Winner': winner,
        'Winner Type': winner_type,
        'First Move Result': first_move_result,
        'First Move Position': first_move_position,
    }])

    if not os.path.exists('logs'):
        os.makedirs('logs')

    file_path = 'logs/game.csv'
    if not os.path.exists(file_path):
        game_data.to_csv(file_path, index=False)
    else:
        df = pd.read_csv(file_path)
        df = pd.concat([df, game_data], ignore_index=True)
        df.to_csv(file_path, index=False)

def generate_winner_stats():
    if not os.path.exists('logs/game.csv'):
        print("No game history found.")
        return

    df = pd.read_csv('logs/game.csv')

    stats = {
        'X Win': len(df[(df['Winner'] == 'X') & (df['Winner Type'] == 'Human')]),
        'O Win': len(df[(df['Winner'] == 'O') & (df['Winner Type'] == 'Human')]),
        'Bot Win': len(df[df['Winner Type'] == 'Computer']),
        'X&O Draw': len(df[(df['Winner Type'] == 'Draw') & (df['Game Type'] == 'Multiplayer')]),
        'X&Bot Draw': len(df[(df['Winner Type'] == 'Draw') & (df['Game Type'] == 'Single Player')])
    }

    labels = list(stats.keys())
    counts = [stats[label] for label in labels]

    fig, ax = plt.subplots()
    ax.bar(labels, counts)
    ax.set_xlabel('Game Outcome')
    ax.set_ylabel('Number of Games')
    ax.set_title('Tic Tac Toe Game Outcomes')

    # Set the y-axis to display only integer scales
    ax.set_yticks(range(0, max(counts) + 1))

    # plt.show()
    plt.tight_layout()
    plt.savefig('game_outcome_stats.png')
    plt.close()

    return stats

def analyze_best_starting_position():
    if not os.path.exists('logs/game.csv'):
        print("No game history found.")
        return

    df = pd.read_csv('logs/game.csv')

    # Mapping locations to categories: corners, centers, edges
    position_mapping = {1: 'Corner', 2: 'Edge', 3: 'Corner', 4: 'Edge', 5: 'Center', 6: 'Edge', 7: 'Corner', 8: 'Edge', 9: 'Corner'}
    df['Position Category'] = df['First Move Position'].map(position_mapping)

    
    position_dummies = pd.get_dummies(df['Position Category'])
    df = df.join(position_dummies)

   
    for category in ['Corner', 'Center', 'Edge']:
        if category not in df.columns:
            df[category] = 0

    # build a model
    X = df[['Corner', 'Center', 'Edge']]
    y = df['Winner'].apply(lambda x: 1 if x == 'X' else 0) 

    model = LinearRegression()
    model.fit(X, y)

    
    print("Model coefficients (for Corner, Center, Edge):", model.coef_)
    print("Model intercept:", model.intercept_)

    
    positions = ['Corner', 'Center', 'Edge']
    for pos in positions:
        pos_data = pd.DataFrame(np.zeros((1, 3)), columns=['Corner', 'Center', 'Edge'])
        pos_data[pos] = 1
        win_probability = model.predict(pos_data)[0]
        print(f"Winning Probability from {pos}: {win_probability:.2f}")