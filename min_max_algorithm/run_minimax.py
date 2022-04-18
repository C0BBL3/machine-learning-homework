from minimax import Minimax
import time
import sys
sys.path.append('genetic_algorithm/')
from tic_tac_toe import Game


game = Game(None, None)
start = time.time()
minimax = Minimax()
minimax.generate_tree(game, 0, prune = True)
print( sum(len(nodes) for nodes in minimax.nodes))
print( minimax.leaf_node_count )
print(time.time()-start)