# cli.py

from logic import TicTacToe, HumanPlayer, ComputerPlayer, log_game_result, generate_winner_stats, analyze_best_starting_position

def main():
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
        first_move_result = game.get_first_move_result()
        log_game_result(is_single_player, player1.player_type, player2.player_type, game.get_winner(), first_move_result, game.first_move_position)
        generate_winner_stats()

    analyze_best_starting_position()

if __name__ == '__main__':
    main()
