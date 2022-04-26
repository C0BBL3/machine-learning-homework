from minimax import Minimax
import time
import sys
sys.path.append('metaheuristic_algorithm/')
from tic_tac_toe import Game

game = Game( None, None )
start = time.time()
minimax = Minimax()
minimax.generate_tree( game, game.current_player )
minimax.evaluate_game_tree( game, game.evaluate )
print( time.time() - start )
print( len( minimax.nodes ) )
print( len( minimax.leaf_nodes ) )

