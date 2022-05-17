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

W = 0
T = 0
L = 0

for node in minimax.nodes.values():
    if node.value == 1: W += 1
    if node.value == 0: T += 1
    if node.value == -1: L += 1

print('W', W)
print('T', T)
print('L', L)
print(minimax.nodes[ 10 ].player)