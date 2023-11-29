# logic.py

import random
import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt

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

def log_game_result(winner, player1, player2, start_time):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    with open('logs/game.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # 确定获胜者类型
        if winner == player1.symbol and player1.player_type == 'human' or \
           winner == player2.symbol and player2.player_type == 'human':
            winner_type = 'Human'
        elif winner:
            winner_type = 'Computer'
        else:
            winner_type = 'Draw'

        # 写入记录
        writer.writerow([
            start_time, end_time, duration,
            player1.symbol, player1.player_type,
            player2.symbol, player2.player_type,
            winner, winner_type
        ])

def generate_winner_stats():
    if not os.path.exists('logs/game.csv'):
        print("No game history found.")
        return

    # 初始化统计字典
    stats = {
        'X Win': 0,
        'O Win': 0,
        'Bot Win': 0,
        'X&O Draw': 0,
        'X&Bot Draw': 0
    }

    with open('logs/game.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            winner = row[7]
            winner_type = row[8]
            player1_type = row[4]
            player2_type = row[6]

            if winner == 'X':
                if winner_type == 'Human':
                    stats['X Win'] += 1
                else:
                    stats['Bot Win'] += 1
            elif winner == 'O':
                if winner_type == 'Human':
                    stats['O Win'] += 1
                else:
                    stats['Bot Win'] += 1
            else:
                if player1_type == 'human' and player2_type == 'human':
                    stats['X&O Draw'] += 1
                elif player1_type == 'computer' or player2_type == 'computer':
                    stats['X&Bot Draw'] += 1

    print(stats)

    # 绘制统计图
    labels = list(stats.keys())
    counts = list(stats.values())

    # 确保所有计数都是整数
    counts = [int(count) for count in counts]

    fig, ax = plt.subplots(figsize=(10, 5))  # Using subplots for more control
    bars = ax.bar(labels, counts, color=['blue', 'orange', 'green', 'red', 'purple'])

    ax.set_xlabel('Game Outcome')
    ax.set_ylabel('Number of Games')
    ax.set_title('Tic Tac Toe Game Outcomes')

    # Set the positions and labels of the x-ticks
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45)

    ax.set_ylim(0, max(counts) + 1)  # Ensure y-axis starts at 0 and has enough range to show all bars

    # Add count labels on top of the bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('game_outcome_stats.png')
    plt.close()

    return stats  # Optionally return the stats for further use or testing
