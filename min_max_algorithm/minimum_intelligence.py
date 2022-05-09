from minimax import Minimax
import time
import sys
sys.path.append('metaheuristic_algorithm/')
from tic_tac_toe import Game

minimax = Minimax()

def minimax_function( board_state, current_player ):
    minimax = Minimax()

    minimax.generate_tree(
        Game( None, None, current_player = current_player ), 
        current_player, 
        root_board_state = board_state, 
        max_depth = 9
    )

    minimax.evaluate_game_tree(
        Game( None, None ), 
        game.evaluate
    )
    
    return minimax.get_best_move( board_state )

def stoopid( board_state, current_player ):
    return board_state.index( 0 )

game = Game( minimax_function, stoopid )
print(game.play())
print(game.board)

game = Game( stoopid, minimax_function )
print(game.play())
print(game.board)