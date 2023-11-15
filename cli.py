# cli.py

from logic import TicTacToe, HumanPlayer, ComputerPlayer

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

        # 检查游戏状态并打印结果
        if game.get_winner():
            game.print_board()
            print(f"Congratulations! Player {game.get_winner()} wins!")
            break
        elif game.is_draw():
            game.print_board()
            print("It's a draw!")
            break

        # 如果是单人游戏且电脑刚刚落子，打印分割线
        if is_single_player and game.players[game.current_player].symbol == 'X':
            print("\n============\n")  # 分割线

if __name__ == '__main__':
    main()