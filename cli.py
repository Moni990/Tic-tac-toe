# cli.py
from logic import TicTacToe

def main():
    game = TicTacToe()
    while True:
        game.print_board()
        try:
            row = int(input(f"Player {game.get_current_player()}, enter your move row (0-2): "))
            col = int(input(f"Player {game.get_current_player()}, enter your move column (0-2): "))
        except ValueError:
            print("Please enter a number between 0 and 2.")
            continue

        if row not in range(3) or col not in range(3):
            print("Invalid move. Please try again.")
            continue

        if not game.make_move(row, col):
            print("This cell is already taken. Please try again.")
            continue

        if game.get_winner():
            game.print_board()
            print(f"Player {game.get_winner()} wins!")
            break
        elif game.is_draw():
            game.print_board()
            print("It's a draw!")
            break

if __name__ == '__main__':
    main()
