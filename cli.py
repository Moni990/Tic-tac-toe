# This file contains the Command Line Interface (CLI) for
# the Tic-Tac-Toe game. This is where input and output happens.
# For core game logic, see logic.py.

from logic import make_empty_board, get_winner, other_player

def print_board(board):
    for row in board:
        print(" ".join([cell if cell else ' ' for cell in row]))
    print("\n")

if __name__ == '__main__':
    board = make_empty_board()
    winner = None
    current_player = 'X'

    while winner is None:
        print(f"It's {current_player}'s turn.")
        print_board(board)

        # Input a move from the player
        move = input("Enter your move (row and column, e.g., '1 2'): ")
        row, col = map(int, move.split())

        # Check if the cell is empty
        if board[row - 1][col - 1] is None:
            board[row - 1][col - 1] = current_player
        else:
            print("Invalid move. Cell is already occupied. Try again.")
            continue

        # Check if someone won
        winner = get_winner(board)
        if winner:
            print_board(board)
            print(f"{winner} wins!")

        # Switch to the other player
        current_player = other_player(current_player)

