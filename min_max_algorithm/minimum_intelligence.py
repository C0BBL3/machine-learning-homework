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
    
    return ( minimax.get_best_move( board_state ), minimax )

def stoopid( board_state, current_player ):
    return board_state.index( 0 )

game = Game( minimax_function, stoopid )

while not game.game_finished()[ 0 ] and game.board.count( 0 ) > 0:

    current_state = game.state( current_player = game.current_player )
    current_move = game.strategies[ game.current_player - 1 ]( game.board, game.current_player )
    if game.current_player == 1:
        game.place( game.current_player, current_move[ 0 ] )
    else:
        game.place( game.current_player, current_move )
    game.current_player = game.get_next_player( game.current_player )
    if isinstance(current_move, tuple):
        game.logs.append( 
            (
                game.state(), [
                    [
                        node.board_state, 
                        node.value
                    ] 
                    for node in current_move[ 1 ].first_layer_nodes
                ]
            )
        )

print(game.logs)

game = Game( stoopid, minimax_function )

while not game.game_finished()[ 0 ] and game.board.count( 0 ) > 0:

    current_state = game.state( current_player = game.current_player )
    current_move = game.strategies[ game.current_player - 1 ]( game.board, game.current_player )
    if game.current_player == 2:
        game.place( game.current_player, current_move[ 0 ] )
    else:
        game.place( game.current_player, current_move )
    game.current_player = game.get_next_player( game.current_player )
    if isinstance(current_move, tuple):
        game.logs.append( 
            (
                game.state(), [
                    [
                        node.board_state, 
                        node.value
                    ] 
                    for node in current_move[ 1 ].first_layer_nodes
                ]
            )
        )

print(game.logs)