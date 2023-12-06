import os
import csv
import matplotlib.pyplot as plt

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

    return stats


if __name__ == '__main__':
    generate_winner_stats()