from tic_tac_toe import Game
from numpy import random
from minimax import Minimax
import sys
sys.path.append('metaheuristic_algorithm/')


def minimax_function(board_state, current_player):
    minimax = Minimax()

    minimax.generate_tree(
        Game(None, None),
        current_player,
        root_board_state=board_state,
        max_depth=9
    )

    minimax.evaluate_game_tree(
        Game(None, None),
        game.evaluate
    )

    return minimax.get_best_move(board_state)


def random_function(board_state, current_player):
    return random.choice([
        i
        for i in range(9)
        if int(board_state[i]) == 0
    ])


minimax_score = 0

for i in range(1, 1001):

    if i % 10 == 0:  # or i < 6:
        print('\nGame:', i)
        print(100 * minimax_score / i, '% winrate for player 1')

    game = Game(minimax_function, minimax_function)
    result = game.play()

    if result[1] == 1:  # minimax_function won
        minimax_score += 1
