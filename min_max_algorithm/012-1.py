from numpy import random
from minimax import Minimax
import sys
sys.path.append('genetic_algorithm/')
from tic_tac_toe import Game

def minimax_function( board_state, current_player ):
    minimax = Minimax()
    minimax.generate_tree(Game(None, None), current_player, root_board_state = board_state, prune = True, max_depth = 6)
    minimax.evaluate_game_tree(Game(None, None))
    
    return minimax.get_best_move(board_state)

def random_function( board_state, current_player ):
    return random.choice( [ i for i in range( 9 ) if int( board_state[ i ] ) == 0 ] )

minimax_score = 0

for i in range(1, 1001):

    
    if i % 100 == 0 or i < 6:
        print('\nGame:', i)

    game = Game( minimax_function, random_function )
    result = game.play()

    if result[ 1 ] == 1: # minimax_function won
        minimax_score += 1

print(minimax_score / 1000)  
