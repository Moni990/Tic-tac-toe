# cli.py
import csv
import os
from datetime import datetime
from logic import TicTacToe, HumanPlayer, ComputerPlayer, log_game_result, generate_winner_stats

def main():
    start_time = datetime.now()

    player_count = int(input("Enter the number of players (1 or 2): "))
    player1 = HumanPlayer('X')
    if player_count == 1:
        player2 = ComputerPlayer('O')
        is_single_player = True
    else:
        player2 = HumanPlayer('O')
        is_single_player = False

    game = TicTacToe(player1, player2)

    while True:
        game.print_board()
        if not game.make_move():
            print("Invalid move. Please try again.")
            continue

        if is_single_player:
            print("\n============\n")

        if game.get_winner():
            game.print_board()
            print(f"Congratulations! Player {game.get_winner()} wins!")
            break
        elif game.is_draw():
            game.print_board()
            print("It's a draw!")
            break

    if game.get_winner() or game.is_draw():
        log_game_result(game.get_winner(), player1, player2, start_time)
        generate_winner_stats()

if __name__ == '__main__':
    main()