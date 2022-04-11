from minimax import Minimax
import sys
sys.path.append('genetic_algorithm/')
from tic_tac_toe import Game

game = Game(None, None)

minimax = Minimax()
minimax.generate_tree(game, 0)
minimax.evaluate_game_tree()
print(minimax.nodes[0].value)
